import sys
import json
import urllib.request
import argparse
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

    ### Set dates
    validate_date(args.date)
    dateFrom = datetime.datetime.strptime(args.date, "%Y-%m-%d")

    ### If return, set date for return flight
    if args.ret is not None:
        dayRange = int(args.ret)
        dateTo = dateFrom + datetime.timedelta(days=dayRange)
        print(dateFrom)
        print(dateTo)

        ### TODO ambiguous condition
        if dateFrom >= dateTo:
            print("Start date is lower or equal to return date")
            os._exit()
        ### TODO Check if search date is not less than current date

    ## Set search conditions - cheapest option as default
    if args.cheapest is False and args.shortest is True:
        option = "duration"
    else:
        option = "price"

    ### Set and check airports
    ### TODO ambiguous information
    airport_name_departure = check_airport_ITA_code(args.airportFrom)
    airport_name_arrival = check_airport_ITA_code(args.airportTo)

    ### CORE ###
    if args.ret is not None:
        flight = "Return"   ## TODO
        url = URL_builder(args.airportFrom, args.airportTo, dateFrom, dateTo=dateTo, option=option)
        print("HALOOOO")
    else:
        flight = "One way"   ## TODO
        url = URL_builder(args.airportFrom, args.airportTo, dateFrom, option=option)


    print(url)

    # TODO Change name URL_laoder
    booking_token = URL_loader(url)

    ### TODO Mockup object
    #payload = { 'booking_token': booking_token, 'currency': "EUR", 'passengers': [{ 'lastName': "tomson", 'title': "Mr", "firstName": "isabel", "email": "asd@asd.com", "documentID": "4888789", "birthday": "1920-12-30"}]}
    #""" % (booking_token)

    payload = {
        "booking_token": "GamFTRHoBQ/v6QB8Irykhs320XfjZPfZzlYyhc7jew1a69GAWqezecCYt+cWhnpzWuptXhyCw2ZUzQhvPHnlJy3io/iLupqyLALq00u+jzH66tfBzdZrHNhDeb2nTRPr5Hvey4zRvvRFSPAbJvkrRO+nEw0Mtde3RkitFiK08ayXWfm+icsCSKyBN+rRSsf+2Ot/G/XytVGJyu5cqXq0f9F6B9GQjn9TMiCCvqgvFt4q1yc/bdf84cBao/RwWU7o9ufC/P5EelqxUm2d2v+7HJyfYBVjvnd68qWwRTh/E18uPVBljGr1VNuhCnPajs6SW455ydpqU8LzVJov8fr4rYykcO0JmmSNgK6znDG6S7Ik4vkP4YxOJjQWs7zWjknrdBbF5y5D5R/PkYSBro6MbD/d/9mOxTyKYRHvba49PIqwoNmZ0I3xifL1BolMU9UropYVPAqaZ7w/GpwVqCGyFw==",
        "currency": "EUR",
        "passengers": [
            {
                "lastName": "tomson",
                "title": "Mr",
                "firstName": "isabel",
                "email": "asd@asd.com",
                "documentID": "4888789",
                "birthday": "1920-12-30"
            }
        ]
    }

    url = 'http://37.139.6.125:8080/booking'
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data = json.dumps(payload), headers=headers)
    x = json.loads(r.text)
    print(x['pnr'])

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



def URL_builder(airportDeparture, airportArrival, dateFrom, *args, **kwargs):

    # temp Date Start
    tDS = str(dateFrom.strftime("%d/%m/%Y"))

    l = []

    l.append("https://api.skypicker.com/flights?")
    l.append("flyFrom=")
    l.append(airportDeparture)
    l.append("&")
    l.append("to=")
    l.append(airportArrival)
    l.append("&")
    l.append("dateFrom=")
    l.append(tDS)
    l.append("&")
    l.append("dateTo=")
    l.append(tDS)

    if ('dateTo' in kwargs):
        # temp Date End
        tDE = str(kwargs['dateTo'].strftime("%d/%m/%Y"))

        l.append("&")
        l.append("returnFrom=")
        l.append(tDE)
        l.append("&")
        l.append("returnTo=")
        l.append(tDE)

    if ('option' in kwargs):
        l.append("&")
        l.append("sort=")
        l.append(kwargs['option'])

    #l.append("&")
    #l.append("limit=1")

    l.append("&")
    l.append("partner=picky")

    return ''.join(l)



def return_url_json(URL):
    """
    Simple function for retrieving JSON object of requested URL
    :param URL: 
    :return JSON object:
    """
    try:
        return json.loads(urllib.request.urlopen(URL).read())
    except:
        print('Exception occurred while handling URL request:')
        print('-' *100)
        raise



def URL_loader(url):
    """
    Request data from URL and process retrieved data.
    :param url_list: 
    :return new_url_list: 
    """

    request_data = return_url_json(url)
    # print(request_data)

    if int(request_data['_results']) != 0:
        price = request_data['data'][0]['price']
        print(price)
        return request_data['data'][0]['booking_token']


# Python 3
if __name__ == "__main__":
    main(sys.argv[1:])
