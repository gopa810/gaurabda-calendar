from . import GCEarthData as GCEarthData
from . import GCStrings as GCStrings
from . import GCTimeZone as GCTimeZone
from . import GCUT as GCUT
import re

def ParseDegreesFromString(str,bNorth):
    lat = lon = None
    m = re.match( r'(\+\-*)(\d+)([W|E|N|S])(\d+)', str )
    if m:
        val = int(m.group(2)) + int(m.group(4))/60
        if m.group(1)=='-':
            val = -val
        if m.group(3)=='W':
            lon = -val
        elif m.group(3)=='E':
            lon = val
        elif m.group(3)=='S':
            lat = -val
        elif m.group(3)=='N':
            lat = val
        elif m.group(3)=='.':
            if bNorth:
                lat = val
            else:
                lon = val
    return lon,lat

class GCLocation:
    def __init__(self,data=None):
        self.Empty()
        if data:
            if 'name' in data:
                self.m_strName = data['name']
            elif 'city' in data and 'country' in data:
                self.m_strCountry = data['country']
                self.m_strCity = data['city']
                self.m_strName = '{} ({})'.format(self.m_strCity, self.m_strCountry)
            else:
                self.m_strName = 'Noplace'
            self.m_fLongitude = data['longitude']
            self.m_fLatitude = data['latitude']
            if 'tzid' in data:
                self.m_nTimezoneId = data['tzid']
                self.m_strTimeZone = GCTimeZone.GetTimeZoneName(id=self.m_nTimezoneId)
                self.m_fTimezone = GCTimeZone.GetTimeZoneOffset(id=self.m_nTimezoneId)
            elif 'tzname' in data:
                tzone = GCTimeZone.GetTimeZone(name=data['tzname'])
                self.m_nTimezoneId = tzone['id']
                self.m_strTimeZone = data['tzname']
                self.m_fTimezone = tzone['offset']/60.0
            elif 'offset' in data:
                self.m_fTimezone = data['offset']

    @property
    def m_strLongitude(self):
        return GCEarthData.GetTextLongitude(self.m_fLongitude)

    @property
    def m_strLatitude(self):
        return GCEarthData.GetTextLatitude(self.m_fLatitude)

    @property
    def m_strFullName(self):
        return str(self)


    def data(self):
        return {
            'city': self.m_strCity,
            'country': self.m_strCountry,
            'name': self.m_strName,
            'latitude': self.m_fLatitude,
            'longitude': self.m_fLongitude,
            'offset': self.m_fTimezone,
            'tzid': self.m_nTimezoneId,
            'tzname': self.m_strTimeZone
        }

    def Empty(self):
        self.m_strTimeZone = ''
        self.m_strName = ''
        self.m_fLatitude = 0.0
        self.m_fLongitude = 0.0
        self.m_fTimezone = 0.0
        self.m_nTimezoneId = 0
        self.m_strCountry = ''
        self.m_strCity = ''

    def __str__(self):
        return "{} ({}, {}, {}: {})".format(self.m_strName, self.m_strLatitude, self.m_strLongitude, GCStrings.getString(12), self.m_strTimeZone)

    def __iter__(self):
        for k,v in self.data().items():
            yield k,v

    def __dict__(self):
        return self.data()

    def copy(self):
        return GCLocation(data = self.data())

    def GetEarthData(self):
        e = GCEarthData.EARTHDATA()
        e.dst = self.m_nTimezoneId
        e.latitude_deg = self.m_fLatitude
        e.longitude_deg = self.m_fLongitude
        e.tzone = self.m_fTimezone
        return e

    def Set(self,L):
        if isinstance(L,GCEarthData.EARTHDATA):
            self.m_fLongitude = L.longitude_deg
            self.m_fLatitude = L.latitude_deg
            self.m_nTimezoneId = L.dst
            self.m_strTimeZone = GCTimeZone.GetTimeZoneName(id=self.m_nTimezoneId)
            self.m_fTimezone = GCTimeZone.GetTimeZoneOffset(id=self.m_nTimezoneId)
        elif isinstance(L,GCLocation):
            self.m_strTimeZone = L.m_strTimeZone
            self.m_strName = L.m_strName
            self.m_strCity = L.m_strCity
            self.m_strCountry = L.m_strCountry
            self.m_fLongitude = L.m_fLongitude
            self.m_fLatitude = L.m_fLatitude
            self.m_fTimezone = L.m_fTimezone
            self.m_nTimezoneId = L.m_nTimezoneId
