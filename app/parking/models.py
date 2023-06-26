from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


class Parking(models.Model):
    """ Parking Model """
    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parkings"

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        """ String represenation of parking model object """
        return f"{self.name}"


class Reservation(models.Model):
    """ Parking Reservation Model """
    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    parking = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        related_name="parking_reservation",
        related_query_name="parking_reservation",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_reservation",
        related_query_name="user_reservation",
    )
    reservation_date_time = models.DateTimeField(auto_created=True)
    reservation_hours = models.PositiveSmallIntegerField()
    reservation_end_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """ String represenation of reservation model object """
        return f"{self.parking.name} - {self.user}"

    def save(self, *args, **kwargs):
        self.reservation_end_date_time = self.reservation_date_time + timedelta(hours=self.reservation_hours)
        super().save(*args, **kwargs)

