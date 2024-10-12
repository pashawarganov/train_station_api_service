from django.contrib.auth.models import User
from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.IntegerField()


class TrainType(models.Model):
    name = models.CharField(max_length=63)


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE, related_name="trains")


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="journeys")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="journeys")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
