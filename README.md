# Train Station API Service 🚇

> Django REST project 

This is a Django REST Framework (DRF) powered API for managing train station services, such as station, journeys, tickets and related entities. The API is designed to handle essential functionalities for a train transport system, including journey scheduling, station management, and user interactions. 

## Run service on your machine

* Install PostgresSQL 
* Create db 
* Set env file with your own credentials
```shell
git clone https://github.com/
cd train_station_api_service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
(Optional) You can load fixture data
```shell
python manage.py loaddata fixtures/data_fixture.json
```
You can use following user:
- email: `user2@exapmle.com`
- password: `3edcvbgt5`

## Run with Docker

Docker should be installed
```shell
docker-compose build
docker-compose up
```

## Features
* JWT Authentication
* Admin panel /admin/
* Swagger documentation
* Managing orders and tickets
* Creating stations, journeys, routes, crews, trains, train types,
* Creating orders and tickets 
* Filtering route model by destination or source
