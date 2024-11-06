import pandas as pd
from django.test import TestCase
from .models import City, Hotel
from .data_handler import DataHandler

class Tests(TestCase):
    def setUp(self):
        self.city_handler = DataHandler('HotelApp', 'City')
        self.hotel_handler = DataHandler('HotelApp', 'Hotel')
        self.handlers = [self.city_handler, self.hotel_handler]

    def test_api_connection(self):
        """
        Test if the API requests from both the City and the Hotel data returns status code 200
        """

        for handler in self.handlers:
            handler.fetch_data()
            self.assertEqual(handler.get_status_code(), 200)

    def test_write_to_db(self):
        """
        Test if the number of hotel model objects that will be written into the database equals the number of
        objects that is collected from that database.
        """

        city_data = {'id': ['AMS'], 'name': ['Amsterdam']}
        hotel_data = {'id': ['AMS01', 'AMS02'], 'name': ['Hotel1', 'Hotel2'], 'city': ['AMS', 'AMS']}

        self.city_handler.df = pd.DataFrame(city_data)
        self.hotel_handler.df = pd.DataFrame(hotel_data)
        self.city_handler.write_to_db()
        self.hotel_handler.write_to_db()

        model_objects = Hotel.objects.select_related('city').all()
        self.assertEqual(len(model_objects), 2)

    def test_filtering_model_objects(self):
        """
        Test if the applied filter on the variable model_objects is actually not case sensitive.
        """

        # Create two variations of the city 'Amsterdam' and one of the city 'Antwerpen'
        city_amsterdam = City.objects.create(id="AMS", name="Amsterdam")
        Hotel.objects.create(id="AMS01", name="Hotel1", city=city_amsterdam)
        Hotel.objects.create(id="AMS02", name="Hotel2", city=city_amsterdam)
        city_antwerpen = City.objects.create(id="ANT", name="Antwerpen")
        Hotel.objects.create(id="ANT01", name="Hotel1", city=city_antwerpen)

        # Apply different variations of city filters and check if the number of filtered objects is the same
        # as expected.
        model_objects = Hotel.objects.select_related('city').filter(city__name__iexact='Amsterdam')
        self.assertEqual(len(model_objects), 2)
        model_objects = Hotel.objects.select_related('city').filter(city__name__iexact='AMSTERDAM')
        self.assertEqual(len(model_objects), 2)
        model_objects = Hotel.objects.select_related('city').filter(city__name__iexact='amsterdam')
        self.assertEqual(len(model_objects), 2)
        model_objects = Hotel.objects.select_related('city').filter(city__name__iexact='AmStErDaM')
        self.assertEqual(len(model_objects), 2)
        model_objects = Hotel.objects.select_related('city').filter(city__name__iexact='ams')
        self.assertEqual(len(model_objects), 0)

    def tearDown(self):
        pass


