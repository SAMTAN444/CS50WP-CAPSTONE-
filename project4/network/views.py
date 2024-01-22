from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import admin
from .models import User, Category, Booking
from django.core.paginator import Paginator
from datetime import datetime, timezone


def index(request):
    return render(request, "network/index.html")

def Ippt(request):
    return render(request, "network/Ippt.html")

def bookings(request):
    page_number = request.GET.get('page', 1)
    bookingsData = Booking.objects.all().order_by('-datetime')
    paginator = Paginator(bookingsData, 5)
    pageposts = paginator.get_page(page_number)
    
    current_time = datetime.utcnow()
    
    for booking in pageposts:
        booking_datetime = booking.datetime.astimezone(timezone.utc).replace(tzinfo=None)
        booking.is_done = booking_datetime < current_time
    
    return render(request, "network/bookings.html", {
        "bookings": pageposts,
        "page_number": page_number,
        "current_time": current_time,
    })
    
def edit(request, id):
    
    categories = Category.objects.all()
    bookingData = Booking.objects.get(pk=id)
        
    return render(request, "network/edit.html", {
        'categories': categories,
        'bookings': bookingData,
    })

def submitedit(request, id):
    
    booking = Booking.objects.get(pk=id)
    if request.method == "POST":
        category = request.POST["category"]
        date = request.POST["datetimeInput"]  
        score_input = request.POST.get("inputscore", None)
        currentUser = request.user
        categoryData = Category.objects.get(pk=category)
        
        try:
            datetime_input = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            done = datetime_input < datetime.now()
        except ValueError:
            # Handle invalid date format
            done = False
        
        if score_input and score_input.isdigit():
            score = int(score_input)
        else:
            score = "Score not logged in yet, please enter your score"
        
        booking.category = categoryData
        booking.datetime = date
        booking.score = str(score)
        booking.done = done
        booking.save()
    
        return HttpResponseRedirect(reverse('bookings'))
    else:
        return render(request, "network/bookings.html")
    
def delete(request, id):
    booking = Booking.objects.get(pk=id)
    booking.delete()
    return HttpResponseRedirect(reverse('bookings'))


def BMI(request):
    return render(request, "network/BMI.html")

def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
       
        return render(request, "network/create.html", {
            'categories': categories
        })
    else:
        #Get the data from the form
        category = request.POST["category"]
        date = request.POST["datetimeInput"]  
        score_input = request.POST.get("inputscore", None)
        currentUser = request.user
        categoryData = Category.objects.get(category_name=category)
        
        try:
            datetime_input = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            if datetime_input < datetime.now():
                done =  True
            else:
                done = False
        except ValueError:
            # Handle invalid date format
            done = False
        
        if score_input and score_input.isdigit():
            score = int(score_input)
        else:
            score = "Score not logged in yet, please enter your score"
        
        newBooking = Booking(
            user = currentUser,
            category = categoryData,
            datetime = date,
            score = str(score),
            done = done,
        )
        newBooking.save()
        
        return HttpResponseRedirect(reverse('bookings'))
        


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
