from django.urls import path

from apps.users.views import UserListView


urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
]

