from django import forms
from .models import Topic, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
