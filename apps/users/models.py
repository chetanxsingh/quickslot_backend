from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return self.display_name

