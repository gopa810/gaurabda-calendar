import flask
import logging
from flask import jsonify, request, Response
import io


from .GCLocationList import FindLocation, FindLocations,GetLocationsForCountry
from .GCCountry import GetCountries
from .GCGregorianDate import GCGregorianDate,Today
from .TCalendar import TCalendar

app = flask.Flask(__name__)


@app.route('/countries', methods=['GET'])
def getListCountries():
    return jsonify(GetCountries())

@app.route('/find-location', methods=['GET','POST'])
def findLocation():
    if request.method == 'GET':
        # get name of location
        name = request.args.get('name')
        country = request.args.get('country')
        e, s, c = FindLocations(name, country)
        obj = {
            'EQUALS': [a.data() for a in e],
            'STARTS': [a.data() for a in s],
            'CONTAINS': [a.data() for a in c]
        }
        return jsonify(obj)
    elif request.method == 'POST':
        content = request.get_json()
        name = None
        country = None
        if 'name' in content:
            name = content['name']
        if 'country' in content:
            country = content['country']
        e, s, c = FindLocations(name, country)
        obj = {
            'EQUALS': [a.data() for a in e],
            'STARTS': [a.data() for a in s],
            'CONTAINS': [a.data() for a in c]
        }
        return jsonify(obj)



@app.route('/calendar', methods=['GET','POST'])
def getCalendar():
    loca = {}
    date = {}
    period = None
    fmt = None
    req_data = None
    if request.method == 'GET':
        req_data = request.args
    elif request.method == 'POST':
        req_data = request.json
    else:
        return flask.make_response('Unknown method', 500)

    loca['city'] = req_data.get('city')
    loca['country'] = req_data.get('country')
    loca['latitude'] = req_data.get('latitude')
    loca['longitude'] = req_data.get('longitude')
    loca['tzname'] = req_data.get('tzname')
    date['year'] = req_data.get('year')
    date['month'] = req_data.get('month')
    date['day'] = req_data.get('day')
    period = req_data.get('period')
    fmt = req_data.get('format')
    
    if loca['latitude'] is None and loca['longitude'] is not None \
       or loca['latitude'] is not None and loca['longitude'] is None:
       return flask.make_response('Either both LATITUDE,LONGITUDE are valid or none of them', 500)

    if loca['city'] is None:
        return flask.make_response('city: - Name of location must be specified.', 500)

    if loca['country'] is None:
        return flask.make_response('country: Name of country must be specified.', 500)

    if loca['latitude'] is None:
        sp = FindLocation(city=loca['city'], country=loca['country'])
        if sp is None:
            return flask.make_response('Location with name \'{}\', country \'{}\' is not found in database.'.format(loca['name'], loca['country']), 500)
        loca['latitude'] = sp.m_fLatitude
        loca['longitude'] = sp.m_fLongitude
        loca['tzname'] = sp.m_strTimeZone
        loca['location'] = sp
    else:
        loca['latitude'] = float(loca['latitude'])
        loca['longitude'] = float(loca['longitude'])

    if loca['tzname'] is None:
        return flask.make_response('tz: Name of timezone must be specified.', 500)
    
    if date['year'] is None:
        d = Today()
        date['year'] = d.year
    else:
        date['year'] = int(date['year'])

    if date['month'] is None:
        date['month'] = 1
    else:
        date['month'] = int(date['month'])

    if date['day'] is None:
        date['day'] = 1
    else:
        date['day'] = int(date['day'])

    if period is None:
        return flask.make_response('p: Time period must be specified.', 500)
    try:
        period = int(period)
    except:
        return flask.make_response('p: Time period is number of days (integer number).', 500)
    if period<1:
        return flask.make_response('p: Time period must be greater than 0 days.', 500)
    if period>3653:
        return flask.make_response('p: Time period must be lower than 3654 days.', 500)

    tc = TCalendar()
    date2 = GCGregorianDate(year=date['year'], month=date['month'], day=date['day'])
    location = loca.get('location')
    if location is None:
        location = GCLocation(data={
            'city': loca['city'],
            'country': loca['country'],
            'latitude': loca['latitude'],
            'longitude': loca['longitude'],
            'tzname': loca['tzname']
        })
    tc.CalculateCalendar(location,date2,period)

    wf = io.StringIO()

    # save results in various formats
    if fmt == 'txt' or fmt=='text' or fmt=='plain':
        tc.write(wf, format='plain')
        return Response(wf.getvalue(), mimetype='text/plain')
    elif fmt=='html':
        tc.write(wf)
        return Response(wf.getvalue(), mimetype='text/html')
    elif fmt=='html-table':
        tc.write(wf, layout='table')
        return Response(wf.getvalue(), mimetype='text/html')
    elif fmt=='xml':
        tc.write(wf, format='xml')
        return Response(wf.getvalue(), mimetype='text/xml')
    else:
        return jsonify(tc.get_json_object())


def run_server(port=8047):
    app.run(port=port)

if __name__=='__main__':
    run_server()