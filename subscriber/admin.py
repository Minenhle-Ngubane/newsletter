from django.contrib import admin

from .models import Newsletter, Subscriber


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at", "owner")
    search_fields = ("name", "owner__username", "owner__email")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "newsletter",
        "is_active",
        "date_subscribed",
        "is_verified",
        "verification_token",
    )
    list_filter = ("is_active", "date_subscribed", "is_verified", "newsletter")
    search_fields = ("email", "name", "newsletter__name")
    ordering = ("-date_subscribed",)
    readonly_fields = ("id", "date_subscribed", "is_verified", "verification_token")
