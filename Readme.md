This is an entry script for [Kiwi's Weekend](https://gist.github.com/martin-kokos/d578679d97eb1652dfeb3e7f2a4e115b) summer 2017.  

#### Preconditions ####
* Python 3

#### Installation ####
For running the script please set entring parameters. Here is an example of the script entry arguments:
* ./book_flight.py --date 2017-10-13 --from BCN --to DUB --one-way
* ./book_flight.py --date 2017-10-13 --from LHR --to DXB --return 5
* ./book_flight.py --date 2017-10-13 --from NRT --to SYD --cheapest
* ./book_flight.py --date 2017-10-13 --from CPH --to MIA --shortest

To check all parameters type in console ./book_flight.py -h. 
* --one-way, --return, --shortest and --cheapest flags are optional
* default setting is set for --one-way and --cheapest