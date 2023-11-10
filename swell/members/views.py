from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
  # creates members objects with Member vals
  members = Member.objects.all().values()
  # load members template to display
  template = loader.get_template('member.html')
  # creating object containing members object
  context = {
    'members': members,
  }
  # outputs html rendered by template
  return HttpResponse(template.render(context, request))

def details(request, id):
  # gets id as an argument - used to locate correct memeber in db
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  # creates the object containing the member
  context = {
    'mymember': mymember,
  }
  # sends object to template
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  mydata = Member.objects.values()
  template = loader.get_template('template.html')
  context = {
    'mymembers': mydata,
  }
  return HttpResponse(template.render(context, request))