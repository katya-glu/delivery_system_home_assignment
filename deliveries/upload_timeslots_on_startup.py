import json
from datetime import datetime
from .models import Courier, Timeslot

def load_courier_timeslots(json_file):
    # erase all timeslots from DB, in order to populate it again
    Courier.objects.all().delete()
    Timeslot.objects.all().delete()

    with open(json_file) as data_file:
        data = json.load(data_file)
        # data is a dictionary of weekdays as keys and list of lists as value. The list of lists contains a list per timeslot
        # that consists of start time as int/float and a list of supported addresses
        courier_id = data["courier_id"]
        for date_str in data["timeslots"]:
            date_next_weekday = datetime.strptime(date_str, '%d/%m/%Y').date()
            year, month, day = [date_next_weekday.year, date_next_weekday.month, date_next_weekday.day]
            # new row for each date per courier - tracking total num of deliveries booked (max of 10)
            new_date_for_courier_table = Courier(courier_id=courier_id,
                                                 num_of_remaining_deliveries=Courier.max_num_of_remaining_deliveries_var,
                                                 date=date_next_weekday, status=Courier.available)
            new_date_for_courier_table.save()
            timeslots_list = data["timeslots"][date_str]
            for timeslot in timeslots_list:
                timeslot_start_time_str, timeslot_end_time_str, supported_addresses_list = timeslot
                timeslot_start_time = datetime.strptime(timeslot_start_time_str, '%H:%M')
                timeslot_end_time   = datetime.strptime(timeslot_end_time_str, '%H:%M')
                new_timeslot_start_time = timeslot_start_time.replace(year=year, month=month, day=day)
                new_timeslot_end_time   = timeslot_end_time.replace(year=year, month=month, day=day)
                # new row for each timeslot per courier - tracking num of scheduled deliveries per timeslot (max of 2),
                # status. contains supported addresses info per timeslot
                new_timeslot = Timeslot(courier=new_date_for_courier_table, start_time=new_timeslot_start_time,
                                        end_time=new_timeslot_end_time, supported_addresses=supported_addresses_list)
                new_timeslot.save()