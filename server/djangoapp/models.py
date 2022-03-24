from enum import Enum
from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.description}'

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModelType(Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    WAGON = "WAGON"
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class CarModel(models.Model):
    name = models.TextField()
    dealer_id = models.IntegerField()
    type = models.CharField(max_length=255, choices=CarModelType.choices())
    year = models.IntegerField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.dealer_id} - {self.type} - {self.year} - {self.car_make}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    address = models.TextField()
    city = models.TextField()
    full_name = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.TextField()
    st = models.TextField()
    state: models.TextField()
    zip: models.TextField()

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return super().__str__()


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(models.Model):
    another = models.TextField()
    car_make = models.TextField()
    car_model = models.TextField()
    car_year = models.IntegerField()
    dealership = models.IntegerField()
    name = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    review = models.TextField()
    sentiment = models.TextField()

    def __init__(self, another, car_make, car_model, car_year, dealership, name, purchase, purchase_date, review):
        self.another = another

        self.car_make = car_make

        self.car_model = car_model

        self.car_year = car_year

        self.dealership = dealership

        self.name = name

        self.purchase = purchase

        self.purchase_date = purchase_date

        self.review = review

    def __str__(self):
        return super().__str__()

