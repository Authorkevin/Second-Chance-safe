from django.db import models
from users.models import CustomUser

class Topic(models.Model):
    title = models.CharField(max_length=200, blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='community_topics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='community_comments')
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.topic}"
