from .GCEnums.CoreEventType import *
from .GCEnums.KalaType import *
from .GCEnums.GCDS import *
from .GCGregorianDate import GCGregorianDate,Today
from .GCLocation import GCLocation
from . import GCTimeZone as GCTimeZone
from .GCSunData import SUNDATA,CalculateKala
from .GCMoonData import MOONDATA,GetNextMoonRasi
from .GCStringBuilder import GCStringBuilder,SBTF_RTF,SBTF_TEXT
from . import GCTithi as GCTithi
from . import GCNaksatra as GCNaksatra
from . import GCSankranti as GCSankranti
from . import GCConjunction as GCConjunction
from . import GCAyanamsha as GCAyanamsha
from . import GCYoga as GCYoga
from . import GCRasi as GCRasi
from . import GCStrings as GCStrings
from . import GCDisplaySettings as GCDisplaySettings
from . import GCLayoutData as GCLayoutData
from math import ceil,floor
from . import GCUT as GCUT
import datetime


class TDayEvent:
    def __init__(self):
        self.nType = 0
        self.nData = 0
        self.Time = GCGregorianDate()
        self.nDst = 0
        self.julianDay = 0

    def Set(self,de):
        nType = de.nType
        nData = de.nData
        Time.Set(de.Time)
        nDst = de.nDst

    def EventText(self):
        if self.nType == CCTYPE_S_ARUN:
            return 'arunodaya'
        elif self.nType == CCTYPE_S_RISE:
            return "sunrise"
        elif self.nType == CCTYPE_S_NOON:
            return "noon"
        elif self.nType == CCTYPE_S_SET:
            return "sunset"
        elif self.nType == CCTYPE_TITHI:
            return GCStrings.GetTithiName(self.nData) + " Tithi starts"
        elif self.nType == CCTYPE_NAKS:
            return GCStrings.GetNaksatraName(self.nData) + " Naksatra starts"
        elif self.nType == CCTYPE_YOGA:
            return GCStrings.GetYogaName(self.nData) + " Yoga starts"
        elif self.nType == CCTYPE_SANK:
            return "Sun enters {}".format(GCStrings.GetSankrantiName(self.nData))
        elif self.nType == CCTYPE_CONJ:
            return "conjunction in {} rasi".format(GCStrings.GetSankrantiName(self.nData))
        elif self.nType == CCTYPE_KALA_START:
            return GCStrings.GetKalaName(self.nData) + " starts"
        elif self.nType == CCTYPE_KALA_END:
            return GCStrings.GetKalaName(self.nData) + " ends"
        elif self.nType == CCTYPE_M_RISE:
            return "moonrise"
        elif self.nType == CCTYPE_M_SET:
            return "moonset"
        elif self.nType == CCTYPE_ASCENDENT:
            return GCStrings.GetSankrantiName(self.nData) + " ascendent"
        elif self.nType == CCTYPE_M_RASI:
            return "Moon enters {}".format(GCStrings.GetSankrantiName(self.nData))
        else:
            return ''

class TCoreEvents:
    header_text = {
        CCTYPE_DATE: " DATE ",
        CCTYPE_S_ARUN: " SUNRISE, SUNSET ",
        CCTYPE_S_RISE: " SUNRISE, SUNSET ",
        CCTYPE_S_NOON: " SUNRISE, SUNSET ",
        CCTYPE_S_SET: " SUNRISE, SUNSET ",
        CCTYPE_TITHI: " TITHI ",
        CCTYPE_NAKS: " NAKSATRA ",
        CCTYPE_SANK: " SANKRANTI ",
        CCTYPE_CONJ: " SUN-MOON CONJUNCTION ",
        CCTYPE_YOGA: " YOGA ",
        CCTYPE_KALA_START: " KALAS ",
        CCTYPE_KALA_END: " KALAS ",
        CCTYPE_M_RISE: " MOONRISE, MOONSET ",
        CCTYPE_M_SET: " MOONRISE, MOONSET ",
        CCTYPE_M_RASI: " MOON RASI ",
        CCTYPE_ASCENDENT: " ASCENDENT "
    }
    def __init__(self):
        self.m_vcStart = GCGregorianDate()
        self.m_vcEnd = GCGregorianDate()
        self.m_options = 0
        self.m_location = GCLocation()
        self.p_events = []
        self.b_sorted = True

    def AddEvent(self, inTime, inType, inData, inDst):
        p = TDayEvent()
        self.p_events.append(p)


        if inDst == 1:
            if (inTime.shour >= 2/24.0):
                inTime.shour += 1/24.0
                inTime.NormalizeValues()
                p.nDst = 1
        elif inDst == 2:
            inTime.shour += 1/24.0
            inTime.NormalizeValues()
            p.nDst = 1
        elif inDst == 3:
            if (inTime.shour <= 2/24.0):
                inTime.shour += 1/24.0
                inTime.NormalizeValues()
                p.nDst = 1
        p.Time.Set(inTime)
        p.Time.InitWeekDay()
        p.julianDay = p.Time.GetJulianComplete()
        p.nData = inData
        p.nType = inType
        return True

    def Sort(self):
        self.p_events = sorted(self.p_events, key = lambda k: k.julianDay)

    def CalculateEvents(self,loc,vcStart,vcEnd):
        sun = SUNDATA()
        ndst = 0

        self.m_location.Set(loc)
        self.m_vcStart.Set(vcStart)
        self.m_vcEnd.Set(vcEnd)

        vcNext = GCGregorianDate()
        earth = loc.GetEarthData()

        vc = GCGregorianDate(date = vcStart)
        vcAdd = GCGregorianDate(date = vcStart)
        vcAdd.InitWeekDay()

        previousLongitude = -100
        todayLongitude = 0
        fromTimeLimit = 0

        while vcAdd.IsBeforeThis(vcEnd):
            if (GCDisplaySettings.getValue(COREEVENTS_SUN)):
                ndst = GCTimeZone.determineDaylightChange(vcAdd, loc.m_nTimezoneId)
                sun.SunCalc(vcAdd, earth)

                vcAdd.shour = sun.arunodaya.GetDayTime()
                self.AddEvent(vcAdd, CCTYPE_S_ARUN, 0, ndst)

                vcAdd.shour = sunRise = sun.rise.GetDayTime()
                self.AddEvent(vcAdd, CCTYPE_S_RISE, 0, ndst)

                vcAdd.shour = sun.noon.GetDayTime()
                self.AddEvent(vcAdd, CCTYPE_S_NOON, 0, ndst)

                vcAdd.shour = sunSet = sun.set.GetDayTime()
                self.AddEvent(vcAdd, CCTYPE_S_SET, 0, ndst)
            else:
                ndst = GCTimeZone.determineDaylightChange(vcAdd, loc.m_nTimezoneId)
                sun.SunCalc(vcAdd, earth)
                sunRise = sun.rise.GetDayTime()
                sunSet = sun.set.GetDayTime()

            if (GCDisplaySettings.getValue(COREEVENTS_ASCENDENT)):
                todayLongitude = sun.longitude_deg
                vcAdd.shour = sunRise
                todaySunriseHour = sunRise
                if (previousLongitude < -10):
                    prevSunrise = GCGregorianDate(date = vcAdd)
                    prevSunrise.PreviousDay()
                    sun.SunCalc(prevSunrise, earth)
                    previousSunriseHour = sun.rise.GetDayTime() - 1
                    previousLongitude = sun.longitude_deg
                    fromTimeLimit = 0

                jd = vcAdd.GetJulianComplete()
                ayan = GCAyanamsha.GetAyanamsa(jd)
                r1 = GCMath.putIn360(previousLongitude - ayan) / 30
                r2 = GCMath.putIn360(todayLongitude - ayan) / 30

                while(r2 > r1 + 13):
                    r2 -= 12.0
                while(r2 < r1 + 11):
                    r2 += 12.0

                a = (r2 - r1) / (todaySunriseHour - previousSunriseHour)
                b = r2 - a * todaySunriseHour

                tr = ceil(r1)
                for tr in range(ceil(r1),ceil(r2)):
                    tm = ( tr - b ) / a
                    if (tm > fromTimeLimit):
                        vcNext.Set(vcAdd)
                        vcNext.shour = tm
                        vcNext.NormalizeValues()
                        self.AddEvent(vcNext, CCTYPE_ASCENDENT, tr, ndst)

                previousLongitude = todayLongitude
                previousSunriseHour = todaySunriseHour - 1
                fromTimeLimit = previousSunriseHour

            if (GCDisplaySettings.getValue(COREEVENTS_RAHUKALAM)):
                r1,r2 = CalculateKala(sunRise, sunSet, vcAdd.dayOfWeek,KT_RAHU_KALAM)
                vcAdd.shour = r1
                self.AddEvent(vcAdd, CCTYPE_KALA_START, KT_RAHU_KALAM, ndst)
                vcAdd.shour = r2
                self.AddEvent(vcAdd, CCTYPE_KALA_END, KT_RAHU_KALAM, ndst)

            if (GCDisplaySettings.getValue(COREEVENTS_YAMAGHANTI)):
                r1,r2 = CalculateKala(sunRise, sunSet, vcAdd.dayOfWeek, KT_YAMA_GHANTI)
                vcAdd.shour = r1
                self.AddEvent(vcAdd, CCTYPE_KALA_START, KT_YAMA_GHANTI, ndst)
                vcAdd.shour = r2
                self.AddEvent(vcAdd, CCTYPE_KALA_END, KT_YAMA_GHANTI, ndst)

            if (GCDisplaySettings.getValue(COREEVENTS_GULIKALAM)):
                r1,r2 = CalculateKala(sunRise, sunSet, vcAdd.dayOfWeek, KT_GULI_KALAM)
                vcAdd.shour = r1
                self.AddEvent(vcAdd, CCTYPE_KALA_START, KT_GULI_KALAM, ndst)
                vcAdd.shour = r2
                self.AddEvent(vcAdd, CCTYPE_KALA_END, KT_GULI_KALAM, ndst)

            if (GCDisplaySettings.getValue(COREEVENTS_ABHIJIT_MUHURTA)):
                r1,r2 = CalculateKala(sunRise, sunSet, vcAdd.dayOfWeek, KT_ABHIJIT)
                if (r1 > 0 and r2 > 0):
                    vcAdd.shour = r1
                    self.AddEvent(vcAdd, CCTYPE_KALA_START, KT_ABHIJIT, ndst)
                    vcAdd.shour = r2
                    self.AddEvent(vcAdd, CCTYPE_KALA_END, KT_ABHIJIT, ndst)

            vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_TITHI)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                nData = GCTithi.GetNextTithiStart(earth, vcAdd, vcNext)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_TITHI, nData, ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.shour += 0.2
                if (vcAdd.shour >= 1.0):
                    vcAdd.shour -= 1.0
                    vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_NAKSATRA)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                nData = GCNaksatra.GetNextNaksatra(earth, vcAdd, vcNext)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_NAKS, nData, ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.shour += 0.2
                if (vcAdd.shour >= 1.0):
                    vcAdd.shour -= 1.0
                    vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_YOGA)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                nData = GCYoga.GetNextYogaStart(earth, vcAdd, vcNext)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_YOGA, nData, ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.shour += 0.2
                if (vcAdd.shour >= 1.0):
                    vcAdd.shour -= 1.0
                    vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_SANKRANTI)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                date,nData = GCSankranti.GetNextSankranti(vcAdd)
                vcNext.Set(date)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_SANK, nData, ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_MOONRASI)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                nData = GetNextMoonRasi(earth, vcAdd, vcNext)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_M_RASI, nData, ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.shour += 0.5
                vcAdd.NormalizeValues()

        if (GCDisplaySettings.getValue(COREEVENTS_CONJUNCTION)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                dlong = GCConjunction.GetNextConjunctionEx(vcAdd, vcNext, True, earth)
                if (vcNext.GetDayInteger() < vcEnd.GetDayInteger()):
                    vcNext.InitWeekDay()
                    ndst = GCTimeZone.determineDaylightChange(vcNext, loc.m_nTimezoneId)
                    self.AddEvent(vcNext, CCTYPE_CONJ, GCRasi.GetRasi(dlong, GCAyanamsha.GetAyanamsa(vcNext.GetJulianComplete())), ndst)
                else:
                    break
                vcAdd.Set(vcNext)
                vcAdd.NextDay()

        if (GCDisplaySettings.getValue(COREEVENTS_MOON)):
            vcAdd.Set(vc)
            vcAdd.shour = 0.0
            while vcAdd.IsBeforeThis(vcEnd):
                vcNext.Set(MOONDATA.GetNextRise(earth, vcAdd, True))
                self.AddEvent(vcNext, CCTYPE_M_RISE, 0, ndst)

                vcNext.Set(MOONDATA.GetNextRise(earth, vcNext, False))
                self.AddEvent(vcNext, CCTYPE_M_SET, 0, ndst)

                vcNext.shour += 0.05
                vcNext.NormalizeValues()
                vcAdd.Set(vcNext)

        if self.b_sorted:
            self.Sort()

    def formatText(self,stream):
        sb = GCStringBuilder(stream)
        sb.Format = SBTF_TEXT

        stream.write("Events from {} to {}.\r\n\r\n".format( self.m_vcStart, self.m_vcEnd))
        stream.write("{}\r\n\r\n".format(self.m_location.m_strFullName))

        prevd = GCGregorianDate()
        prevd.day = 0
        prevd.month = 0
        prevd.year = 0
        prevt = -1

        last_header = ''
        for dnr in self.p_events:
            new_header = ''
            if self.b_sorted:
                new_header = " {} - {} ".format(dnr.Time, GCStrings.GetDayOfWeek(dnr.Time.dayOfWeek))
            else:
                new_header = header_text[dnr.nType]
            if last_header != new_header:
                sb.AppendLine()
                sb.AppendHeader3(new_header)
                sb.AppendLine()
                last_header = new_header

            stream.write("            {} {}    {}".format(dnr.Time.time_str(), GCStrings.GetDSTSignature(dnr.nDst), dnr.EventText()))
            sb.AppendLine()

        sb.AppendLine()
        sb.AppendNote()
        return 1

    def formatXml(self,strXml):
        strXml.write("<xml>\r\n<program version=\"{}\">\r\n<location longitude=\"{}\" latitude=\"{}\" timezone=\"{}\" dst=\"{}\" />\n".format(GCStrings.getString(130), self.m_location.m_fLongitude, self.m_location.m_fLatitude , self.m_location.m_fTimezone, GCTimeZone.GetTimeZoneName(self.m_location.m_nTimezoneId)))

        for dnr in self.p_events:
            strXml.write("  <event type=\"{}\" date=\"{}\" time=\"{}\" dst=\"{}\" />\n".format(dnr.EventText(), str(dnr.Time), dnr.Time.time_str(), dnr.nDst))

        strXml.write("</xml>\n")
        return 1

    def formatRtf(self,stream):
        sb = GCStringBuilder(stream)
        sb.Format = SBTF_RTF
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote

        sb.AppendDocumentHeader()

        sb.AppendHeader1("Events")

        stream.write("\\par from {} to {}.\\par\r\n\\par\r\n".format( self.m_vcStart, self.m_vcEnd))
        stream.write("{}\\par\r\n\\par\r\n".format(self.m_location.m_strFullName))

        prevd = GCGregorianDate()
        prevd.day = 0
        prevd.month = 0
        prevd.year = 0
        prevt = -1

        last_header = ''
        for dnr in self.p_events:
            new_header = ''
            if self.b_sorted:
                new_header = " {} - {} ".format(dnr.Time, GCStrings.GetDayOfWeek(dnr.Time.dayOfWeek))
            else:
                new_header = header_text[dnr.nType]
            if last_header != new_header:
                sb.AppendLine()
                sb.AppendHeader2(new_header)
                sb.AppendLine()
                last_header = new_header

            stream.write("\\par            {} {}    {}".format(dnr.Time.time_str(), GCStrings.GetDSTSignature(dnr.nDst), dnr.EventText()))

        sb.AppendLine()
        sb.AppendNote()
        sb.AppendDocumentTail()
        return 1


    def writeHtml(self,stream):
        stream.write("<html>\n<head>\n<title>Core Events</title>\n\n")
        stream.write("<style>\n<!--\nbody {\n  font-family:Verdana;\n  font-size:11pt;\n}\n\ntd.hed {\n  font-size:11pt;\n  font-weight:bold;\n")
        stream.write("  background:#aaaaaa;\n  color:white;\n  text-align:center;\n  vertical-align:center;\n  padding-left:15pt;\n  padding-right:15pt;\n")
        stream.write("  padding-top:5pt;\n  padding-bottom:5pt;\n}\n-->\n</style>\n")
        stream.write("</head>\n")
        stream.write("<body>\n\n")
        stream.write("<h1 align=center>Events</h1>\n<p align=center>From {} to {}.</p>\n\n".format( self.m_vcStart, self.m_vcEnd))

        stream.write("<p align=center>{}</p>\n".format(self.m_location.m_strFullName))

        prevd = GCGregorianDate()
        prevd.day = 0
        prevd.month = 0
        prevd.year = 0
        prevt = -1

        stream.write("<table align=center><tr>\n")
        last_header = ''
        new_header = ''
        for dnr in self.p_events:
            if self.b_sorted:
                new_header = " {} - {} ".format(dnr.Time, GCStrings.GetDayOfWeek(dnr.Time.dayOfWeek))
            else:
                new_header = self.header_text[dnr.nType]
            if last_header != new_header:
                stream.write(f"<td class=\"hed\" colspan=2>{new_header}</td></tr>\n<tr>\n")
                last_header = new_header

            stream.write("<td>{}</td><td>{}</td></tr><tr>\n".format(dnr.EventText(), dnr.Time.time_str() ))

        stream.write("</tr></table>\n")
        stream.write("<hr align=center width=\"50%%\">\n<p align=center>Generated by {}</p>".format(GCStrings.getString(130)))
        stream.write("</body>\n</html>\n")
        return 1

    def write(self,stream,format='html',layout='list'):
        if format=='plain':
            self.formatText(stream)
        elif format=='rtf':
            self.formatRtf(stream)
        elif format=='xml':
            self.formatXml(stream)
        elif format=='html':
            self.writeHtml(stream)
            
def unittests():
    GCUT.info('core events results')
    loc = GCLocation(data={
        'latitude': 48.150002,
        'longitude': 17.116667,
        'tzid': 321,
        'name': 'Bratislava, Slovakia'
    })
    earth = loc.GetEarthData()
    today = Today()
    future = GCGregorianDate(date = today, addDays=100)

    tc = TCoreEvents()


    print('start calculate', datetime.datetime.now())
    tc.CalculateEvents(loc,today,future)
    print('end calculate', datetime.datetime.now())

    with open('test/events.xml','wt') as wf:
        tc.formatXml(wf)
    with open('test/events.txt','wt') as wf:
        tc.formatText(wf)
    with open('test/events.rtf','wt') as wf:
        tc.formatRtf(wf)
    with open('test/events.html','wt') as wf:
        tc.writeHtml(wf)
