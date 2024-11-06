from django.shortcuts import render
from django.views import View
from .data_handler import DataHandler
from .models import City, Hotel
from .forms import CityForm


class Index(View):
    def get(self, request):
        """
        View-method to call when the user lands on the index page. Before the page will be rendered, the data from
        the API is collected and written to the database.
        :return: The index page or an error page
        """

        # Fetch the data from the specific city and hotel api and write it to the database
        model_names = ['City', 'Hotel']
        for model_name in model_names:
            handler = DataHandler('HotelApp',model_name)
            handler.fetch_data()
            # If the response status code returns 404, then render an error page
            if handler.get_status_code() == 404:
                return render(request, "HotelApp/error.html")
            handler.parse_data()
            handler.write_to_db()

        # Get all hotel objects with all related city objects into it.
        model_objects = Hotel.objects.select_related('city').all()

        # Get list with all available city names
        city_names = list(City.objects.values_list('name', flat=True))

        return render(request, "HotelApp/index.html", {"model_objects": model_objects, "city_names": city_names})

    def post(self, request):
        """
        View-method to call when the user fetches the data using a city filter. Before the page will be rendered, the
        stored data inside the model will be filtered with the city value.
        :return: The index page or an error page
        """

        city_form = CityForm(request.POST)

        # Get list with all available city names
        city_names = list(City.objects.values_list('name', flat=True))

        if city_form.is_valid():
            city_filter = request.POST.get('city')

            # Use the city filter to get all hotel objects from that specific city
            model_objects = Hotel.objects.select_related('city').filter(city__name__iexact=city_filter)

            return render(request, "HotelApp/index.html", {"model_objects": model_objects, "city_names": city_names})

        model_objects = Hotel.objects.select_related('city').all()
        return render(request, "HotelApp/index.html", {"model_objects": model_objects, "city_names": city_names})