import json
import random
from datetime import datetime, timedelta, date

# courier id is random (each courier should have unique ID. in real life couriers should enter their ID)
courier_id_max_val = (2 ** 32) - 1
courier_id = random.randint(0, courier_id_max_val)

# generate dates for curr week, week starts on Monday
today = datetime.now()
curr_week_num = today.isocalendar()[1]
first_day_of_week = date.fromisocalendar(today.year, curr_week_num, 1)
curr_week_dates = []
for day_num in range(7):
    curr_date = first_day_of_week + timedelta(days=day_num)
    curr_date_str = curr_date.strftime("%d/%m/%Y")
    curr_week_dates.append(curr_date)


# value for each day of the week is a list of timeslot lists, each timeslot list contains starting time, end time and list of supported addresses
available_timeslots_dict = \
    {"courier_id": courier_id, "timeslots":
        {curr_week_dates[0].strftime("%d/%m/%Y"): [["08:00", "10:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan", "Bnei Brak"]],
                                                   ["12:00", "14:00", ["Ramat Gan", "Bnei Brak", "Petah Tikva"]],
                                                   ["14:00", "16:00", ["Bnei Brak", "Petah Tikva", "Rosh Haayin"]],
                                                   ["16:00", "18:00", ["Bnei Brak", "Petah Tikva", "Tel Aviv-Yafo"]]],
        curr_week_dates[1].strftime("%d/%m/%Y"):  [["08:00", "10:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan", "Bnei Brak"]],
                                                   ["12:00", "14:00", ["Ramat Gan", "Bnei Brak", "Petah Tikva"]],
                                                   ["14:00", "16:00", ["Bnei Brak", "Petah Tikva", "Rosh Haayin"]]],
        curr_week_dates[2].strftime("%d/%m/%Y"):  [["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["12:00", "14:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["14:00", "16:00", ["Bnei Brak", "Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["16:00", "18:00", ["Bnei Brak", "Petah Tikva", "Tel Aviv-Yafo"]]],
        curr_week_dates[3].strftime("%d/%m/%Y"):  [["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["12:00", "14:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["14:00", "16:00", ["Bnei Brak", "Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["16:00", "18:00", ["Bnei Brak", "Petah Tikva", "Tel Aviv-Yafo"]]],
        curr_week_dates[4].strftime("%d/%m/%Y"):  [["08:00", "10:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["12:00", "14:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["14:00", "16:00", ["Bnei Brak", "Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["16:00", "18:00", ["Bnei Brak", "Petah Tikva", "Tel Aviv-Yafo"]]],
        curr_week_dates[5].strftime("%d/%m/%Y"):  [["08:00", "10:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["10:00", "12:00", ["Tel Aviv-Yafo", "Ramat Gan"]],
                                                   ["12:00", "14:00", ["Tel Aviv-Yafo", "Ramat Gan"]]]
        }
    }

with open('courier_timeslots.json', 'w') as f:
    json.dump(available_timeslots_dict, f, indent=2)