import requests
import pandas as pd
from io import StringIO
from decouple import config
from django.apps import apps


class DataHandler:
    URL_CITY = config('URL_CITY')
    URL_HOTEL = config('URL_HOTEL')

    def __init__(self, django_app, db_model_name):
        """
        Class for handling all data-related actions like fetching, parsing and writing data.
        """

        self.response = None
        self.df = None
        self.django_app = django_app
        self.db_model_name = db_model_name
        self.db_model = apps.get_model(self.django_app, self.db_model_name)
        self.db_model_column_names = [f.name for f in self.db_model._meta.fields]
        self.db_model_relational_columns = self._get_relational_columns_dict()

    def fetch_data(self):
        """
        Method for retrieving the data from the webserver by performing an authenticated HTTP GET request.
        """

        url = config(f'URL_{self.db_model_name.upper()}')
        headers = {
            "Username": config('URL_USERNAME'),
            "Password": config('URL_PASSWORD')
        }
        try:
            self.response = requests.get(url, headers=headers)
        except:
            self.response = None

    def get_status_code(self):
        return self.response.status_code

    def parse_data(self):
        """
        Method for parsing the raw text response data and transforming it into a pandas dataframe
        """

        data = StringIO(self.response.text)
        self.df = pd.read_csv(data, delimiter=";", header=None, names=self.db_model_column_names)

    def _get_relational_columns_dict(self):
        """
        Private method for building up a dictionary in the following form: {'column name': related model object, etc...}
        :return: the builded dictionary
        """

        relational_columns = {}

        for column_obj in self.db_model._meta.get_fields():
            # If the column is a foreign key and the column is not auto created by Django
            if column_obj.is_relation and not column_obj.auto_created:
                relational_columns[column_obj.name] = column_obj.related_model

        return relational_columns

    def write_to_db(self):
        """
        This method creates a list with database records and writes that list with records into the database.
        For each row and for each column within that row is checked if the column is a foreign key.
        If that is the case, then the related model instance is passed into the database record instead of the value
        itself.
        """

        db_records = []

        for _, row in self.df.iterrows():
            db_record = {}

            for column in self.db_model_column_names:
                # If the column is a foreign key
                if column in self.db_model_relational_columns:
                    # Get the related model (table where the foreign key is referencing to)
                    related_model = self.db_model_relational_columns[column]
                    # From that model, get the correct record that corresponds to the collected foreign key value
                    related_db_record = related_model.objects.get(pk=row[column])
                    db_record[column] = related_db_record
                else:
                    db_record[column] = row[column]

            # Add the record into the list with all database records
            db_records.append(self.db_model(**db_record))

        # Write the list with database records at once to the database
        # The 'ignore_conflicts' parameter is used to skip records from the bulk that are already in the database.
        # This is needed to avoid duplicate errors like 'duplicate entry'.
        self.db_model.objects.bulk_create(db_records, ignore_conflicts=True)
