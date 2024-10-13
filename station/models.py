from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()      # Use Decimal ???
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_routes")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class TrainType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE, related_name="trains")

    @property
    def capacity(self) -> int:
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return f"{self.name}({self.train_type.name})"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="journeys")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="journeys")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys", blank=True)

    def __str__(self):
        return f"{self.route} {self.train.name} Departure: {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"{self.user}({str(self.created_at)})"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_ticket(cargo, seat, train, error_to_raise):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "places_in_cargo"),
        ]:
            count_attrs = getattr(train, train_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {train_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.journey.train,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.journey.route} cargo: {self.cargo} seat: {self.seat}"

    class Meta:
        unique_together = ("journey", "cargo", "seat")
