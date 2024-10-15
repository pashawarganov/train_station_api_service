from django.urls import path, include
from rest_framework import routers

from station.views import (
    CrewViewSet,
    StationViewSet,
    TrainViewSet,
    TrainTypeViewSet,
    JourneyViewSet,
    OrderViewSet,
    TicketViewSet,
    RouteViewSet
)

app_name = "station"

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("train_types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]
