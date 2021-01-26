from .GCLocation import GCLocation
from .GCDayData import GCDayData
from .GCGregorianDate import GCGregorianDate, Today
from .GCStringBuilder import GCStringBuilder,SBTF_TEXT,SBTF_RTF
from math import floor
from . import GCUT as GCUT
import datetime
from . import GCMath as GCMath
from . import GCEarthData as GCEarthData
from . import GCAyanamsha as GCAyanamsha
from . import GCRasi as GCRasi
from .GCEnums.MasaId import *
from .GCPancangaDate import GCGaurabdaDate
from . import GCCalendar as GCCalendar
from . import GCStrings as GCStrings
from . import GCTimeZone as GCTimeZone
from . import GCDisplaySettings as GCDisplaySettings
from . import GCLayoutData as GCLayoutData

TRESULT_APP_CELEBS = 3


class TAppDay:
    def __init__(self):
        self.m_location = GCLocation()
        self.eventTime = GCGregorianDate()
        self.details = GCDayData()
        self.b_adhika = False
        self.celeb_gy = [0] * TRESULT_APP_CELEBS
        self.celeb_date = [GCGregorianDate() for i in range(TRESULT_APP_CELEBS)]

    def calculateAppDay(self, location, eventDate):
        d = self.details
        vc = GCGregorianDate(date = eventDate)
        vcsun = GCGregorianDate(date = eventDate)
        dprev = GCGregorianDate()
        dnext = GCGregorianDate()
        m_earth = location.GetEarthData()

        self.b_adhika = False
        self.eventTime.Set(eventDate)
        self.m_location.Set(location)

        vcsun.shour -= vcsun.tzone/24.0
        vcsun.NormalizeValues()
        vcsun.tzone = 0.0
        d.sun.SunPosition(vcsun, m_earth, vcsun.shour - 0.5)
        d.moon.Calculate(vcsun.GetJulianComplete(), m_earth)
        d.msDistance = GCMath.putIn360( d.moon.longitude_deg - d.sun.longitude_deg - 180.0)
        d.msAyanamsa = GCAyanamsha.GetAyanamsa( vc.GetJulianComplete() )

        # tithi
        dd = d.msDistance / 12.0
        d.nTithi = int(floor(dd))
        d.nTithiElapse = (dd - floor(dd)) * 100.0

        # naksatra
        dd = GCMath.putIn360( d.moon.longitude_deg - d.msAyanamsa )
        dd = ( dd * 3.0) / 40.0
        d.nNaksatra = int(floor(dd))
        d.nNaksatraElapse = (dd - floor(dd)) * 100.0
        d.nMasa = d.MasaCalc(vc, m_earth)
        d.nMoonRasi = GCRasi.GetRasi(d.moon.longitude_deg, d.msAyanamsa)
        d.nSunRasi = GCRasi.GetRasi(d.sun.longitude_deg, d.msAyanamsa)

        if (d.nMasa == ADHIKA_MASA):
            d.nMasa = GCRasi.GetRasi(d.sun.longitude_deg, d.msAyanamsa)
            self.b_adhika = True

        vc.Today()
        vc.tzone = m_earth.tzone
        m = 0
        va = GCGaurabdaDate()
        vctemp = GCGregorianDate()

        va.tithi = d.nTithi
        va.masa  = d.nMasa
        va.gyear = GCCalendar.GetGaurabdaYear(vc, m_earth)
        if (va.gyear < d.nGaurabdaYear):
            va.gyear = d.nGaurabdaYear


        for i in range(6):
            GCCalendar.Gaurabda2Gregorian(va, vctemp, m_earth)
            if (va.gyear > d.nGaurabdaYear):
                if (m < TRESULT_APP_CELEBS):
                    self.celeb_date[m].Set(vctemp)
                    self.celeb_gy[m] = va.gyear
                    m+=1
            va.gyear+=1

    def formatPlainText(self, stream):
        d = self.details
        vc = GCGregorianDate(date = self.eventTime)
        m_earth = self.m_location.GetEarthData()

        sb = GCStringBuilder(stream)
        sb.Format = SBTF_TEXT

        sb.AppendLine(GCStrings.getString(25))
        sb.AppendLine("")

        sb.AppendLine("{:15s} : {} {} {}".format(GCStrings.getString(7), vc.day, GCStrings.GetMonthAbreviation(vc.month), vc.year))

        sb.AppendLine("{:15s} : {}:{:02d}".format(GCStrings.getString(8), vc.GetHour(), vc.GetMinuteRound()))
        sb.AppendLine("")

        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(9), self.m_location.m_strName))
        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(10), self.m_location.m_strLatitude))
        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(11), self.m_location.m_strLongitude))
        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(12),  self.m_location.m_strTimeZone))
        sb.AppendLine("{:15s} : N/A".format("DST"))
        sb.AppendLine("")

        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(13), GCStrings.GetTithiName(d.nTithi)))
        sb.AppendLine("{:15s} : {:.2f} %".format(GCStrings.getString(14), d.nTithiElapse))
        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(15), GCStrings.GetNaksatraName(d.nNaksatra)))
        sb.AppendLine("{:15s} : {:.2f} % ({} pada)".format(GCStrings.getString(16), d.nNaksatraElapse,
            GCStrings.getString(811+int(d.nNaksatraElapse/25.0))))
        sb.AppendLine("{:15s} : {} ({})".format("Moon Rasi", GCStrings.GetSankrantiName(d.nMoonRasi), GCStrings.GetSankrantiNameEn(d.nMoonRasi)))
        sb.AppendLine("{:15s} : {} ({})".format("Sun Rasi", GCStrings.GetSankrantiName(d.nSunRasi), GCStrings.GetSankrantiNameEn(d.nSunRasi)))

        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(20), GCStrings.GetPaksaName(d.nPaksa)))
        if (self.b_adhika == True):
            sb.AppendLine("{:15s} : {} {}".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa), GCStrings.getString(21)))
        else:
            sb.AppendLine("{:15s} : {}".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa)))
        sb.AppendLine("{:15s} : {}".format(GCStrings.getString(23), d.nGaurabdaYear))

        if (GCDisplaySettings.getValue(48)):
            sb.AppendLine()
            sb.AppendLine(GCStrings.getString(17))
            sb.AppendLine()

            sb.AppendLine("%25s : {}... ".format(GCStrings.getString(18) , GCStrings.GetNaksatraChildSylable(d.nNaksatra, int(d.nNaksatraElapse/25.0))))
            sb.AppendLine("%25s : {}... ".format(GCStrings.getString(19), GCStrings.GetRasiChildSylable(d.nMoonRasi)))

        sb.AppendLine()
        sb.AppendLine(GCStrings.getString(24))
        sb.AppendLine()

        for o in range(TRESULT_APP_CELEBS):
            sb.AppendLine("   Gaurabda {:3d} : {} ".format(self.celeb_gy[o] , self.celeb_date[o]))

        sb.AppendNote()

    def formatRtf(self,stream):
        d = self.details
        vc = GCGregorianDate(date=self.eventTime)
        m_earth = self.m_location.GetEarthData()

        sb = GCStringBuilder(stream)
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote
        sb.Format = SBTF_RTF

        sb.AppendDocumentHeader()

        sb.AppendHeader1(GCStrings.getString(25))


        sb.AppendLine("\\tab {} : {{\\b {} {} {} }}".format(GCStrings.getString(7), vc.day, GCStrings.GetMonthAbreviation(vc.month), vc.year))

        sb.AppendLine("\\tab {} : {{\\b {}:{:02d} }}".format(GCStrings.getString(8), vc.GetHour(), vc.GetMinuteRound()))
        sb.AppendLine("")

        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(9), self.m_location.m_strName))
        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(10), self.m_location.m_strLatitude))
        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(11), self.m_location.m_strLongitude))
        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(12), GCTimeZone.GetTimeZoneName(self.m_location.m_nTimezoneId)))
        sb.AppendLine("\\tab {} : {{\\b N/A }}".format("DST"))
        sb.AppendLine("")

        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(13), GCStrings.GetTithiName(d.nTithi)))
        sb.AppendLine("\\tab {} : {{\\b {:.2f} % }}".format(GCStrings.getString(14), d.nTithiElapse))
        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(15), GCStrings.GetNaksatraName(d.nNaksatra)))
        sb.AppendLine("\\tab {} : {{\\b {:.2f} % ({} pada) }}".format(GCStrings.getString(16), d.nNaksatraElapse, GCStrings.getString(811+int(d.nNaksatraElapse/25.0))))
        sb.AppendLine("\\tab {} : {{\\b {} ({}) }}".format("Moon Rasi", GCStrings.GetSankrantiName(d.nMoonRasi), GCStrings.GetSankrantiNameEn(d.nMoonRasi)))
        sb.AppendLine("\\tab {} : {{\\b {} ({}) }}".format("Sun Rasi", GCStrings.GetSankrantiName(d.nSunRasi), GCStrings.GetSankrantiNameEn(d.nSunRasi)))

        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(20), GCStrings.GetPaksaName(d.nPaksa)))
        if (self.b_adhika == True):
            sb.AppendLine("\\tab {} : {{\\b {} {} }}".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa), GCStrings.getString(21)))
        else:
            sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa)))
        sb.AppendLine("\\tab {} : {{\\b {} }}".format(GCStrings.getString(23), d.nGaurabdaYear))

        if (GCDisplaySettings.getValue(48)):
            sb.AppendLine("")
            sb.AppendHeader2(GCStrings.getString(17))
            sb.AppendLine("")
            sb.AppendLine("\\tab {} : {{\\b {}...  }}".format(GCStrings.getString(18) , GCStrings.GetNaksatraChildSylable(d.nNaksatra, int(d.nNaksatraElapse/25.0))))
            sb.AppendLine("\\tab {} : {{\\b {}...  }}".format(GCStrings.getString(19), GCStrings.GetRasiChildSylable(d.nMoonRasi)))


        sb.AppendLine("{{\\fs{} {} }}".format(GCLayoutData.textSizeH2, GCStrings.getString(24)))
        sb.AppendLine("")

        for o in range(TRESULT_APP_CELEBS):
            sb.AppendLine("\\tab Gaurabda {} : {{\\b {} }}".format(self.celeb_gy[o] , self.celeb_date[o]))

        sb.AppendDocumentTail()

    def formatXml(self,stream):
        d = self.details
        vc = GCGregorianDate(date=self.eventTime)
        m_earth = self.m_location.GetEarthData()
        loc = self.m_location
        bDuringAdhika = False

        stream.write('''<xml>
    <request name="AppDay" version="{}">
        <arg name="longitude" value="{}" />
        <arg name="latitude" value="{}" />
        <arg name="timezone" value="{}" />
        <arg name="year" value="{}" />
        <arg name="month" value="{}" />
        <arg name="day" value="{}" />
        <arg name="hour" value="{}" />
        <arg name="minute" value="{}" />
    </request>'''.format(GCStrings.getString(130), loc.m_fLongitude, loc.m_fLatitude, loc.m_fTimezone, self.eventTime.year, self.eventTime.month, self.eventTime.day, self.eventTime.GetHour(), self.eventTime.GetMinuteRound() ))

        npada = int (floor(d.nNaksatraElapse / 25.0)) + 1
        if (npada > 4): npada = 4
        is_adhika = "yes" if bDuringAdhika else "no"
        stream.write("\t<result name=\"AppDay\" >\n\t\t<tithi name=\"{}\" elapse=\"%f\" />\n\t\t<naksatra name=\"{}\" elapse=\"%f\" pada=\"{}\"/>\n\t\t<paksa name=\"{}\" />\n\t\t<masa name=\"{}\" adhikamasa=\"{}\"/>\n\t\t<gaurabda value=\"{}\" />\n".format(GCStrings.GetTithiName(d.nTithi), d.nTithiElapse , GCStrings.GetNaksatraName(d.nNaksatra), d.nNaksatraElapse, npada , GCStrings.GetPaksaName(d.nPaksa) , GCStrings.GetMasaName(d.nMasa), is_adhika , d.nGaurabdaYear ))

        stream.write("\t\t<celebrations>\n")
        for i in range(TRESULT_APP_CELEBS):
            stream.write("\t\t\t<celebration gaurabda=\"{}\" day=\"{}\" month=\"{}\" monthabr=\"{}\" year=\"{}\" />\n".format(self.celeb_gy[i], self.celeb_date[i].day, self.celeb_date[i].month, GCStrings.GetMonthAbreviation(self.celeb_date[i].month), self.celeb_date[i].year))

        stream.write("\t\t</celebrations>\n\t</result>\n</xml>\n")


    def writeHtml(self,stream):
        d = self.details
        vc = GCGregorianDate(date = self.eventTime)
        m_earth = self.m_location.GetEarthData()

        stream.write("<html><head><title>Appearance day</title>")
        stream.write("<style>\n<!--\nbody {\n  font-family:Verdana;\n  font-size:11pt;\n}\n\ntd.hed {\n  font-size:11pt;\n  font-weight:bold;\n")
        stream.write("  background:#aaaaaa;\n  color:white;\n  text-align:center;\n  vertical-align:center;\n  padding-left:15pt;\n  padding-right:15pt;\n")
        stream.write("  padding-top:5pt;\n  padding-bottom:5pt;\n}\n-->\n</style>\n")
        stream.write("</head>\n\n<body>\n")
        stream.write("<h2 align=center>Appearance day Calculation</h2>")
        stream.write("<table align=center><tr><td valign=top>\n\n")
        stream.write("<table align=center>")
        stream.write("<tr><td colspan=3 class=hed>Details</td></tr>\n")
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(7), vc))
        stream.write("<tr><td colspan=2>{}</td><td> {}:{:02d}</td></tr>\n\n".format(GCStrings.getString(8), vc.GetHour(), vc.GetMinuteRound()))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(9), self.m_location.m_strName))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(10), GCEarthData.GetTextLatitude(self.m_location.m_fLatitude)))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(11), GCEarthData.GetTextLongitude(self.m_location.m_fLongitude)))
        stream.write("<tr><td colspan=2>{}</td><td> ".format(GCStrings.getString(12)))
        stream.write(GCTimeZone.GetTimeZoneOffsetText(self.m_location.m_fTimezone))
        stream.write("</td></tr>\n")
        stream.write("<tr><td colspan=2>DST</td><td>N/A</td></tr>\n")
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(13), GCStrings.GetTithiName(d.nTithi)))
        stream.write("<tr><td colspan=2>{}</td><td> {:.2f} %</td></tr>\n".format(GCStrings.getString(14), d.nTithiElapse))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(15), GCStrings.GetNaksatraName(d.nNaksatra)))
        stream.write("<tr><td colspan=2>{}</td><td> {:.2f} %</td></tr>\n".format(GCStrings.getString(16), d.nNaksatraElapse))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(20), GCStrings.GetPaksaName(d.nPaksa)))
        if (self.b_adhika == True):
            stream.write("<tr><td colspan=2>{}</td><td> {} {}</td></tr>\n".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa), GCStrings.getString(21)))
        else:
            stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n".format(GCStrings.getString(22), GCStrings.GetMasaName(d.nMasa)))
        stream.write("<tr><td colspan=2>{}</td><td> {}</td></tr>\n\n".format(GCStrings.getString(23), d.nGaurabdaYear))

        stream.write("</table></td><td valign=top><table>")
        stream.write("<tr><td colspan=3 class=hed>{}</td></tr>\n".format(GCStrings.getString(24)))

        for o in range(TRESULT_APP_CELEBS):
            stream.write("<tr><td>Gaurabda {}</td><td>&nbsp;&nbsp;:&nbsp;&nbsp;</td><td><b>{}</b></td></tr>".format(self.celeb_gy[o] , self.celeb_date[o]))
        stream.write("</table>")
        stream.write("</td></tr></table>\n\n")
        stream.write("<hr align=center width=\"50%\">\n<p style=\'text-align:center;font-size:8pt\'>Generated by {}</p>".format(GCStrings.getString(130)))
        stream.write("</body></html>")

    def write(self,stream,format='html',layout='list'):
        if format=='plain':
            self.formatPlainText(stream)
        elif format=='rtf':
            self.formatRtf(stream)
        elif format=='xml':
            self.formatXml(stream)
        elif format=='html':
            self.writeHtml(stream)

def unittests():
    GCUT.info('result app')
    loc = GCLocation(data={
        'latitude': 48.150002,
        'longitude': 17.116667,
        'tzid': 321,
        'name': 'Bratislava, Slovakia'
    })
    earth = loc.GetEarthData()
    today = Today()

    tc = TAppDay()

    print('start calculate', datetime.datetime.now())
    tc.calculateAppDay(loc,today)
    print('end calculate', datetime.datetime.now())

    with open('test/app.xml','wt') as wf:
        tc.formatXml(wf)
    with open('test/app.txt','wt') as wf:
        tc.formatPlainText(wf)
    with open('test/app.rtf','wt') as wf:
        tc.formatRtf(wf)
    with open('test/app.html','wt') as wf:
        tc.writeHtml(wf)
