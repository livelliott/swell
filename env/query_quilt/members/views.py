from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
  # creates members objects with Member vals
  members = Member.objects.all().values()
  # load all members
  template = loader.get_template('member.html')
  # creating object containing members object
  context = {
    'members': members,
  }
  return HttpResponse(template.render(context, request))