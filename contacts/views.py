from django.shortcuts import render , redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method=="POST":
        listing=request.POST['listing']
        listing_id=request.POST['listing_id']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']
        
        #check if the user has already inqueiry for property.
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted :
                messages.error(request,'Inquery Already Processed! ')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email, phone=phone,message=message,user_id=user_id)

        contact.save()
        
        #send mail
        send_mail(
                  'property inquery',
                  'There has an inquiry for the '+listing+'. sign into admin portal for more!' ,
                  'kukkarkushal7@gmail.com',
                  [realtor_email, 'kushalkukkar54399@gmail.com']
                  )

        return redirect('/listings/'+listing_id)
