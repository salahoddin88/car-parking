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
    authentication,
    permissions,
    response,
    status,
    viewsets,
)
from parking.models import Parking, Reservation
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
    """ NOTE: Uncomment the following code to enable endpoint for authenticated user only """
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get_queryset(self):
        filters = {}
        if(
            self.request.query_params.get('lat') and
            self.request.query_params.get('lon') and
            self.request.query_params.get('radius')
            ):
            # Input parameters
            search_lat = float(self.request.query_params.get('lat'))  # Search latitude
            search_lon = float(self.request.query_params.get('lon'))  # Search longitude
            radius = float(self.request.query_params.get('radius'))  # Radius in meters

            # Convert the radius to degrees for the Haversine formula
            radius_degrees = radius / 111000

            # Calculate the latitude and longitude boundaries for the search
            min_lat = search_lat - radius_degrees
            max_lat = search_lat + radius_degrees
            min_lon = search_lon - radius_degrees
            max_lon = search_lon + radius_degrees

            filters = {
                'latitude__gte':min_lat,
                'latitude__lte':max_lat,
                'longitude__gte':min_lon,
                'longitude__lte':max_lon,
            }

        current_datetime = timezone.now()
        available_parkings = Parking.objects.annotate(
            reserved_count=Count(
                'parking_reservation',
                filter=Q(
                    parking_reservation__reservation_end_date_time__gt=current_datetime
                )
            )
        ).filter(capacity__gt=F('reserved_count'), **filters).values(
            'name',
            'address',
            'latitude',
            'longitude',
            'capacity',
            'reserved_count'
        )
        return available_parkings

    def get_context_data(self, **kwargs):
        context = super(ParkingView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'give-default-value')
        context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
        return context
