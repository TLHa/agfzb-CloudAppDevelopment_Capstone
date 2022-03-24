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
        # dealerships = get_dealers_from_cf(get_dealer_url)
        context['dealership_list'] = [
            {
            "_id": "87a6635f9858bb5ef7d768b651091893",
            "_rev": "1-34e7ebd07643af43db578a46ee1d6365",
            "address": "3 Nova Court",
            "city": "El Paso",
            "full_name": "Holdlamis Car Dealership",
            "id": 1,
            "lat": 31.6948,
            "long": -106.3,
            "short_name": "Holdlamis",
            "st": "TX",
            "state": "Texas",
            "zip": "88563"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651091b07",
            "_rev": "1-d1778a396ca8cb0ef2966a9854eb93ee",
            "address": "6337 Butternut Crossing",
            "city": "Minneapolis",
            "full_name": "Temp Car Dealership",
            "id": 2,
            "lat": 44.9762,
            "long": -93.2759,
            "short_name": "Temp",
            "st": "MN",
            "state": "Minnesota",
            "zip": "55402"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510929c7",
            "_rev": "1-cc5d5c13aa879d1cef8253dfa1dce77d",
            "address": "9477 Twin Pines Center",
            "city": "Birmingham",
            "full_name": "Sub-Ex Car Dealership",
            "id": 3,
            "lat": 33.5446,
            "long": -86.9292,
            "short_name": "Sub-Ex",
            "st": "AL",
            "state": "Alabama",
            "zip": "35285"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651092b59",
            "_rev": "1-a79013b42c83451d49e7e3aba4a575e3",
            "address": "85800 Hazelcrest Circle",
            "city": "Dallas",
            "full_name": "Solarbreeze Car Dealership",
            "id": 4,
            "lat": 32.6722,
            "long": -96.7774,
            "short_name": "Solarbreeze",
            "st": "TX",
            "state": "Texas",
            "zip": "75241"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651093a3d",
            "_rev": "1-c16dcd97a91588c9866814f61ea72751",
            "address": "93 Golf Course Pass",
            "city": "Baltimore",
            "full_name": "Regrant Car Dealership",
            "id": 5,
            "lat": 39.2847,
            "long": -76.6205,
            "short_name": "Regrant",
            "st": "MD",
            "state": "Maryland",
            "zip": "21203"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651093c42",
            "_rev": "1-e37424d3be7785cbdbc4ed12ec29b343",
            "address": "2 Burrows Hill",
            "city": "Wilkes Barre",
            "full_name": "Stronghold Car Dealership",
            "id": 6,
            "lat": 41.2722,
            "long": -75.8801,
            "short_name": "Stronghold",
            "st": "PA",
            "state": "Pennsylvania",
            "zip": "18763"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510946be",
            "_rev": "1-96db320a9c736d2e08e8b1bf873d0e04",
            "address": "9 Cambridge Park",
            "city": "Pueblo",
            "full_name": "Job Car Dealership",
            "id": 7,
            "lat": 38.1286,
            "long": -104.5523,
            "short_name": "Job",
            "st": "CO",
            "state": "Colorado",
            "zip": "81010"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651094e7d",
            "_rev": "1-4e4889794e42a9e092c1442118889232",
            "address": "288 Larry Place",
            "city": "Topeka",
            "full_name": "Bytecard Car Dealership",
            "id": 8,
            "lat": 39.0429,
            "long": -95.7697,
            "short_name": "Bytecard",
            "st": "KS",
            "state": "Kansas",
            "zip": "66642"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510959ee",
            "_rev": "1-63f1a1984f40f1de1eabceaec90f7fb6",
            "address": "253 Hanson Junction",
            "city": "Dallas",
            "full_name": "Job Car Dealership",
            "id": 9,
            "lat": 32.7086,
            "long": -96.7955,
            "short_name": "Job",
            "st": "TX",
            "state": "Texas",
            "zip": "75216"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109628b",
            "_rev": "1-1510e7ca88f225bef573a98f9cb45452",
            "address": "108 Memorial Pass",
            "city": "Washington",
            "full_name": "Alphazap Car Dealership",
            "id": 10,
            "lat": 38.9067,
            "long": -77.0312,
            "short_name": "Alphazap",
            "st": "DC",
            "state": "District of Columbia",
            "zip": "20005"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651096bbe",
            "_rev": "1-25e4e732c54e2138a7d6c344f7c906f4",
            "address": "8108 Dryden Court",
            "city": "Carol Stream",
            "full_name": "Rank Car Dealership",
            "id": 11,
            "lat": 41.9166,
            "long": -88.1208,
            "short_name": "Rank",
            "st": "IL",
            "state": "Illinois",
            "zip": "60351"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510978c8",
            "_rev": "1-87eca1b09104f3efd4373e4edfacbb38",
            "address": "168 Pawling Lane",
            "city": "Silver Spring",
            "full_name": "Tin Car Dealership",
            "id": 12,
            "lat": 39.144,
            "long": -77.2076,
            "short_name": "Tin",
            "st": "MD",
            "state": "Maryland",
            "zip": "20918"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b651097add",
            "_rev": "1-97762bda9286ea2d1218a64383ab5370",
            "address": "452 Fair Oaks Drive",
            "city": "Baltimore",
            "full_name": "Y-Solowarm Car Dealership",
            "id": 13,
            "lat": 39.2847,
            "long": -76.6205,
            "short_name": "Y-Solowarm",
            "st": "MD",
            "state": "Maryland",
            "zip": "21275"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510988e3",
            "_rev": "1-7828b3ead20b34e43a00d8305fee6cd2",
            "address": "2109 Scott Parkway",
            "city": "San Francisco",
            "full_name": "It Car Dealership",
            "id": 14,
            "lat": 37.7848,
            "long": -122.7278,
            "short_name": "It",
            "st": "CA",
            "state": "California",
            "zip": "94147"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109952e",
            "_rev": "1-018064051a79bae4a38595f6d712f1f4",
            "address": "5057 Pankratz Hill",
            "city": "San Antonio",
            "full_name": "Tempsoft Car Dealership",
            "id": 15,
            "lat": 29.3875,
            "long": -98.5245,
            "short_name": "Tempsoft",
            "st": "TX",
            "state": "Texas",
            "zip": "78225"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109a29d",
            "_rev": "1-cfc990372e5aead5c1461c5363ab9661",
            "address": "0 Rieder Trail",
            "city": "El Paso",
            "full_name": "Treeflex Car Dealership",
            "id": 16,
            "lat": 31.6948,
            "long": -106.3,
            "short_name": "Treeflex",
            "st": "TX",
            "state": "Texas",
            "zip": "79994"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109a55a",
            "_rev": "1-ee4a7286b4515e5c4ef7fb152c6dc37d",
            "address": "7670 American Ash Drive",
            "city": "San Jose",
            "full_name": "Home Ing Car Dealership",
            "id": 17,
            "lat": 37.2602,
            "long": -121.7709,
            "short_name": "Home Ing",
            "st": "CA",
            "state": "California",
            "zip": "95138"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109a967",
            "_rev": "1-2c1ccca9532d409320038cb83d4f80d6",
            "address": "4 Pearson Avenue",
            "city": "Whittier",
            "full_name": "Bitchip Car Dealership",
            "id": 18,
            "lat": 33.9413,
            "long": -118.0356,
            "short_name": "Bitchip",
            "st": "CA",
            "state": "California",
            "zip": "90605"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109b7b6",
            "_rev": "1-4467795f20d7931f351651580bc75d0d",
            "address": "93 Monument Circle",
            "city": "Hialeah",
            "full_name": "Otcom Car Dealership",
            "id": 19,
            "lat": 25.8594,
            "long": -80.2725,
            "short_name": "Otcom",
            "st": "FL",
            "state": "Florida",
            "zip": "33013"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109bf51",
            "_rev": "1-3518514abb91e959ae2c73d2a0468962",
            "address": "4580 Waubesa Lane",
            "city": "Detroit",
            "full_name": "Subin Car Dealership",
            "id": 20,
            "lat": 42.4098,
            "long": -82.9441,
            "short_name": "Subin",
            "st": "MI",
            "state": "Michigan",
            "zip": "48224"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109ce39",
            "_rev": "1-3f78374abc08662f7f9bde1cc4b726a6",
            "address": "046 Mockingbird Junction",
            "city": "San Francisco",
            "full_name": "Andalax Car Dealership",
            "id": 21,
            "lat": 37.7848,
            "long": -122.7278,
            "short_name": "Andalax",
            "st": "CA",
            "state": "California",
            "zip": "94154"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109d879",
            "_rev": "1-cd8b9f26a5f3445ac312f1242a67fe6b",
            "address": "45737 Butternut Lane",
            "city": "Fort Lauderdale",
            "full_name": "Y-Solowarm Car Dealership",
            "id": 22,
            "lat": 26.0663,
            "long": -80.3339,
            "short_name": "Y-Solowarm",
            "st": "FL",
            "state": "Florida",
            "zip": "33330"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109de81",
            "_rev": "1-35acfb718ff5e840b6dfa2234635a9cc",
            "address": "21425 Bartelt Pass",
            "city": "Des Moines",
            "full_name": "Bitchip Car Dealership",
            "id": 23,
            "lat": 41.6727,
            "long": -93.5722,
            "short_name": "Bitchip",
            "st": "IA",
            "state": "Iowa",
            "zip": "50936"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109dfc0",
            "_rev": "1-f64046127bcb266e6d8621a6e0761edf",
            "address": "408 Delaware Circle",
            "city": "Utica",
            "full_name": "Aerified Car Dealership",
            "id": 24,
            "lat": 43.0872,
            "long": -75.2603,
            "short_name": "Aerified",
            "st": "NY",
            "state": "New York",
            "zip": "13505"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109ea38",
            "_rev": "1-b9645c81abd6ad8111bbd1c3adddc211",
            "address": "6505 Melrose Junction",
            "city": "Washington",
            "full_name": "Opela Car Dealership",
            "id": 25,
            "lat": 38.8933,
            "long": -77.0146,
            "short_name": "Opela",
            "st": "DC",
            "state": "District of Columbia",
            "zip": "20580"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b65109f8b9",
            "_rev": "1-4ca2683a2bc5d6adc9d7f17d6a6d3815",
            "address": "306 Jenna Parkway",
            "city": "Pittsburgh",
            "full_name": "Flowdesk Car Dealership",
            "id": 26,
            "lat": 40.4344,
            "long": -80.0248,
            "short_name": "Flowdesk",
            "st": "PA",
            "state": "Pennsylvania",
            "zip": "15279"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a033b",
            "_rev": "1-0d1ad5ed7cfde86fde2b69345e3b8163",
            "address": "95321 Superior Hill",
            "city": "San Antonio",
            "full_name": "Namfix Car Dealership",
            "id": 27,
            "lat": 29.4189,
            "long": -98.6895,
            "short_name": "Namfix",
            "st": "TX",
            "state": "Texas",
            "zip": "78245"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a0ab5",
            "_rev": "1-fdc867c57002345cfe2e0d17fbb0d4b1",
            "address": "5458 Maple Way",
            "city": "Hialeah",
            "full_name": "Fixflex Car Dealership",
            "id": 28,
            "lat": 25.9098,
            "long": -80.3889,
            "short_name": "Fixflex",
            "st": "FL",
            "state": "Florida",
            "zip": "33018"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a10b9",
            "_rev": "1-a017eedc4af988246172b38580dd1bc5",
            "address": "9 Harper Circle",
            "city": "San Francisco",
            "full_name": "Fix San Car Dealership",
            "id": 29,
            "lat": 37.7509,
            "long": -122.4153,
            "short_name": "Fix San",
            "st": "CA",
            "state": "California",
            "zip": "94110"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a1d3b",
            "_rev": "1-bc91c48db51d66e73a2e6b759f566014",
            "address": "5423 Spaight Road",
            "city": "Houston",
            "full_name": "Opela Car Dealership",
            "id": 30,
            "lat": 29.834,
            "long": -95.4342,
            "short_name": "Opela",
            "st": "TX",
            "state": "Texas",
            "zip": "77218"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a2451",
            "_rev": "1-9000d475bd23c5fd22121b16319db543",
            "address": "5 Northfield Pass",
            "city": "New York City",
            "full_name": "Fintone Car Dealership",
            "id": 31,
            "lat": 40.7808,
            "long": -73.9772,
            "short_name": "Fintone",
            "st": "NY",
            "state": "New York",
            "zip": "10131"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a2acc",
            "_rev": "1-cdbfaad14f48d0bd80b435460a802b38",
            "address": "3 Carey Junction",
            "city": "Wilkes Barre",
            "full_name": "Subin Car Dealership",
            "id": 32,
            "lat": 41.2722,
            "long": -75.8801,
            "short_name": "Subin",
            "st": "PA",
            "state": "Pennsylvania",
            "zip": "18768"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a3243",
            "_rev": "1-c6418f907fbb6365e6a996004b7100f0",
            "address": "627 Cottonwood Circle",
            "city": "Des Moines",
            "full_name": "Tres-Zap Car Dealership",
            "id": 33,
            "lat": 41.6727,
            "long": -93.5722,
            "short_name": "Tres-Zap",
            "st": "IA",
            "state": "Iowa",
            "zip": "50335"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a3ab4",
            "_rev": "1-4d8add6ff98d59554709f3bd95e0b7fa",
            "address": "8 Green Hill",
            "city": "Silver Spring",
            "full_name": "Gembucket Car Dealership",
            "id": 34,
            "lat": 39.0668,
            "long": -76.9969,
            "short_name": "Gembucket",
            "st": "MD",
            "state": "Maryland",
            "zip": "20904"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a409b",
            "_rev": "1-046cb455b152448daea503bc1fb84941",
            "address": "9 Beilfuss Trail",
            "city": "Seattle",
            "full_name": "Treeflex Car Dealership",
            "id": 35,
            "lat": 47.4497,
            "long": -122.3076,
            "short_name": "Treeflex",
            "st": "WA",
            "state": "Washington",
            "zip": "98158"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a4c83",
            "_rev": "1-9a5b78f2e289c88181452eae51029f19",
            "address": "311 Paget Alley",
            "city": "Vienna",
            "full_name": "Latlux Car Dealership",
            "id": 36,
            "lat": 38.8318,
            "long": -77.2888,
            "short_name": "Latlux",
            "st": "VA",
            "state": "Virginia",
            "zip": "22184"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a53ab",
            "_rev": "1-0938f528ee4ec72ba5710e4f855e3688",
            "address": "152 Moland Lane",
            "city": "Detroit",
            "full_name": "Ventosanzap Car Dealership",
            "id": 37,
            "lat": 42.4098,
            "long": -82.9441,
            "short_name": "Ventosanzap",
            "st": "MI",
            "state": "Michigan",
            "zip": "48224"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a5ab7",
            "_rev": "1-6e07d6d5c6d7a616ba7b7358db413d1a",
            "address": "821 New Castle Trail",
            "city": "Dallas",
            "full_name": "Zamit Car Dealership",
            "id": 38,
            "lat": 32.7887,
            "long": -96.7676,
            "short_name": "Zamit",
            "st": "TX",
            "state": "Texas",
            "zip": "75226"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a5f8b",
            "_rev": "1-aad3e04d9c8755694ad22d3bb6915553",
            "address": "990 Raven Road",
            "city": "Fresno",
            "full_name": "Stronghold Car Dealership",
            "id": 39,
            "lat": 36.7464,
            "long": -119.6397,
            "short_name": "Stronghold",
            "st": "CA",
            "state": "California",
            "zip": "93740"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a6596",
            "_rev": "1-50617ded0848567bbdbda0551272923b",
            "address": "89375 Main Trail",
            "city": "Merrifield",
            "full_name": "Greenlam Car Dealership",
            "id": 40,
            "lat": 38.8318,
            "long": -77.2888,
            "short_name": "Greenlam",
            "st": "VA",
            "state": "Virginia",
            "zip": "22119"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a682f",
            "_rev": "1-e258b026351685c07473fd61d7facca1",
            "address": "9 Sherman Hill",
            "city": "Baltimore",
            "full_name": "Tres-Zap Car Dealership",
            "id": 41,
            "lat": 39.2847,
            "long": -76.6205,
            "short_name": "Tres-Zap",
            "st": "MD",
            "state": "Maryland",
            "zip": "21275"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a722f",
            "_rev": "1-a627885eb87bc547ab133dc9ecea681b",
            "address": "62 Manley Point",
            "city": "Jersey City",
            "full_name": "Konklab Car Dealership",
            "id": 42,
            "lat": 40.7324,
            "long": -74.0431,
            "short_name": "Konklab",
            "st": "NJ",
            "state": "New Jersey",
            "zip": "07310"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a7d91",
            "_rev": "1-0ef43a2fc9385b68c4365489004d2b97",
            "address": "91 Declaration Avenue",
            "city": "Atlanta",
            "full_name": "Opela Car Dealership",
            "id": 43,
            "lat": 33.8913,
            "long": -84.0746,
            "short_name": "Opela",
            "st": "GA",
            "state": "Georgia",
            "zip": "31119"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a8142",
            "_rev": "1-2acfaaf786b749f0c71351f6468dfbaa",
            "address": "0 Northview Point",
            "city": "Roanoke",
            "full_name": "Veribet Car Dealership",
            "id": 44,
            "lat": 37.2327,
            "long": -79.9463,
            "short_name": "Veribet",
            "st": "VA",
            "state": "Virginia",
            "zip": "24014"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a8dbb",
            "_rev": "1-759fc681fcdf10e034bbf8accd3acb00",
            "address": "283 Mockingbird Plaza",
            "city": "Norfolk",
            "full_name": "Konklux Car Dealership",
            "id": 45,
            "lat": 36.8787,
            "long": -76.2604,
            "short_name": "Konklux",
            "st": "VA",
            "state": "Virginia",
            "zip": "23509"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510a9b70",
            "_rev": "1-76c2eb4c28da3ba6cd385dfb820ed4d0",
            "address": "527 Hayes Junction",
            "city": "New Orleans",
            "full_name": "Regrant Car Dealership",
            "id": 46,
            "lat": 30.033,
            "long": -89.8826,
            "short_name": "Regrant",
            "st": "LA",
            "state": "Louisiana",
            "zip": "70165"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510aa339",
            "_rev": "1-83ab719b3f039b858e9e7c9c9462748d",
            "address": "840 Pepper Wood Crossing",
            "city": "Stamford",
            "full_name": "Prodder Car Dealership",
            "id": 47,
            "lat": 41.0888,
            "long": -73.5435,
            "short_name": "Prodder",
            "st": "CT",
            "state": "Connecticut",
            "zip": "06905"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510aa97e",
            "_rev": "1-0d5f62c07f25299a7d95b6422f193c63",
            "address": "48610 Morning Street",
            "city": "Tucson",
            "full_name": "It Car Dealership",
            "id": 48,
            "lat": 32.2138,
            "long": -110.824,
            "short_name": "It",
            "st": "AZ",
            "state": "Arizona",
            "zip": "85710"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510aaee8",
            "_rev": "1-b07c086e72acf42643a1a478e2a07feb",
            "address": "222 Grasskamp Plaza",
            "city": "Athens",
            "full_name": "Veribet Car Dealership",
            "id": 49,
            "lat": 33.9321,
            "long": -83.3525,
            "short_name": "Veribet",
            "st": "GA",
            "state": "Georgia",
            "zip": "30605"
        },
        {
            "_id": "87a6635f9858bb5ef7d768b6510aba3e",
            "_rev": "1-eba2086b344cc60c0a4dd407a6ced307",
            "address": "76 Clove Trail",
            "city": "Atlanta",
            "full_name": "Aerified Car Dealership",
            "id": 50,
            "lat": 33.7217,
            "long": -84.3339,
            "short_name": "Aerified",
            "st": "GA",
            "state": "Georgia",
            "zip": "30316"
        }]
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

