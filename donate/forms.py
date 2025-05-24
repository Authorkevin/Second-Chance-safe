from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    amount = forms.DecimalField(
        min_value=0.01,
        label="Donation Amount (USD)",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 25.00', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
    )

    class Meta:
        model = Donation
        fields = ['first_name', 'last_name', 'email', 'amount']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email (optional)', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'email': "Email (for receipt)",
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Donation amount must be greater than zero.")
        return amount

