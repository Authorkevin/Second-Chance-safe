from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import time # For simulating delays in comment creation

from users.models import CustomUser
from .models import Topic, Comment
from .forms import TopicForm, CommentForm

class CommunityAppSetupTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client = Client()

    def test_community_main_page_loads(self):
        response = self.client.get(reverse('community:topic_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_topic_page_loads_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('community:create_topic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/create_topic.html')

    def test_create_topic_page_redirects_unauthenticated(self):
        response = self.client.get(reverse('community:create_topic'))
        self.assertEqual(response.status_code, 302) # Should redirect to login
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('community:create_topic')}")


class TopicModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='topiccreator', email='creator@example.com', password='password')

    def test_create_topic_instance(self):
        topic = Topic.objects.create(title="Test Topic Title", created_by=self.user)
        self.assertIsInstance(topic, Topic)
        self.assertEqual(topic.title, "Test Topic Title")
        self.assertEqual(topic.created_by, self.user)
        self.assertTrue(topic.created_at)
        self.assertTrue(topic.updated_at)

    def test_topic_str_method(self):
        topic = Topic.objects.create(title="My Awesome Topic", created_by=self.user)
        self.assertEqual(str(topic), "My Awesome Topic")


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='commenter', email='commenter@example.com', password='password')
        self.topic_creator = CustomUser.objects.create_user(username='topauthor', email='ta@example.com', password='password')
        self.topic = Topic.objects.create(title="Topic for Comments", created_by=self.topic_creator)

    def test_create_comment_instance(self):
        comment = Comment.objects.create(
            topic=self.topic,
            author=self.user,
            content="This is a test comment."
        )
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.topic, self.topic)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "This is a test comment.")
        self.assertTrue(comment.created_at)
        self.assertTrue(comment.updated_at)

    def test_comment_str_method(self):
        comment = Comment.objects.create(
            topic=self.topic,
            author=self.user,
            content="Another comment here."
        )
        expected_str = f"Comment by {self.user.username} on {self.topic.title}"
        self.assertEqual(str(comment), expected_str)


class TopicWorkflowTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='workflowuser', email='wf@example.com', password='password123')
        self.client = Client()
        self.client.login(username='workflowuser', password='password123')

    def test_topic_creation_workflow(self):
        initial_topic_count = Topic.objects.count()
        topic_title = "A Brand New Topic"
        response = self.client.post(reverse('community:create_topic'), {'title': topic_title})
        
        self.assertEqual(Topic.objects.count(), initial_topic_count + 1)
        created_topic = Topic.objects.latest('created_at')
        self.assertEqual(created_topic.title, topic_title)
        self.assertEqual(created_topic.created_by, self.user)
        self.assertRedirects(response, reverse('community:topic_detail', args=[created_topic.id]))

    def test_topic_detail_view(self):
        topic = Topic.objects.create(title="Detailed Topic", created_by=self.user)
        response = self.client.get(reverse('community:topic_detail', args=[topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, topic.title)
        self.assertTemplateUsed(response, 'community/topic_detail.html')

    def test_topic_list_view(self):
        Topic.objects.create(title="Topic Alpha", created_by=self.user)
        Topic.objects.create(title="Topic Beta", created_by=self.user)
        
        response = self.client.get(reverse('community:topic_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Topic Alpha")
        self.assertContains(response, "Topic Beta")
        self.assertTemplateUsed(response, 'community/topic_list.html')


class CommentWorkflowTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='commentflowuser', email='cf@example.com', password='password123')
        self.topic_creator = CustomUser.objects.create_user(username='topicowner', email='to@example.com', password='password')
        self.topic = Topic.objects.create(title="Topic for Comment Workflow", created_by=self.topic_creator)
        self.client = Client()
        # Login the user who will be making comments
        self.client.login(username='commentflowuser', password='password123')

    def test_comment_creation_workflow(self):
        initial_comment_count = self.topic.comments.count()
        comment_content = "This is a new comment on the workflow topic."
        
        response = self.client.post(reverse('community:add_comment', args=[self.topic.id]), {
            'content': comment_content
        })
        
        self.assertEqual(self.topic.comments.count(), initial_comment_count + 1)
        new_comment = self.topic.comments.latest('created_at')
        self.assertEqual(new_comment.content, comment_content)
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.topic, self.topic)
        
        self.assertRedirects(response, reverse('community:topic_detail', args=[self.topic.id]))
        
        # Verify comment is visible on detail page
        detail_response = self.client.get(reverse('community:topic_detail', args=[self.topic.id]))
        self.assertContains(detail_response, comment_content)

    def test_comment_display_order(self):
        # Create first comment
        Comment.objects.create(topic=self.topic, author=self.user, content="First comment")
        time.sleep(0.01) # Ensure a slight time difference
        # Create second comment
        Comment.objects.create(topic=self.topic, author=self.user, content="Second comment, should be newer")
        
        response = self.client.get(reverse('community:topic_detail', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        
        # Comments are ordered by '-created_at' in the view
        # So, "Second comment" should appear before "First comment" in the response content
        comments_in_response = [comment.content for comment in response.context['comments']]
        self.assertEqual(comments_in_response[0], "Second comment, should be newer")
        self.assertEqual(comments_in_response[1], "First comment")


    def test_unauthenticated_comment_attempt(self):
        # Log out the current user
        self.client.logout()
        
        comment_content = "Attempting to comment while logged out."
        response = self.client.post(reverse('community:add_comment', args=[self.topic.id]), {
            'content': comment_content
        })
        
        self.assertEqual(response.status_code, 302) # Should redirect to login
        login_url = reverse('users:login')
        expected_redirect_url = f"{login_url}?next={reverse('community:add_comment', args=[self.topic.id])}"
        # The add_comment_view redirects to topic_detail if it's a GET or form is invalid,
        # but for POST without auth, it should redirect to login via the @login_required decorator on add_comment_view
        # which then redirects to the topic_detail page after login.
        # However, the initial redirect from @login_required is to the login page.
        # The view itself for add_comment redirects to topic_detail if method is not POST or form invalid.
        # The @login_required decorator on add_comment_view means this POST should first hit the decorator's redirect.
        
        # The add_comment_view, if it were reached by an unauthenticated user (which it won't be due to @login_required),
        # would redirect to topic_detail. But @login_required intercepts first.
        # The target of the redirect for an unauthenticated POST to a @login_required view is the login page.
        
        # The add_comment_view itself redirects to 'topic_detail' if the form is invalid or if it's a GET request.
        # However, @login_required decorator on `add_comment_view` handles unauthenticated access for POST.
        # The view `add_comment_view` is decorated with `@login_required`.
        # When an unauthenticated user tries to POST to `add_comment_view`, the decorator should redirect to login.
        # The `add_comment_view` has logic: `return redirect('topic_detail', topic_id=topic.id)` at the end.
        # This final redirect in `add_comment_view` happens *after* a comment is posted or if the form is invalid (for a POST) or if it's a GET.
        # For an unauthenticated POST, `@login_required` should redirect to login.

        # Let's re-evaluate based on how @login_required works for POST:
        # It should redirect to the login page with a 'next' parameter.
        # The add_comment_view itself *if reached by unauthenticated user* would redirect to topic_detail.
        # But the decorator should prevent this.
        # The test for create_topic_page_redirects_unauthenticated is a good reference.

        # Correct check for @login_required on a POST view:
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('community:add_comment', args=[self.topic.id])}")
        self.assertEqual(self.topic.comments.count(), 0) # No comment should be created
