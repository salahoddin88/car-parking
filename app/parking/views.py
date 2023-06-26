from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django.db.models import (
    Count,
    Q,
    F,
)
from django.utils import timezone
from rest_framework import (
    viewsets,
)
from parking.models import Parking
from parking.serializers import ParkingSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'lat',
                OpenApiTypes.STR,
                description='latitude to filters',
            ),
            OpenApiParameter(
                'lon',
                OpenApiTypes.STR,
                description='longitude to filters',
            ),
            OpenApiParameter(
                'radius',
                OpenApiTypes.STR,
                description='Radius in meter',
            ),
        ]
    )
)
class ParkingViewSet(viewsets.ModelViewSet):

    """ Parking REST API """

    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()
    http_method_names = ['get']

    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        filters = {}
        if self.request.query_params.get('lat') \
           and self.request.query_params.get('lon') \
           and self.request.query_params.get('radius'):

            search_lat = float(self.request.query_params.get('lat'))
            search_lon = float(self.request.query_params.get('lon'))
            radius = float(self.request.query_params.get('radius'))
            radius_degrees = radius / 111000
            min_lat = search_lat - radius_degrees
            max_lat = search_lat + radius_degrees
            min_lon = search_lon - radius_degrees
            max_lon = search_lon + radius_degrees

            filters = {
                'latitude__gte': min_lat,
                'latitude__lte': max_lat,
                'longitude__gte': min_lon,
                'longitude__lte': max_lon,
                }

        cd = timezone.now()
        available_parkings = Parking.objects.prefetch_related(
            'parking_reservation'
        ).annotate(
            reserved_count=Count(
                'parking_reservation',
                filter=Q(
                    parking_reservation__reservation_end_date_time__gt=cd
                )
            )
        ).filter(capacity__gt=F('reserved_count'), **filters).values(
            'name',
            'address',
            'latitude',
            'longitude',
            'capacity',
            'reserved_count'
        ).order_by('reserved_count')
        return available_parkings
