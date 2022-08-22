from api_keys import *
import requests
from .models import *
import holidays
from datetime import datetime

def get_structured_address_from_address_string(address_str, user):
    params = {'key': geocoding_api_key, 'address': address_str}
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        # extract the relevant info from the response
        address_components = response['results'][0]['address_components']
        home_num, street, city, country = ["", "", "", ""]
        for address_component in address_components:
            if address_component['types'][0] == 'street_number':
                home_num = address_component['long_name']

            elif address_component['types'][0] == 'route':
                street = address_component['long_name']

            elif address_component['types'][0] == 'locality':
                city = address_component['long_name']

            elif address_component['types'][0] == 'country':
                country = address_component['long_name']

        resolved_address = Address(street=street, house_num=home_num, city=city, country=country, user=user)
        resolved_address.save()

        return {'message': 'Address added to database'}

    elif response['status'] == 'ZERO_RESULTS':
        return {'message': 'Address does not exist. Please provide a valid address'}

    else:  # response['status'] is any other status
        return {'message': 'Something went wrong'}


def create_user(name, email, address_str):
    name = name
    email = email
    user = User(name=name, email=email)
    user.save()
    resolved_address_response = get_structured_address_from_address_string(address_str, user)
    if resolved_address_response['message'] == 'Address added to database':
        return {'message': 'User created'}

    elif resolved_address_response['message'] == 'ZERO_RESULTS':
        return {'message': 'Please create user again using a valid address'}

    else:
        return {'message': 'Something went wrong'}


class Timeslots:
    def __init__(self):
        self.available_timeslots_list = []
        self.user_city                = ''
        self.user_country             = ''
        self.holidays                = set()


    def get_available_timeslots(self, user_email):
        # returns all available timeslots in the upcoming week for user's address contained in user table in db.
        # decision whether the address is supported by specific courier is based on user_city
        try:
            user = User.objects.get(email=user_email)
        except:
            return {'message': 'User does not exist. Please create user to see available timeslots'}

        self.user_country = user.address.country
        self.user_city    = user.address.city
        self.get_holidays()

        timeslots = Timeslot.objects.filter(status=Timeslot.available).all()
        for timeslot in timeslots:
            courier       = timeslot.courier

            if courier.status == Courier.available and self.is_city_in_supported_addresses(timeslot) \
                    and not self.is_holiday(timeslot):
                self.add_to_available_timeslots(timeslot)

            elif self.is_holiday(timeslot):    # if date is holiday, update timeslot as not available
                timeslot.status = Timeslot.not_available
                timeslot.save()

        return self.available_timeslots_list


    def add_to_available_timeslots(self, timeslot):
        start_time      = timeslot.start_time
        start_time_str  = start_time.strftime('%d/%m/%Y, %H:%M')
        end_time        = timeslot.end_time
        end_time_str    = end_time.strftime('%d/%m/%Y, %H:%M')
        timeslot_string = '{}-{}'.format(start_time_str, end_time_str)
        timeslot_id_str = str(timeslot.id)
        self.available_timeslots_list.append([timeslot_id_str, timeslot_string])


    def is_city_in_supported_addresses(self, timeslot):
        supported_addresses_list = timeslot.supported_addresses
        return (self.user_city in supported_addresses_list)


    def is_holiday(self, timeslot):
        date = timeslot.start_time.date()# TODO: check if needed
        return (date in self.holidays)


    def get_holidays(self):
        holidays_dict = holidays.country_holidays(self.user_country)
        for holiday in holidays_dict:
            # all holidays from dict are add to the holidays set (even though some holidays in Irsrael are considered workdays)
            # TODO: check which holiday is a workday
            holiday_datetime_obj = datetime.strptime(holiday['date'], '%Y-%m-%d')
            self.holidays.add(holiday_datetime_obj.date())


def book_delivery(user_email, timeslot_id):
    if User.objects.filter(email=user_email).exists():  # TODO: add a redirect to user creation if user does not exist in db
        user = User.objects.get(email=user_email)
        timeslot = Timeslot.objects.get(id=timeslot_id)
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

        else:  # timeslot is not available
            return {'message': 'Timeslot is not available. Please choose another timeslot'}

    else:  # user does not exist in database
        return {'message': 'User does not exist. Please create user to book a timeslot'}


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