from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Envelope
# Create your views here.

@login_required
def create_envelope(request):
    if request.method == "POST":
        # get user info
        name = request.POST.get('envelope_name')
        members = request.POST.getlist('envelope_members')
        envelope_id = request.POST.getlist('envelope_id')
        # create envelope instance
        envelope = Envelope.objects.create(envelope_name=name)
        envelope.envelope_members.add(request.user)
        # add creator to group
        # for all members to be added
          # add users to group
        messages.success(request, "Successfully created: " + name)
        return redirect(reverse('board:board_home'))
    else:
        return render(request, 'create_envelope.html')