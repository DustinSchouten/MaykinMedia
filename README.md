# MaykinMedia
Django webapp for collecting, storing and showing hotels and cities

![image](https://github.com/user-attachments/assets/5c2e912c-c56e-454b-85e0-98681f7a2d81)

![image](https://github.com/user-attachments/assets/e8a639ee-869a-4ca0-88b6-06df00a36605)

## Run the project
To run a Django project from this repository, you will need to follow a series of steps to make it work. Follow the steps below:
- Clone the repository by running `git clone https://github.com/DustinSchouten/MaykinMedia.git` in a new folder on your local machine and navigate to that project folder.
- Set up a virtual environment.
- Install the project dependencies by running `pip install -r requirements.txt`.
- Create a .env file on the same level as the folders `HotelApp`, `MaykinMedia` and `manage.py`. Put all environment variables in it.
- Apply the database migrations by running `python manage.py makemigrations` and then `python manage.py migrate`.
- (optional) To use the Django admin panel, create a superuseraccount by running `python manage.py createsuperuser`.
- Run the Django development server locally by running `python manage.py runserver`. The webapp can be visited at `http://127.0.0.1:8000/`.

## Project description
This Hotel app is a builded proof-of-concept for the case "Integrating third parties". It is a webapp written in Django where the user can view hotels and also filter on hotels by a specific city.

### Data
The data is retrieved from an authenticated HTTP server where two CSV-files are located. One of the files contains cities (PK and name) and the other contains hotels (PK, FK to city and name). See the simple datamodel below:
![image](https://github.com/user-attachments/assets/4233186f-0567-4fc3-b61a-f063308856fb)

In this Django project, these tables are represented as models and the data is stored in a MySQL database.

### Custom management command
In the app-folder in management/commands, a custom management command named `load_csv_data_into_db` is created for collecting the data and writing it into the database. This command can be called by running `python manage.py load_csv_data_into_db`.

### View and templates
The Django project contains one class-based view named `"Index"` with a `get()` and a `post()` method. The `get()` method is called when the user visits the page and the `post()` method is called when the user clicks on the Search-button. 

There are two HTML-templates used in this project:
#### - base.html
This file contains basic HTML-content like the `<header>` tag and the `<body>` tag with a `<h1>` tag but without the actual content. This is done so that new pages can easily be added by reusing this template.
#### - index.html
This file contains all HTML-content for showing the city input filter and the results section.

### Tests
In this project, seven unit tests are added in `tests.py`. These tests can be easily run with the command `python manage.py test HotelApp` in the terminal.