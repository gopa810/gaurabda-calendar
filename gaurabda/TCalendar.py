from .GCLocation import GCLocation
from .GCCalendarDay import GCCalendarDay
from .GCGregorianDate import GCGregorianDate,Today
from .GCEarthData import EARTHDATA
from .GCEnums.MahadvadasiType import *
from .GCEnums.FastType import *
from .GCEnums.FeastType import *
from .GCEnums.SpecialFestivalId import *
from .GCEnums.GCDS import *
from .GCEnums.DisplayPriorities import *
from .GCEnums.MasaId import *
from .GCEnums.TithiId import *
from .GCEnums.EkadasiParanaType import *
from .GCEnums.CaturmasyaCodes import *
from .GCEnums.NaksatraId import *
from .GCEnums.PaksaId import *
from .GCEnums.SankrantiId import *
from .GCMoonData import MOONDATA,CalcMoonTimes
from .GCStringBuilder import GCStringBuilder,SBTF_TEXT,SBTF_RTF

from . import GCMath
from . import GCEvent
from . import GCStrings
from . import GCTithi
from . import GCNaksatra
from . import GCSankranti
from . import GCDisplaySettings
from . import GCTimeZone
from . import GCAyanamsha
from . import GCEventList
from . import GCLayoutData
from . import GCGlobal
from . import GCUT

from math import modf,floor
from io import StringIO
import datetime
import json

CDB_MAXDAYS = 16
BEFORE_DAYS = 8

class TCalendar:
    def __init__(self):
        self.m_data = []
        self.m_nCount = 0
        self.m_PureCount = 0
        self.m_Location = None
        self.m_vcStart = None
        self.m_vcCount = 0
        self.nBeg = 0
        self.nTop = 0
        self.top = 0
        self.days = [None] * CDB_MAXDAYS

    def __dict__(self):
        days = [dict(v) for v in self.days_iter()]
        return {
            'location': dict(self.m_Location),
            'start': dict(self.m_vcStart),
            'count': self.m_vcCount,
            'days': days
        }

    def __iter__(self):
        yield 'location', dict(self.m_Location)
        yield 'start', dict(self.m_vcStart)
        yield 'count', self.m_vcCount
        yield 'days', [dict(v) for v in self.days_iter()]

    def days_iter(self):
        for v in range(BEFORE_DAYS,self.m_vcCount+BEFORE_DAYS):
            if self.m_data[v] != None:
                yield self.m_data[v]

    def DAYS_TO_ENDWEEK(self,lastMonthDay):
        return (21-(lastMonthDay - GCDisplaySettings.getValue(GENERAL_FIRST_DOW)))%7

    def DAYS_FROM_BEGINWEEK(self,firstMonthDay):
        return (firstMonthDay-GCDisplaySettings.getValue(GENERAL_FIRST_DOW)+14)%7

    def DAY_INDEX(self,day):
        return (day + GCDisplaySettings.getValue(GENERAL_FIRST_DOW))%7

    def NextNewFullIsVriddhi(self,nIndex,earth):
        i = 0
        nPrevTithi = 100

        for i in range(BEFORE_DAYS):
            if nIndex>=len(self.m_data): return False
            nTithi = self.m_data[nIndex].astrodata.nTithi
            if (nTithi == nPrevTithi) and GCTithi.TITHI_FULLNEW_MOON(nTithi):
                return True
            nPrevTithi = nTithi
            nIndex+=1

        return False

    def IsMhd58(self, nIndex):
        t = self.m_data[nIndex]
        u = self.m_data[nIndex + 1]

        if t.astrodata.nNaksatra != u.astrodata.nNaksatra:
            return EV_NULL

        if t.astrodata.nPaksa != 1:
            return EV_NULL

        if t.astrodata.nTithi == t.astrodata.nTithiSunset:
            if t.astrodata.nNaksatra == 6: # punarvasu
                return EV_JAYA
            elif t.astrodata.nNaksatra == 3: # rohini
                return EV_JAYANTI
            elif t.astrodata.nNaksatra == 7: # pusyami
                return EV_PAPA_NASINI
            elif t.astrodata.nNaksatra == 21: # sravana
                return EV_VIJAYA
            else:
                return EV_NULL
        else:
            if t.astrodata.nNaksatra == 21: # sravana
                return EV_VIJAYA
        return EV_NULL

    def CalculateCalendar(self, loc, begDate, iCount):
        nTotalCount = iCount + 2 * BEFORE_DAYS
        date = GCGregorianDate()
        prev_paksa = 0
        lastMasa = 0
        lastGYear = 0
        bCalcMoon = GCDisplaySettings.getValue(4) > 0 or GCDisplaySettings.getValue(5) > 0
        bCalcMasa = [ True, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True ]

        self.m_Location = loc.copy()
        self.m_vcStart = begDate.copy()
        self.m_vcCount = iCount
        earth = loc.GetEarthData()

        self.m_data = [GCCalendarDay() for i in range(nTotalCount)]

        self.m_nCount = nTotalCount
        self.m_PureCount = iCount

        date = begDate.copy()
        date.shour = 0.0
        date.tzone = loc.m_fTimezone
        date.InitWeekDay()
        date.AddDays(-BEFORE_DAYS)

        # initialization of days
        for i,mp in enumerate(self.m_data):
            mp.date.Set(date)
            date.NextDay()
            mp.moonrise.SetValue(-1)
            mp.moonset.SetValue(-1)

        # calculating moon times
        for mp in self.m_data:
            mp.hasDST = GCTimeZone.determineDaylightStatus(mp.date, loc.m_nTimezoneId)

        if bCalcMoon:
            for mp in self.m_data:
                CalcMoonTimes(earth, mp.date, double(mp.hasDST), mp.moonrise, mp.moonset)

                if GCDisplaySettings.getValue(CAL_MOON_RISE) and mp.moonrise.hour >= 0:
                    mp.AddEvent(PRIO_MOON, CAL_MOON_RISE, "{} {}:{:02d} ({})".format(GCStrings.getString(53), mp.moonrise.hour , mp.moonrise.min, GCStrings.GetDSTSignature(mp.hasDST)))

                if GCDisplaySettings.getValue(GCDS.CAL_MOON_SET) and mp.moonset.hour >= 0:
                    mp.AddEvent(PRIO_MOON, CAL_MOON_SET, "{} {}:{:02d} ({})".format(GCStrings.getString(54), mp.moonset.hour
                        , mp.moonset.min, GCStrings.GetDSTSignature(mp.hasDST)))

        # init of astro data
        for mp in self.m_data:
            mp.astrodata.DayCalc(mp.date, earth)

        calc_masa = False

        # 5
        # init of masa
        prev_paksa = -1
        for i,mp in enumerate(self.m_data):
            calc_masa = (mp.astrodata.nPaksa != prev_paksa)
            prev_paksa = mp.astrodata.nPaksa

            if i == 0: calc_masa = True

            if calc_masa:
                mp.astrodata.MasaCalc(mp.date, earth)
                lastMasa = mp.astrodata.nMasa
                lastGYear = mp.astrodata.nGaurabdaYear
            mp.astrodata.nMasa = lastMasa
            mp.astrodata.nGaurabdaYear = lastGYear

            if (GCDisplaySettings.getValue(CAL_ARUN_TITHI)):
                mp.AddEvent(PRIO_ARUN, CAL_ARUN_TITHI, "{}: {}".format(GCStrings.getString(98), GCStrings.GetTithiName(mp.astrodata.nTithiArunodaya)))

            if (GCDisplaySettings.getValue(CAL_ARUN_TIME)):
                mp.AddEvent(PRIO_ARUN, CAL_ARUN_TIME, "{} {}:{:02d} ({})".format(GCStrings.getString(99), mp.astrodata.sun.arunodaya.hour , mp.astrodata.sun.arunodaya.min, GCStrings.GetDSTSignature(mp.hasDST)))

            if (GCDisplaySettings.getValue(CAL_SUN_RISE)):
                mp.AddEvent(PRIO_SUN, CAL_SUN_RISE, "{} {}:{:02d} ({})".format(GCStrings.getString(51), mp.astrodata.sun.rise.hour , mp.astrodata.sun.rise.min, GCStrings.GetDSTSignature(mp.hasDST)))

            if (GCDisplaySettings.getValue(CAL_SUN_NOON)):
                mp.AddEvent(PRIO_SUN, CAL_SUN_NOON, "{} {}:{:02d} ({})".format(GCStrings.getString(857), mp.astrodata.sun.noon.hour , mp.astrodata.sun.noon.min, GCStrings.GetDSTSignature(mp.hasDST)))

            if (GCDisplaySettings.getValue(CAL_SUN_SET)):
                mp.AddEvent(PRIO_SUN, CAL_SUN_SET, "{} {}:{:02d} ({})".format(GCStrings.getString(52), mp.astrodata.sun.set.hour , mp.astrodata.sun.set.min, GCStrings.GetDSTSignature(mp.hasDST)))

            if (GCDisplaySettings.getValue(CAL_SUN_LONG)):
                mp.AddEvent(PRIO_ASTRO, CAL_SUN_LONG, "{}: {} (*)".format(GCStrings.getString(100), mp.astrodata.sun.longitude_deg))

            if (GCDisplaySettings.getValue(CAL_MOON_LONG)):
                mp.AddEvent(PRIO_ASTRO, CAL_MOON_LONG, "{}: {} (*)".format(GCStrings.getString(101), mp.astrodata.moon.longitude_deg))

            if (GCDisplaySettings.getValue(CAL_AYANAMSHA)):
                mp.AddEvent(PRIO_ASTRO, CAL_AYANAMSHA, "{} {} ({}) (*)".format(GCStrings.getString(102), mp.astrodata.msAyanamsa, GCAyanamsha.GetAyanamsaName(GCAyanamsha.GetAyanamsaType())))

            if (GCDisplaySettings.getValue(CAL_JULIAN)):
                mp.AddEvent(PRIO_ASTRO, CAL_JULIAN, "{} {} (*)".format(GCStrings.getString(103), mp.astrodata.jdate))


        if GCDisplaySettings.getValue(CAL_MASA_CHANGE):
            for i in range(BEFORE_DAYS, self.m_PureCount + BEFORE_DAYS + 2):
                if (self.m_data[i-1].astrodata.nMasa != self.m_data[i].astrodata.nMasa):
                    self.m_data[i].AddEvent(PRIO_MASA_CHANGE, CAL_MASA_CHANGE, "{} {} {}".format(GCStrings.getString(780), GCStrings.GetMasaName(self.m_data[i].astrodata.nMasa), GCStrings.getString(22)))

                if (self.m_data[i+1].astrodata.nMasa != self.m_data[i].astrodata.nMasa):
                    self.m_data[i].AddEvent(PRIO_MASA_CHANGE, CAL_MASA_CHANGE, "{} {} {}".format(GCStrings.getString(781), GCStrings.GetMasaName(self.m_data[i].astrodata.nMasa), GCStrings.getString(22)))


        if GCDisplaySettings.getValue(CAL_DST_CHANGE):
            for i in range(BEFORE_DAYS, self.m_PureCount + BEFORE_DAYS + 2):
                if (self.m_data[i-1].hasDST == 0 and self.m_data[i].hasDST==1):
                    self.m_data[i].AddEvent(PRIO_DST_CHANGE, CAL_DST_CHANGE, GCStrings.getString(855))
                elif (self.m_data[i].hasDST==1 and self.m_data[i+1].hasDST==0):
                    self.m_data[i].AddEvent(PRIO_DST_CHANGE, CAL_DST_CHANGE, GCStrings.getString(856))

        # init of mahadvadasis
        for i in range(2,self.m_PureCount + BEFORE_DAYS + 3):
            self.m_data[i].Clear()
            self.MahadvadasiCalc(i, earth)

        # init for Ekadasis
        for i in range(3,self.m_PureCount + BEFORE_DAYS + 3):
            self.EkadasiCalc(i, earth)

        # init of festivals
        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS + 3):
            self.CompleteCalc(i, earth)

        # init of festivals
        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS):
            self.ExtendedCalc(i, earth)

        # resolve festivals fasting
        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS):
            if self.m_data[i].eparana_time1 > 0.0:
                self.m_data[i].eparana_time1 += self.m_data[i].hasDST

            if self.m_data[i].eparana_time2 > 0.0:
                self.m_data[i].eparana_time2 += self.m_data[i].hasDST

            if self.m_data[i].astrodata.sun.longitude_deg > 0.0:
                self.m_data[i].astrodata.sun.rise.hour += self.m_data[i].hasDST
                self.m_data[i].astrodata.sun.set.hour += self.m_data[i].hasDST
                self.m_data[i].astrodata.sun.noon.hour += self.m_data[i].hasDST
                self.m_data[i].astrodata.sun.arunodaya.hour += self.m_data[i].hasDST

            self.ResolveFestivalsFasting(i)

        # init for sankranti
        date.Set(self.m_data[0].date)
        i = 0
        bFoundSan = True
        zodiac = 0
        i_target = 0
        while bFoundSan:
            sd,zodiac = GCSankranti.GetNextSankranti(date)
            date.Set(sd)
            date.shour += GCTimeZone.determineDaylightStatus(date, loc.m_nTimezoneId)/24.0
            date.NormalizeValues()

            bFoundSan = False
            for i in range(self.m_nCount-1):
                i_target = -1
                if GCSankranti.GetSankrantiType() == 0:
                    if date.CompareYMD(self.m_data[i].date) == 0:
                        i_target = i
                    break
                if GCSankranti.GetSankrantiType() == 1:
                    if (date.CompareYMD(self.m_data[i].date) == 0):
                        if (date.shour < self.m_data[i].astrodata.sun.rise.GetDayTime()):
                            i_target = i - 1
                        else:
                            i_target = i
                    break
                if GCSankranti.GetSankrantiType() == 2:
                    if (date.CompareYMD(self.m_data[i].date) == 0):
                        if (date.shour > self.m_data[i].astrodata.sun.noon.GetDayTime()):
                            i_target = i+1
                        else:
                            i_target = i
                    break
                if GCSankranti.GetSankrantiType() == 3:
                    if (date.CompareYMD(self.m_data[i].date) == 0):
                        if (date.shour > self.m_data[i].astrodata.sun.set.GetDayTime()):
                            i_target = i+1
                        else:
                            i_target = i
                    break

                if i_target >= 0:
                    self.m_data[i_target].sankranti_zodiac = zodiac
                    self.m_data[i_target].sankranti_day.Set(date)

                    if GCDisplaySettings.getValue(CAL_SANKRANTI):
                        " {} {} ({} {} {} {} {}, {:02d}:{:02d} {}) ".format( GCStrings.GetSankrantiName(self.m_data[i_target].sankranti_zodiac) , GCStrings.getString(56) , GCStrings.getString(111), GCStrings.GetSankrantiNameEn(self.m_data[i_target].sankranti_zodiac) , GCStrings.getString(852) , self.m_data[i_target].sankranti_day.day, GCStrings.GetMonthAbreviation(self.m_data[i_target].sankranti_day.month) , self.m_data[i_target].sankranti_day.GetHour(), self.m_data[i_target].sankranti_day.GetMinuteRound() , GCStrings.GetDSTSignature(self.m_data[i_target].hasDST))

                        dc = self.m_data[i_target].AddEvent(PRIO_SANKRANTI, CAL_SANKRANTI, str)
                        dc['spec'] = "sankranti"
                    bFoundSan = True
                    break
            date.NextDay()
            date.NextDay()

        # init for festivals dependent on sankranti
        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS):
            if (self.m_data[i].sankranti_zodiac == MAKARA_SANKRANTI):
                self.m_data[i].AddEvent(PRIO_FESTIVALS_5, CAL_FEST_5, GCStrings.getString(78))
            elif (self.m_data[i].sankranti_zodiac == MESHA_SANKRANTI):
                self.m_data[i].AddEvent(PRIO_FESTIVALS_5, CAL_FEST_5, GCStrings.getString(79))
            elif (self.m_data[i+1].sankranti_zodiac == VRSABHA_SANKRANTI):
                self.m_data[i].AddEvent(PRIO_FESTIVALS_5, CAL_FEST_5, GCStrings.getString(80))

        # init ksaya data
        # init of second day of vriddhi
        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS):
            if self.m_data[i].astrodata.nTithi == self.m_data[i-1].astrodata.nTithi:
                if (GCDisplaySettings.getValue(CAL_VRDDHI)):
                    self.m_data[i].AddEvent(PRIO_KSAYA, CAL_VRDDHI, GCStrings.getString(90))
            elif (self.m_data[i].astrodata.nTithi != ((self.m_data[i-1].astrodata.nTithi + 1)%30)):
                d1 = GCGregorianDate()
                d2 = GCGregorianDate()

                day1 = GCGregorianDate(date = self.m_data[i].date)
                day1.shour = self.m_data[i].astrodata.sun.sunrise_deg/360.0 + earth.tzone/24.0

                GCTithi.GetPrevTithiStart(earth, day1, d2)
                day1.Set(d2)
                day1.shour -= 0.1
                day1.NormalizeValues()
                GCTithi.GetPrevTithiStart(earth, day1, d1)

                d1.shour += (self.m_data[i].hasDST/24.0)
                d2.shour += (self.m_data[i].hasDST/24.0)

                d1.NormalizeValues()
                d2.NormalizeValues()

                # zaciatok ksaya tithi
                (m,h) = modf(d1.shour*24)
                str2 = "{} {} {:02d}:{:02d}".format(d1.day, GCStrings.GetMonthAbreviation(d1.month), int(h), int(m*60))

                # end of ksaya tithi
                (m,h) = modf(d2.shour*24)
                str3 = "{} {} {:02d}:{:02d}".format(d2.day, GCStrings.GetMonthAbreviation(d2.month), int(h), int(m*60))

                str4 = "{}: {} -- {} {} {} ({})".format(GCStrings.getString(89), GCStrings.GetTithiName((self.m_data[i].astrodata.nTithi + 29)%30), str2, GCStrings.getString(851), str3, GCStrings.GetDSTSignature(self.m_data[i].hasDST))
                #print(str4, str4.encode('utf-8'))
                self.m_data[i].AddEvent(PRIO_KSAYA, CAL_KSAYA, str4)

        for i in range(BEFORE_DAYS,self.m_PureCount + BEFORE_DAYS):
           self.m_data[i].dayEvents = sorted(self.m_data[i].dayEvents, key=lambda k: k["prio"])

        return 1


    def EkadasiCalc(self, nIndex, earth):
        s = self.m_data[nIndex-1]
        t = self.m_data[nIndex]
        u = self.m_data[nIndex+1]

        if (GCTithi.TITHI_EKADASI(t.astrodata.nTithi)):
            # if TAT < 11 then NOT_EKADASI
            if (GCTithi.TITHI_LESS_EKADASI(t.astrodata.nTithiArunodaya)):
                t.nMhdType = EV_NULL
                t.ekadasi_vrata_name = ''
                t.nFastType = FAST_NULL
            else:
                # else ak MD13 then MHD1 and/or 3
                if (GCTithi.TITHI_EKADASI(s.astrodata.nTithi) and GCTithi.TITHI_EKADASI(s.astrodata.nTithiArunodaya)):
                    if (GCTithi.TITHI_TRAYODASI(u.astrodata.nTithi)):
                        t.nMhdType = EV_UNMILANI_TRISPRSA
                        t.ekadasi_vrata_name = GCStrings.GetEkadasiName(t.astrodata.nMasa, t.astrodata.nPaksa)
                        t.nFastType = FAST_EKADASI
                    else:
                        t.nMhdType = EV_UNMILANI
                        t.ekadasi_vrata_name = GCStrings.GetEkadasiName(t.astrodata.nMasa, t.astrodata.nPaksa)
                        t.nFastType = FAST_EKADASI
                else:
                    if (GCTithi.TITHI_TRAYODASI(u.astrodata.nTithi)):
                        t.nMhdType = EV_TRISPRSA
                        t.ekadasi_vrata_name = GCStrings.GetEkadasiName(t.astrodata.nMasa, t.astrodata.nPaksa)
                        t.nFastType = FAST_EKADASI
                    else:
                        # else ak U je MAHADVADASI then NOT_EKADASI
                        if (GCTithi.TITHI_EKADASI(u.astrodata.nTithi) or (u.nMhdType >= EV_SUDDHA)):
                            t.nMhdType = EV_NULL
                            t.ekadasi_vrata_name = ''
                            t.nFastType = FAST_NULL
                        elif (u.nMhdType == EV_NULL):
                            # else suddha ekadasi
                            t.nMhdType = EV_SUDDHA
                            t.ekadasi_vrata_name = GCStrings.GetEkadasiName(t.astrodata.nMasa, t.astrodata.nPaksa)
                            t.nFastType = FAST_EKADASI
        # test for break fast
        if (s.nFastType == FAST_EKADASI):
            self.CalculateEParana(s, t, earth)
        return 1

    def CheckFestivals(self,s,t,u,v):
        _masa_from = -1
        _masa_to = -1
        _tithi_from = -1
        _tithi_to = -1

        if t.astrodata.nMasa > 11:
            return

        if (s.astrodata.nTithi != t.astrodata.nTithi):
            _tithi_to = t.astrodata.nTithi
            _masa_to  = t.astrodata.nMasa

        # resolving
        if (GCDisplaySettings.getValue(71) == 0):
            # if ksaya tithi, then s2 is true
            if ((t.astrodata.nTithi != s.astrodata.nTithi) and
                (t.astrodata.nTithi != (s.astrodata.nTithi + 1)%30)):
                n2 = (t.astrodata.nMasa * 30 + t.astrodata.nTithi + 359 ) % 360; # this is index into table of festivals for previous tithi
                _tithi_from   = n2 % 30
                _masa_from    = int(floor(n2 / 30))
        else:
            # if ksaya tithi, then s2 is true
            if ((u.astrodata.nTithi != t.astrodata.nTithi) and
                (u.astrodata.nTithi != (t.astrodata.nTithi + 1)%30)):
                n2 = (t.astrodata.nMasa * 30 + t.astrodata.nTithi + 1) % 360; # this is index into table of festivals for previous tithi
                _tithi_from   = n2 % 30
                _masa_from    = int(floor(n2 / 30))

        currFestTop = 0
        eventSelected = 0

        #print('Events list length: ', len(GCEventList.get_list()))
        for kn,pEvx in enumerate(GCEventList.get_list()):
            eventSelected = 0
            if (_masa_from >= 0 and pEvx.nMasa==_masa_from and pEvx.nTithi == _tithi_from and pEvx.nUsed and pEvx.nVisible):
                eventSelected = 1
            elif (_masa_to >= 0 and pEvx.nMasa==_masa_to and pEvx.nTithi==_tithi_to and pEvx.nUsed and pEvx.nVisible):
                eventSelected = 1

            if not eventSelected: continue
            md = t.AddEvent(PRIO_FESTIVALS_0 + pEvx.nClass*100 + currFestTop, CAL_FEST_0 + pEvx.nClass,
                pEvx.strText)
            currFestTop += 5
            if (pEvx.nFastType > 0):
                md["fasttype"] = pEvx.nFastType
                md["fastsubject"] = pEvx.strFastSubject

            if (GCDisplaySettings.getValue(51) != 2 and pEvx.nStartYear > -7000):
                years = t.astrodata.nGaurabdaYear - (pEvx.nStartYear - 1496)
                appx = "th"
                if (years % 10 == 1):
                    appx = "st"
                elif (years % 10 == 2):
                    appx = "nd"
                elif (years % 10 == 3):
                    appx = "rd"
                if (GCDisplaySettings.getValue(51) == 0):
                    md['text'] = "{} ({}{} anniversary)".format(pEvx.strText, years, appx)
                else:
                    md['text'] = "{} ({}{})".format(pEvx.strText, years, appx)


    def CompleteCalc(self, nIndex, earth):
        s = self.m_data[nIndex-1]
        t = self.m_data[nIndex]
        u = self.m_data[nIndex+1]
        v = self.m_data[nIndex+2]

        # test for Govardhan-puja
        if (t.astrodata.nMasa == DAMODARA_MASA):
            if (t.astrodata.nTithi == TITHI_GAURA_PRATIPAT):
                s.moonrise, s.moonset = CalcMoonTimes(earth, u.date, s.hasDST)
                t.moonrise, t.moonset = CalcMoonTimes(earth, t.date, t.hasDST)
                if (s.astrodata.nTithi == TITHI_GAURA_PRATIPAT):
                    pass
                elif (u.astrodata.nTithi == TITHI_GAURA_PRATIPAT):
                    if (t.moonrise.hour >= 0):
                        if (t.moonrise.IsGreaterThan(t.astrodata.sun.rise)):
                        # today is GOVARDHANA PUJA
                            t.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
                        else:
                            u.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
                    elif (u.moonrise.hour >= 0):
                        if (u.moonrise.IsLessThan(u.astrodata.sun.rise)):
                        # today is GOVARDHANA PUJA
                            t.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
                        else:
                            u.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
                    else:
                        t.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
                else:
                    # today is GOVARDHANA PUJA
                    t.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)
            elif ((t.astrodata.nTithi == TITHI_GAURA_DVITIYA) and (s.astrodata.nTithi == TITHI_AMAVASYA)):
                # today is GOVARDHANA PUJA
                t.AddSpecFestival(SPEC_GOVARDHANPUJA, CAL_FEST_1)

        if (t.astrodata.nMasa == HRSIKESA_MASA):
            # test for Janmasthami
            if (self.IsFestivalDay(s, t, TITHI_KRSNA_ASTAMI)):
                # if next day is not astami, so that means that astami is not vriddhi
                # then today is SKJ
                if (u.astrodata.nTithi != TITHI_KRSNA_ASTAMI):
                    # today is Sri Krsna Janmasthami
                    t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                    u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                    u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                else: # tithi is vriddhi and we have to test both days
                    # test when both days have ROHINI
                    if ((t.astrodata.nNaksatra == ROHINI_NAKSATRA) and (u.astrodata.nNaksatra == ROHINI_NAKSATRA)):
                        mid_nak_t = GCNaksatra.CalculateMidnightNaksatra(t.date, earth)
                        mid_nak_u = GCNaksatra.CalculateMidnightNaksatra(u.date, earth)

                        # test when both days have modnight naksatra ROHINI
                        if ((ROHINI_NAKSATRA == mid_nak_u) and (mid_nak_t == ROHINI_NAKSATRA)):
                            # choice day which is monday or wednesday
                            if ((u.date.dayOfWeek == 1) or (u.date.dayOfWeek == 3)):
                                u.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                                v.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                                v.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                            else:
                                # today is Sri Krsna Janmasthami
                                t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                                u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                                u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                        elif (mid_nak_t == ROHINI_NAKSATRA):
                            # today is Sri Krsna Janmasthami
                            t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                            u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                            u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                        elif (mid_nak_u == ROHINI_NAKSATRA):
                            u.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                            v.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                            v.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                        else:
                            if ((u.date.dayOfWeek == 1) or (u.date.dayOfWeek == 3)):
                                u.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                                v.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                                v.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                            else:
                                # today is Sri Krsna Janmasthami
                                t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                                u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                                u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                    elif (t.astrodata.nNaksatra == ROHINI_NAKSATRA):
                        # today is Sri Krsna Janmasthami
                        t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                        u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                        u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                    elif (u.astrodata.nNaksatra == ROHINI_NAKSATRA):
                        u.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                        v.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                        v.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                    else:
                        if ((u.date.dayOfWeek == 1) or (u.date.dayOfWeek == 3)):
                            u.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                            v.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                            v.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)
                        else:
                            # today is Sri Krsna Janmasthami
                            t.AddSpecFestival(SPEC_JANMASTAMI, CAL_FEST_0)
                            u.AddSpecFestival(SPEC_NANDAUTSAVA, CAL_FEST_1)
                            u.AddSpecFestival(SPEC_PRABHAPP, CAL_FEST_2)

        # test for RathaYatra
        if (t.astrodata.nMasa == VAMANA_MASA):
            if (self.IsFestivalDay(s, t, TITHI_GAURA_DVITIYA)):
                t.AddSpecFestival(SPEC_RATHAYATRA, CAL_FEST_1)

            if (nIndex > 4):
                if (self.IsFestivalDay(self.m_data[nIndex - 5], self.m_data[nIndex - 4], TITHI_GAURA_DVITIYA)):
                    t.AddSpecFestival(SPEC_HERAPANCAMI, CAL_FEST_1)

            if (nIndex > 8):
                if (self.IsFestivalDay(self.m_data[nIndex - 9], self.m_data[nIndex - 8], TITHI_GAURA_DVITIYA)):
                    t.AddSpecFestival(SPEC_RETURNRATHA, CAL_FEST_1)

            if (self.IsFestivalDay(self.m_data[nIndex], self.m_data[nIndex + 1], TITHI_GAURA_DVITIYA)):
                t.AddSpecFestival(SPEC_GUNDICAMARJANA, CAL_FEST_1)

        # test for Gaura Purnima
        if (s.astrodata.nMasa == GOVINDA_MASA):
            if (self.IsFestivalDay(s, t, TITHI_PURNIMA)):
                t.AddSpecFestival(SPEC_GAURAPURNIMA, CAL_FEST_0)

        # test for Jagannatha Misra festival
        if (self.m_data[nIndex-2].astrodata.nMasa == GOVINDA_MASA):
            if (self.IsFestivalDay(self.m_data[nIndex - 2], s, TITHI_PURNIMA)):
                t.AddSpecFestival(SPEC_MISRAFESTIVAL, CAL_FEST_1)


        # test for other festivals
        self.CheckFestivals(s,t,u,v)

        # bhisma pancaka test
        if (t.astrodata.nMasa == DAMODARA_MASA):
            if ((t.astrodata.nPaksa == GAURA_PAKSA) and (t.nFastType == FAST_EKADASI)):
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(81))

        # ---------------------------
        # caturmasya tests
        # ---------------------------
        if s.astrodata.nMasa == ADHIKA_MASA:
            if t.astrodata.nMasa == SRIDHARA_MASA:
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(115))
            if (t.astrodata.nMasa == HRSIKESA_MASA):
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(119))
            if (t.astrodata.nMasa == PADMANABHA_MASA):
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(123))
            if (t.astrodata.nMasa == DAMODARA_MASA):
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(127))

        if (GCDisplaySettings.getValue(CATURMASYA_PURNIMA) and GCTithi.TITHI_TRANSIT(t.astrodata.nTithi, u.astrodata.nTithi, TITHI_GAURA_CATURDASI, TITHI_PURNIMA)):
            if t.astrodata.nMasa == VAMANA_MASA:
                u.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(112)))
                u.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PURNIMA, GCStrings.getString(114))
                u.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_FIRST | CMASYA_MONTH_1
            elif t.astrodata.nMasa == SRIDHARA_MASA:
                # first day of particular month for PURNIMA system, when purnima is not KSAYA
                u.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(116)))
                u.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PURNIMA, GCStrings.getString(118))
                u.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_FIRST | CMASYA_MONTH_2
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(113)))
                t.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_LAST | CMASYA_MONTH_1
            elif (t.astrodata.nMasa == HRSIKESA_MASA):
            # first day of particular month for PURNIMA system, when purnima is not KSAYA
                u.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(120)))
                u.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PURNIMA, GCStrings.getString(122))
                u.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_FIRST | CMASYA_MONTH_3
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(117)))
                t.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_LAST | CMASYA_MONTH_2
            elif (t.astrodata.nMasa == PADMANABHA_MASA):
                u.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(124)))
                u.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PURNIMA, GCStrings.getString(126))
                u.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_FIRST | CMASYA_MONTH_4
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(121)))
                t.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_LAST | CMASYA_MONTH_3
            elif (t.astrodata.nMasa == DAMODARA_MASA):
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_PURNIMA, "{} [PURNIMA SYSTEM]".format(GCStrings.getString(125)))
                t.nCaturmasya = CMASYA_SYSTEM_PURNIMA | CMASYA_DAY_LAST | CMASYA_MONTH_4

        # first month for punima and ekadasi systems
        if (GCDisplaySettings.getValue(CATURMASYA_EKADASI) and (t.astrodata.nPaksa == GAURA_PAKSA) and (t.nMhdType != EV_NULL)):
            if (t.astrodata.nMasa == VAMANA_MASA):
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(112)))
                t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_EKADASI, GCStrings.getString(114))
                t.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_FIRST | CMASYA_MONTH_1
            elif t.astrodata.nMasa == SRIDHARA_MASA:
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(116)))
                t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_EKADASI, GCStrings.getString(118))
                t.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_FIRST | CMASYA_MONTH_2
                s.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(113)))
                s.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_LAST | CMASYA_MONTH_1
            elif (t.astrodata.nMasa == HRSIKESA_MASA):
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(120)))
                t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_EKADASI, GCStrings.getString(122))
                t.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_FIRST | CMASYA_MONTH_3
                s.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(117)))
                s.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_LAST | CMASYA_MONTH_2
            elif (t.astrodata.nMasa == PADMANABHA_MASA):
                t.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(124)))
                t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_EKADASI, GCStrings.getString(126))
                t.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_FIRST | CMASYA_MONTH_4
                s.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(121)))
                s.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_LAST | CMASYA_MONTH_3
            elif (t.astrodata.nMasa == DAMODARA_MASA):
                s.AddEvent(PRIO_CM_DAY, CATURMASYA_EKADASI, "{} [EKADASI SYSTEM]".format(GCStrings.getString(125)))
                s.nCaturmasya = CMASYA_SYSTEM_EKADASI | CMASYA_DAY_LAST | CMASYA_MONTH_4

        if GCDisplaySettings.getValue(CATURMASYA_PRATIPAT):
            if GCTithi.TITHI_TRANSIT(s.astrodata.nTithi, t.astrodata.nTithi, TITHI_PURNIMA, TITHI_KRSNA_PRATIPAT):
                if (t.astrodata.nMasa == SRIDHARA_MASA):
                    t.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(112)))
                    t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PRATIPAT, GCStrings.getString(114))
                    t.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_FIRST | CMASYA_MONTH_1
                elif (t.astrodata.nMasa == HRSIKESA_MASA):
                    t.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(116)))
                    t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PRATIPAT, GCStrings.getString(118))
                    t.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_FIRST | CMASYA_MONTH_2
                    s.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(113)))
                    s.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_LAST | CMASYA_MONTH_1
                elif (t.astrodata.nMasa == PADMANABHA_MASA):
                    t.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(120)))
                    t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PRATIPAT, GCStrings.getString(122))
                    t.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_FIRST | CMASYA_MONTH_3
                    s.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(117)))
                    s.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_LAST | CMASYA_MONTH_2
                elif (t.astrodata.nMasa == DAMODARA_MASA):
                    t.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(124)))
                    t.AddEvent(PRIO_CM_DAYNOTE, CATURMASYA_PRATIPAT, GCStrings.getString(126))
                    t.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_FIRST | CMASYA_MONTH_4
                    s.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(121)))
                    s.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_LAST | CMASYA_MONTH_3
            if (GCTithi.TITHI_TRANSIT(t.astrodata.nTithi, u.astrodata.nTithi, TITHI_PURNIMA, TITHI_KRSNA_PRATIPAT)):
                if (t.astrodata.nMasa == DAMODARA_MASA):
                    t.AddEvent(PRIO_CM_DAY, CATURMASYA_PRATIPAT, "{} [PRATIPAT SYSTEM]".format(GCStrings.getString(125)))
                    t.nCaturmasya = CMASYA_SYSTEM_PRATIPAT | CMASYA_DAY_LAST | CMASYA_MONTH_4



        if (t.astrodata.nMasa == DAMODARA_MASA):
            if (GCTithi.TITHI_TRANSIT(t.astrodata.nTithi, u.astrodata.nTithi, TITHI_PURNIMA, TITHI_KRSNA_PRATIPAT)):
                t.AddEvent(PRIO_CM_DAYNOTE, DISP_ALWAYS, GCStrings.getString(82))

        return 1

    def MahadvadasiCalc(self, nIndex, earth):
        nMahaType = 0
        nMhdDay = -1

        s = self.m_data[nIndex-1]
        t = self.m_data[nIndex]
        u = self.m_data[nIndex+1]

        # if yesterday is dvadasi
        # then we skip this day
        if (GCTithi.TITHI_DVADASI(s.astrodata.nTithi)):
            return 1

        nMahaType = self.IsMhd58(nIndex)
        if (TITHI_GAURA_DVADASI == t.astrodata.nTithi and TITHI_GAURA_DVADASI == t.astrodata.nTithiSunset and nMahaType!=0):
            t.nMhdType = nMahaType
            nMhdDay = nIndex
        elif (GCTithi.TITHI_DVADASI(t.astrodata.nTithi)):
            if (GCTithi.TITHI_DVADASI(u.astrodata.nTithi) and GCTithi.TITHI_EKADASI(s.astrodata.nTithi) and GCTithi.TITHI_EKADASI(s.astrodata.nTithiArunodaya)):
                t.nMhdType = EV_VYANJULI
                nMhdDay = nIndex
            elif (self.NextNewFullIsVriddhi(nIndex, earth)):
                t.nMhdType = EV_PAKSAVARDHINI
                nMhdDay = nIndex
            elif (GCTithi.TITHI_LESS_EKADASI(s.astrodata.nTithiArunodaya)):
                t.nMhdType = EV_SUDDHA
                nMhdDay = nIndex

        if (nMhdDay >= 0):
            # fasting day
            self.m_data[nMhdDay].nFastType = FAST_EKADASI
            self.m_data[nMhdDay].ekadasi_vrata_name = GCStrings.GetEkadasiName(t.astrodata.nMasa, t.astrodata.nPaksa)
            self.m_data[nMhdDay].ekadasi_parana = False
            self.m_data[nMhdDay].eparana_time1 = 0.0
            self.m_data[nMhdDay].eparana_time2 = 0.0

            # parana day
            self.m_data[nMhdDay + 1].nFastType = FAST_NULL
            self.m_data[nMhdDay + 1].ekadasi_parana = True
            self.m_data[nMhdDay + 1].eparana_time1 = 0.0
            self.m_data[nMhdDay + 1].eparana_time2 = 0.0

        return 1

    def GetDay(self, nIndex):
        nReturn = nIndex + BEFORE_DAYS
        if nReturn >= self.m_nCount: return None
        return self.m_data[nReturn]

    def ExtendedCalc(self, nIndex, earth):
        s = self.m_data[nIndex-1]
        t = self.m_data[nIndex]
        u = self.m_data[nIndex+1]
        v = self.m_data[nIndex+2]

        # test for Rama Navami
        if ((t.astrodata.nMasa == VISNU_MASA) and (t.astrodata.nPaksa == GAURA_PAKSA)):
            if (self.IsFestivalDay(s, t, TITHI_GAURA_NAVAMI)):
                if (u.nFastType >= FAST_EKADASI):
                    # yesterday was Rama Navami
                    s.AddSpecFestival(SPEC_RAMANAVAMI, CAL_FEST_0)
                else:
                    # today is Rama Navami
                    t.AddSpecFestival(SPEC_RAMANAVAMI, CAL_FEST_0)

        return 1

    #******************************************************************************************/
    #                                                                                        */
    #*  TEST if today is given festival tithi                                                 */
    #*                                                                                        */
    #*  if today is given tithi and yesterday is not this tithi                               */
    #*  then it is festival day (it is first day of this tithi, when vriddhi)                 */
    #*                                                                                        */
    #*  if yesterday is previous tithi to the given one and today is next to the given one    */
    #*  then today is day after ksaya tithi which is given                                    */
    #*                                                                                        */
    #*                                                                                        */
    #******************************************************************************************/

    def IsFestivalDay(self, yesterday, today, nTithi):
        return ((today.astrodata.nTithi == nTithi) and GCTithi.TITHI_LESS_THAN(yesterday.astrodata.nTithi, nTithi)) or (GCTithi.TITHI_LESS_THAN(yesterday.astrodata.nTithi, nTithi) and GCTithi.TITHI_GREAT_THAN(today.astrodata.nTithi, nTithi))

    def FindDate(self,vc):
        for i in range(BEFORE_DAYS,self.m_nCount):
            if ((self.m_data[i].date.day == vc.day) and (self.m_data[i].date.month == vc.month) and (self.m_data[i].date.year == vc.year)):
                return (i - BEFORE_DAYS)
        return -1


    def CalculateEParana(self, s, t, earth):
        t.nMhdType = EV_NULL
        t.ekadasi_parana = True
        t.nFastType = FAST_NULL

        parBeg = -1.0
        parEnd = -1.0
        snd = GCGregorianDate()
        nend = GCGregorianDate()

        sunRise = t.astrodata.sun.sunrise_deg / 360.0 + earth.tzone / 24.0
        third_day = sunRise + t.astrodata.sun.length_deg / 1080.0
        tithi_len, titBeg, titEnd = GCTithi.GetTithiTimes(earth, t.date, sunRise)
        tithi_quart = tithi_len / 4.0 + titBeg

        if s.nMhdType == EV_UNMILANI:
            parEnd = titEnd
            t.eparana_type2 = EP_TYPE_TEND
            if (parEnd > third_day):
                parEnd = third_day
                t.eparana_type2 = EP_TYPE_3DAY
            parBeg = sunRise
            t.eparana_type1 = EP_TYPE_SUNRISE
        elif s.nMhdType == EV_VYANJULI:
            parBeg = sunRise
            t.eparana_type1 = EP_TYPE_SUNRISE
            parEnd = GCMath.Min(titEnd, third_day)
            if (parEnd == titEnd):
                t.eparana_type2 = EP_TYPE_TEND
            else:
                t.eparana_type2 = EP_TYPE_3DAY
        elif s.nMhdType == EV_TRISPRSA:
            parBeg = sunRise
            parEnd = third_day
            t.eparana_type1 = EP_TYPE_SUNRISE
            t.eparana_type2 = EP_TYPE_3DAY
        elif s.nMhdType == EV_JAYANTI or s.nMhdType == EV_VIJAYA:
            naksEnd = GCNaksatra.GetEndHour(earth, s.date, t.date)
            if (GCTithi.TITHI_DVADASI(t.astrodata.nTithi)):
                if (naksEnd < titEnd):
                    if (naksEnd < third_day):
                        parBeg = naksEnd
                        t.eparana_type1 = EP_TYPE_NAKEND
                        parEnd = GCMath.Min(titEnd, third_day)
                        if (parEnd == titEnd):
                            t.eparana_type2 = EP_TYPE_TEND
                        else:
                            t.eparana_type2 = EP_TYPE_3DAY
                    else:
                        parBeg = naksEnd
                        t.eparana_type1 = EP_TYPE_NAKEND
                        parEnd = titEnd
                        t.eparana_type2 = EP_TYPE_TEND
                else:
                    parBeg = sunRise
                    t.eparana_type1 = EP_TYPE_SUNRISE
                    parEnd = GCMath.Min(titEnd, third_day)
                    if (parEnd == titEnd):
                        t.eparana_type2 = EP_TYPE_TEND
                    else:
                        t.eparana_type2 = EP_TYPE_3DAY
            else:
                parBeg = sunRise
                t.eparana_type1 = EP_TYPE_SUNRISE
                parEnd = GCMath.Min( naksEnd, third_day )
                if (parEnd == naksEnd):
                    t.eparana_type2 = EP_TYPE_NAKEND
                else:
                    t.eparana_type2 = EP_TYPE_3DAY
        elif s.nMhdType == EV_JAYA or s.nMhdType == EV_PAPA_NASINI:
            naksEnd = GCNaksatra.GetEndHour(earth, s.date, t.date)
            if (GCTithi.TITHI_DVADASI(t.astrodata.nTithi)):
                if (naksEnd < titEnd):
                    if (naksEnd < third_day):
                        parBeg = naksEnd
                        t.eparana_type1 = EP_TYPE_NAKEND
                        parEnd = GCMath.Min(titEnd, third_day)
                        if (parEnd == titEnd):
                            t.eparana_type2 = EP_TYPE_TEND
                        else:
                            t.eparana_type2 = EP_TYPE_3DAY
                    else:
                        parBeg = naksEnd
                        t.eparana_type1 = EP_TYPE_NAKEND
                        parEnd = titEnd
                        t.eparana_type2 = EP_TYPE_TEND
                else:
                    parBeg = sunRise
                    t.eparana_type1 = EP_TYPE_SUNRISE
                    parEnd = GCMath.Min(titEnd, third_day)
                    if (parEnd == titEnd):
                        t.eparana_type2 = EP_TYPE_TEND
                    else:
                        t.eparana_type2 = EP_TYPE_3DAY
            else:
                if (naksEnd < third_day):
                    parBeg = naksEnd
                    t.eparana_type1 = EP_TYPE_NAKEND
                    parEnd = third_day
                    t.eparana_type2 = EP_TYPE_3DAY
                else:
                    parBeg = naksEnd
                    t.eparana_type1 = EP_TYPE_NAKEND
                    parEnd = -1.0
                    t.eparana_type2 = EP_TYPE_NULL
        else:
            parEnd = GCMath.Min(titEnd, third_day)
            if (parEnd == titEnd):
                t.eparana_type2 = EP_TYPE_TEND
            else:
                t.eparana_type2 = EP_TYPE_3DAY
            parBeg = GCMath.Max(sunRise, tithi_quart)
            if (parBeg == sunRise):
                t.eparana_type1 = EP_TYPE_SUNRISE
            else:
                t.eparana_type1 = EP_TYPE_4TITHI

            if (GCTithi.TITHI_DVADASI(s.astrodata.nTithi)):
                parBeg = sunRise
                t.eparana_type1 = EP_TYPE_SUNRISE

            if (parBeg > parEnd):
                parEnd = -1.0
                t.eparana_type2 = EP_TYPE_NULL


        begin = parBeg
        end = parEnd

        if (begin > 0.0):
            begin *= 24.0
        if (end > 0.0):
            end *= 24.0

        t.eparana_time1 = begin
        t.eparana_time2 = end

        return parBeg, parEnd


    ''' Function before is writen accoring this algorithms:


    1. Normal - fasting day has ekadasi at sunrise and dvadasi at next sunrise.

    2. Viddha - fasting day has dvadasi at sunrise and trayodasi at next
    sunrise, and it is not a naksatra mahadvadasi

    3. Unmilani - fasting day has ekadasi at both sunrises

    4. Vyanjuli - fasting day has dvadasi at both sunrises, and it is not a
    naksatra mahadvadasi

    5. Trisprsa - fasting day has ekadasi at sunrise and trayodasi at next
    sunrise.

    6. Jayanti/Vijaya - fasting day has gaura dvadasi and specified naksatra at
    sunrise and same naksatra at next sunrise

    7. Jaya/Papanasini - fasting day has gaura dvadasi and specified naksatra at
    sunrise and same naksatra at next sunrise

    ==============================================
    Case 1 Normal (no change)

    If dvadasi tithi ends before 1/3 of daylight
       then PARANA END = TIME OF END OF TITHI
    but if dvadasi TITHI ends after 1/3 of daylight
       then PARANA END = TIME OF 1/3 OF DAYLIGHT

    if 1/4 of dvadasi tithi is before sunrise
       then PARANA BEGIN is sunrise time
    but if 1/4 of dvadasi tithi is after sunrise
       then PARANA BEGIN is time of 1/4 of dvadasi tithi

    if PARANA BEGIN is before PARANA END
       then we will write "BREAK FAST FROM xx TO yy
    but if PARANA BEGIN is after PARANA END
       then we will write "BREAK FAST AFTER xx"

    ==============================================
    Case 2 Viddha

    If trayodasi tithi ends before 1/3 of daylight
       then PARANA END = TIME OF END OF TITHI
    but if trayodasi TITHI ends after 1/3 of daylight
       then PARANA END = TIME OF 1/3 OF DAYLIGHT

    PARANA BEGIN is sunrise time

    we will write "BREAK FAST FROM xx TO yy

    ==============================================
    Case 3 Unmilani

    PARANA END = TIME OF 1/3 OF DAYLIGHT

    PARANA BEGIN is end of Ekadasi tithi

    if PARANA BEGIN is before PARANA END
       then we will write "BREAK FAST FROM xx TO yy
    but if PARANA BEGIN is after PARANA END
       then we will write "BREAK FAST AFTER xx"

    ==============================================
    Case 4 Vyanjuli

    PARANA BEGIN = Sunrise

    PARANA END is end of Dvadasi tithi

    we will write "BREAK FAST FROM xx TO yy

    ==============================================
    Case 5 Trisprsa

    PARANA BEGIN = Sunrise

    PARANA END = 1/3 of daylight hours

    we will write "BREAK FAST FROM xx TO yy

    ==============================================
    Case 6 Jayanti/Vijaya

    PARANA BEGIN = Sunrise

    PARANA END1 = end of dvadasi tithi or sunrise, whichever is later
    PARANA END2 = end of naksatra

    PARANA END is earlier of END1 and END2

    we will write "BREAK FAST FROM xx TO yy

    ==============================================
    Case 7 Jaya/Papanasini

    PARANA BEGIN = end of naksatra

    PARANA END = 1/3 of Daylight hours

    if PARANA BEGIN is before PARANA END
       then we will write "BREAK FAST FROM xx TO yy
    but if PARANA BEGIN is after PARANA END
       then we will write "BREAK FAST AFTER xx"
      '''


    def ResolveFestivalsFasting(self, nIndex):
        s = self.m_data[nIndex-1]
        t = self.m_data[nIndex]
        u = self.m_data[nIndex+1]

        fasting = 0

        if (t.nMhdType != EV_NULL):
            t.AddEvent(PRIO_EKADASI, CAL_EKADASI_PARANA, "{} {}".format(GCStrings.getString(87), t.ekadasi_vrata_name))

        ch = GCStrings.GetMahadvadasiName(t.nMhdType)
        if ch:
            t.AddEvent(PRIO_MAHADVADASI, CAL_EKADASI_PARANA, ch)

        if (t.ekadasi_parana):
            t.AddEvent(PRIO_EKADASI_PARANA, CAL_EKADASI_PARANA, t.GetTextEP())

        for md in t.dayEvents:
            nftype = 0
            if 'fasttype' in md:
                nftype = md["fasttype"]
                subject = md["fastsubject"]

            if (nftype != 0):
                if (s.nFastType == FAST_EKADASI):
                    if (GCDisplaySettings.getValue(42)==0):
                        s.AddEvent(PRIO_FASTING, DISP_ALWAYS, "(Fast today for {})".format(subject))
                        t.AddEvent(md['prio'] + 1, md['disp'], GCStrings.getString(860))
                    else:
                        s.AddEvent(PRIO_FASTING, DISP_ALWAYS, "(Fast till noon for {}, with feast tomorrow)".format(subject))
                        t.AddEvent(md['prio'] + 1, md['disp'], GCStrings.getString(861))
                elif (t.nFastType == FAST_EKADASI):
                    if (GCDisplaySettings.getValue(42)!=0):
                        t.AddEvent(md['prio'] + 1, md['disp'], GCStrings.getString(862))
                    else:
                        t.AddEvent(md['prio'] + 1, md['disp'], GCStrings.getString(756))
                else:
                    if (GCDisplaySettings.getValue(42) == 0):
                        if nftype > 1:
                            nftype = 7
                        else:
                            nftype = 0
                    if (nftype != 0):
                        t.AddEvent(md["prio"] + 1, md["disp"],
                            GCStrings.GetFastingName(0x200 + nftype))
            if (fasting < nftype):
                fasting = nftype

        if fasting:
            if (s.nFastType == FAST_EKADASI):
                t.nFeasting = FEAST_TODAY_FAST_YESTERDAY
                s.nFeasting = FEAST_TOMMOROW_FAST_TODAY
            elif (t.nFastType == FAST_EKADASI):
                u.nFeasting = FEAST_TODAY_FAST_YESTERDAY
                t.nFeasting = FEAST_TOMMOROW_FAST_TODAY
            else:
                t.nFastType = 0x200 + fasting

    def writeXml(self,xml):
        date = GCGregorianDate()
        nPrevMasa = -1
        nPrevPaksa = -1

        xml.write("<xml>\n")
        xml.write("\t<request name=\"Calendar\" version=\"")
        xml.write(GCStrings.getString(130))
        xml.write("\">\n")
        xml.write("\t\t<arg name=\"longitude\" val=\"")
        xml.write(str(self.m_Location.m_fLongitude))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"latitude\" val=\"")
        xml.write(str(self.m_Location.m_fLatitude))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"timezone\" val=\"")
        xml.write(str(self.m_Location.m_fTimezone))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"startdate\" val=\"")
        xml.write(str(self.m_vcStart))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"daycount\" val=\"")
        xml.write(str(self.m_vcCount))
        xml.write("\" />\n")
        xml.write("\t\t<arg name=\"dst\" val=\"")
        xml.write(str(self.m_Location.m_nTimezoneId))
        xml.write("\" />\n")
        xml.write("\t</request>\n")
        xml.write("\t<result name=\"Calendar\">\n")
        if (self.m_Location.m_nTimezoneId > 0):
            xml.write("\t<dstsystem name=\"")
        xml.write(GCTimeZone.GetTimeZoneName(self.m_Location.m_nTimezoneId))
        xml.write("\" />\n")

        for k in range(self.m_vcCount):
            pvd = self.GetDay(k)
            if pvd:
                if (nPrevMasa != pvd.astrodata.nMasa):
                    if (nPrevMasa != -1):
                        xml.write("\t</masa>\n")
                    xml.write("\t<masa name=\"")
                    xml.write(GCStrings.GetMasaName(pvd.astrodata.nMasa))
                    xml.write(" Masa")
                    if (nPrevMasa == ADHIKA_MASA):
                        xml.write(" ")
                        xml.write(GCStrings.getString(109))
                    xml.write("\"")
                    xml.write(" gyear=\"Gaurabda ")
                    xml.write(str(pvd.astrodata.nGaurabdaYear))
                    xml.write("\"")
                    xml.write(">\n")
                nPrevMasa = pvd.astrodata.nMasa

                # date data
                xml.write("\t<day date=\"")
                xml.write(str(pvd.date))
                xml.write("\" dayweekid=\"")
                xml.write(str(pvd.date.dayOfWeek))
                xml.write("\" dayweek=\"{}\">\n".format(GCStrings.getString(pvd.date.dayOfWeek)[:2]))

                # sunrise data
                xml.write("\t\t<sunrise time=\"")
                xml.write(str(pvd.astrodata.sun.rise))
                xml.write("\">\n")

                xml.write("\t\t\t<tithi name=\"")
                xml.write(pvd.GetFullTithiName())
                xml.write("\" elapse=\"{}\" index=\"{}\"/>\n".format(pvd.astrodata.nTithiElapse, pvd.astrodata.nTithi % 30 + 1 ))

                xml.write("\t\t\t<naksatra name=\"{}\" elapse=\"{}\" />\n".format(GCStrings.GetNaksatraName(pvd.astrodata.nNaksatra), pvd.astrodata.nNaksatraElapse ))

                xml.write("\t\t\t<yoga name=\"{}\" />\n".format(GCStrings.GetYogaName(pvd.astrodata.nYoga) ))

                xml.write("\t\t\t<paksa id=\"%c\" name=\"{}\"/>\n".format(GCStrings.GetPaksaChar(pvd.astrodata.nPaksa), GCStrings.GetPaksaName(pvd.astrodata.nPaksa) ))

                xml.write("\t\t</sunrise>\n")

                xml.write("\t\t<dst offset=\"{}\" />\n".format(pvd.hasDST))
                # arunodaya data
                xml.write("\t\t<arunodaya time=\"{}\">".format(pvd.astrodata.sun.arunodaya))
                xml.write("\t\t\t<tithi name=\"{}\" />\n".format(GCStrings.GetTithiName(pvd.astrodata.nTithiArunodaya)))
                xml.write("\t\t</arunodaya>\n")


                xml.write("\t\t<noon time=\"{}\" />\n".format(pvd.astrodata.sun.noon))
                xml.write("\t\t<sunset time=\"{}\" />\n".format(pvd.astrodata.sun.set))

                # moon data
                if pvd.moonrise.hour>=0 or pvd.moonset.hour>=0:
                    xml.write("\t\t<moon")
                    if pvd.moonrise.hour>=0: xml.write(" rise=\"{}\"".format(pvd.moonrise))
                    if pvd.moonset.hour>=0: xml.write(" set=\"{}\"".format(pvd.moonset))
                    xml.write(" />\n")

                if (pvd.ekadasi_parana):
                    (m1,h1) = modf(pvd.eparana_time1)
                    if (pvd.eparana_time2 >= 0.0):
                        (m2,h2) = modf(pvd.eparana_time2)
                        xml.write("\t\t<parana from=\"{:02d}:{:02d}\" to=\"{:02d}:{:02d}\" />\n".format(int(h1), int(m1*60), int(h2), int(m2*60)))
                    else:
                        xml.write("\t\t<parana after=\"{:02d}:{:02d}\" />\n".format(int(h1), int(m1*60) ))

                for md in pvd.dayEvents:
                    prio = md['prio']
                    if (prio >= PRIO_FESTIVALS_0 and prio <= PRIO_FESTIVALS_6):
                        xml.write("\t\t<festival name=\"{}\" class=\"{}\"/>\n".format(md['text'], md['disp'] - CAL_FEST_0))

                if (pvd.nFastType != FAST_NULL):
                    xml.write("\t\t<fast type=\"\" mark=\"")
                    if (pvd.nFastType == FAST_EKADASI):
                        xml.write("*")
                    xml.write("\" />\n")

                if (pvd.sankranti_zodiac >= 0):
                    xml.write("\t\t<sankranti rasi=\"{}\" time=\"{:02d}:{:02d}:{:02d}\" />\n".format(GCStrings.GetSankrantiName(pvd.sankranti_zodiac), pvd.sankranti_day.GetHour()
                        , pvd.sankranti_day.GetMinute(), pvd.sankranti_day.GetSecond()))

                if (pvd.nCaturmasya != 0):
                    xml.write("\t\t<caturmasya day=\"" )
                    xml.write("first" if (pvd.nCaturmasya & CMASYA_DAY_MASK) == CMASYA_DAY_FIRST else "last")
                    xml.write("\" month=\"")
                    xml.write(str(int(pvd.nCaturmasya & CMASYA_MONTH_MASK) - CMASYA_MONTH_MASK + 1))
                    xml.write("\" system=\"")
                    if ((pvd.nCaturmasya & CMASYA_SYSTEM_MASK) == CMASYA_SYSTEM_PURNIMA):
                        xml.write("PURNIMA")
                    elif ((pvd.nCaturmasya & CMASYA_SYSTEM_MASK) == CMASYA_SYSTEM_PRATIPAT):
                        xml.write("PRATIPAT")
                    else:
                        xml.write("EKADASI")
                    xml.write("\" />\n")
                xml.write("\t</day>\n\n")
            date.shour = 0
            date.NextDay()
        xml.write("\t</masa>\n")
        xml.write("</result>\n")
        xml.write("</xml>\n")
        return 1

    def centeredString(self,str,width):
        p = ''.rjust(int((width-len(str))/2), ' ')
        return p + str + p

    def formatPlainText(self,stream):
        lastmasa = -1
        lastmonth = -1
        bCalcMoon = (GCDisplaySettings.getValue(4) > 0 or GCDisplaySettings.getValue(5) > 0)
        sb = GCStringBuilder(stream)
        sb.Format = SBTF_TEXT

        for k in range(self.m_vcCount):
            prevd = self.GetDay(k - 1)
            pvd = self.GetDay(k)
            nextd = self.GetDay(k + 1)

            if (pvd):
                nMasaHeader = 0
                if ((GCDisplaySettings.getValue(18) == 1) and (pvd.astrodata.nMasa != lastmasa)):
                    nMasaHeader = 1
                    stream.write("\r\n")
                    str = self.centeredString("{} {}, Gaurabda {}".format(GCStrings.GetMasaName(pvd.astrodata.nMasa), GCStrings.getString(22), pvd.astrodata.nGaurabdaYear), 80)
                    str2 = GCStrings.GetVersionText()
                    stream.write(str[:80-len(str2)] + str2)
                    stream.write("\r\n")
                    if ((pvd.astrodata.nMasa == ADHIKA_MASA) and ((lastmasa >= SRIDHARA_MASA) and (lastmasa <= DAMODARA_MASA))):
                        sb.AppendTwoColumnText("", GCStrings.getString(128))
                    stream.write("\r\n")
                    lastmasa = pvd.astrodata.nMasa

                if ((GCDisplaySettings.getValue(19) == 1) and (pvd.date.month != lastmonth)):
                    nMasaHeader = 1
                    stream.write("\r\n")
                    str = self.centeredString("{} {}".format(GCStrings.getString(759 + pvd.date.month), pvd.date.year), 80)
                    str2 = GCStrings.GetVersionText()
                    stream.write(str[:80-len(str2)] + str2)
                    stream.write("\r\n")
                    lastmonth = pvd.date.month
                if nMasaHeader:
                    str = self.m_Location.m_strFullName
                    miss = int(floor((80 - len(str))/2))
                    stream.write(''.rjust(miss,' '))
                    stream.write(str)
                    stream.write("\r\n\r\n")
                    nMasaHeader = stream.tell()
                    stream.write(" DATE            TITHI                         ")
                    if (GCDisplaySettings.getValue(39)):
                        stream.write("PAKSA ")
                    else:
                        stream.write("      ")
                    if (GCDisplaySettings.getValue(37)):
                        stream.write("YOGA      ")
                    if (GCDisplaySettings.getValue(36)):
                        stream.write("NAKSATRA       ")
                    if (GCDisplaySettings.getValue(38)):
                        stream.write("FAST ")
                    if (GCDisplaySettings.getValue(41)):
                        stream.write("RASI           ")
                    nMasaHeader = stream.tell() - nMasaHeader
                    stream.write("\r\n")
                    stream.write(''.rjust(nMasaHeader,'-'))
                    nMasaHeader = 0
                    stream.write("\r\n")

                dayText = self.formatPlainTextDay(pvd)
                if (GCDisplaySettings.getValue(20) == 0):
                    stream.write(dayText)
                elif (pvd.dayEvents.Count() > 0):
                    stream.write(dayText)
        sb.AppendNote()
        return 1

    def formatPlainTextDay(self,pvd):
        dayText = StringIO()
        sb = GCStringBuilder(dayText)
        sb.Format = SBTF_TEXT

        dayText.seek(0)
        if pvd.astrodata.sun.longitude_deg < 0.0:
            sb.AppendTwoColumnText(str(pvd.date), "No rise and no set of the sun. No calendar information.")
            return dayText.getvalue()

        sb.AppendLine(pvd.GetTextA())

        for ed in pvd.dayEvents:
            if 'disp' not in ed or ed['disp']==-1 or GCDisplaySettings.getValue(ed['disp']):
                if 'spec' in ed:
                    length = int((82 - len(ed['text'])) / 2)
                    sb.AppendSeparatorWithWidth(length)
                    sb.AppendString(ed['text'])
                    sb.AppendSeparatorWithWidth(length)
                    sb.AppendLine()
                else:
                    sb.AppendTwoColumnText("", ed['text'])
        return dayText.getvalue()

    def formatRtf(self,stream):
        bShowColumnHeaders = 0
        lastmasa = -1
        lastmonth = -1
        bCalcMoon = GCDisplaySettings.getValue(4) > 0 or GCDisplaySettings.getValue(5) > 0

        sb = GCStringBuilder(stream)
        sb.Format = SBTF_RTF
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote

        sb.AppendDocumentHeader()

        for k in range(self.m_vcCount):
            prevd = self.GetDay(k - 1)
            pvd = self.GetDay(k)
            nextd = self.GetDay(k + 1)

            if (pvd):
                bShowColumnHeaders = 0
                if ((GCDisplaySettings.getValue(18) == 1) and (pvd.astrodata.nMasa != lastmasa)):
                    if (bShowColumnHeaders == 0):
                        stream.write("\\par ")
                    bShowColumnHeaders = 1
                    stream.write("\\par \\pard\\f2\\fs{}\\qc {} {}, Gaurabda {}".format(GCLayoutData.textSizeH2
                        , GCStrings.GetMasaName(pvd.astrodata.nMasa), GCStrings.getString(22)
                        , pvd.astrodata.nGaurabdaYear))
                    if ((pvd.astrodata.nMasa == ADHIKA_MASA) and ((lastmasa >= SRIDHARA_MASA) and (lastmasa <= DAMODARA_MASA))):
                        stream.write("\\line ")
                        stream.write(GCStrings.getString(128))
                    lastmasa = pvd.astrodata.nMasa

                if ((GCDisplaySettings.getValue(19) == 1) and (pvd.date.month != lastmonth)):
                    if (bShowColumnHeaders == 0):
                        stream.write("\\par ")
                    bShowColumnHeaders = 1
                    stream.write("\\par\\pard\\f2\\qc\\fs{}\r\n".format(GCLayoutData.textSizeH2))
                    stream.write("{} {}".format(GCStrings.getString(759 + pvd.date.month), pvd.date.year))
                    lastmonth = pvd.date.month

                # print location text
                if (bShowColumnHeaders):
                    stream.write("\\par\\pard\\qc\\cf2\\fs22 ")
                    stream.write(self.m_Location.m_strFullName)

                if (bShowColumnHeaders):
                    stream.write("\\par\\pard\\fs{}\\qc {}".format(GCLayoutData.textSizeNote, GCStrings.GetVersionText()))
                    stream.write("\\par\\par\r\n")

                if (bShowColumnHeaders):
                    tabStop = 5760*GCLayoutData.textSizeText/24
                    stream.write("\\pard\\tx{}\\tx{} ".format(2000*GCLayoutData.textSizeText/24, tabStop))
                    if (GCDisplaySettings.getValue(39)):
                        tabStop += 990*GCLayoutData.textSizeText/24
                        stream.write("\\tx{}".format(tabStop))
                    if (GCDisplaySettings.getValue(37)):
                        tabStop += 1720*GCLayoutData.textSizeText/24
                        stream.write("\\tx{}".format(tabStop))
                    if (GCDisplaySettings.getValue(36)):
                        tabStop += 1800*GCLayoutData.textSizeText/24
                        stream.write("\\tx{}".format(tabStop))
                    if (GCDisplaySettings.getValue(38)):
                        tabStop += 750*GCLayoutData.textSizeText/24
                        stream.write("\\tx{}".format(tabStop))
                    if (GCDisplaySettings.getValue(41)):
                        tabStop += 1850*GCLayoutData.textSizeText/24
                        stream.write("\\tx{}".format(tabStop))
                    # paksa width 990
                    # yoga width 1720
                    # naks width 1800
                    # fast width 990
                    # rasi width 1850
                    stream.write("{{\\highlight15\\cf7\\fs{}\\b DATE\\tab TITHI".format(GCLayoutData.textSizeNote))
                    if (GCDisplaySettings.getValue(39)):
                        stream.write("\\tab PAKSA")
                    if (GCDisplaySettings.getValue(37)):
                        stream.write("\\tab YOGA")
                    if (GCDisplaySettings.getValue(36)):
                        stream.write("\\tab NAKSATRA")
                    if (GCDisplaySettings.getValue(38)):
                        stream.write("\\tab FAST")
                    if (GCDisplaySettings.getValue(41)):
                        stream.write("\\tab RASI")
                    stream.write("}")
                stream.write("\\fs{} ".format(GCLayoutData.textSizeText))

                dayText = self.formatRtfDay(pvd)

                if (GCDisplaySettings.getValue(20) == 0) or pvd.dayEvents.Count()>0:
                    stream.write(dayText)

        sb.AppendNote()
        sb.AppendDocumentTail()
        return 1

    def formatRtfDay(self,pvd):
        dayText = StringIO()
        sb = GCStringBuilder(dayText)
        sb.Format = SBTF_RTF
        sb.fontSizeH1 = GCLayoutData.textSizeH1
        sb.fontSizeH2 = GCLayoutData.textSizeH2
        sb.fontSizeText = GCLayoutData.textSizeText
        sb.fontSizeNote = GCLayoutData.textSizeNote

        if (pvd.astrodata.sun.longitude_deg < 0.0):
            return "\\par\\tab No rise and no set of the sun. No calendar information."

        dayText.write(pvd.GetTextRtf())

        for ed in pvd.dayEvents:
            if 'disp' not in ed or ed['disp'] == -1 or GCDisplaySettings.getValue(ed['disp']):
                if 'spec' in ed:
                    length = (80 - len(ed['text'])) / 2
                    dayText.write("\\par ")
                    sb.AppendSeparatorWithWidth(length)
                    dayText.write(str)
                    sb.AppendSeparatorWithWidth(length)
                else:
                    sb.AppendTwoColumnText("", ed['text'])
        return dayText.getvalue()

    def getDayBkgColorCode(self,p):
        if p == None: return "white"
        if (p.nFastType == FAST_EKADASI): return "#FFFFBB"
        if (p.nFastType != 0): return "#BBFFBB"
        return "white"

    def writeHtml(self,xml):
        dat = GCGregorianDate()
        nPrevMasa = -1
        nPrevPaksa = -1

        xml.write("<html><head><title>Calendar {}</title>".format(self.m_vcStart.year))
        xml.write("<style>\n")
        xml.write("body {\n")
        xml.write("  font-family:Verdana;\n")
        xml.write("  font-size:11pt;\n}\n\n")
        xml.write("td.hed {\n")
        xml.write("  font-family:Verdana;\n")
        xml.write("  font-size:9pt;\n")
        xml.write("  font-weight:bold;\n")
        xml.write("  background:#aaaaaa;\n")
        xml.write("  color:white;\n")
        xml.write("  text-align:center;\n")
        xml.write("  vertical-align:center;\n  padding-left:15pt;\n  padding-right:15pt;\n")
        xml.write("  padding-top:5pt;\n  padding-bottom:5pt;\n}\n-.\n</style>\n")
        xml.write("</head>\n<body>")

        for k in range(self.m_vcCount):
            pvd = self.GetDay(k)
            if (pvd):
                if (nPrevMasa != pvd.astrodata.nMasa):
                    if (nPrevMasa != -1):
                        xml.write("\t</table>\n")
                    xml.write("<p style=\'text-align:center;font-weight:bold\'><span style =\'font-size:14pt\'>")
                    xml.write(GCStrings.GetMasaName(pvd.astrodata.nMasa))
                    xml.write(" Masa")
                    if (nPrevMasa == ADHIKA_MASA):
                        xml.write(" ")
                    xml.write(GCStrings.getString(109))
                    xml.write("</span>")
                    xml.write("<br><span style=\'font-size:10pt;\'>Gaurabda {}<br>{}</font></span></p>\n".format(pvd.astrodata.nGaurabdaYear, self.m_Location.m_strFullName))
                    xml.write("<table align=center>")
                    xml.write("<tr><td  class=\"hed\"colspan=2>")
                    xml.write("DATE</td><td class=\"hed\">TITHI</td><td class=\"hed\">P</td><td class=\"hed\">NAKSATRA</td><td class=\"hed\">YOGA</td><td class=\"hed\">FAST</td></tr>")

                nPrevMasa = pvd.astrodata.nMasa
                #if len(pvd.dayEvents) > 0: continue

                # date data
                xml.write("<tr>")
                xml.write("<td>{}</td>".format(pvd.date))
                xml.write("<td>{}</td>\n".format(GCStrings.getString(pvd.date.dayOfWeek)[:2]))

                # sunrise data

                xml.write("<td>{}</td>\n".format(pvd.GetFullTithiName()))
                xml.write("<td>{}</td>\n".format(GCStrings.GetPaksaChar(pvd.astrodata.nPaksa) ))
                xml.write("<td>{}</td>\n".format(GCStrings.GetNaksatraName(pvd.astrodata.nNaksatra)))
                xml.write("<td>{}</td>\n".format(GCStrings.GetYogaName(pvd.astrodata.nYoga) ))
                xml.write("<td>{}</td>\n".format("FAST" if pvd.nFastType!=FAST_NULL else ""))

                xml.write("</tr>\n\n<tr>\n<td></td><td></td><td colspan=4>")
                for ed in pvd.dayEvents:
                    if 'disp' not in ed or ed['disp'] == -1 or GCDisplaySettings.getValue(ed['disp']):
                        if 'spec' in ed:
                            xml.write("<font color=\"blue\">{}</font><br>\n".format(ed['text']))
                        else:
                            xml.write(ed['text'])
                            xml.write("<br>\n")
                xml.write("\t</tr>\n\n")
        xml.write("\t</table>\n\n")
        xml.write("<hr align=center width=\"65%\">\n")
        xml.write("<p align=center>Generated by {}</p>\n".format(GCStrings.getString(130)))
        xml.write("</body>\n</html>\n")
        return 1

    def writeTableHtml(self,xml):
        g_firstday_in_week = GCDisplaySettings.getValue(GENERAL_FIRST_DOW)
        date = GCGregorianDate()
        nPrevMasa = -1
        prevMas = -1
        brw = 0

        xml.write("<html>\n<head>\n<title>Calendar {}</title>".format(self.m_vcStart))

        xml.write("<style>\n<!--\np.MsoNormal, li.MsoNormal, div.MsoNormal\n    {mso-style-parent:\"\";")
        xml.write("margin:0in;margin-bottom:.0001pt;mso-pagination:widow-orphan;font-size:8.0pt;font-family:Arial;")
        xml.write("mso-fareast-font-family:Arial;}")
        xml.write("p.month\n{mso-style-name:month;\nmso-margin-top-alt:auto;\nmargin-right:0in;\nmso-margin-bottom-alt:auto;\nmargin-left:0in;\nmso-pagination:widow-orphan;\nfont-size:17.0pt;font-family:Arial;mso-fareast-font-family:Arial;}\n")
        xml.write(".text\n{mso-style-name:text;\nmso-margin-top-alt:auto;\nmargin-right:0in;\nmso-margin-bottom-alt:auto;\nmargin-left:0in;\n    mso-pagination:widow-orphan;\nfont-size:6.0pt;\nmso-bidi-font-size:6.0pt;\nfont-family:Arial;    mso-fareast-font-family:\"Arial\";mso-bidi-font-family:\"Arial\";}\n")
        xml.write(".tnote\n{mso-style-name:text;\nmso-margin-top-alt:auto;\nmargin-right:0in;\nmso-margin-bottom-alt:auto;\nmargin-left:0in;\n    mso-pagination:widow-orphan;\nfont-size:7.0pt;\nmso-bidi-font-size:7.0pt;\nfont-family:Arial;    mso-fareast-font-family:Arial;mso-bidi-font-family:Arial;}\n")
        xml.write(".tithiname\n{mso-style-name:text;\nmso-margin-top-alt:auto;\nmargin-right:0in;\nmso-margin-bottom-alt:auto;\nmargin-left:0in;\n    mso-pagination:widow-orphan;\nfont-size:8.0pt;\nmso-bidi-font-size:8.0pt;\nfont-family:Arial;    mso-fareast-font-family:\"Arial\";mso-bidi-font-family:\"Arial\";}\n")
        xml.write(".dayt\n    {mso-style-name:dayt;\nfont-size:12.0pt;\nmso-ansi-font-size:12.0pt;\nfont-family:Arial;\nmso-ascii-font-family:Arial;\nmso-hansi-font-family:Arial;\nfont-weight:bold;\nmso-bidi-font-weight:normal;}\n")
        xml.write("span.SpellE\n{mso-style-name:\"\";\nmso-spl-e:yes;}\n")
        xml.write("span.GramE\n{mso-style-name:\"\";\nmso-gram-e:yes;}\n")
        xml.write("-.\n</style>\n")

        xml.write("</head>\n\n<body>\n\n")

        for k in range(self.m_vcCount):
            pvd = self.GetDay(k)
            if (pvd):
                bSemicolon = False
                bBr = False
                lwd = pvd.date.dayOfWeek
                if (nPrevMasa != pvd.date.month):
                    if (nPrevMasa != -1):
                        for y in range(self.DAYS_TO_ENDWEEK(pvd.date.dayOfWeek)):
                            xml.write("<td style=\'border:solid windowtext 1.0pt;mso-border-alt:solid windowtext .5pt;padding:3.0pt 3.0pt 3.0pt 3.0pt\'>&nbsp;</td>")
                        xml.write("</tr></table>\n<p>&nbsp;</p>")
                    xml.write("\n<table width=\"100%\" border=0 frame=bottom cellspacing=0 cellpadding=0><tr><td width=\"60%\"><p class=month>")
                    xml.write(GCStrings.getString(pvd.date.month + 759))
                    xml.write(" {}".format(pvd.date.year))
                    xml.write("</p></td><td><p class=tnote align=right>")
                    xml.write(self.m_Location.m_strName)
                    xml.write("<br>Timezone: ")
                    xml.write(GCTimeZone.GetTimeZoneName(self.m_Location.m_nTimezoneId))
                    xml.write("</p>")
                    xml.write("</td></tr></table><hr>")
                    nPrevMasa = pvd.date.month
                    xml.write("\n<table width=\"100%\" bordercolor=black cellpadding=0 cellspacing=0>\n<tr>\n")
                    for y in range(7):
                        xml.write("<td width=\"14%\" align=center style=\'font-size:10.0pt;border:none\'>")
                        xml.write(GCStrings.getString(self.DAY_INDEX(y)))
                        xml.write("</td>\n")
                    xml.write("<tr>\n")
                    for y in range(self.DAYS_FROM_BEGINWEEK(pvd.date.dayOfWeek)):
                        xml.write("<td style=\'border:solid windowtext 1.0pt;mso-border-alt:solid windowtext .5pt;padding:3.0pt 3.0pt 3.0pt 3.0pt\'>&nbsp;</td>")
                else:
                    if (pvd.date.dayOfWeek == g_firstday_in_week):
                        xml.write("<tr>\n")

                # date data
                xml.write("\n<td valign=top style=\'border:solid windowtext 1.0pt;mso-border-alt:solid windowtext .5pt;padding:3.0pt 3.0pt 3.0pt 3.0pt\' ")
                xml.write("bgcolor=\"")
                xml.write(self.getDayBkgColorCode(pvd))
                xml.write("\">")
                xml.write("<table width=\"100%\" border=0><tr><td><p class=text><span class=dayt>")
                xml.write(pvd.date.day.__str__())
                xml.write("</span></td><td>")


                xml.write("<span class=\"tithiname\">{}</span>".format(pvd.GetFullTithiName()))
                xml.write("</td></tr></table>\n")
                brw = 0
                xml.write("<span class=\"text\">\n")

                str = ''

                if len(pvd.dayEvents) > 0:
                    if (brw):
                        xml.write("<br>\n")
                    brw = 1
                    bSemicolon = False

                for ed in pvd.dayEvents:
                    if 'disp' not in ed or ed['disp'] == -1 or GCDisplaySettings.getValue(ed['disp']):
                        if (bSemicolon): xml.write("; ")
                        bSemicolon=True
                        if 'spec' in ed:
                            xml.write(ed.stringForKey("text"))
                        else:
                            xml.write("<i>{}</i>\n".format(ed['text']))

                if (prevMas != pvd.astrodata.nMasa):
                    if (brw):
                        xml.write("<br>\n")
                    brw = 1
                    xml.write("<b>[")
                    xml.write(GCStrings.GetMasaName(pvd.astrodata.nMasa))
                    xml.write(" Masa]</b>")
                    prevMas = pvd.astrodata.nMasa
                xml.write("</span>")
                xml.write("</td>\n\n")
            date.shour = 0
            date.NextDay()

        for y in range(1,self.DAYS_TO_ENDWEEK(lwd)):
            xml.write("<td style=\'border:solid windowtext 1.0pt;mso-border-alt:solid windowtext .5pt;padding:3.0pt 3.0pt 3.0pt 3.0pt\'>&nbsp;</td>")

        xml.write("</tr>\n</table>\n")
        xml.write("</body>\n</html>\n")
        return 1

    def write(self,stream,format='html',layout='list'):
        if format=='plain':
            self.formatPlainText(stream)
        elif format=='rtf':
            self.formatRtf(stream)
        elif format=='xml':
            self.writeXml(stream)
        elif format=='html':
            if layout=='list':
                self.writeHtml(stream)
            elif layout=='table':
                self.writeTableHtml(stream)
        elif format=='json':
            stream.write(json.dumps(dict(self), indent=4))

    def get_json_object(self):
        return dict(self)

def unittests():
    GCUT.info('calendar results')
    loc = GCLocation(data={
        'latitude': 48.150002,
        'longitude': 17.116667,
        'tzid': 321,
        'name': 'Bratislava, Slovakia'
    })
    earth = loc.GetEarthData()
    today = Today()

    tc = TCalendar()

    GCUT.val(tc.DAYS_TO_ENDWEEK(3),4,'days')
    GCUT.val(tc.DAYS_FROM_BEGINWEEK(3),3,'days s')
    GCUT.val(tc.DAY_INDEX(3),3,'dayindx')

    print('start calculate', datetime.datetime.now())
    tc.CalculateCalendar(loc,today,365)
    print('end calculate', datetime.datetime.now())

    with open('test/calendar.xml','wt') as wf:
        tc.writeXml(wf)
    with open('test/calendar.txt','wt') as wf:
        tc.formatPlainText(wf)
    with open('test/calendar.rtf','wt') as wf:
        tc.formatRtf(wf)
    with open('test/calendar.html','wt') as wf:
        tc.writeHtml(wf)
    with open('test/calendar2.html','wt') as wf:
        tc.writeTableHtml(wf)
