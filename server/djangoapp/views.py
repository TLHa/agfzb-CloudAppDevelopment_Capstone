import random

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, add_review_by_cf
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
get_dealer_url = 'https://6e71488e.au-syd.apigw.appdomain.cloud/htl-capstone/api/dealership'

# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf(get_dealer_url)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)
    return HttpResponse([])


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://6e71488e.au-syd.apigw.appdomain.cloud/htl-capstone/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealerId=dealer_id)
        dealer = get_dealers_from_cf(get_dealer_url,dealerId=dealer_id)[0]
        context['reviews'] = reviews
        context['dealership'] = dealer
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)
    return HttpResponse([])

# Create a `add_review` view to submit a review
def add_review_on_cf(request,dealer_id):
    if request.method == "POST":
        car_infor = [x for x in car_list if x['id'] == int(request.POST['car'])][0]
        new_review = {
            "another": "",
            "car_make": car_infor['car_make'],
            "car_model": car_infor['car_model'],
            "car_year": car_infor['car_year'],
            "dealership": int(dealer_id),
            "id": random.randint(1000,2000),
            "name": request.user.username,
            "purchase": True if request.POST['purchase'] is 'on' else False,
            "purchase_date": request.POST['purchase_date'],
            "review": request.POST['review']
        }
        add_review_by_cf(new_review)
        return redirect("djangoapp:get_dealer_reviews", dealer_id=dealer_id)

car_list = [
    {
        "id": 1,
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021,
    },{
        "id": 2,
        "car_make": "Mercerdes",
        "car_model": "C180",
        "car_year": 2019,
    },{
        "id": 3,
        "car_make": "Mercerdes",
        "car_model": "C200",
        "car_year": 2020,
    },{
        "id": 4,
        "car_make": "Mercerdes",
        "car_model": "C250",
        "car_year": 2021,
    },{
        "id": 5,
        "car_make": "Audi",
        "car_model": "Q5",
        "car_year": 2017,
    },{
        "id": 6,
        "car_make": "Audi",
        "car_model": "R8",
        "car_year": 2021,
    },{
        "id": 7,
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021,
    },{
        "id": 8,
        "car_make": "Kia",
        "car_model": "Sorento",
        "car_year": 2019,
    },{
        "id": 9,
        "car_make": "Kia",
        "car_model": "Morning",
        "car_year": 2017,
    },{
        "id": 10,
        "car_make": "Honda",
        "car_model": "CRV",
        "car_year": 2018,
    },{
        "id": 11,
        "car_make": "Kia",
        "car_model": "K3",
        "car_year": 2021
    }]
def add_review_view(request,dealer_id):
    context = {}
    dealer = get_dealers_from_cf(get_dealer_url, dealerId=dealer_id)[0]
    context['dealership'] = dealer
    context['cars'] = car_list
    return render(request, 'djangoapp/add_review.html', context)

