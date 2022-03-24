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
    return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://6e71488e.au-syd.apigw.appdomain.cloud/htl-capstone/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    return HttpResponse([])


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://6e71488e.au-syd.apigw.appdomain.cloud/htl-capstone/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealerId=dealer_id)
        # Concat all dealer's short name
        reviews_content_list = ' '.join([review.sentiment for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(reviews_content_list)
    return HttpResponse([])

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        new_review = {}
        for key in request.POST:
            value = request.POST[key]
            if key == 'dealership' or key == 'car_year' or key == 'id':
                new_review[key] = int(value)
            else:
                new_review[key] = value
        add_review_by_cf(new_review)
        return HttpResponse({
            'Success': True
        })

