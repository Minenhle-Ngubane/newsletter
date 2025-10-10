import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone


class Newsletter(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier for this newsletter."
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters",
        help_text="The account that owns this newsletter."
    )
    
    name = models.CharField(
        max_length=150,
        help_text="The display name of the newsletter."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the newsletter was created."
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the newsletter was last updated."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"
        unique_together = ("owner", "name")

    def __str__(self):
        return f"{self.name} ({self.owner.username})"
    
    
class Subscriber(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    newsletter = models.ForeignKey(
        "Newsletter",
        on_delete=models.CASCADE,
        null=True,
        related_name="subscribers",
        help_text="The newsletter this subscriber belongs to."
    )
    
    email = models.EmailField(
        db_index=True
    )
    
    name = models.CharField(
        max_length=100
    )
    
    date_subscribed = models.DateTimeField(
        default=timezone.now
    )
    
    is_active = models.BooleanField(
        default=True
    )
    
    is_verified = models.BooleanField(
        default=False
    )
    
    verification_token = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )

    class Meta:
        verbose_name = "Email Subscriber"
        verbose_name_plural = "Email Subscribers"
        ordering = ["-date_subscribed"] 
        
        constraints = [
            models.UniqueConstraint(
                fields=["newsletter", "email"],
                name="unique_subscriber_per_newsletter"
            )
        ]
        
    def __str__(self):
        return self.email

    def deactivate(self): 
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        self.is_active = True
        self.save(update_fields=["is_active"])
        
    def verify(self):
        self.is_verified = True
        self.save(update_fields=["is_verified"])
