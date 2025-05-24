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


class PaymentForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
            'rows': 4
        }),
        label='Shipping Address',
        required=True
    )
