from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages 
from django.urls import reverse
from .forms import RegisterUserForm, AcceptInvite
from board.models import Invitation, UserGroup
from envelope.models import Envelope

# displays the landing page
def landing(request):
    return render(request, 'landing.html', {})

# login page for the user
# @redirect - home page if logged in
def login_user(request):
    # if the user is tries to view protected page
    if not request.user.is_authenticated and 'next' in request.GET:
        messages.info(request, 'You must log in to view this page.')
    # redirect home if already logged in
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
            return redirect(reverse('board:board_home'))
        else:
            # Return an 'invalid login' error message.
            # they just went to the page, so show the page
            messages.success(request, "Invalid username or password.")
            return redirect(reverse('members:login_users'))
    else:
        return render(request, 'registration/login.html', {})

# logout user functionality
# @redirect - login page if logged out  
def logout_user(request):
    logout(request)
    if not request.user.is_authenticated:
        messages.success(request, "Successfully logged out.")
    return redirect('login')

# registers new user
# @redirect - home page if registered
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
    return render(request, 'registration/register.html', {'form':form})

@login_required
def accept_invite(request, invite_token):
    form = AcceptInvite()
    if request.method == "POST":
        form = AcceptInvite(request.POST)
        if form.is_valid():
            current_user = request.user
            invite = get_object_or_404(Invitation, invite_token=invite_token)
            envelope = get_object_or_404(Envelope, envelope_id=invite.envelope_id)
            if joined_envelope(request.user, invite.envelope_id):
                messages.success(request, f"Already joined {envelope.envelope_name}.")
            else:
                # update invite status
                invite.recipient = current_user
                invite.email = current_user.email
                invite.delete()
                # create user group with form info
                user_group = UserGroup(user=current_user, display_name=form.cleaned_data['display_name'], envelope=envelope, env_id=envelope.envelope_id)
                user_group.save()
                messages.success(request, f"Successfully joined group {envelope.envelope_name}.")
            return redirect(reverse('board:board_home'))
    return render(request, 'registration/accept_invite.html', {'form': form, 'invite_token': invite_token})

def joined_envelope(user, env_id):
    try:
        UserGroup.objects.get(user=user, env_id=env_id)
        return True
    except ObjectDoesNotExist:
        return False