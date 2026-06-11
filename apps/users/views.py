from rest_framework.generics import ListAPIView

from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by("id")

