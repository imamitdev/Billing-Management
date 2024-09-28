from django.shortcuts import render,redirect
from .forms import RegistrationForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from .models import User, UserProfile
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request, "account/login.html")

def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # Fixed typo
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            
            # Fix user reference to User model
            user = User.objects.create_user(
                name=name,
                email=email,
                username=username,
                password=password,
            )
            user.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Registration failed. Please check the form.")

    else:
        form = RegistrationForm()  # Fixed typo

    return render(request, 'account/register.html', {"form": form})
@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

def forgetpassword(request):
    return render(request, 'account/forget-password.html')