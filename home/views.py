from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']                                                                   
        print(name, email, phone, content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5:
            messages.error(request, "please fill correctly")
        else:    
            content= Contact(Name=name, email=email, phone=phone, content=content)
            content.save()
            messages.success(request, "message sent")
    return render(request, 'home/contact.html')

def search(request):
    query=request.GET['query']
    allPoststitle=Post.objects.filter(title__icontains=query)
    allPostscontent=Post.objects.filter(content__icontains=query)
    allPosts=allPoststitle.union(allPostscontent)
    a={'allPosts': allPosts, 'query':query }
    return render(request, 'home/search.html', a)
    
def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mail_id=request.POST['mail_id']
        password=request.POST['password']
        x=User.objects.create_user(username, mail_id, password)
        x.firstname= firstname
        x.lastname= lastname

        x.save()
        messages.success(request, "Your Vcoder account has been created succesfully")
        return redirect('/')
    else:
        return HttpResponse('error 404 not found')  

def login(request):
    if request.method=='POST':
        un=request.POST['username']
        pw=request.POST['password']
        x=auth.authenticate(username=un, password=pw)
        if x is None:
            messages.error(request, "Invalid credentials, try again")
            return redirect('/')
        else:
            auth.login(request,x)
            messages.success(request, "Successfully logged in")
            return redirect('/')
    return HttpResponse('404- not found')

def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out")
    return redirect('/')    