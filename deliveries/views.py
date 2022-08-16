from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .serializers import CourierSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .service_functions import *

def home(request):
    return HttpResponse('home')


def courier_list(request):
    couriers = Courier.objects.all()
    serializer = CourierSerializer(couriers, many=True)
    return JsonResponse({'couriers': serializer.data})

@api_view(['POST'])
def resolve_address(request):
    address_str = request.data['string_address']  # TODO: add a check that the data is valid
    response = get_structured_address_from_address_string(address_str)
    return Response(response)

"""@api_view(['POST'])
def get_available_timeslots(request):
"""