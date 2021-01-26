from . import GCStrings
from . import GCCountry
from . import GCLocation
from . import GCLocationList
from . import GCDisplaySettings
from . import GCEventList
from . import GCTimeZone

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
