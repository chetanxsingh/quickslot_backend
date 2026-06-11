from rest_framework import serializers

from apps.venues.models import Venue


class VenueSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source="get_sport_type_display", read_only=True)

    class Meta:
        model = Venue
        fields = (
            "id",
            "name",
            "sport_type",
            "sport_name",
            "address",
            "city",
        )

