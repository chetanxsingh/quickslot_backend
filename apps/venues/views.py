from rest_framework.generics import ListAPIView

from apps.venues.models import Venue
from apps.venues.serializers import VenueSerializer


class VenueListView(ListAPIView):
    serializer_class = VenueSerializer
    pagination_class = None

    def get_queryset(self):
        return Venue.objects.filter(is_active=True)

