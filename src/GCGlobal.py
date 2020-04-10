import GCStrings
import GCCountry
import GCLocation
import GCLocationList
import GCDisplaySettings
import GCEventList
import GCTimeZone

GCStrings.readFile('strings.json')
GCCountry.InitWithFile('countries.json')
GCTimeZone.LoadFile('timezones.json')
GCLocationList.OpenFile('locations.json')
GCDisplaySettings.readFile('displays.json')

myLocation = GCLocation.GCLocation(data = {
    'latitude': 27.583,
    'longitude': 77.73,
    'tzid': 188,
    'name': 'Vrndavan, India'
})

lastLocation = GCLocation.GCLocation(data = {
    'latitude': 27.583,
    'longitude': 77.73,
    'tzid': 188,
    'name': 'Vrndavan, India'
})

GCEventList.SetOldStyleFasting(GCDisplaySettings.getValue(42))
