from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.urls import reverse

# Create your views here.
def login_user(request):
    # if the did 'something' >> i.e. clicked a button
    if request.method == "POST":
        # grab info from user
        username = request.POST["username"] # passing names from login.html
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(reverse('board:board_home'))
        else:
            # Return an 'invalid login' error message.
            # they just went to the page, so show the page
            messages.success(request, "There was an error logging in.")
            return redirect('/')
    else:
        return render(request, 'registration/login.html', {})