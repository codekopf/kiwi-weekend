This is an entry script for [Kiwi's weekend](https://gist.github.com/martin-kokos/d578679d97eb1652dfeb3e7f2a4e115b) in
summer 2017 which I also improved for [Kiwi's weekend](https://engeto.online/study/lesson/_wl9/unit/_36ZR) in 
spring 2018. 

Unfortunately, I have never managed to send the script to competition. But the Python script works if all API is 
working correctly.    

#### Preconditions ####
* This project is done for Python 3. For running the script, it is necessary to have a functional terminal or IDE which 
supports Python 3. It is also necessary to specify script's arguments (as explained below) to run it properly. 
* Additional Python 3 libraries (use pip for install):
    * [Requests](http://docs.python-requests.org/en/master/)

#### How to run this script ####
For running this script please set specific parameters. Here is an example of the script entry arguments:
* ./book_flight.py --date 2017-10-13 --from BCN --to DUB --one-way
* ./book_flight.py --date 2017-10-13 --from LHR --to DXB --return 5
* ./book_flight.py --date 2017-10-13 --from NRT --to SYD --cheapest
* ./book_flight.py --date 2017-10-13 --from CPH --to MIA --shortest

**Argument description**: 
* --one-way indicates need of flight only to location 
* --return 5 should book flight with passenger staying 5 nights in destination
* --cheapest will book the cheapest flight 
* --fastest will work similarly to cheapest, will book the fastest route 
* --from and --to parameters only need to support airport IATA codes

To check all parameters type in console ./book_flight.py -h. 
* --one-way, --return, --shortest and --cheapest flags are optional
* default setting is set for --one-way and --cheapest

The program output a PNR number which serves as confirmation of booking. In case of failure, program will exit with 
non-zero exit code.

#### Dev. Notes ####
* How to discover POST arguments for /booking API interface? I opened Postman and tried just simple placed random 
strings into JSON. I got a response with missing parameters. This is the way how I build final JSON payload. The HTTP 
response with valid booking code (PNR number) was working in summer 2017 and spring 2018. 


#### TODO ####
Ideas for improvement:
* In general, the script requires clean-up and develop/execute TODO messages. I started to develop this script usually 
few hours before the deadline, so there was not much time for clean-up and ordering.
* Test and check if all arguments are returning right
* Good to have some tests, right?
 

