from django.urls import path

from .views import (
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView, 
    NewsletterUpdatedView,
    NewletterDeleteView,
    NewsletterSubscribeView,
    
    SubscribeView,
    VerifySubscriberView,
    EmailVerifiedView,
)

app_name = "subscriber"

urlpatterns = [
    path("", NewsletterListView.as_view(), name="newsletter_list"),
    path("create/", NewsletterCreateView.as_view(), name="newsletter_create"),
    path("<uuid:pk>/", NewsletterDetailView.as_view(), name="newsletter_details"),
    path("update/<uuid:pk>/", NewsletterUpdatedView.as_view(), name="newsletter_update"),
    path("delete/<uuid:pk>/", NewletterDeleteView.as_view(), name="newsletter_delete"),
    path("subscribe/<uuid:pk>/", NewsletterSubscribeView.as_view(), name="newsletter_subscribe"),
]