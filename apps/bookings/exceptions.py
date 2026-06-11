from rest_framework import status
from rest_framework.exceptions import APIException


class SlotAlreadyBooked(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This slot has already been booked."
    default_code = "slot_already_booked"

