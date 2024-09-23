from django.shortcuts import render,redirect
from .forms import UserCreateForm,UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")

        else:
            messages.error(request, "Invalid Login credentials")
            return redirect("login")    

    return render(request, 'account/login.html')
def user_register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
                # Redirect to a success page or homepage
            return redirect("home")
    else:
        form = UserCreateForm()

    return render(request,'account/register.html',{"form":form,})
def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged out")
    return redirect("login")
def forgetpassword(request):
    return render(request,'account/forget-password.html')