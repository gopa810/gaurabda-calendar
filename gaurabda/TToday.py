from .GCGregorianDate import GCGregorianDate,Today
from .GCLocation import GCLocation
from .TCalendar import TCalendar
from .GCCalendarDay import GCCalendarDay
from .GCStringBuilder import GCStringBuilder,SBTF_RTF,SBTF_TEXT,SBTF_HTML

from . import GCTimeZone as GCTimeZone
from . import GCLayoutData as GCLayoutData
from . import GCStrings as GCStrings
from . import GCEarthData as GCEarthData
from . import GCDisplaySettings as GCDisplaySettings
from . import GCUT as GCUT
import datetime


class TToday:
    def __init__(self):
        self.currentDay = GCGregorianDate()
        self.calendar = TCalendar()

    def Calculate(self, dateTime, location):
        self.currentDay.Set(dateTime)
        self.currentDay.InitWeekDay()
        vc2 = GCGregorianDate(date = self.currentDay, addDays=-4)
        vc2.tzone = location.m_fTimezone
        self.calendar.CalculateCalendar(location, vc2, 9)

    def GetCurrentDay(self):
        i = self.calendar.FindDate(self.currentDay)
        return self.calendar.GetDay(i)

    def formatPlain(self, stream):
        p = self.GetCurrentDay()
        loc = self.calendar.m_Location
        vc = p.date

        sb = GCStringBuilder(stream)
        sb.Format = SBTF_TEXT

        if (p == None): return

        stream.write("{} ({}, {}, Timezone: {})\r\n\r\n[{} - {}]\r\n  {}, {} {}\r\n  {} {}, {} Gaurabda\r\n\r\n".format(loc.m_strName, GCEarthData.GetTextLatitude(loc.m_fLatitude), GCEarthData.GetTextLongitude(loc.m_fLongitude), GCTimeZone.GetTimeZoneName(loc.m_nTimezoneId), vc, GCStrings.getString(vc.dayOfWeek), GCStrings.GetTithiName(p.astrodata.nTithi), GCStrings.GetPaksaName(p.astrodata.nPaksa), GCStrings.getString(20), GCStrings.GetMasaName(p.astrodata.nMasa), GCStrings.getString(22), p.astrodata.nGaurabdaYear))

        self.WriteTodayInfo(sb,p)

    def formatRtf(self, stream):
        p = self.GetCurrentDay()
        loc = self.calendar.m_Location
        vc = p.date

        sb = GCStringBuilder(stream)
        sb.Format = SBTF_RTF
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote

        sb.AppendDocumentHeader()

        stream.write("\\f2\\fs{} {} ".format(GCLayoutData.textSizeH1, vc.GetDateTextWithTodayExt()))
        stream.write("\\par\\f2\\fs{} {{\\fs{} {} }}\\line {} ({}, {}, Timezone: {})\\par\r\n\\par\r\n  {}, {} {}\\par\r\n  {} {}, {} Gaurabda\\par\r\n\\par\r\n".format( GCLayoutData.textSizeText, GCLayoutData.textSizeText+4, GCStrings.getString(p.date.dayOfWeek), loc.m_strName, GCEarthData.GetTextLatitude(loc.m_fLatitude), GCEarthData.GetTextLongitude(loc.m_fLongitude), GCTimeZone.GetTimeZoneName(loc.m_nTimezoneId), GCStrings.GetTithiName(p.astrodata.nTithi), GCStrings.GetPaksaName(p.astrodata.nPaksa), GCStrings.getString(20), GCStrings.GetMasaName(p.astrodata.nMasa), GCStrings.getString(22), p.astrodata.nGaurabdaYear))

        self.WriteTodayInfo(sb,p)


    def writeHtml(self, stream):
        p = self.GetCurrentDay()
        loc = self.calendar.m_Location
        vc = p.date
        sb = GCStringBuilder(stream)
        sb.Format = SBTF_HTML

        if (p == None): return

        stream.write("<html>\n<head>\n<title></title>")
        stream.write("<style>\n<!--\nbody {\n  font-family:Verdana;\n  font-size:9.5pt;\n}\n\ntd.hed {\n  font-size:9.5pt;\n  font-weight:bold;\n")
        stream.write("  background:#aaaaaa;\n  color:white;\n  text-align:center;\n  vertical-align:center;\n  padding-left:15pt;\n  padding-right:15pt;\n")
        stream.write("  padding-top:5pt;\n  padding-bottom:5pt;\n}\n-->\n</style>\n")
        stream.write("</head>\n")
        stream.write("<body>\n")
        stream.write("<h2>{}</h2>\n".format(vc.GetDateTextWithTodayExt()))
        stream.write("<h4>{}</h4>\n".format(loc.m_strFullName))
        stream.write("<p>  {}, {} {}<br>  {} {}, {} Gaurabda</p>".format(GCStrings.GetTithiName(p.astrodata.nTithi), GCStrings.GetPaksaName(p.astrodata.nPaksa), GCStrings.getString(20), GCStrings.GetMasaName(p.astrodata.nMasa), GCStrings.getString(22), p.astrodata.nGaurabdaYear))

        prevCountFest = 0

        stream.write("<p>")
        self.WriteTodayInfo(sb,p)

    def WriteTodayInfo(self,sb,p):
        sb.AppendLine()
        stream = sb.Target

        for ed in p.dayEvents:
            if 'disp' not in ed or ed['disp'] == -1 or GCDisplaySettings.getValue(ed['disp']):
                if 'spec' in ed:
                    sb.AppendHeader3(ed['text'],fillChar='-')
                else:
                    sb.AppendString(ed['text'])
                sb.AppendLine()

        if GCDisplaySettings.getValue(45):
            tda = p.astrodata.sun.rise
            sb.AppendLine()
            stream.write("Brahma Muhurta {} - {} ({})".format(tda.short(-96), tda.short(-48), GCStrings.GetDSTSignature(p.hasDST)))

        if GCDisplaySettings.getValue(29):
            sb.AppendLine()
            tda = p.astrodata.sun.rise
            stream.write("{} {} ".format(GCStrings.getString(51), tda.short() ))
            if (GCDisplaySettings.getValue(32)):
                stream.write(" sandhya {} - {} ", tda.short(-24), tda.short(24))
            stream.write(" ({})".format(GCStrings.GetDSTSignature(p.hasDST)))
            sb.AppendLine()


        if (GCDisplaySettings.getValue(30)):
            sb.AppendLine()
            tda = p.astrodata.sun.noon
            stream.write("{} {} ".format(GCStrings.getString(857), tda.short() ))
            if (GCDisplaySettings.getValue(32)):
                stream.write(" sandhya {} - {} ", tda.short(-24), tda.short(24))
            stream.write(" ({})".format(GCStrings.GetDSTSignature(p.hasDST)))
            sb.AppendLine()

        if (GCDisplaySettings.getValue(31)):
            sb.AppendLine()
            tda = p.astrodata.sun.set
            stream.write("{} {} ".format(GCStrings.getString(52), tda.short() ))
            if (GCDisplaySettings.getValue(32)):
                stream.write(" sandhya {} - {} ", tda.short(-24), tda.short(24))
            stream.write(" ({})".format(GCStrings.GetDSTSignature(p.hasDST)))
            sb.AppendLine()

        if (GCDisplaySettings.getValue(33)):
            sb.AppendLine()
            sb.AppendString(GCStrings.getString(51) + " info")
            sb.AppendLine()
            sb.AppendString("   Moon in {} {}".format(GCStrings.GetNaksatraName(p.astrodata.nNaksatra), GCStrings.getString(15)))

            if (GCDisplaySettings.getValue(47)):
                sb.AppendString(", {:.1f}% passed ({} Pada)".format(p.astrodata.nNaksatraElapse, GCStrings.getString(811+int(p.astrodata.nNaksatraElapse/25))))

            if (GCDisplaySettings.getValue(46)):
                sb.AppendString(", Moon in {} {}".format( GCStrings.GetSankrantiName(p.astrodata.nMoonRasi), GCStrings.getString(105)))

            sb.AppendString(", {} {}".format(GCStrings.GetYogaName(p.astrodata.nYoga), GCStrings.getString(104)))
            sb.AppendLine()
            sb.AppendString("   Sun in {} {}.".format(GCStrings.GetSankrantiName(p.astrodata.nSunRasi), GCStrings.getString(105)))
            sb.AppendLine()

        sb.AppendNote()
        sb.AppendDocumentTail()

    def write(self,stream,format='html'):
        if format=='plain':
            self.formatPlain(stream)
        elif format=='rtf':
            self.formatRtf(stream)
        elif format=='html':
            self.writeHtml(stream)


def unittests():
    GCUT.info('today results')
    loc = GCLocation(data={
        'latitude': 48.150002,
        'longitude': 17.116667,
        'tzid': 321,
        'name': 'Bratislava, Slovakia'
    })
    earth = loc.GetEarthData()
    today = Today()

    tc = TToday()

    print('start calculate', datetime.datetime.now())
    tc.Calculate(today,loc)
    print('end calculate', datetime.datetime.now())

    with open('test/today.txt','wt') as wf:
        tc.formatPlain(wf)
    with open('test/today.rtf','wt') as wf:
        tc.formatRtf(wf)
    with open('test/today.html','wt') as wf:
        tc.writeHtml(wf)
