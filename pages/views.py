from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from .choices import state_choice , bedroom_choice , bathroom_choice ,price_choice
# Create your views here.

def index(request):
    list_index = Listing.objects.order_by('-listing_date').filter(is_published=True)[:3]
    content={'lists':list_index,
            'state_choice':state_choice,
            'bedroom_choice':bedroom_choice,
            'bathroom_choice':bathroom_choice,
            'price_choice':price_choice,
        
            }
    return render(request,'pages/index.html',content)

def about(request):
    realtor = Realtor.objects.order_by('hire_date')[:3]
    is_mvp = Realtor.objects.all().filter(is_mvp=True)
    content={'realtors': realtor,
        'is_mvps' :is_mvp,
            }
    
    return render(request,'pages/about.html',content)
