import re
import csv
import datetime


def check_airport_ita_code(airport_ita_code):
    if len(airport_ita_code) != 3:
        print("Incorrect length of airport ITA code")
        exit(1)

    match = re.search(r"^[A-Z]{3}$", airport_ita_code)
    if match is None:
        print("Airport code does not mach required criteria for ITA code")
        exit(1)

    with open('airports.csv', encoding="utf8") as csvfile:
        reader = list(csv.reader(csvfile))
        for row in reader:
            if airport_ita_code == row[4]:
                # print("Found an airport {} - {}".format(row[4], row[1]))
                return row[1]


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
