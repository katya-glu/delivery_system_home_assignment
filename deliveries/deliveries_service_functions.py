from .models import *


def book_delivery(user_email, timeslot_id):
    try:
        user = User.objects.get(email=user_email)
    except:
        return {'message': 'User does not exist. Please create user to book delivery'}

    try:
        timeslot = Timeslot.objects.get(id=timeslot_id)
    except:
        return {'message': 'Timeslot is not available. Please choose another timeslot'}

    if timeslot.status == timeslot.available:
        courier = timeslot.courier
        address = user.address
        new_delivery = Delivery(timeslot=timeslot, courier=courier, user=user, address=address)
        new_delivery.save()
        # courier status update
        if courier.num_of_remaining_deliveries > 0:  # courier not fully booked
            courier.num_of_remaining_deliveries -= 1
            if courier.num_of_remaining_deliveries == 0:
                courier.status = Courier.full
            courier.save()

        # timeslot status update
        if timeslot.num_of_scheduled_deliveries < Timeslot.max_num_of_deliveries:
            timeslot.num_of_scheduled_deliveries += 1
            if timeslot.num_of_scheduled_deliveries == Timeslot.max_num_of_deliveries:
                timeslot.status = Timeslot.not_available
            timeslot.save()

        return {'message': 'Delivery booked! Delivery ID: {}'.format(new_delivery.id)}


def mark_delivery_complete(user_email, delivery_id):
    # marks delivery as complete
    try:
        user = User.objects.get(email=user_email)
    except:
        return {'message': 'User does not exist'}

    try:
        delivery = Delivery.objects.get(id=delivery_id)
    except:
        return {'message': 'Delivery does not exist'}

    if user and delivery:
        if delivery.status != Delivery.completed:
            delivery.status = Delivery.completed
            delivery.save()
            return {'message': 'Delivery completed'}

        return {'message': 'Delivery already completed in the past'}


def cancel_delivery(user_email, delivery_id):
    # cancels a delivery
    try:
        user = User.objects.get(email=user_email)
    except:
        return {'message': 'User does not exist'}

    try:
        delivery = Delivery.objects.get(id=delivery_id)
    except:
        return {'message': 'Delivery does not exist'}

    if user and delivery:
        courier = delivery.courier
        # courier status update
        if courier.num_of_remaining_deliveries < Courier.max_num_of_remaining_deliveries_var:  # courier not fully booked
            courier.num_of_remaining_deliveries += 1
            if courier.status == Courier.full:
                courier.status = Courier.available

            courier.save()

        # timeslot status update
        timeslot = delivery.timeslot
        if timeslot.num_of_scheduled_deliveries > 0:
            timeslot.num_of_scheduled_deliveries -= 1
        if timeslot.status == Timeslot.not_available:  # status before deletion was full
            timeslot.status = Timeslot.available

        timeslot.save()
        delivery.delete()

        return {'message': 'Delivery deleted'}


def get_deliveries_for_specific_date(date):
    # returns list of deliveries scheduled for a specific date
    year = date.year
    month = date.month
    day = date.day
    try:
        daily_deliveries = Delivery.objects.filter(timeslot__start_time__year=year, timeslot__start_time__month=month,
                                                   timeslot__start_time__day=day)
    except:
        return []

    daily_deliveries_list = create_delivery_strings_list(daily_deliveries)
    return daily_deliveries_list


def create_delivery_strings_list(delivery_queries_list):
    deliveries_list = []
    for delivery_query in delivery_queries_list:
        delivery_id       = delivery_query.id
        timeslot_id       = delivery_query.timeslot.id
        delivery_date     = delivery_query.timeslot.start_time.date()
        delivery_string   = 'Delivery ID: {}, Timeslot ID: {}, Delivery date: {}'.format(delivery_id, timeslot_id, delivery_date)
        deliveries_list.append(delivery_string)
    return deliveries_list