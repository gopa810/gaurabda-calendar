# How to run GCAL as server

1. make sure you have Python 3.x installed
1. download sources from [GitHub](https://github.com/gopa810/gaurabda-calendar/archive/master.zip)
2. install Flask python library `pip install Flask`
3. set current durectory to `./server` in `gaurabda-calendar` sources
4. (optional) set environment variable `GCAL_SERVER_PORT` to the number of IP port you want, by default it is 8047
5. start server as `python3 server.py` or `python server.py` (depends how you start python3 interpreter)


# REST API

REST API exposes a few methods to get what you want from GCAL server.

1. get list of countries
2. find location by name and/or country
3. calculate calendar

## List of countries

Request:

```
http://serveraddress:port/countries
```

Response:

```json
[
    "Andorra",
    "United Arab Emirates",
    "Afghanistan",
    "Antigua",
    "Albania",
    "Armenia",
    "Curacao",
    "Angola",
    "Argentina",
    "American Samoa",
    "Austria",
    "Australia",
    ...
]
```

## Find locations with given part of name 

Using GET method (specify name of city or part of the name):

```
http://serveraddress/find-location?name=<name-of-city>
```

Return value is dictionary in JSON with 3 keys:
* list of locations with name equal to given string
* list of locations starting with given string
* list of locations where given string is part of their name

Example output: [example-find-locations](./example-find-location.md)

## Find locations for given country

Using GET method (specify name of country):

```
http://serveraddress:port/find-location?country=<exact-name-of-country>
```

List of cities is limited to number 200. Name of country must be exact. For example `USA` will not work. It has to be `United States of America`.



## Calculate calendar


In general for calculation of calendar data we need 3 types of information:
* location
* start date
* end date or number of days

Location can be given in these forms:
* city + country + longitude + latitude + timezone
* city + country (in this case city has to be in database and latitude, longitude and timezone are added automatically)

Start date can be given in these forms:
* year (by default month is January, and day is 1)
* year + month (by default day is 1)
* year + month + day

End date is not given, only number of days to calculate.
* period = number of days since start date



[Calendar request example](./example-calendar.md)






