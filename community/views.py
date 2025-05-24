from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
# Import forms that will be created in the next step
from .forms import TopicForm, CommentForm

def topic_list_view(request):
    topics = Topic.objects.all().order_by('-updated_at')
    return render(request, 'community/topic_list.html', {'topics': topics})

def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = topic.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'community/topic_detail.html', {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def create_topic_view(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            return redirect(reverse('community:topic_detail', args=[topic.id]))
    else:
        form = TopicForm()
    return render(request, 'community/create_topic.html', {'form': form})

@login_required
def add_comment_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.topic = topic
            comment.save()
            return redirect(reverse('community:topic_detail', args=[topic.id]))
    # If GET or form is invalid, redirect to topic detail view.
    # The CommentForm is instantiated and passed to the template in topic_detail_view.
    return redirect('community:topic_detail', topic_id=topic.id)
