import json

from django.views import View
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("subscriber:newsletter_list")
        
        form = UserCreationForm()
        return render(
            request, 
            "accounts/register.html", 
            {
                "form": form
            }
        )

    def post(self, request):
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            response = HttpResponse()
            response["HX-Redirect"] = reverse("subscriber:newsletter_list") 
            return response
        
        return render(
            request,
            "accounts/includes/register_form.html",
            {
                "form": form,
                "error_message": "Please correct the errors below."
            }
        )


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("subscriber:newsletter_list")
        
        return render(
            request, 
            "accounts/login.html",
            {
                "form": AuthenticationForm()
            }
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            response = HttpResponse()
            response["HX-Redirect"] = reverse("subscriber:newsletter_list") 
            return response
        
        return render(
            request,
            "accounts/includes/login_form.html",
            {
                "form": form,
                "error_message":  "Invalid username or password"
            }
        )

    
class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        response = HttpResponse()
        response["HX-Redirect"] = reverse("accounts:login")
        return response
