import json

from django.views import View
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubscriberForm, NewsletterForm, SendEmailForm
from .models import Subscriber, Newsletter


# Newsletter
class NewsletterListView(LoginRequiredMixin, View):
    
    def get(self, request):
        form = NewsletterForm()
        newsletters = Newsletter.objects.filter(owner=request.user)
        
        return render (
            request,
            "subscriber/newsletter_index_page.html",
            {
                "form": form,
                "newsletters": newsletters,
            }
        )    
    
class NewsletterDetailView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        newsletter = get_object_or_404(
            Newsletter, 
            owner=request.user, 
            id=pk
        )
        
        return render (
            request,
            "subscriber/newsletter_details.html",
            {
                "newsletter": newsletter,
            }
        )
 
class NewsletterCreateView(LoginRequiredMixin, View):
    
    def get(self, request):
        form = NewsletterForm()
        
        return render (
            request,
            "subscriber/includes/create_newsletter_form.html",
            {
                "form": form, 
            }
        )
 
    def post(self, request):
        form = NewsletterForm(request.POST)
        newsletters = Newsletter.objects.filter(owner=request.user)
        
        if form.is_valid():
            new_newsletter = form.save(commit=False)
            new_newsletter.owner = request.user
            new_newsletter.save()
            
            response = render(
                request,
                "subscriber/includes/newsletter_card_item.html",
                {
                    "newsletter": new_newsletter,
                    "newsletters": newsletters,
                }
            )
            
            response["HX-Retarget"] = "#newsletter-items-grid"
            response["HX-Reswap"] = "afterbegin"
            response["HX-Trigger"] = "closeModal"
            return response
        
        response = render(
            request,
            "subscriber/includes/create_newsletter_form.html",
            {
                "form": form,
            }
        )
        
        response["HX-Retarget"] = "#create-newsletter-form"
        response["HX-Reswap"] = "outerHTML"
        return response 
   
class NewsletterUpdatedView(LoginRequiredMixin, View):
 
    def get(self, request, pk):
        newsletter = get_object_or_404(Newsletter, owner=request.user, id=pk)
        form = NewsletterForm(instance=newsletter)
        
        return render (
            request,
            "subscriber/includes/newsletter_form.html",
            {
                "form": form, 
                "newsletter": newsletter,
            }
        )
    
    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, owner=request.user, id=pk)
        form = NewsletterForm(request.POST, instance=newsletter)
        
        if form.is_valid():
            new_newsletter = form.save()
            
            response = render(
                request,
                "subscriber/includes/newsletter_card_item.html",
                {
                    "newsletter": new_newsletter
                }
            )
            
            response["HX-Reswap"] = "outerHTML"
            response["HX-Retarget"] = f"#card-{newsletter.id}"
            response["HX-Trigger"] = "closeModal"
            return response
        
        response = render(
            request,
            "subscriber/includes/newsletter_form.html",
            {
                "form": form,
                "newsletter": newsletter,
            }
        )
        return response
      
class NewletterDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, owner=request.user, id=pk)
        newsletter.delete()
        
        response = HttpResponse()
        response["HX-Trigger"] = json.dumps({
            "removeElement": f"card-{pk}",
            "closeModal": "",
        })
        return response
        
class NewsletterSubscribeView(View):
 
    def get(self, request, pk):
        newsletter = get_object_or_404(Newsletter, id=pk)
        form = SubscriberForm()
        
        return render (
            request,
            "subscriber/newsletter_subscribe_page.html",
            {
                "form": form,
                "pk": pk,
                "newsletter": newsletter
            }
        )
    
    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, id=pk)
        form = SubscriberForm(request.POST)
        
        if form.is_valid():
            new_subscriber = form.save(commit=False)
            new_subscriber.is_active = True
            new_subscriber.newsletter = newsletter
            new_subscriber.save()
            
            response = render(
                request,
                "subscriber/includes/thankyou_message.html",
                {
                    "newsletter": newsletter,
                    "subscriber": new_subscriber,
                }
            )
            
            response["HX-Reswap"] = "outerHTML"
            response["HX-Retarget"] = f"#subscribe-page-content"
            return response
        
        response = render(
            request,
            "subscriber/includes/newsletter_subscribe_form.html",
            {
                "form": form,
                "pk": pk
            }
        )
        response["HX-Reswap"] = "outerHTML"
        response["HX-Retarget"] = f"#newsletter-subscriber-form"
        return response  
        

# Subscriber
class SubscriberCreateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        newsletter = get_object_or_404(
            Newsletter, 
            owner=request.user, 
            id=pk
        )
        form = SubscriberForm()
        
        return render(
            request,
            "subscriber/includes/admin/create_subscriber_form.html",
            {
                "form": form,
                "newsletter": newsletter,   
            }
        )
        
    def post(self, request, pk):
        newsletter = get_object_or_404(
            Newsletter, 
            owner=request.user, 
            id=pk
        )
        
        form = SubscriberForm(request.POST)

        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.newsletter = newsletter
            subscriber.save()
            
            # verify_url = request.build_absolute_uri(
            #     reverse("verify-subscriber", args=[subscriber.verification_token])
            # )

            response = render(
                request, 
                "subscriber/includes/admin/subscriber_row_item.html", 
                {
                    "subscriber": subscriber,
                }
            )
          
            response["HX-Retarget"] = "#subscriber-table"
            response["HX-Reswap"] = "afterbegin"
            response["HX-Trigger"] = "closeModal"
            return response

        return render(
            request, 
            "subscriber/includes/admin/create_subscriber_form.html",
            {
                "form": form,
                "newsletter": newsletter,
            }
        )
    
class SubscriberUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        subscriber = get_object_or_404(Subscriber, id=pk)
        form = SubscriberForm(instance=subscriber)
        
        return render(
            request,
            "subscriber/includes/admin/update_subscriber_form.html",
            {
                "form": form, 
                "subscriber": subscriber,
            }
        )
        
    def post(self, request, pk):
        subscriber = get_object_or_404(Subscriber, id=pk)
        form = SubscriberForm(request.POST, instance=subscriber)
        
        if form.is_valid():
            new_subscriber = form.save()
            
            response = render(
                request,
                "subscriber/includes/admin/subscriber_row_item.html",
                {
                    "subscriber": new_subscriber,
                }
            )
            
            response["HX-Reswap"] = "outerHTML"
            response["HX-Retarget"] = f"#row-{pk}"
            response["HX-Trigger"] = "closeModal"
            return response
        
        response = render(
            request,
            "subscriber/includes/admin/update_subscriber_form.html",
            {
                "form": form,
                "subscriber": subscriber
            }
        )
        return response
    
class SubscriberDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        subscriber = get_object_or_404(Subscriber, id=pk)
        subscriber.delete()
        
        response = HttpResponse()
        response["HX-Trigger"] = json.dumps({
            "removeElement": f"row-{pk}",
            "closeModal": "",
        })
        return response

    
class SendEmailView(LoginRequiredMixin, View):
      
    def get(self, request, pk):
        newsletter = get_object_or_404(
            Newsletter, 
            owner=request.user, 
            id=pk
        )
        form = SendEmailForm()
        
        return render(
            request,
            "subscriber/includes/send_email_form.html",
            {
                "form": form,
                "newsletter": newsletter,
            }
        )
    
        
    def post(self, request, pk):
        newsletter = get_object_or_404(
            Newsletter,
            owner=request.user,
            id=pk,
        )
        form = SendEmailForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["body"]

            recipient_list = list(
                newsletter.subscribers.values_list("email", flat=True)
            )

            if recipient_list:

                # Prepare bulk email tuples
                from_email = settings.DEFAULT_FROM_EMAIL
                messages = [
                    (subject, body, from_email, [email])
                    for email in recipient_list
                ]
                
                send_mass_mail(messages, fail_silently=False)

                response = HttpResponse()
                response["HX-Trigger"] = "closeModal"
                return response

        return render(
            request,
            "subscriber/includes/send_email_form.html",
            {
                "form": form, 
                "newsletter": newsletter
            },
        )
    
      
class VerifySubscriberView(View):
    def get(self, request, token):
        subscriber = get_object_or_404(
            Subscriber, 
            verification_token=token, 
            is_verified=False
        )
        subscriber.verify()
        return redirect("email-verified")
     
class EmailVerifiedView(View):
    template_name = "newsletter/email_verified.html"

    def get(self, request):
        return render(request, self.template_name)
    
