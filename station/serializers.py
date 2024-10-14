from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station.models import (
    Crew,
    Station,
    Route,
    TrainType,
    Train,
    Journey,
    Order,
    Ticket
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_station = serializers.CharField(source="source.name", read_only=True)
    destination_station = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source_station", "destination_station", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer(read_only=True)
    destination = StationSerializer(read_only=True)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "name", "cargo_num", "places_in_cargo", "train_type")


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name", read_only=True)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ("id", "route", "train", "departure_time", "arrival_time", "crew")


class JourneyListSerializer(JourneySerializer):
    train_name = serializers.CharField(source="train.name", read_only=True)
    train_capacity = serializers.IntegerField(
        source="train.capacity", read_only=True
    )
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    route_path = serializers.SerializerMethodField()

    class Meta:
        model = Journey
        fields = ("id", "route_path", "train_name", "train_capacity", "departure_time", "arrival_time", "crew")

    def get_route_path(self, obj):
        return f"{obj.route.source.name} - {obj.route.destination.name}"


class JourneyDetailSerializer(JourneySerializer):
    route = RouteListSerializer(read_only=True)
    train = TrainListSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"],
            attrs["seat"],
            attrs["journey"].train,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")


class TicketListSerializer(TicketSerializer):
    journey = JourneyListSerializer(read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("cargo", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    tickets = TicketListSerializer(many=True, read_only=True)
