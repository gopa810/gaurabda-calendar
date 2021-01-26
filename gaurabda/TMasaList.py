from . import GCStrings as GCStrings
from . import GCStringBuilder as GCStringBuilder
from . import GCLayoutData as GCLayoutData
from .GCLocation import GCLocation
from .GCGregorianDate import GCGregorianDate
from .GCDayData import GCDayData, GetFirstDayOfYear
from . import GCUT as GCUT

class TMasaList:
    def __init__(self):
        self.start = None
        self.end = None
        self.countYears = 0
        self.countMasa = 0
        self.startYear = 0
        self.location = None
        self.arr = []

    def CalculateMasaList(self,loc,year,count):
        day = GCDayData()
        earth = loc.GetEarthData()

        self.startYear = year
        self.countYears = count
        self.start = GCGregorianDate(date = GetFirstDayOfYear(earth, year))
        self.end = GCGregorianDate(date = GetFirstDayOfYear(earth, year + count))
        self.location = GCLocation()
        self.location.Set(loc)

        i = 0
        prev_masa = -1
        prev_paksa = -1
        prev_gyear = -1
        current = 0
        d = GCGregorianDate(date = self.start)

        while d.IsBeforeThis(self.end):
            day.DayCalc(d, earth)
            if prev_paksa != day.nPaksa:
                day.nMasa = day.MasaCalc(d, earth)
                if prev_masa != day.nMasa:
                    if len(self.arr)>0:
                        self.arr[-1]['end'] = GCGregorianDate(date = d, addDays=-1)
                    prev_masa = day.nMasa
                    self.arr.append({
                        'masa': day.nMasa,
                        'masaName': GCStrings.GetMasaName(day.nMasa),
                        'year': day.nGaurabdaYear,
                        'start': GCGregorianDate(date=d)
                    })
            prev_paksa = day.nPaksa
            d.NextDay()

        self.arr[-1]['end'] = GCGregorianDate(date = d, addDays=-1)
        return len(self.arr)

    def formatText(self,stream):
        sb = GCStringBuilder.GCStringBuilder(stream)
        sb.Format = GCStringBuilder.SBTF_TEXT

        stream.write(" {}\r\n\r\n{}: {}\r\n".format(GCStrings.getString(39), GCStrings.getString(40), self.location.m_strFullName))
        stream.write("{} {} {} {}\r\n".format(GCStrings.getString(41), str(self.start), GCStrings.getString(42), str(self.end)))
        stream.write("=" * 65)
        stream.write("\r\n\r\n")

        for m in self.arr:
            stream.write('{:30s}'.format('{} {}'.format(m['masaName'],m['year'])))
            stream.write('   {} - {}\r\n'.format(str(m['start']).rjust(12,' '), str(m['end']).rjust(12,' ')))

        sb.AppendNote()
        sb.AppendDocumentTail()
        return 1

    def formatRtf(self,stream):
        sb = GCStringBuilder.GCStringBuilder(stream)
        sb.Format = GCStringBuilder.SBTF_RTF
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote

        sb.AppendDocumentHeader()

        stream.write("{{\\fs{}\\f2 {} }}\\par\\tx{}\\tx{}\\f2\\fs{}\r\n\\par\r\n{}: {}\\par\r\n".format(GCLayoutData.textSizeH1 , GCStrings.getString(39), 1000*GCLayoutData.textSizeText/24, 4000*GCLayoutData.textSizeText/24 , GCLayoutData.textSizeText, GCStrings.getString(40), self.location.m_strFullName))
        stream.write("{} {} {} {}\\par\r\n".format( GCStrings.getString(41), str(self.start) , GCStrings.getString(42), str(self.end)))
        sb.AppendSeparatorWithWidth(65)
        sb.AppendLine()
        sb.AppendLine()

        for m in self.arr:
            stream.write('\\tab {} {}\\tab '.format(m['masaName'],m['year']))
            stream.write('{} - '.format(str(m['start'])))
            stream.write('{}\\par\r\n'.format(str(m['end'])))

        sb.AppendNote()
        sb.AppendDocumentTail()

        return 1


    def writeXml(self,stream):
        stream.write("<xml>\r\n")
        stream.write("   <body title=\"Masa List\">\n\n")
        stream.write("      <location>{}</location>\r\n".format(self.location.m_strFullName))
        stream.write("      <masalist>\r\n")
        for m in self.arr:
            stream.write("         <masa name=\"{}\" year=\"{}\" start=\"{}\" end=\"{}\" />\r\n".format(m['masaName'], m['year'], str(m['start']), str(m['end'])))
        stream.write("      </masalist>\r\n")
        stream.write("      <author>{}</author>\r\n".format(GCStrings.getString(130)))
        stream.write("   </body>\r\n</xml>\r\n")
        return 1

    def writeHtml(self,stream):
        stream.write("<html>\n<head>\n<title>Masa List</title>\n\n")
        stream.write("<style>\n<!--\nbody {\n  font-family:Verdana;\n  font-size:11pt;\n}\n\ntd.hed {\n  font-size:11pt;\n  font-weight:bold;\n")
        stream.write("  background:#aaaaaa;\n  color:white;\n  text-align:center;\n  vertical-align:center;\n  padding-left:15pt;\n  padding-right:15pt;\n")
        stream.write("  padding-top:5pt;\n  padding-bottom:5pt;\n}\n-->\n</style>\n")
        stream.write("</head>\n")
        stream.write("<body>\n\n")

        stream.write("<p style=\'text-align:center\'><span style=\'font-size:14pt\'>Masa List</span></br>{}: {}</p>\n".format(GCStrings.getString(40), self.location.m_strFullName))
        stream.write("<p align=center>{} {} {} {} </p>\n".format(GCStrings.getString(41), str(self.start), GCStrings.getString(42), str(self.end)))
        stream.write("<hr width=\"50%\">")

        stream.write("<table align=center>")
        stream.write("<tr><td class=\"hed\" style=\'text-align:left\'>MASA NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td class=\"hed\">START</td><td class=\"hed\">END</td></tr>")

        for m in self.arr:
            stream.write("<tr>")
            stream.write("<td>{} {}&nbsp;&nbsp;&nbsp;&nbsp;</td>".format( m['masaName'], m['year']))
            stream.write("<td>{}</td>".format(str(m['start'])))
            stream.write("<td>{}</td>".format(str(m['end'])))
            stream.write("</tr>")

        stream.write("</table>")
        stream.write("<hr width=\"50%%\">\n<p align=center>Generated by {}</p>".format(GCStrings.getString(130)))
        stream.write("</body></html>")
        return 1

    def write(self,stream,format='html'):
        if format=='plain':
            self.formatText(stream)
        elif format=='rtf':
            self.formatRtf(stream)
        elif format=='xml':
            self.writeXml(stream)
        elif format=='html':
            self.writeHtml(stream)


def unittests():
    tm = TMasaList()
    loc = GCLocation(data={
        'latitude': 48.150002,
        'longitude': 17.116667,
        'tzid': 321,
        'name': 'Bratislava, Slovakia'
    })
    tm.CalculateMasaList(loc,2020,2)

    with open('test/masalist.rtf','wt') as wf:
        tm.formatRtf(wf)
    with open('test/masalist.html','wt') as wf:
        tm.writeHtml(wf)
