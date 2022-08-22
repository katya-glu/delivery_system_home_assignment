from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .service_functions import *
from datetime import datetime, timedelta


def home(request):
    return HttpResponse('home')


@api_view(['POST'])
def create_new_user(request):
    name = request.data['name']
    email = request.data['email']
    address_str = request.data['string_address']
    response = create_user(name, email, address_str)
    return Response(response)

@api_view(['POST'])
def get_available_timeslots(request):
    user_email = request.data['user_email']
    timeslots_obj = Timeslots()
    timeslots_list = timeslots_obj.get_available_timeslots(user_email)
    return JsonResponse(timeslots_list, safe=False)

@api_view(['POST'])
def book_new_delivery(request):
    email = request.data['email']
    timeslot_id = int(request.data['timeslot_id'])
    new_delivery = book_delivery(email, timeslot_id)
    return Response(new_delivery)

@api_view(['POST'])
def mark_complete(request, delivery_id):
    email = request.data['email']
    response = mark_delivery_complete(email, delivery_id)
    return Response(response)

@api_view(['DELETE'])
def delete_delivery(request, delivery_id):
    email = request.data['email']
    response = cancel_delivery(email, delivery_id)
    return Response(response)


@api_view(['GET'])
def get_daily_deliveries(request):
    today = datetime.now()
    daily_deliveries = get_deliveries_for_specific_date(today)
    if len(daily_deliveries) == 0:
        return JsonResponse({'message': 'No deliveries today'})

    return JsonResponse(daily_deliveries, safe=False)

@api_view(['GET'])
def get_weekly_deliveries(request):
    today = datetime.now()
    dates_list = [today]
    for num in range(1, 8):
        curr_date = today + timedelta(days=num)
        dates_list.append(curr_date)

    weekly_deliveries = []
    for date in dates_list:
        curr_date_deliveries = get_deliveries_for_specific_date(date)
        weekly_deliveries += curr_date_deliveries

    if len(weekly_deliveries) == 0:
        return JsonResponse({'message': 'No deliveries this week'})

    return JsonResponse(weekly_deliveries, safe=False)