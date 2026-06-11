from django.urls import path

from apps.venues.views import VenueListView


urlpatterns = [
    path("", VenueListView.as_view(), name="venue-list"),
]

