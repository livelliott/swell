
# sendemail/emailapp/views.py
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            message = form.cleaned_data.get('message')
            email_inquiry(name=name, email=email, message=message, subject="Invitation to Swell")
            messages.success(request, message="Email was sent successfully!")
            return render(request, 'contact.html', {'form':form,})
        else:
            messages.error(request, "Error processesing emails, please try again")
            return render(request, 'contact.html', {'form':form,})
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'contact.html', {'form':form,})

def email_inquiry(name, email, message, subject):
    msg_plain = render_to_string('email_inquiry.txt', {'contactName':name, 'contactEmail':email, 'contactMessage':message,})
    msg_html = render_to_string('email_inquiry.html', {'contactName':name, 'contactEmail':email, 'contactMessage':message,})
    send_mail(subject=subject,message=msg_plain,from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.EMAIL_HOST_USER], html_message=msg_html)
