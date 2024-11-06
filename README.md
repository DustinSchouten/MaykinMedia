# MaykinMedia
Django webapp for collecting, storing and showing hotels and cities

![image](https://github.com/user-attachments/assets/5c2e912c-c56e-454b-85e0-98681f7a2d81)

![image](https://github.com/user-attachments/assets/e8a639ee-869a-4ca0-88b6-06df00a36605)

### Run the project
This Django webapp can be run locally by navigating to the app-folder `HotelApp` and then running the command `python manage.py runserver` in the terminal.

### Project description
This Hotel app is a builded proof-of-concept for the case "Integrating third parties". It is a webapp written in Django where the user can view hotels and also filter on hotels by a specific city.

#### Data
The data is retrieved from an authenticated HTTP server where two CSV-files are located. One of the files contains cities (PK and name) and the other contains hotels (PK, FK to city and name). See the simple datamodel below:
![image](https://github.com/user-attachments/assets/4233186f-0567-4fc3-b61a-f063308856fb)

In this Django project, these tables are represented as models and the data is stored in a MySQL database.

#### View and templates
The Django project contains one class-based view named 'Index' with a get() and a post() method. The get() method is called when the user visits the page and the post() method is called when the user clicks on the Search-button. 

There are three HTML-templates used in this project:
##### base.html
This file contains basic HTML-content like the `<header>` tag and the `<body>` tag with a `<h1>` tag but without the actual content. This is done so that new pages can easily be added by reusing this template.
##### index.html
This file contains all HTML-content for showing the city input filter and the results section.
##### error.html
This file contains HTML-content for showing an error page.

### Tests
In this project, three unit tests are added in `tests.py`. These tests can be easily run with the command `python manage.py test HotelApp` in the terminal.

##### test_api_connection()
Test if the API requests from both the City and the Hotel data returns status code 200
##### test_write_to_db()
Test if the number of hotel model objects that will be written into the database equals the number of objects that is collected from that database.
##### test_filtering_model_objects()
Test if the applied filter on the variable model_objects is actually not case sensitive.
