# Introduction
This is the capstone prject for full stack nanodegree which is a casting agency which models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. This was created using python and flask to create the backend with postgres as a database also using Auth0 for authentication. 

#### Virtual Enviornment

It is recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
 Run th follwing coammnd to upgrade the migrations made 
```bash
flask db upgrade
```
## Running the server

From within the project directory first ensure you are working using your created virtual environment and ensure you are inside it.

To run the server on MAC, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

To run the server on windows, execute:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` directory and the `app.py` file to find the application. 

# Testing Endpoints in development

There is a postman collection added in the project named "" for testing the endpoints with different tokens for differnet users, use it to test the endpoints.

# Testing Endpoints in prod

URL
```bash
https://capstonefsnd2020.herokuapp.com/
```

There is a postman collection added in the project named "" for testing the endpoints in prodction or the deployed the project in heroku with different tokens for differnet users.

# AUTH

Auth0 is used for authentication in this project , if you need new tokens 

## Roles
The app use Role-based access cotrol to restrict access and to give different permissions to differnet users

- There is three roles:

  1- Casting Assistant
    - Can view actors and movies

  2- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies

  3- Executive Produce
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

# Endpoints

GET '/movies'
- Fetches a list of movies
- Request Arguments: None
- Returns: json which contain a list of movies. 

```bash
{
    "movies": [
        {
            "id": 1,
            "release_date": "1990",
            "title": "The legend of 1900"
        }
    ],
    "success": true
}
```

POST '/movies'
- Creates a new movie
- Request Arguments:  body containg movie object
- Returns: json object containing list of updated movies after creation, success

```bash
{
    "movie": [
        {
            "id": 1,
            "release_date": "1990",
            "title": "The legend of 1900"
        },
        {
            "id": 2,
            "release_date": "1990",
            "title": "The legend of 1900"
        }
    ],
    "success": true
}
```

DELETE '/movies/<int:movie_id>'
- Delete movie based on a given id
- Request Arguments: Parameter named 'movie_id'
- Returns: json object containing delete id, success

```bash
{
    "delete": "1",
    "success": true
}
```

PATCH '/movies'
- partially or fully update a movie
- Request Arguments:  body containg updated movie object
- Returns: json object containing the updated movie after patch, success

```bash
{
    "movie": [
        {
            "id": 2,
            "release_date": "1990",
            "title": "updated"
        }
    ],
    "success": true
}
```

GET '/actors'
- Fetches a list of actors
- Request Arguments: None
- Returns: json which contain a list of actors. 

```bash
{
    "actors": [
        {
            "age": 50,
            "gender": "male",
            "id": 2,
            "name": "test"
        }
    ],
    "success": true
}
```

POST '/actors'
- Creates a new actor
- Request Arguments:  body containg actor object
- Returns: json object containing list of updated actors after creation, success

```bash
{
    "actors": [
        {
            "age": 50,
            "gender": "male",
            "id": 2,
            "name": "test"
        }
    ],
    "success": true
}
```

DELETE '/actors/<int:actor_id>'
- Delete actor based on a given id
- Request Arguments: Parameter named 'actor_id'
- Returns: json object containing delete id, success

```bash
{
    "delete": "2",
    "success": true
}
```

PATCH '/actors'
- partially or fully update an actor
- Request Arguments:  body containg updated actor object
- Returns: json object containing list of updated actors after patch, success

```bash
{
    "actors": [
        {
            "age": 50,
            "gender": "male",
            "id": 3,
            "name": "test"
        },
        {
            "age": 50,
            "gender": "male",
            "id": 4,
            "name": "test"
        }
    ],
    "success": true
}
```

## Unit Test
To run the unit tests, run this command inside enviroment

```bash
python test_app.py 
```