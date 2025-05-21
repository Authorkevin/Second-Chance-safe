from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']  #  we only need the text field.
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-2 border rounded-md'}),
        }
        labels = {
            'text': 'Your Review',
        }

