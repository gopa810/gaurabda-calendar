from .GCMoonData import MOONDATA
from .GCSunData import SUNDATA, GetSunLongitude
from .GCGregorianDate import GCGregorianDate,Today
from . import GCEarthData as GCEarthData
from . import GCAyanamsha as GCAyanamsha
from . import GCMath as GCMath
from . import GCUT as GCUT
from math import floor

def GetNextYogaStart(ed, startDate, nextDate):
    phi = 40.0/3.0
    jday = startDate.GetJulianComplete()
    moon = MOONDATA()
    d = GCGregorianDate(date=startDate)
    xd = GCGregorianDate()
    scan_step = 0.5
    prev_tit = 0
    new_tit = -1
    ayanamsha = GCAyanamsha.GetAyanamsa(jday)
    moon.Calculate(jday, ed)
    sunl = GetSunLongitude(d)
    l1 = GCMath.putIn360( moon.longitude_deg + sunl - 2*ayanamsha)
    prev_tit = int(floor(l1/phi))

    counter = 0
    while counter < 20:
        xj = jday
        xd.Set(d)

        jday += scan_step
        d.shour += scan_step
        d.NormalizeHours()

        moon.Calculate(jday, ed)
        sunl = GetSunLongitude(d)
        l2 = GCMath.putIn360( moon.longitude_deg + sunl - 2*ayanamsha)
        new_tit = int(floor(l2/phi))

        if prev_tit != new_tit:
            jday = xj
            d.Set(xd)
            scan_step *= 0.5
            counter+=1
            continue
        else:
            l1 = l2
    nextDate.Set(d)

    return new_tit

def unittests():
    GCUT.info('yoga')
    e = GCEarthData.EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = Today()
    vc2 = GCGregorianDate()
    GetNextYogaStart(e,vc,vc2)
    print('Next yoga:', repr(vc2))
