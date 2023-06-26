from django.contrib import admin
from . models import (
    Parking,
    Reservation
)


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    """ Parking Admin Class """
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', )
    list_filter = ("capacity", )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """ Reservation Admin Class """
    list_display = (
        'parking',
        'user',
        'reservation_date_time',
        'reservation_end_date_time',
        'reservation_hours'
    )
    search_fields = ('name', )
    list_filter = ("parking", )
    date_hierarchy = "reservation_date_time"
