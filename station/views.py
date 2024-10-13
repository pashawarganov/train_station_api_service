from django.db.models import F
from rest_framework import viewsets

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
from station.serializers import (
    CrewSerializer,
    StationSerializer,
    RouteSerializer,
    TrainTypeSerializer,
    TrainSerializer,
    JourneySerializer,
    OrderSerializer,
    TicketSerializer,
    RouteListSerializer, TrainListSerializer, JourneyListSerializer, OrderListSerializer, TicketListSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        return RouteSerializer


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.select_related("train_type")

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer

        return TrainSerializer

class JourneyViewSet(viewsets.ModelViewSet):
    queryset = (
        Journey.objects
        .select_related("route", "train")
        .prefetch_related("crew")
    )   # 27 -> 23 -> 20

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer

        return JourneySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("journey__route", "order__user")

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer

        return TicketSerializer
