from api_keys import *
import requests
from .models import *
import holidays
from datetime import datetime

def get_structured_address_from_address_string(address_str):
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
                # country_code = address_component['short_name']  # country code is needed for accessing Holiday API

        resolved_address = Address(street=street, house_num=home_num, city=city, country=country)
        resolved_address.save()

        return {'message': 'Address added to database'}

    elif response['status'] == 'ZERO_RESULTS':
        return {'message': 'Address does not exist. Please provide a valid address'}

    else:  # response['status'] is any other status
        return {'message': 'Something went wrong'}


class Timeslots:
    def __init__(self):
        self.available_timeslots_list = []
        self.user_city                = ''
        self.user_country        = ''
        #self.holidays                 = set()


    def get_available_timeslots(self, user_email):
        # returns all available timeslots in the upcoming week for user's address contained in user table in db.
        # decision whether the address is supported by specific courier is based on user_city
        user = User.objects.get(email=user_email)
        if user:    # TODO: add a redirect to user creation if user does not exist in db
            self.user_country = user.country
            self.user_city         = user.address_object.city
            self.get_holidays()

            timeslots = TimeslotsModel.query.filter_by(status=TimeslotsModel.available).all()
            for timeslot in timeslots:
                courier_id    = timeslot.courier_id
                timeslot_date = timeslot.date
                courier       = CouriersModel.query.filter_by(courier_id=courier_id, date=timeslot_date).first()

                if courier.status == CouriersModel.available and self.is_city_in_supported_addresses(timeslot) \
                        and not self.is_holiday(timeslot):
                    self.add_to_available_timeslots(timeslot)

                elif self.is_holiday(timeslot):    # if date is holiday, update timeslot as not available
                    timeslot.status = TimeslotsModel.not_available

            db.session.commit()

            return self.available_timeslots_list

        else:   # user does not exist in database
            return {'message': 'User does not exist. Please create user to see available timeslots'}


    def add_to_available_timeslots(self, timeslot):
        start_time      = timeslot.start_time
        start_time_str  = start_time.strftime('%d/%m/%Y, %H:%M')
        end_time        = timeslot.end_time
        end_time_str    = end_time.strftime('%d/%m/%Y, %H:%M')
        timeslot_string = '{}-{}'.format(start_time_str, end_time_str)
        timeslot_id_str = str(timeslot.timeslot_id)
        self.available_timeslots_list.append([timeslot_id_str, timeslot_string])


    def is_city_in_supported_addresses(self, timeslot):
        supported_addresses_list = timeslot.supported_addresses
        return (self.user_city in supported_addresses_list)


    def is_holiday(self, timeslot):
        date = timeslot.date.date()# TODO: check if needed
        return (date in self.holidays)


    def get_holidays(self):
        holidays_dict = holidays.country_holidays(self.user_country)
        for holiday in holidays_dict:
            # all holidays from dict are add to the holidays set (even though some holidays in Irsrael are considered workdays)
            # TODO: check which holiday is a workday
            holiday_datetime_obj = datetime.strptime(holiday['date'], '%Y-%m-%d')
            self.holidays.add(holiday_datetime_obj.date())
