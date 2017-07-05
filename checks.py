import os
import re
import csv
import datetime

def check_airport_ITA_code(airport_ITA_code):
    if len(airport_ITA_code) != 3:
        print("Incorrect length of airport ITA code")
        os._exit()

    match = re.search(r"^[A-Z]{3}$", airport_ITA_code)
    if match is None:
        print("Airport code does not mach required criteria for ITA code")
        os._exit()

    with open('airports.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile))
        for row in reader:
            if airport_ITA_code == row[4]:
                # print("Found an airport {} - {}".format(row[4], row[1]))
                return row[1]

def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
