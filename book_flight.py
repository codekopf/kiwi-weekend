import sys
import json
import argparse
import urllib.request
import urllib.parse

import requests

from checks import *


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--date",
                        help="journey start date",
                        required=True)

    parser.add_argument("--from",
                        help="departure airport ITA code",
                        required=True,
                        dest="airportFrom")

    parser.add_argument("--to",
                        help="arrival airport ITA code",
                        required=True,
                        dest="airportTo")

    parser.add_argument("--one-way",
                        help="check direct flights",
                        action="store_true",
                        dest="onew")

    parser.add_argument("--return",
                        help="check return flights in certain time range",
                        # nargs='+', # If I want to make a list
                        dest="ret")

    parser.add_argument("--cheapest",
                        help="check cheapest flights",
                        action="store_true")

    parser.add_argument("--shortest",
                        help="check shortest flights",
                        action="store_true")

    args = parser.parse_args()

    # Set dates
    validate_date(args.date)
    date_from = datetime.datetime.strptime(args.date, "%Y-%m-%d")

    # If return, set date for return flight
    if args.ret is not None:
        day_range = int(args.ret)
        date_to = date_from + datetime.timedelta(days=day_range)

        # TODO ambiguous condition
        if date_from >= date_to:
            print("Start date is lower or equal to return date")
            exit(1)
            # TODO Check if search date is not less than current date

    # Set search conditions - cheapest option as default
    if args.cheapest is False and args.shortest is True:
        option = "duration"
    else:
        option = "price"

    # Set and check airports
    # TODO ambiguous information
    airport_name_departure = check_airport_ita_code(args.airportFrom)
    airport_name_arrival = check_airport_ita_code(args.airportTo)

    # CORE #
    if args.ret is not None:
        flight = "Return"  # TODO
        url = url_builder(args.airportFrom, args.airportTo, date_from, dateTo=date_to, option=option)
    else:
        flight = "One way"  # TODO
        url = url_builder(args.airportFrom, args.airportTo, date_from, option=option)

    # TODO Change name URL_laoder
    url_data = return_url_content(url)
    url_data_json = json.loads(url_data)

    if len(url_data_json['data']) != 0:
        price = url_data_json['data'][0]['price']
    extracted_booking_token = url_data_json['data'][0]['booking_token']

    # TODO Mockup object
    json_data = {'booking_token': extracted_booking_token, 'bags': "0", 'currency': "EUR", 'passengers': [
        {'title': "Mr", "firstName": "Isabel", 'lastName': "Thomson", "email": "asd@asd.com", "documentID": "4888789",
         "birthday": "1920-12-30"}]}

    json_data = json.dumps(json_data)

    # payload = { booking_token': extracted_booking_token, 'currency': "EUR", 'passengers': [{ 'lastName': "tomson",
    # 'title': "Mr", "firstName": "isabel", "email": "asd@asd.com", "documentID": "4888789", "birthday": "1920-12-30"}]}
    # """ % (booking_token)

    # payload = {
    #     "booking_token": "GamFTRHoBQ/v6QB8Irykhs320XfjZPfZzlYyhc7jew1a69GAWqezecCYt+cWhnpzWuptXhyCw2ZUzQhvPHnlJy3io/
    # iLupqyLALq00u+jzH66tfBzdZrHNhDeb2nTRPr5Hvey4zRvvRFSPAbJvkrRO+nEw0Mtde3RkitFiK08ayXWfm+icsCSKyBN+rRSsf+2Ot/G/XytVGJ
    # yu5cqXq0f9F6B9GQjn9TMiCCvqgvFt4q1yc/bdf84cBao/RwWU7o9ufC/P5EelqxUm2d2v+7HJyfYBVjvnd68qWwRTh/E18uPVBljGr1VNuhCnPajs
    # 6SW455ydpqU8LzVJov8fr4rYykcO0JmmSNgK6znDG6S7Ik4vkP4YxOJjQWs7zWjknrdBbF5y5D5R/PkYSBro6MbD/d/9mOxTyKYRHvba49PIqwoNmZ
    # 0I3xifL1BolMU9UropYVPAqaZ7w/GpwVqCGyFw==",
    #     "currency": "EUR",
    #     "passengers": [
    #         {
    #             "lastName": "tomson",
    #             "title": "Mr",
    #             "firstName": "isabel",
    #             "email": "asd@asd.com",
    #             "documentID": "4888789",
    #             "birthday": "1920-12-30"
    #         }
    #     ]
    # }

    booking_url = "http://128.199.48.38:8080/booking"

    # json_data = urllib.parse.urlencode(json_data)
    # json_data = json_data.encode('utf-8')

    # req = urllib.request.Request(booking_url, json_data, headers={'content-type': 'application/json'})
    # r = urllib.request.urlopen(booking_url, json_data)
    try:
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(booking_url, json_data, headers=headers)
        # print(r.status_code)
        print(r.json()['pnr'])  # TADAAA
        # print(r['pnr'])

        # data = bytes(urllib.parse.urlencode(json_data).encode())
        # handler = urllib.request.urlopen(booking_url, data)
        # print(handler.read().decode('utf-8'))

        # with urllib.request.urlopen(req) as response:
        # response.read()
        # print(the_page.decode('utf-8'))
    except urllib.error.URLError as e:
        print(e.reason)

        #     the_page = response.read()
        # print(the_page)
        # x = r.read().decode('utf-8')
        # print(x)
        # print(x['pnr']) # THIS IS WHAT I AM LOOKING FOR

        # ### Control print
        # print("Departure airport ITA code: {}".format(airport_name_departure))
        # print("Arrival airport ITA code: {}".format(airport_name_arrival))
        # print("Flight date: {}".format(dateFrom))
        # print("One-way: {}".format(args.onew))
        # print("Return: {}".format(args.ret))
        # print("Cheapest: {}".format(args.cheapest))
        # print("Shortest: {}".format(args.shortest))
        # print("Flight: {}".format(flight))
        # print("Option: {}".format(option))


def url_builder(airport_departure, airport_arrival, date_from, **kwargs):
    # temp Date Start
    temp_date_start = str(date_from.strftime("%d/%m/%Y"))

    l = ["https://api.skypicker.com/flights?", "flyFrom=", airport_departure, "&", "to=", airport_arrival, "&",
         "dateFrom=", temp_date_start, "&", "dateTo=", temp_date_start]

    if 'dateTo' in kwargs:
        # temp Date End
        temp_date_end = str(kwargs['dateTo'].strftime("%d/%m/%Y"))

        l.append("&")
        l.append("returnFrom=")
        l.append(temp_date_end)
        l.append("&")
        l.append("returnTo=")
        l.append(temp_date_end)

    if 'option' in kwargs:
        l.append("&")
        l.append("sort=")
        l.append(kwargs['option'])

    # l.append("&")
    # l.append("limit=1")

    l.append("&")
    l.append("partner=picky")

    return ''.join(l)


def return_url_content(url):
    """
    Simple function for retrieving JSON object of requested URL
    :param url: 
    :return JSON object:
    """
    try:
        # params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
        # url = "http://www.musi-cal.com/cgi-bin/query?%s" % params
        return urllib.request.urlopen(url).read().decode('utf-8')
    except:
        print('Exception occurred while handling URL request:')
        print('-' * 100)
        raise


# Python 3
if __name__ == "__main__":
    main(sys.argv[1:])
