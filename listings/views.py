from django.shortcuts import render ,get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage , PageNotAnInteger  , Paginator
from pages.choices import state_choice , bedroom_choice , bathroom_choice ,price_choice
from django.db.models import Q

# Create your views here.
def index(request):
    listing = Listing.objects.order_by('-listing_date').filter(is_published=True)
    paginator = Paginator(listing,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    content = {'listings' : paged_listings}
    return render(request,'listings/listings.html',content)


def listing(request,listing_id):
    list = get_object_or_404(Listing, pk=listing_id)
    content={'lists':list}
    return render(request,'listings/listing.html',content)


def search(request):
    queryset_list = Listing.objects.order_by('-listing_date')
    
    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list= queryset_list.filter(description__icontains=keywords)
    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list=queryset_list.filter(Q(state__iexact=state))
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__iexact=bedrooms)
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__iexact=price)

    context={
        'state_choice':state_choice,
        'bedroom_choice':bedroom_choice,
        'bathroom_choice':bathroom_choice,
        'price_choice':price_choice,
        'listings':queryset_list,
        'values':request.GET,
            }
    return render(request,'listings/search.html',context)
