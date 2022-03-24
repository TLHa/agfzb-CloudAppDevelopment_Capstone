import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth
import random
api_key = '83QizwpCda76_6QXPD0Q1tGndougBAjMAOlWI8xEzDwC'
watson_nul_service = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/6bf3caaf-c82c-44cf-a8f5-945e5a2e8a8c'

add_review_url = 'https://6e71488e.au-syd.apigw.appdomain.cloud/htl-capstone/api/review'

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},)
    except Exception as ex:
        # If any error occurs
        print('Error',ex)
        return json.dumps({
            'message':"Internal Server Error!"
        })
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_payload)
    except Exception as ex:
        # If any error occurs
        print('Error',ex)
        return json.dumps({
            'message':"Internal Server Error!"
        })
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    key_pair_params = []
    for key, value in kwargs:
        key_pair_params.append(f'{key}={value}')
    url = url + '?' + '&'.join(key_pair_params)
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url,**kwargs):
    results = []

    json_result = get_request(url,dealershipId = kwargs['dealerId'])
    if json_result:

        reviews = json_result["docs"]

        for review in reviews:
            review = DealerReview(another=review['another'] if review.get('another') else '',
                                  car_make=review['car_make'],
                                  car_model=review['car_model'],
                                  car_year=review['car_year'],
                                  dealership=review['dealership'],
                                  name=review['name'],
                                  purchase=review['purchase'],
                                  purchase_date=review['purchase_date'],
                                  review=review['review']
                                  )
            review.sentiment = analyze_review_sentiments(review.review)
            results.append(review)
    return results

def add_review_by_cf(review):
    response = post_request(add_review_url,{
        'review': review
    })
    return response

def analyze_review_sentiments(dealerreview):
    sentiment = ['positive','negative','neutral']
    index = random.randint(0,2)
    return sentiment[index]