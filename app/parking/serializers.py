from rest_framework import serializers
from . models import Parking


class ParkingSerializer(serializers.ModelSerializer):
    """ Parking Model Serializer """
    reserved_count = serializers.CharField()
    class Meta:
        model = Parking
        fields = (
            'name',
            'address',
            'latitude',
            'longitude',
            'capacity',
            'reserved_count',
        )
