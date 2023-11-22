from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.urls import reverse
from .forms import RegisterUserForm

def landing(request):
    return render(request, 'landing.html', {})


def login_user(request):
    # if the user is tries to view protected page
    if not request.user.is_authenticated and 'next' in request.GET:
        messages.info(request, 'You must log in to view this page.')
    if request.user.is_authenticated:
        return redirect(reverse('board:board_home'))
    # if the did 'something' >> i.e. clicked a button
    if request.method == "POST":
        # grab info from user
        username = request.POST["username"] # passing names from login.html
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            messages.success(request, "You are logged in as " + username + ".")
            return redirect(reverse('board:board_home'))
        else:
            # Return an 'invalid login' error message.
            # they just went to the page, so show the page
            messages.success(request, "Invalid username or password.")
            return redirect(reverse('members:login_users'))
    else:
        return render(request, 'registration/login.html', {})
    
def logout_user(request):
    logout(request) # calling function we imported
    if not request.user.is_authenticated:
        messages.success(request, "Successfully logged out.")
    return redirect('login')

def register_users(request):
    # if user filled out the form
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully registered as " + username + "!")
            return redirect(reverse('board:board_home'))
    else:
        form = RegisterUserForm()
        pass
    return render(request, 'registration/register.html', {'form':form})