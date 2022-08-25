# Magic the Gathering (MTG) Card Trading Application

Magic the Gathering (MTG) is a collectible card game with millions of players around the world.
Players have card collections with cards ranging in value from several cents to thousands of dollars. 
Players value their collections and in addition to purchasing cards also trade them with other players.  

This is a Flask REST API project which aims to enable players to create card collections and trade their cards with others.

The application's main entrypoint is contained within the `main.py` file.

The application was developed and tested using Python 3.10.5. 

## Getting Started

### Clone the application on your machine:

    git clone https://github.com/aleksandraangelova/MtgTrading

### Install requirements 

    pip install -r requirements.txt

### Set up Postgres
Create a Postgres database to host the application's data and paste the credentials in a .env file in the project's root 
directory. The migrations expect a database called mtgtrading to exist.  

The application expects the following environment variables in a .env file on your local machine.
Make sure you create your Postgres database in advance.

### .env file
    JWT_SECRET=
    DB_USER=
    DB_PASSWORD=
    DB_PORT=
    DB_NAME=
    AWS_KEY=
    AWS_SECRET_KEY=
    S3_REGION=
    S3_BUCKET_NAME=
    TEST_DB_USER=
    TEST_DB_PASSWORD=
    TEST_DB_PORT=
    TEST_DB_NAME=

### Provide the Flask environment variable
    set FLASK_APP=./main.py

### Create the database objects
    flask db upgrade

You are ready to run the application from `main.py`

Swagger documentation of the application is available at (http://127.0.0.1:5000/api/docs/)
