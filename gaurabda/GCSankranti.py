from .GCGregorianDate import GCGregorianDate,Today
from .GCLocation import GCLocation
from . import GCMath as GCMath
from . import GCAyanamsha as GCAyanamsha
from .GCTime import GCTime
from .GCSunData import SUNDATA
from . import GCSunData as GCSunData
from . import GCStrings as GCStrings
from math import floor
from . import GCUT as GCUT

sankrantiDetermineType = 2

def GetSankrantiType():
    return sankrantiDetermineType

def SetSankrantiType(i):
    prev = sankrantiDetermineType
    sankrantiDetermineType = i
    return prev

def GetSankMethodName(i):
    snam = ["midnight to midnight",
        "sunrise to sunrise",
        "noon to noon",
        "sunset to sunset"]
    return snam[i]


#********************************************************************/
#  Finds next time when rasi is changed                             */
#                                                                   */
#  startDate - starting date and time, timezone member must be valid */
#  zodiac [out] - found zodiac sign into which is changed           */
#                                                                   */
#********************************************************************/
def GetNextSankranti(startDate):
    zodiac = 0
    step = 1.0
    count = 0
    prevday = GCGregorianDate()

    d = GCGregorianDate(date = startDate)

    prev = GCMath.putIn360( GCSunData.GetSunLongitude(d) - GCAyanamsha.GetAyanamsa(d.GetJulian()))
    prev_rasi = int(floor(prev / 30.0))

    while count < 20:
        prevday.Set(d)
        d.shour += step
        d.NormalizeHours()

        ld = GCMath.putIn360(GCSunData.GetSunLongitude(d) - GCAyanamsha.GetAyanamsa(d.GetJulian()))
        new_rasi = int(floor(ld/30.0))

        if prev_rasi != new_rasi:
            zodiac = new_rasi
            step *= 0.5
            d.Set(prevday)
            count+=1
            continue

    return d,zodiac


def writeXml(xml, loc, vcStart, vcEnd):
    dt = GCTime()
    zodiac = 0

    d = GCGregorianDate(date = vcStart)

    xml.write("<xml>\n")
    xml.write("\t<request name=\"Sankranti\" version=\"")
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
    xml.write("\t\t<arg name=\"location\" val=\"")
    xml.write(loc.m_strName)
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"startdate\" val=\"")
    xml.write(repr(vcStart))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"enddate\" val=\"")
    xml.write(repr(vcEnd))
    xml.write("\" />\n")
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"SankrantiList\">\n")

    while d.IsBeforeThis(vcEnd):
        nextDate,zodiac = GetNextSankranti(d)
        d.Set(nextDate)
        d.InitWeekDay()
        xml.write("\t\t<sank date=\"")
        xml.write(str(d))
        xml.write("\" ")
        xml.write("dayweekid=\"")
        xml.write(str(d.dayOfWeek))
        xml.write("\" dayweek=\"")
        xml.write(GCStrings.getString(d.dayOfWeek))
        xml.write("\" ")

        dt.SetDegTime( 360 * d.shour )

        xml.write(" time=\"")
        xml.write(repr(dt))
        xml.write("\" >\n")
        xml.write("\t\t\t<zodiac sans=\"")
        xml.write(GCStrings.GetSankrantiName(zodiac))
        xml.write("\" eng=\"")
        xml.write(GCStrings.GetSankrantiNameEn(zodiac))
        xml.write("\" id=\"")
        xml.write(str(zodiac))
        xml.write("\" />\n")
        xml.write("\t\t</sank>\n")

        d.NextDay()
        d.NextDay()

    xml.write("\t</result>\n")
    xml.write("</xml>")

    return 1


def unittests():
    GCUT.info('sankranti')
    vc = Today()
    vc2 = GCGregorianDate()
    vc3 = GCGregorianDate(date = vc)
    vc3.AddDays(100)
    n = GetSankMethodName(GetSankrantiType())
    GCUT.msg('Sankranti Type: {}'.format(n))
    import io
    s = io.StringIO()
    clr = GCLocation()
    writeXml(s, clr, vc, vc3)
    GCUT.msg(s.getvalue())
