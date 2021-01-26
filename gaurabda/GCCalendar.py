from .GCGregorianDate import GCGregorianDate,Today
from .GCEarthData import EARTHDATA
from .GCPancangaDate import GCGaurabdaDate
from .GCLocation import GCLocation
from .GCDayData import GCDayData,GetFirstDayOfYear
from .GCEnums import MasaId
from . import GCTithi as GCTithi
from . import GCStrings as GCStrings
from math import floor
from . import GCUT as GCUT

def GetGaurabdaYear(vc, earth):
    day = GCDayData()
    day.DayCalc(vc, earth)
    day.MasaCalc(vc, earth)
    return day.nGaurabdaYear


def FormatDate(vc,va):
    return "{} {} {}\r\n{}, {} Paksa, {} Masa, {}".format(vc.day, GCStrings.GetMonthAbreviation(vc.month), vc.year, GCStrings.GetTithiName(va.tithi%15), GCStrings.GetPaksaName(va.paksa), GCStrings.GetMasaName(va.masa), va.gyear)

#===========================================================================
#
#===========================================================================

def Gaurabda2Gregorian(va, vc, earth):
    vc.Set(GCTithi.CalcTithiDate(va.gyear, va.masa, va.paksa, va.tithi % 15, earth))

#===========================================================================
#
#===========================================================================

def Gregorian2Gaurabda(vc, va, earth):
    day = GCDayData()
    day.DayCalc(vc, earth)
    va.masa = day.MasaCalc(vc, earth)
    va.tithi = day.nTithi
    va.gyear = day.nGaurabdaYear

def CalcEndDate(m_earth, vcStart, vaStart, vcEnd, vaEnd, nType, nCount):
    if nType==1:
        vcEnd.Set(vcStart)
        if nCount > 30240: nCount = 30240
        vcEnd.AddDays(nCount)
        Gregorian2Gaurabda(vcEnd, vaEnd, m_earth)
    elif nType==2:
        vcEnd.Set(vcStart)
        if nCount > 4320: nCount = 4320
        vcEnd.AddDays(nCount*7)
        Gregorian2Gaurabda(vcEnd, vaEnd, m_earth)
    elif nType==3:
        vcEnd.Set(vcStart)
        if nCount > 1080: nCount = 1080
        vcEnd.month += nCount
        while vcEnd.month > 12:
            vcEnd.year += 1
            vcEnd.month -= 12
        Gregorian2Gaurabda(vcEnd, vaEnd, m_earth)
    elif nType == 4:
        vcEnd.Set(vcStart)
        if nCount > 90: nCount = 90
        vcEnd.year += nCount
        Gregorian2Gaurabda(vcEnd, vaEnd, m_earth)
    elif nType == 5:
        vaEnd.Set(vaStart)
        if nCount > 30240: nCount = 30240
        vaEnd.tithi += nCount
        while vaEnd.tithi >= 30:
            vaEnd.tithi-=30
            vaEnd.masa+=1
        while vaEnd.masa >= 12:
            vaEnd.masa -= 12
            vaEnd.gyear+=1
        Gaurabda2Gregorian(vaEnd, vcEnd, m_earth)
    elif nType==6:
        vaEnd.Set(vaStart)
        if nCount > 1080: nCount = 1080
        vaEnd.masa = MasaToComboMasa(vaEnd.masa)
        if vaEnd.masa == MasaId.ADHIKA_MASA:
            vcEnd.Set(vcStart)
            vcEnd.month += nCount
            while vcEnd.month > 12:
                vcEnd.year+=1
                vcEnd.month -= 12
            Gregorian2Gaurabda(vcEnd, vaEnd, m_earth)
            vaEnd.tithi = vaStart.tithi
            Gaurabda2Gregorian(vaEnd, vcEnd, m_earth)
        else:
            vaEnd.masa += nCount
            while vaEnd.masa >= 12:
                vaEnd.masa -= 12
                vaEnd.gyear+=1
            vaEnd.masa = GCCalendar.ComboMasaToMasa(vaEnd.masa)
            Gaurabda2Gregorian(vaEnd, vcEnd, m_earth)
    elif nType==7:
        vaEnd.Set(vaStart)
        if nCount > 90: nCount = 90
        vaEnd.gyear += nCount
        Gaurabda2Gregorian(vaEnd, vcEnd, m_earth)
    return 1

def ComboMasaToMasa(nComboMasa):
    return 12 if nComboMasa == 12 else (nComboMasa + 11) % 12

def MasaToComboMasa(nMasa):
    return 12 if nMasa == 12 else (nMasa + 1) % 12

def writeFirstDayXml(xml,loc,vc):

    vcStart = GCGregorianDate(date=GetFirstDayOfYear(loc.GetEarthData(), vcStart.year))
    vcStart.InitWeekDay()

    # write
    xml.write("<xml>\n")
    xml.write("\t<request name=\"FirstDay\" version=\"")
    xml.write(GCStrings.getString(130))
    xml.write("\">\n")
    xml.write("\t\t<arg name=\"longitude\" val=\"")
    xml.write(str(loc.m_fLongitude))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"latitude\" val=\"")
    xml.write(str(loc.m_fLatitude))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"year\" val=\"")
    xml.write(str(vcStart.year))
    xml.write("\" />\n")
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"FirstDay_of_GaurabdaYear\">\n")
    xml.write("\t\t<firstday date=\"")
    xml.write(str(vcStart))
    xml.write("\" dayweekid = \"")
    xml.write(str(vcStart.dayOfWeek))
    xml.write("\" dayweek=\"")
    xml.write(GCStrings.getString(vcStart.dayOfWeek))
    xml.write("\" />\n")
    xml.write("\t</result>\n")
    xml.write("</xml>\n")
    return 0


def unittests():
    GCUT.info('calendar')
    e = EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = Today()
    a = GetGaurabdaYear(vc,e)
    GCUT.msg('Gaurabda year:' + str(a))

    va = GCGaurabdaDate()
    Gregorian2Gaurabda(vc,va,e)
    GCUT.msg('Vatime: ' + str(va))

    va.prevMasa()
    va.tithi = 0
    vc2 = GCGregorianDate()
    Gaurabda2Gregorian(va,vc2,e)
    GCUT.msg('vctime2:' + str(vc2) + ' --> ' + str(va))
