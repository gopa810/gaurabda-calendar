from .GCGregorianDate import GCGregorianDate, Today
from . import GCEarthData as GCEarthData
from . import GCLocation as GCLocation
from .GCMoonData import MOONDATA
from . import GCAyanamsha as GCAyanamsha
from . import GCStrings as GCStrings
from . import GCMath as GCMath
from .GCTime import GCTime
from .GCSunData import SUNDATA
from . import GCUT as GCUT

import math

def CalculateMidnightNaksatra(date,earth):
    moon = MOONDATA()
    date = GCGregorianDate(date = date)
    date.shour = 1.0
    jdate = date.GetJulianDetailed()
    moon.Calculate(jdate, earth)
    d = GCMath.putIn360( moon.longitude_deg - GCAyanamsha.GetAyanamsa(jdate))
    return math.floor(( d * 3.0) / 40.0 )


def GetNextNaksatra(ed, startDate, nextDate, forward=True):
    phi = 40.0/3.0
    jday = startDate.GetJulianComplete()
    moon = MOONDATA()
    d = GCGregorianDate(date = startDate)
    ayanamsa = GCAyanamsha.GetAyanamsa(jday)
    prev_naks = 0
    new_naks = -1
    dir = 1.0 if forward else -1.0
    scan_step = 0.5 * dir

    xd = GCGregorianDate()

    moon.Calculate(jday, ed)
    l1 = GCMath.putIn360(moon.longitude_deg - ayanamsa)
    prev_naks = int(math.floor(l1 / phi))

    counter = 0
    while counter < 20:
        xj = jday
        xd.Set(d)

        jday += scan_step
        d.shour += scan_step
        d.NormalizeHours()

        moon.Calculate(jday, ed)
        l2 = GCMath.putIn360(moon.longitude_deg - ayanamsa)
        new_naks = int(math.floor(l2/phi))
        if prev_naks != new_naks:
            jday = xj
            d.Set(xd)
            scan_step *= 0.5
            counter+=1
            continue
        else:
            l1 = l2
    nextDate.Set(d)
    return new_naks

def GetPrevNaksatra(ed, startDate, nextDate):
    return GetNextNaksatra(ed, startDate, nextDate, forward=False)

def writeXml(xml, loc, vc, nDaysCount):
    date = GCGregorianDate()

    xml.write("<xml>")
    xml.write("\t<request name=\"Naksatra\" version=\"")
    xml.write(GCStrings.getString(130))
    xml.write("\">\n")
    xml.write("\t\t<arg name=\"longitude\" val=\"")
    xml.write(str(loc.m_fLongitude))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"latitude\" val=\"")
    xml.write(str(loc.m_fLatitude))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"timezone\" val=\"")
    xml.write(str(loc.m_fTimezone))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"startdate\" val=\"")
    xml.write(str(vc))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"daycount\" val=\"")
    xml.write(str(nDaysCount))
    xml.write("\" />\n")
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"Naksatra\">\n")

    d = GCGregorianDate(date = vc)
    d.tzone = loc.m_fTimezone
    dn = GCGregorianDate()
    dt = GCTime()
    sun = SUNDATA()
    earth = loc.GetEarthData()

    for i in range(30):
        nak = GetNextNaksatra(earth, d, dn)
        d.Set(dn)
        xml.write("\t\t<day date=\"")
        xml.write(str(d).strip())
        xml.write("\">\n")
        xml.write("\t\t\t<naksatra id=\"")
        xml.write(str(nak))
        xml.write("\" name=\"")
        xml.write(GCStrings.GetNaksatraName(nak))
        xml.write("\" ")
        dt.SetDegTime( d.shour * 360)
        xml.write("starttime=\"")
        xml.write(repr(dt))
        xml.write("\" />\n")

        sun.SunCalc(d, earth);
        xml.write("\t\t\t<sunrise time=\"");
        xml.write(repr(sun.rise))
        xml.write("\" />\n")

        xml.write("\t\t</day>\n");
        d.Set(dn)
        d.shour += 1.0/8.0


    xml.write("\t</result>\n")
    xml.write("</xml>\n")
    return 1

def GetEndHour(earth, yesterday, today):
    nend = GCGregorianDate()
    snd = GCGregorianDate(date = yesterday)
    snd.shour = 0.5
    GetNextNaksatra(earth, snd, nend)
    return nend.GetJulian() - today.GetJulian() + nend.shour

def unittests():
    GCUT.info('naksatra')
    e = GCEarthData.EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = Today()
    vc2 = GCGregorianDate()
    vc3 = GCGregorianDate(date = vc)
    vc3.NextDay()
    n = GetEndHour(e,vc,vc3)
    GCUT.msg('End hour: {}, {}'.format(n,repr(vc3)))
    import io
    s = io.StringIO()
    clr = GCLocation.GCLocation()
    writeXml(s, clr, vc, 10)
    GCUT.msg(s.getvalue())
