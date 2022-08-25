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
directory. The migrations expect a database called `mtgtrading` to exist.  

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

### Create temp_files directory
Create an empty temp_files directory to store initially uploaded images before moving them to AWS.

You are ready to run the application from `main.py`

Swagger documentation of the application is available at (http://127.0.0.1:5000/api/docs/) but is currently incomplete.


## REST API
The following endpoints are available.  
Note: Only 2XX responses are described below.  
TODO: Describe responses != 2XX.

### User Register
Public endpoint.

#### Request

`POST /register/`

    curl --location --request POST 'http://127.0.0.1:5000/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{"first_name": "Aleksandra", "last_name": "Angelova", "city": "Sofia", "email": "a.angelova@test.com", "password": "password"}'

#### Response
`HTTP/1.1 201 CREATED`

    {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOm51bGwsImV4cCI6MTY2MTYxNzQwMX0.mGrF0bsKMeC5CdG1OZuY6r3Wd5jV_9h5LxZ43DmhpSs"
    }

### User Login
Public endpoint.

### Request

`POST /login/`

    curl --location --request POST 'http://127.0.0.1:5000/login/' \
    --header 'Content-Type: application/json' \
    --data-raw '{"email": "a.angelova@test.com", "password": "password"}'

#### Response

`HTTP/1.1 200 OK`

    {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTY2MTYxOTcxMX0.Z01oY6BBgSX8N13l3M9Es_28Yq-m_uoI4lFgKMeeGxk"
    }

### Create Card
Private endpoint accessible only to users who are logged in.  
Integration with AWS S3 is available - users should upload a photo of their card and it is stored in S3.  
Adds a new card to the user's collection. 

#### Request

`POST /card/`

    curl --location --request POST 'http://127.0.0.1:5000/card/' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTY2MTYyMDA5OX0.yQ1UgwNhf1AGQB4bbpR2X7aoq7KgSJs2ls_WQO2MAzc' \
    --data-raw {"name": "Nicol Bolas", "set": "Archenemy: Nicol Bolas", "condition": "mint", "tradeable": true, "foil": false, "photo": "<base64encoded image string>", "extension": "jpg"}

#### Response

`HTTP/1.1 201 CREATED`

    {
        "set": "Archenemy: Nicol Bolas",
        "tradeable": true,
        "foil": false,
        "name": "Nicol Bolas",
        "condition": "mint"
    }

### Get Cards in Collection
Private endpoint accessible only to users who are logged in.   
Gets the cards available in a user's collection.  
Users can only see their own collection - if they request to see the collection of another user, they will get a Forbidden response.

#### Request
`GET /trader/<id>/cards/`

    curl --location --request GET 'http://127.0.0.1:5000/trader/1/cards/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTY2MTE1NzMyN30.Xt9harrf_wdT98A9zADqMApvowe5-hOvZArzLZTAvWM'

#### Response 
`HTTP/1.1 200 OK`

    {
        "full_name": "Aleksandra Angelova",
        "cards": [
            {
                "set": "Test Set",
                "tradeable": true,
                "foil": false,
                "name": "Test Card 2",
                "condition": "CardCondition.mint"
            },
            {
                "set": "Test Set",
                "tradeable": true,
                "foil": false,
                "name": "Test Card 2",
                "condition": "CardCondition.mint"
            }
        ],
        "id": 1
    }

### Create Trade
Private endpoint accessible only to users who are logged in.  
Propose a trade with another trader.  
Users cannot create trades with themselves - there is a decorator validating that the counterparty_id != current user id.  
Integration with AWS SES has been done - when a trade is posted, the counterparty should receive an email about the event.  
TODO: handle errors when the counterparty does not exist in the database or does not own the requested cards.

#### Request
`POST /trade/`

    curl --location --request POST 'http://127.0.0.1:5000/trade/' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTY2MTYyMDA5OX0.yQ1UgwNhf1AGQB4bbpR2X7aoq7KgSJs2ls_WQO2MAzc' \
    --data-raw '{"requester_cards": [2], "counterparty_id": 6, "counterparty_cards": [3]}'

#### Response
`HTTP/1.1 201 CREATED`

    {
        "created_on": "2022-08-25T20:38:44.779071",
        "status": "pending",
        "id": 3
    }

### Get Trade Details
Private endpoint accessible only to users who are logged in.  
Get the details of a trade to which you are a party.  
Users can only see details of trades that they are parties to - if they request to see trades of other users, they will get a Forbidden response.

#### Request
`GET /trade/<id>/`

    curl --location --request GET 'http://127.0.0.1:5000/trade/3/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImV4cCI6MTY2MTYyMTgzNn0.2zjHdVHpXkMgDF4VK-gnfP54P5CAHZgmrRW28SqnOc8' 

#### Response

`HTTP/1.1 200 OK`

    {
        "created_on": "2022-08-25T20:38:44.779071",
        "status": "pending",
        "id": 3
    }

### Approve Trade
Private endpoint accessible only to users who are logged in.  
Approve a trade proposed by another trader.  
Only the counterparty to a trade can approve it. If you are not a trade counterparty, you will get a Forbidden response.  
Only a trade in status `Pending` can be approved.  
Once a trade is approved, an update to the cards table is made - card ownership is changed for the cards listed in the trade.

#### Request

`PUT /trade/<id>/approve/`

    curl --location --request PUT 'http://127.0.0.1:5000/trade/3/approve/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImV4cCI6MTY2MTYyMjgzNn0.f--LDQhzadS7I8vuT5JsWlNBgOqXiNVwJllhWqP-DEU'

#### Response

`HTTP/1.1 200 OK`

    {
        "transferred_to_requester": [
            3
        ],
        "status": "approved",
        "transferred_to_counterparty": [
            2
        ],
        "id": 3
    }

### Reject Trade
Private endpoint accessible only to users who are logged in.  
Approve a trade proposed by another trader.  
Only the counterparty to a trade can reject it. If you are not a trade counterparty, you will get a Forbidden response.  
Only a trade in status `Pending` can be rejected.  
No changes to card ownership are made.

#### Request

`PUT /trade/<id>/reject/`

    curl --location --request PUT 'http://127.0.0.1:5000/trade/3/reject/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImV4cCI6MTY2MTYyMjgzNn0.f--LDQhzadS7I8vuT5JsWlNBgOqXiNVwJllhWqP-DEU' 

#### Response

`HTTP/1.1 200 OK`

    {
        "transferred_to_requester": [],
        "status": "rejected",
        "transferred_to_counterparty": [],
        "id": 3
    }

### Get Cards for Trade
Private endpoint accessible only to users who are logged in.  
Get all the cards in the cards table that are tradeable. This is required so the user can pick the cards he/she wants to trade with another player.  

`GET /cards/tradeable/`

    curl --location --request GET 'http://127.0.0.1:5000/cards/tradeable' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjYsImV4cCI6MTY2MTYyMTgzNn0.2zjHdVHpXkMgDF4VK-gnfP54P5CAHZgmrRW28SqnOc8'

#### Response
`HTTP/1.1 200 OK`

    {
        "cards": [
            {
                "set": "Test Set",
                "tradeable": true,
                "owner_id": "1",
                "foil": false,
                "name": "Test Card 2",
                "condition": "mint"
            }
        ]
    }

### Get Trades
Private endpoint accessible only to users who are logged in.  
Get the details of all trade to which you are a party.  
Users can only see details of trades that they are parties to - if they request to see trades of other users, they will get a Forbidden response.

#### Request

`GET /trade/<trade_id>`

    curl --location --request GET 'http://127.0.0.1:5000/trade/3' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsImV4cCI6MTY2MTYyMjg4M30.JjguFg934TL56gotCdQKkDaNjZNwX9ztVbPPrNt8J6w'

#### Response 

`HTTP/1.1 200 OK`

    {
        "id": 3,
        "created_on": "2022-08-25T20:38:44.779071",
        "status": "rejected"
    }