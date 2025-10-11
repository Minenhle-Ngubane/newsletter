from django import forms
from django.core.exceptions import ValidationError

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
        fields = ["email", "name"]
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name")

        newsletter = getattr(self.instance, "newsletter", None)
        if newsletter is None and hasattr(self, "newsletter"):
            newsletter = self.newsletter

        if newsletter and email:
            exists = Subscriber.objects.filter(
                newsletter=newsletter, email=email
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise ValidationError({
                    "email": "This email is already subscribed to this newsletter."
                })
        return cleaned_data
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")
        return email
