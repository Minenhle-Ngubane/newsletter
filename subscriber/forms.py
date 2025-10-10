from django import forms

from .models import Newsletter, Subscriber


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["name"]
        
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Newsletter name cannot be empty.")
        return name


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "name", "is_active"]
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        return email
