from .GCGregorianDate import GCGregorianDate,Today
from .GCTime import GCTime
from . import GCLocation as GCLocation
from . import GCPancangaDate as GCPancangaDate
from . import GCEarthData as GCEarthData
from . import GCTithi as GCTithi
from .GCPancangaDate import GCGaurabdaDate
from .GCMoonData import MOONDATA
from .GCSunData import GetSunLongitude, SUNDATA
from .GCDayData import GCDayData, GetFirstDayOfYear, gGaurBeg
from . import GCMath as GCMath
from . import GCStrings as GCStrings
from math import floor
from . import GCUT as GCUT


def TITHI_EKADASI(a):
	return a in [10,25]

def TITHI_DVADASI(a):
	return a in [11,26]

def TITHI_TRAYODASI(a):
	return a in [12,27]

def TITHI_CATURDASI(a):
    return a in [13,28]

def TITHI_LESS_EKADASI(a):
    return a in [9,24,8,23]

def TITHI_LESS_DVADASI(a):
    return a in [10,25,9,24]

def TITHI_LESS_TRAYODASI(a):
    return a in [11,26,10,25]

def TITHI_FULLNEW_MOON(a):
    return a in [14,29]

def PREV_PREV_TITHI(a):
    return (a + 28) % 30

def PREV_TITHI(a):
    return (a + 29) % 30

def NEXT_TITHI(a):
    return (a + 1) % 30

def NEXT_NEXT_TITHI(a):
    return (a + 2) % 30

def TITHI_LESS_THAN(a,b):
    return a == PREV_TITHI(b) or a == PREV_PREV_TITHI(b)

def TITHI_GREAT_THAN(a,b):
    return a == NEXT_TITHI(b) or a == NEXT_NEXT_TITHI(b)

# TRUE when transit from A to B is between T and U
def TITHI_TRANSIT(t,u,a,b):
    return ((t==a) and (u==b)) or ((t==a) and (u==NEXT_TITHI(b))) or ((t==PREV_TITHI(a)) and (u == b))

#********************************************************************/
#                                                                   */
#   finds next time when starts next tithi                          */
#                                                                   */
#   timezone is not changed                                         */
#                                                                   */
#   return value: index of tithi 0..29                              */
#                 or -1 if failed                                   */
#********************************************************************/

def GetNextTithiStart(ed, startDate, nextDate, forward=True):
    phi = 12.0
    jday = startDate.GetJulianComplete()
    moon = MOONDATA()
    d = GCGregorianDate(date = startDate)
    xd = GCGregorianDate()
    dir = 1.0 if forward else -1.0
    scan_step = 0.5*dir
    prev_tit = 0
    new_tit = -1

    moon.Calculate(jday, ed)
    sunl = GetSunLongitude(d)
    l1 = GCMath.putIn360(moon.longitude_deg - sunl - 180.0)
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
        l2 = GCMath.putIn360(moon.longitude_deg - sunl - 180.0)
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


#********************************************************************/
#                                                                   */
#   finds previous time when starts next tithi                      */
#                                                                   */
#   timezone is not changed                                         */
#                                                                   */
#   return value: index of tithi 0..29                              */
#                 or -1 if failed                                   */
#********************************************************************/

def GetPrevTithiStart(ed, startDate, nextDate):
    return GetNextTithiStart(ed,startDate,nextDate,forward=False)


def GetTithiTimes(ed, vc, sunRise):
    d1 = GCGregorianDate()
    d2 = GCGregorianDate()

    vc.shour = sunRise
    GetPrevTithiStart(ed, vc, d1)
    GetNextTithiStart(ed, vc, d2)

    titBeg = d1.shour + d1.GetJulian() - vc.GetJulian()
    titEnd = d2.shour + d2.GetJulian() - vc.GetJulian()

    return titEnd - titBeg,titBeg,titEnd


#********************************************************************/
# Finds starting and ending time for given tithi                    */
#                                                                   */
# tithi is specified by Gaurabda year, masa, paksa and tithi number */
#      nGYear - 0..9999                                             */
#       nMasa - 0..12, 0-Madhusudana, 1-Trivikrama, 2-Vamana        */
#                      3-Sridhara, 4-Hrsikesa, 5-Padmanabha         */
#                      6-Damodara, 7-Kesava, 8-narayana, 9-Madhava  */
#                      10-Govinda, 11-Visnu, 12-PurusottamaAdhika   */
#       nPaksa -       0-Krsna, 1-Gaura                             */
#       nTithi - 0..14                                              */
#       earth  - used timezone                                      */
#                                                                   */
#********************************************************************/

def CalcTithiEnd(nGYear, nMasa, nPaksa, nTithi, earth, endTithi):
    d = GCGregorianDate(date = GetFirstDayOfYear(earth, nGYear + 1486))
    d.shour = 0.5
    d.tzone = earth.tzone

    return CalcTithiEndEx(d, nGYear, nMasa, nPaksa, nTithi, earth, endTithi)


def CalcTithiEndEx(vcStart, GYear, nMasa, nPaksa, nTithi, earth, endTithi):
    d = GCGregorianDate()
    dtemp = GCGregorianDate()
    day = GCDayData()
    tithi = 0
    counter = 0
    sunrise = 0.0
    start = GCGregorianDate()
    end = GCGregorianDate()
    start.shour = -1.0
    end.shour = -1.0
    start.day = start.month = start.year = -1
    end.day = end.month = end.year = -1

    d.Set(vcStart)

    i = 0
    while True:
        d.AddDays(13)
        day.DayCalc(d, earth)
        day.nMasa = day.MasaCalc(d, earth)
        gy = day.nGaurabdaYear
        i+=1
        if ((day.nPaksa == nPaksa) and (day.nMasa == nMasa)) or i > 30:
            break

    if i > 30:
        d.year = d.month = d.day = -1
        return d

    # we found masa and paksa
    # now we have to find tithi
    tithi = nTithi + nPaksa*15

    if day.nTithi == tithi:
        # loc1
        # find tithi juncts in this day and according to that times,
        # look in previous or next day for end and start of this tithi
        nType = 1
    else:
        if day.nTithi < tithi:
            # do increment of date until nTithi == tithi
            #   but if nTithi > tithi
            #       then do decrement of date
            counter = 0
            while counter < 30:
                d.NextDay()
                day.DayCalc(d, earth)
                if day.nTithi == tithi:
                    break
                if (day.nTithi < tithi ) and (day.nPaksa != nPaksa):
                    d.PreviousDay()
                    break
                if day.nTithi > tithi:
                    d.PreviousDay()
                    break
                counter+=1
            # somewhere is error
            if counter>=30:
                d.year = d.month = d.day = 0
                nType = 0
        else:
            # do decrement of date until nTithi <= tithi
            counter = 0
            while counter < 30:
                d.PreviousDay()
                day.DayCalc(d, earth)
                if day.nTithi == tithi:
                    break
                if (day.nTithi > tithi ) and (day.nPaksa != nPaksa):
                    break
                if day.nTithi < tithi:
                    break
                counter+=1
            # somewhere is error
            if counter >= 30:
                d.year = d.month = d.day = 0
                nType = 0

        if day.nTithi == tithi:
            # do the same as in loc1
            nType = 1
        else:
            # nTithi != tithi and nTithi < tithi
            # but on next day is nTithi > tithi
            # that means we will find start and the end of tithi
            # in this very day or on next day before sunrise
            nType = 2

    # now we know the type of day-accurancy
    # nType = 0 means, that we dont found a day
    # nType = 1 means, we find day, when tithi was present at sunrise
    # nType = 2 means, we found day, when tithi started after sunrise
    #                  but ended before next sunrise
    #
    sunrise = day.sun.sunrise_deg / 360 + earth.tzone/24

    if nType == 1:
        d1 = GCGregorianDate()
        d2 = GCGregorianDate()
        d.shour = sunrise
        GCTithi.GetPrevTithiStart(earth, d, d1)
        #d = d1
        #d.shour += 0.02
        GCTithi.GetNextTithiStart(earth, d, d2)

        endTithi.Set(d2)
        return d1
    elif nType == 2:
        d1 = GCGregorianDate()
        d2 = GCGregorianDate()
        d.shour = sunrise
        GCTithi.GetNextTithiStart(earth, d, d1)
        d.Set(d1)
        d.shour += 0.1
        d.NormalizeValues()
        GCTithi.GetNextTithiStart(earth, d, d2)

        endTithi.Set(d2)
        return d1

    # if nType == 0, then this algoritmus has some failure
    if nType == 0:
        d.year = 0
        d.month = 0
        d.day = 0
        d.shour = 0.0
        endTithi.Set(d)
    else:
        d.Set(start)
        endTithi.Set(end)

    return d

#********************************************************************/
#  Calculates Date of given Tithi                                   */
#********************************************************************/

def CalcTithiDate(nGYear, nMasa, nPaksa, nTithi, earth):
    i = 0
    gy = 0
    d = GCGregorianDate()
    dtemp = GCGregorianDate()
    day = GCDayData()
    tithi = 0
    counter = 0
    tmp = 0

    if nGYear >= 464 and nGYear < 572:
        tmp = gGaurBeg[(nGYear-464)*26 + nMasa*2 + nPaksa]
        d.month = (tmp & 0x3e0) >> 5
        d.day   = (tmp & 0x1f)
        d.year  = (tmp & 0xfffc00) >> 10
        d.tzone = earth.tzone
        d.NextDay()

        day.DayCalc(d, earth)
        day.nMasa = day.MasaCalc(d, earth)
        gy = day.nGaurabdaYear
    else:
        #d = GetFirstDayOfYear(earth, nGYear + 1486)
        d.day = 15
        d.month = 2 + nMasa
        d.year = nGYear + 1486
        if d.month > 12:
            d.month -= 12
            d.year+=1
        d.shour = 0.5
        d.tzone = earth.tzone

        i = 0
        while True:
            d.AddDays(13)
            day.DayCalc(d, earth)
            day.nMasa = day.MasaCalc(d, earth)
            gy = day.nGaurabdaYear
            i+=1
            if i>=30: break
            if (day.nPaksa == nPaksa) and (day.nMasa == nMasa): break

    if i >= 30:
        d.year = d.month = d.day = -1
        return d

    # we found masa and paksa
    # now we have to find tithi
    tithi = nTithi + nPaksa*15

    if day.nTithi == tithi:
        # loc1
        # find tithi juncts in this day and according to that times,
        # look in previous or next day for end and start of this tithi
        d.PreviousDay()
        day.DayCalc(d, earth)
        if (day.nTithi > tithi ) and (day.nPaksa != nPaksa):
            d.NextDay()
        return d

    if day.nTithi < tithi:
        # do increment of date until nTithi == tithi
        #   but if nTithi > tithi
        #       then do decrement of date
        counter = 0
        while counter < 16:
            d.NextDay()
            day.DayCalc(d, earth)
            if day.nTithi == tithi:
                return d
            if (day.nTithi < tithi ) and (day.nPaksa != nPaksa):
                return d
            if day.nTithi > tithi:
                return d
            counter+=1
        # somewhere is error
        d.year = d.month = d.day = 0
        return d
    else:
        # do decrement of date until nTithi <= tithi
        counter = 0
        while counter < 16:
            d.PreviousDay()
            day.DayCalc(d, earth)
            if day.nTithi == tithi:
                return d
            if (day.nTithi > tithi ) and (day.nPaksa != nPaksa):
                d.NextDay()
                return d
            if day.nTithi < tithi:
                d.NextDay()
                return d
            counter+=1
        # somewhere is error
        d.year = d.month = d.day = 0
        return d

    # now we know the type of day-accurancy
    # nType = 0 means, that we dont found a day
    # nType = 1 means, we find day, when tithi was present at sunrise
    # nType = 2 means, we found day, when tithi started after sunrise
    #                  but ended before next sunrise
    #

    return d

def writeXml(xml,loc,vc):
    date = GCGregorianDate()
    xml.write("<xml>\n")
    xml.write("\t<request name=\"Tithi\" version=\"")
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
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"Tithi\">\n")

    d1 = GCGregorianDate()
    d2 = GCGregorianDate()
    dn = GCGregorianDate()
    dt = GCTime()
    earth = loc.GetEarthData()

    day = GCDayData()
    day.DayCalc(vc, earth)

    d = GCGregorianDate(date = vc)
    d.tzone = loc.m_fTimezone
    d.shour = day.sun.sunrise_deg/360.0 + loc.m_fTimezone/24.0

    GCTithi.GetPrevTithiStart(earth, d, d1)
    GCTithi.GetNextTithiStart(earth, d, d2)

    dt.SetDegTime( d1.shour * 360 )
    # start tithi at t[0]
    xml.write("\t\t<tithi\n\t\t\tid=\"")
    xml.write(str(day.nTithi))
    xml.write("\"\n")
    xml.write("\t\t\tname=\"")
    xml.write(GCStrings.GetTithiName(day.nTithi))
    xml.write("\"\n")
    xml.write("\t\t\tstartdate=\"")
    xml.write(str(d1))
    xml.write("\"\n")
    xml.write("\t\t\tstarttime=\"")
    xml.write(repr(dt))
    xml.write("\"\n")

    dt.SetDegTime( d2.shour * 360 )
    xml.write("\t\t\tenddate=\"")
    xml.write(str(d2))
    xml.write("\"\n")
    xml.write("\t\t\tendtime=\"")
    xml.write(repr(dt))
    xml.write("\"\n />")

    xml.write("\t</result>\n")
    xml.write("</xml>\n")

    return 1



def writeGaurabdaTithiXml(xml,loc,vaStart,vaEnd):
    gyearA = vaStart.gyear
    gyearB = vaEnd.gyear
    gmasa = vaStart.masa
    gpaksa = 1 if vaStart.tithi >= 15 else 0
    gtithi = vaStart.tithi % 15

    if gyearB < gyearA:
        gyearB = gyearA

    xml.write("<xml>\n")
    xml.write("\t<request name=\"Tithi\" version=\"")
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
    if gyearA > 1500:
        xml.write("\t\t<arg name=\"year-start\" val=\"")
        xml.write(str(gyearA))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"year-end\" val=\"")
        xml.write(str(gyearB))
        xml.write("\" />\n")
    else:
        xml.write("\t\t<arg name=\"gaurabdayear-start\" val=\"")
        xml.write(str(gyearA))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"gaurabdayear-end\" val=\"")
        xml.write(str(gyearB))
        xml.write("\" />\n")
    xml.write("\t\t<arg name=\"masa\" val=\"")
    xml.write(str(gmasa))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"paksa\" val=\"")
    xml.write(str(gpaksa))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"tithi\" val=\"")
    xml.write(str(gtithi))
    xml.write("\" />\n")
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"Tithi\">\n")


    earth = loc.GetEarthData()
    vcs = GCGregorianDate()
    vce = GCGregorianDate()
    today = GCGregorianDate()
    sun = SUNDATA()
    day = GCDayData()
    A = B = 0

    if gyearA > 1500:
        A = gyearA - 1487
        B = gyearB - 1485
    else:
        A = gyearA
        B = gyearB

    for A in range(A,B+1):
        vcs.Set(GCTithi.CalcTithiEnd(A, gmasa, gpaksa, gtithi, earth, vce))
        if gyearA > 1500:
            if (vcs.year < gyearA) or (vcs.year > gyearB):
                continue
        oTithi = gpaksa*15 + gtithi
        oMasa = gmasa
        oPaksa = gpaksa
        oYear = 0
        xml.write("\t<celebration\n")
        xml.write("\t\trtithi=\"")
        xml.write(GCStrings.GetTithiName(oTithi))
        xml.write("\"\n")
        xml.write("\t\trmasa=\"")
        xml.write(GCStrings.GetMasaName(oMasa))
        xml.write("\"\n")
        xml.write("\t\trpaksa=\"")
        xml.write('Gaura' if oPaksa else "Krsna")
        xml.write("\"\n")
        # test ci je ksaya
        today.Set(vcs)
        today.shour = 0.5
        sun.SunCalc(today, earth)
        sunrise = (sun.sunrise_deg + loc.m_fTimezone*15.0)/360
        if sunrise < vcs.shour:
            today.Set(vce)
            sun.SunCalc(today, earth)
            sunrise = (sun.sunrise_deg + loc.m_fTimezone*15.0)/360
            if sunrise < vce.shour:
                # normal type
                vcs.NextDay()
                xml.write("\t\ttype=\"normal\"\n")
            else:
                # ksaya
                vcs.NextDay()
                day.DayCalc(vcs, earth)
                oTithi = day.nTithi
                oPaksa = day.nPaksa
                oMasa = day.MasaCalc(vcs, earth)
                oYear = day.nGaurabdaYear
                xml.write("\t\ttype=\"ksaya\"\n")
        else:
            # normal, alebo prvy den vriddhi
            today.Set(vce)
            sun.SunCalc(today, earth)
            if (sun.sunrise_deg + loc.m_fTimezone*15.0)/360 < vce.shour:
                # first day of vriddhi type
                xml.write("\t\ttype=\"vriddhi\"\n")
            else:
                # normal
                xml.write("\t\ttype=\"normal\"\n")
        xml.write("\t\tdate=\"")
        xml.write(str(vcs))
        xml.write("\"\n")
        xml.write("\t\totithi=\"")
        xml.write(GCStrings.GetTithiName(oTithi))
        xml.write("\"\n")
        xml.write("\t\tomasa=\"")
        xml.write(GCStrings.GetMasaName(oMasa))
        xml.write("\"\n")
        xml.write("\t\topaksa=\"")
        xml.write('Gaura' if oPaksa else 'Krsna')
        xml.write("\"\n")
        xml.write("\t/>\n")

    xml.write("\t</result>\n")
    xml.write("</xml>\n")
    return 1

def writeGaurabdaNextTithiXml(xml,loc,vcStart,vaStart):
    gmasa = vaStart.masa
    gpaksa = 1 if vaStart.tithi >= 15 else 0
    gtithi = vaStart.tithi % 15

    xml.write("<xml>\n")
    xml.write("\t<request name=\"Tithi\" version=\"")
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
    xml.write("\t\t<arg name=\"start date\" val=\"")
    xml.write(str(vcStart))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"masa\" val=\"")
    xml.write(str(gmasa))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"paksa\" val=\"")
    xml.write(str(gpaksa))
    xml.write("\" />\n")
    xml.write("\t\t<arg name=\"tithi\" val=\"")
    xml.write(str(gtithi))
    xml.write("\" />\n")
    xml.write("\t</request>\n")
    xml.write("\t<result name=\"Tithi\">\n")

    earth = loc.GetEarthData()
    vcs = GCGregorianDate()
    vce = GCGregorianDate()
    sun = SUNDATA()
    A = 0
    day = GCDayData()

    today = GCGregorianDate(date = vcStart)
    today.PreviousDay()
    vcStart.SubtractDays(15)
    for A in range(0,4):
        vcs.Set(GCTithi.CalcTithiEndEx(vcStart, 0, gmasa, gpaksa, gtithi, earth, vce))
        if not vcs.IsBeforeThis(today):
            oTithi = gpaksa*15 + gtithi
            oMasa = gmasa
            oPaksa = gpaksa
            oYear = 0
            xml.write("\t<celebration\n")
            xml.write("\t\trtithi=\"")
            xml.write(GCStrings.GetTithiName(oTithi))
            xml.write("\"\n")
            xml.write("\t\trmasa=\"")
            xml.write(GCStrings.GetMasaName(oMasa))
            xml.write("\"\n")
            xml.write("\t\trpaksa=\"")
            xml.write("Gaura" if oPaksa else "Krsna")
            xml.write("\"\n")
            # test ci je ksaya
            today.Set(vcs)
            today.shour = 0.5
            sun.SunCalc(today, earth)
            sunrise = (sun.sunrise_deg + loc.m_fTimezone*15.0)/360
            if sunrise < vcs.shour:
                today.Set(vce)
                sun.SunCalc(today, earth)
                sunrise = (sun.sunrise_deg + loc.m_fTimezone*15.0)/360
                if sunrise < vce.shour:
                    # normal type
                    vcs.NextDay()
                    xml.write("\t\ttype=\"normal\"\n")
                else:
                    # ksaya
                    vcs.NextDay()
                    day.DayCalc(vcs, earth)
                    oTithi = day.nTithi
                    oPaksa = day.nPaksa
                    oMasa = day.MasaCalc(vcs, earth)
                    oYear = day.nGaurabdaYear
                    xml.write("\t\ttype=\"ksaya\"\n")
            else:
                # normal, alebo prvy den vriddhi
                today.Set(vce)
                sun.SunCalc(today, earth)
                if (sun.sunrise_deg + loc.m_fTimezone*15.0)/360 < vce.shour:
                    # first day of vriddhi type
                    xml.write("\t\ttype=\"vriddhi\"\n")
                else:
                    # normal
                    xml.write("\t\ttype=\"normal\"\n")
            xml.write("\t\tdate=\"")
            xml.write(str(vcs))
            xml.write("\"\n")
            xml.write("\t\totithi=\"")
            xml.write(GCStrings.GetTithiName(oTithi))
            xml.write("\"\n")
            xml.write("\t\tomasa=\"")
            xml.write(GCStrings.GetMasaName(oMasa))
            xml.write("\"\n")
            xml.write("\t\topaksa=\"")
            xml.write("Gaura" if oPaksa else "Krsna")
            xml.write("\"\n")
            xml.write("\t/>\n")
            break
        else:
            vcStart.Set(vcs)
            vcs.NextDay()

    xml.write("\t</result>\n")
    xml.write("</xml>\n")
    return 1

# Finds first day of given masa and gaurabda year
def GetFirstDayOfMasa(earth,GYear,nMasa):
    return CalcTithiDate(GYear, nMasa, 0, 0, earth)


def unittests():
    GCUT.info('gc tithi')
    e = GCEarthData.EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = Today()
    vc2 = GCGregorianDate()
    vc3 = GCGregorianDate(date = vc)
    vc3.NextDay()

    if False:
        import io
        s = io.StringIO()
        clr = GCLocation.GCLocation()
        writeXml(s, clr, vc)
        GCUT.msg(s.getvalue())
        s.seek(0)
        writeGaurabdaTithiXml(s,clr,GCGaurabdaDate(2,1,512),GCGaurabdaDate(20,1,514))
        GCUT.msg('writeGaurabdaTithiXml')
        GCUT.msg(s.getvalue())

        s = io.StringIO()
        writeGaurabdaNextTithiXml(s,clr,vc,GCGaurabdaDate(2,1,512))
        GCUT.msg('writeGaurabdaNextTithiXml')
        GCUT.msg(s.getvalue())

    print(GetTithiTimes(e,vc,0.25))
