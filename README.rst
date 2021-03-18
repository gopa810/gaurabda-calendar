gaurabda-calendar
=================

Python library for calculating panchanga calendar with vaisnava events.

Installation
------------

::

    pip install gaurabda

Using
-----

Here are a few examples of code that you can try quickly. Examples are
related to calculation of calendar. Before calendar calculation we need
to specify location and start date.

We can obtain location object basically in two ways:

-  create new location

.. code:: python

    # import module

    import gaurabda as gcal


    # create new location

    loc = gcal.GCLocation(data = {
        'latitude': 27.583,
        'longitude': 77.73,
        'tzname': '+5:30 Asia/Calcutta',
        'name': 'Vrindavan, India'
    })

List of all timezones can be obtained by calling
``gcal.GetTimeZones()``.

-  find location in existing list

.. code:: python

    # find existing location

    loc = gcal.FindLocation(city='Vrindavan')

List of all countries ``gcal.GetCountries()`` and list of cities for
given country: ``gcal.GetLocationsForCountry('India')``. Function
GetLocationsForCountry has optional parameter limit, that takes whole
number limiting number of locations returned by this method. Default
value is -1, that means there is no limit.

Then we need create date object.

::

    today = gcal.Today()
    print(repr(today))

    date1 = gcal.GCGregorianDate(text='24 apr 2017')
    print(repr(date1))

Constructor for GCGregorianDate contains more optional parameters:

-  **year**, **month**, **day** that are whole natural numbers, year
   between 1500 - 2500, month 1-12, day according given month
-  **shour** is from interval 0.0 up to 1.0 where 0.0 is mignight, 0.5
   is noon (12:00 PM) and 1.0 is next midnight.
-  **tzone** is offset from UTC 0:00 in hours, so value +5.5 means
   offset 5:30, which is actual for India
-  **date** is existing GCGregorianDate object
-  **text** can be text form of date (e.g. '24 Apr 2017')

Parameters can be combined with certain succession of evaluation.
Parameters are evaluated in this order, where later parameter overrides
previous values.

-  text
-  date
-  year
-  month
-  day
-  shour

So for example, to get first day of current month, we may use:

::

    d = gcal.GCGregorianDate(date=gcal.Today(), day=1)

Next step is to create calculation engine for calendar, execute
calculation and write results to file:

::

    # create calculation engine and calculate
    tc = gcal.TCalendar()
    tc.CalculateCalendar(loc,today,365)

    # save results in various formats
    with open('calendar.txt','wt') as wf:
        tc.write(wf, format='plain')
    with open('test/calendar.rtf','wt') as wf:
        tc.write(wf, format='rtf')
    with open('test/calendar.html','wt') as wf:
        tc.write(wf)
    with open('test/calendar2.html','wt') as wf:
        tc.write(wf, layout='table')
    with open('test/calendar.json','wt') as wf:
        tc.write(wf, format='json')
    with open('test/calendar.xml','wt') as wf:
        tc.write(wf, format='xml')

Arguments for write method of TCalendar class:

-  **stream** any text writer, for example subclass of io.TextWriter
-  **format** this is optional parameter, default value is 'html',
   posible values are: 'plain', 'rtf', 'xml', 'html', 'json'
-  **layout** this is optional, denotes layout of output. It is
   effective for 'html' format, and possible values are 'list' and
   'table'. Default is 'list'.
