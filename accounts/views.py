from django.shortcuts import render , redirect
from django.contrib import messages , auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.


def login(request):
    if request.method =="POST":
        username= request.POST['username']
        password= request.POST['password']
    
        user = auth.authenticate(username=username,password=password)
    
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Successfully logged in!')
            return redirect('dash')
        else:
            messages.error(request,'username or password is wrong , try again!')
            return redirect('login')
    
    else:
        return render(request,'accounts/login.html')

def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('index')

def register(request):
    if request.method=="POST":
        first_name= request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        # check for password
        if password==password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email id already exists!')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password)
                    ## direct logged in after register.
                    #auth.login(request,user)
                    # messages.success(request,'now you are logged in!')
                    # return redirect('index')
                    #save and afterwards logged in!
                    user.save()
                    messages.success(request,'Account Created , log in now.')
                    return redirect('login')
                
                   
        else:
            messages.error(request,'Password does not match!')
            return redirect('register')

    else:
        return render(request,'accounts/register.html')


def dash(request):
    contact = Contact.objects.order_by('-contact_date').filter(user_id= request.user.id)
    context={
        'contacts':contact,
            }
    return render(request,'accounts/dash.html',context)
