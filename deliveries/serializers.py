from rest_framework import serializers
from .models import *

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'timeslot', 'status', 'address', 'courier', 'user']


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['id', 'courier_id', 'num_of_remaining_deliveries', 'date', 'status']


"""class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'courier_id', 'num_of_remaining_deliveries', 'date', 'status']"""