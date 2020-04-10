import gaurabda.GCStrings as GCStrings
import gaurabda.GCCountry as GCCountry
import gaurabda.GCLocation as GCLocation
import gaurabda.GCLocationList as GCLocationList
import gaurabda.GCDisplaySettings as GCDisplaySettings
import gaurabda.GCEventList as GCEventList
import gaurabda.GCTimeZone as GCTimeZone

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
