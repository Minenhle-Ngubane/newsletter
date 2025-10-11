from django.urls import path

from .views import (
    # Newsletter
    NewsletterListView,
    NewsletterDetailView,
    NewsletterCreateView, 
    NewsletterUpdatedView,
    NewletterDeleteView,
    NewsletterSubscribeView,
    
    # Subscriber
    SubscriberCreateView,
    SubscriberUpdateView,
    SubscriberDeleteView,
    
    # Email
    SendEmailView,
    
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
    
    path("subscriber/create/<uuid:pk>/", SubscriberCreateView.as_view(), name="subscriber_create"),
    path("subscriber/update/<uuid:pk>/", SubscriberUpdateView.as_view(), name="subscriber_update"),
    path("subscriber/delete/<uuid:pk>/", SubscriberDeleteView.as_view(), name="subscriber_delete"),
    
    path("send-email/<uuid:pk>/", SendEmailView.as_view(), name="send_email"),
]