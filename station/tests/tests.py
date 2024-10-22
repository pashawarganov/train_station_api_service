from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.test import APIClient

from station.models import (
    Station,
    Route,
    Train, Journey
)
from station.serializers import (
    RouteListSerializer,
    RouteDetailSerializer,
)

ROUTE_URL = reverse("station:route-list")
JOURNEY_URL = reverse("station:journey-list")


def sample_route(**params):
    station1 = Station.objects.create(
        name="Station 1", latitude=70.0, longitude=53.5
    )
    station2 = Station.objects.create(
        name="Station 2", latitude=140.0, longitude=107.0
    )

    defaults = {
        "distance": 100,
        "destination": station1,
        "source": station2
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def detail_url(route_id):
    return reverse("station:route-detail", args=[route_id])


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

        self.station1 = Station.objects.create(name="Station 1", latitude=70.0, longitude=53.5)
        self.station2 = Station.objects.create(name="Station 2", latitude=30.0, longitude=105.0)

        self.route1 = sample_route(distance=100, destination=self.station1, source=self.station2)
        self.route2 = sample_route(distance=101, destination=self.station2, source=self.station1)
        self.route3 = sample_route(distance=0)

    def test_list_routes(self):
        sample_route()
        sample_route()

        res = self.client.get(ROUTE_URL)

        routes = Route.objects.order_by("id")
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_routes_by_destination(self):
        res = self.client.get(
            ROUTE_URL, {"destination": {self.station2.id}}
        )

        serializer2 = RouteListSerializer(self.route2)
        serializer3 = RouteListSerializer(self.route3)

        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_routes_by_source(self):
        res = self.client.get(
            ROUTE_URL, {"source": {self.station1.id}}
        )

        serializer2 = RouteListSerializer(self.route2)
        serializer3 = RouteListSerializer(self.route3)

        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_route_detail(self):
        url = detail_url(self.route1.id)
        res = self.client.get(url)

        serializer = RouteDetailSerializer(self.route1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_route_forbidden(self):
        payload = {"distance": 100}
        res = self.client.post(ROUTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.station1 = Station.objects.create(name="Station 1", latitude=70.0, longitude=53.5)
        self.station2 = Station.objects.create(name="Station 2", latitude=30.0, longitude=105.0)

    def test_create_route(self):
        payload = {
            "distance": 100,
            "source": self.station1.id,
            "destination": self.station2.id
        }
        res = self.client.post(ROUTE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        route = Route.objects.get(id=res.data["id"])
        source = route.source
        destination = route.destination
        self.assertEqual(source, self.station1)
        self.assertEqual(destination, self.station2)
