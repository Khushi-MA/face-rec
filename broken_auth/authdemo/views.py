from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
import random


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create(email=email, password=password)  # No hashing (vulnerable)
        return HttpResponse("User registered!")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(email=email, password=password).first()

        if user:
            user.session_id = str(random.randint(1000, 9999))  # Weak session ID
            user.save()
            response = redirect("dashboard", user_id=user.id)
            response.set_cookie("sessionid", user.session_id)  # Weak cookie
            return response
        else:
            return HttpResponse('Invalid credentials. <a href="/register/">Register here</a>')

    return render(request, "login.html")


def dashboard(request, user_id):
    session_id = request.COOKIES.get("sessionid")
    user = User.objects.filter(id=user_id, session_id=session_id).first()
    if user:
        return render(request, "dashboard.html", {"user": user})
    else:
        return HttpResponse("Invalid session. Please log in again.")


# Weak password reset with no rate limiting
def password_reset(request):
    if request.method == "POST":
        email = request.POST["email"]
        new_password = request.POST["new_password"]
        reset_token = request.POST.get("reset_token")

        user = User.objects.filter(email=email).first()
        if user and reset_token == "1234":  # Dummy token check for demonstration
            user.password = new_password  # No email verification (vulnerable)
            user.save()
            return HttpResponse("Password reset successful!")
        else:
            return HttpResponse("Email not found or invalid reset token")

    return render(request, "password_reset.html")


def index(request):
    return render(request, "index.html")

def user_detail(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        return render(request, "user_detail.html", {"user": user})
    else:
        return HttpResponse("User not found")
