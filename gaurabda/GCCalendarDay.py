from .GCEnums import FeastType,FastType,MahadvadasiType,SpecialFestivalId
from .GCGregorianDate import GCGregorianDate
from .GCDayData import GCDayData
from .GCTime import GCTime
from .GCEnums.DisplayPriorities import *
from .GCEnums.GCDS import *
from .GCEnums.CaturmasyaCodes import *

from . import GCNaksatra as GCNaksatra
from . import GCTithi as GCTithi
from . import GCRasi as GCRasi
from . import GCStrings as GCStrings
from . import GCDisplaySettings as GCDisplaySettings
from . import GCMath as GCMath

from math import floor,modf

class GCCalendarDay:
    def __init__(self):
        # date
        self.date = GCGregorianDate()
        # moon times
        self.moonrise = GCTime()
        self.moonset = GCTime()
        # astronomical data from astro-sub-layer
        self.astrodata = GCDayData()

        self.nCaturmasya = 0
        self.hasDST = 0
        self.nFeasting = FeastType.FEAST_NULL
        # data for vaisnava calculations
        self.dayEvents = []

        self.festivals = ''
        self.nFastType = FastType.FAST_NULL
        self.nMhdType = MahadvadasiType.EV_NULL
        self.ekadasi_vrata_name = ''
        self.ekadasi_parana = False
        self.eparana_time1 = 0.0
        self.eparana_time2 = 0.0
        self.eparana_type1 = 0
        self.eparana_type2 = 0
        self.sankranti_zodiac = -1
        #double sankranti_time
        self.sankranti_day = GCGregorianDate()

    def __iter__(self):
        yield 'date', dict(self.date)
        yield 'astrodata', dict(self.astrodata)
        yield 'hasDST', self.hasDST
        yield 'feasting', self.nFeasting
        if len(self.dayEvents)>0:
            yield 'events', self.dayEvents
        yield 'fast', self.nFastType
        yield 'ekadashiType', self.nMhdType
        yield 'ekadashiName', self.ekadasi_vrata_name
        if self.ekadasi_parana:
            yield 'ekadashiParana', {
                'startTime': self.eparana_time1,
                'endTime': self.eparana_time2,
                'startReason': self.eparana_type1,
                'endReason': self.eparana_type2
            }
        if self.sankranti_zodiac>=0:
            yield 'sankranti', {
                'rasi': self.sankranti_zodiac,
                'datetime': dict(self.sankranti_day)
            }

    def GetTextLineCount(self):
        nCount = 1
        for ed in self.dayEvents:
            if 'disp' not in ed:
                nCount+=1
            else:
                disp = int(ed['disp'])
                if disp == -1 or GCDisplaySettings.getValue(disp):
                    nCount+=1
        return nCount

    def Clear(self):
        self.nFastType = FastType.FAST_NULL
        self.nFeasting = FeastType.FEAST_NULL
        self.nMhdType = MahadvadasiType.EV_NULL
        self.ekadasi_parana = False
        self.ekadasi_vrata_name = ''
        self.eparana_time1 = self.eparana_time2 = 0.0
        self.sankranti_zodiac = -1
        self.sankranti_day.day = 0
        self.sankranti_day.shour = 0.0
        self.sankranti_day.month = 0
        self.sankranti_day.year = 0
        self.nCaturmasya = 0

    def GetTextA(self):
        str = "{} {}  {} ".format(self.date.__str__().rjust(12,' '), GCStrings.GetDayOfWeek(self.date.dayOfWeek)[:2], self.GetFullTithiName().ljust(34,' '))

        if GCDisplaySettings.getValue(39):
            str += GCStrings.GetPaksaChar(self.astrodata.nPaksa) + ' '
        else:
            str += '  '

        if GCDisplaySettings.getValue(37):
            str += '{}'.format(GCStrings.GetYogaName(self.astrodata.nYoga).ljust(10,' '))

        if GCDisplaySettings.getValue(36):
            str += '{}'.format(GCStrings.GetNaksatraName(self.astrodata.nNaksatra).ljust(15,' '))

        if GCDisplaySettings.getValue(38) and self.nFastType != FastType.FAST_NULL:
            str += " *"
        else:
            str += "  "

        if GCDisplaySettings.getValue(41):
            rasi = GCRasi.GetRasi(self.astrodata.moon.longitude_deg, self.astrodata.msAyanamsa)
            if GCDisplaySettings.getValue(41) == 1:
                str += "   {}".format(GCStrings.GetSankrantiName(rasi).ljust(15,' '))
            else:
                str += "   {}".format(GCStrings.GetSankrantiNameEn(rasi).ljust(15,' '))
        return str

    def GetTextRtf(self):
        str = "\\par {} {}\\tab {}\\tab ".format(self.date, GCStrings.GetDayOfWeek(self.date.dayOfWeek)[:2], self.GetFullTithiName())

        if GCDisplaySettings.getValue(39):
            str += GCStrings.GetPaksaChar(self.astrodata.nPaksa) + ' '
        else:
            str += '  '

        if GCDisplaySettings.getValue(37):
            str += '\\tab {}'.format(GCStrings.GetYogaName(self.astrodata.nYoga))

        if GCDisplaySettings.getValue(36):
            str += '\\tab {}'.format(GCStrings.GetNaksatraName(self.astrodata.nNaksatra))

        if GCDisplaySettings.getValue(38) and self.nFastType != FastType.FAST_NULL:
            str += "\\tab *"
        else:
            str += "\\tab  "

        if GCDisplaySettings.getValue(41):
            rasi = GCRasi.GetRasi(self.astrodata.moon.longitude_deg, self.astrodata.msAyanamsa)
            if GCDisplaySettings.getValue(41) == 1:
                str += "\\tab {}".format(GCStrings.GetSankrantiName(rasi))
            else:
                str += "\\tab {}".format(GCStrings.GetSankrantiNameEn(rasi))

        str += "\r\n"
        return str


    def GetTextEP(self):
        str = ''
        (m1,h1) = modf(self.eparana_time1)
        if self.eparana_time2 >= 0.0:
            (m2,h2) = modf(self.eparana_time2)
            if GCDisplaySettings.getValue(50):
                str += "{} {:02d}:{:02d} ({}) - {:02d}:{:02d} ({}) {}".format( GCStrings.getString(60), int(h1), int(m1*60), GCStrings.GetParanaReasonText(self.eparana_type1), int(h2), int(m2*60), GCStrings.GetParanaReasonText(self.eparana_type2), GCStrings.GetDSTSignature(self.hasDST))
            else:
                str += "{} {:02d}:{:02d} - {:02d}:{:02d} ({})".format( GCStrings.getString(60), int(h1), int(m1*60), int(h2), int(m2*60), GCStrings.GetDSTSignature(self.hasDST))
        elif self.eparana_time1 >= 0.0:
            if GCDisplaySettings.getValue(50):
                str += "{} {:02d}:{:02d} ({}) {}".format(GCStrings.getString(61), int(h1), int(m1*60), GCStrings.GetParanaReasonText(self.eparana_type1), GCStrings.GetDSTSignature(self.hasDST) )
            else:
                str += "{} {:02d}:{:02d} ({})".format(GCStrings.getString(61), int(h1), int(m1*60), GCStrings.GetDSTSignature(self.hasDST) )
        else:
            str = GCStrings.getString(62)
        return str

    def GetNaksatraTimeRange(self, earth, fromTime, toTime):
        start = GCGregorianDate(date = self.date)
        start.shour = self.astrodata.sun.sunrise_deg / 360 + earth.tzone/24.0

        GCNaksatra.GetNextNaksatra(earth, start, toTime)
        GCNaksatra.GetPrevNaksatra(earth, start, fromTime)
        return True


    def GetTithiTimeRange(self, earth, fromTime, toTime):
        start = GCGregorianDate(date = self.date)
        start.shour = self.astrodata.sun.sunrise_deg / 360 + earth.tzone/24.0

        GCTithi.GetNextTithiStart(earth, start, toTime)
        GCTithi.GetPrevTithiStart(earth, start, fromTime)

        return True

    def AddEvent(self, priority, dispItem, text):
        dc = {
            'prio': priority,
            'disp': dispItem,
            'text': text
        }
        self.dayEvents.append(dc)
        return dc

    def hasEventsOfDisplayIndex(self,dispIndex):
        for md in self.dayEvents:
            if 'disp' in md and md['disp']==dispIndex:
                return True
        return False

    def findEventsText(self,text):
        for md in self.dayEvents:
            if md['text'].find(text)>=0:
                return md
        return None

    def AddSpecFestival(self, nSpecialFestival, nFestClass):
        str = ''
        fasting = -1
        fastingSubject = None

        if nSpecialFestival == SpecialFestivalId.SPEC_JANMASTAMI:
            str = GCStrings.getString(741)
            fasting = 5
            fastingSubject = "Sri Krsna"
        elif nSpecialFestival == SpecialFestivalId.SPEC_GAURAPURNIMA:
            str = GCStrings.getString(742)
            fasting = 3
            fastingSubject = "Sri Caitanya Mahaprabhu"
        elif nSpecialFestival == SpecialFestivalId.SPEC_RETURNRATHA:
            str = GCStrings.getString(743)
        elif nSpecialFestival == SpecialFestivalId.SPEC_HERAPANCAMI:
            str = GCStrings.getString(744)
        elif nSpecialFestival == SpecialFestivalId.SPEC_GUNDICAMARJANA:
            str = GCStrings.getString(745)
        elif nSpecialFestival == SpecialFestivalId.SPEC_GOVARDHANPUJA:
            str = GCStrings.getString(746)
        elif nSpecialFestival == SpecialFestivalId.SPEC_RAMANAVAMI:
            str = GCStrings.getString(747)
            fasting = 2
            fastingSubject = "Sri Ramacandra"
        elif nSpecialFestival == SpecialFestivalId.SPEC_RATHAYATRA:
            str = GCStrings.getString(748)
        elif nSpecialFestival == SpecialFestivalId.SPEC_NANDAUTSAVA:
            str = GCStrings.getString(749)
        elif nSpecialFestival == SpecialFestivalId.SPEC_PRABHAPP:
            str = GCStrings.getString(759)
            fasting = 1
            fastingSubject = "Srila Prabhupada"
        elif nSpecialFestival == SpecialFestivalId.SPEC_MISRAFESTIVAL:
            str = GCStrings.getString(750)
        else:
            return False

        md = self.AddEvent(PRIO_FESTIVALS_0 + (nFestClass-CAL_FEST_0)*100, nFestClass, str)
        if fasting > 0:
            md['fasttype'] = fasting
            md["fastsubject"] = fastingSubject

        return False

    def GetFullTithiName(self):
        str = GCStrings.GetTithiName(self.astrodata.nTithi)
        if (self.astrodata.nTithi == 10) or (self.astrodata.nTithi == 25) or (self.astrodata.nTithi == 11) or (self.astrodata.nTithi == 26):
            if self.ekadasi_parana == False:
                str += " "
                if self.nMhdType == MahadvadasiType.EV_NULL:
                    str += GCStrings.getString(58)
                else:
                    str += GCStrings.getString(59)
        return str

    def ConditionEvaluate(self, nClass, nValue, strText, defaultRet):
        pcstr = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, CAL_FEST_0, CAL_FEST_1, CAL_FEST_2, CAL_FEST_3, CAL_FEST_4, CAL_FEST_5, 0, 0]

        # mahadvadasis
        if nClass==1:
            if nValue == MahadvadasiType.EV_NULL:
                return (self.nMhdType != EV_NULL) and (self.nMhdType != EV_SUDDHA)
            else:
                return self.nMhdType == nValue
        # sankrantis
        elif nClass==2:
            if nValue == 0xff:
                return self.sankranti_zodiac >= 0
            else:
                return self.sankranti_zodiac == nValue
        # tithi + paksa
        elif nClass==3:
            return self.astrodata.nTithi == nValue
        # naksatras
        elif nClass==4:
            return self.astrodata.nNaksatra == nValue
        # yogas
        elif nClass==5:
            return self.astrodata.nYoga == nValue
        # fast days
        elif nClass==6:
            if nValue == 0:
                return self.nFastType != FastType.FAST_NULL
            else:
                return self.nFastType == (0x200 + nValue)

        # week day
        elif nClass==7:
            return self.date.dayOfWeek == nValue
        # tithi
        elif nClass==8:
            return self.astrodata.nTithi % 15 == nValue
        # paksa
        elif nClass==9:
            return self.astrodata.nPaksa == nValue
        elif nClass in [10, 11, 12, 13, 14]:
            if nValue == 0xffff:
                return self.hasEventsOfDisplayIndex(pcstr[nClass])
            else:
                if self.astrodata.nMasa == 12:
                    return False
                if abs(self.astrodata.nTithi + self.astrodata.nMasa*30 - nValue + 200) > 2:
                    return False
                if self.findEventsText(strText) != 0:
                    return True
            return False
        elif nClass==15:
            if nValue == 0xffff:
                return False
            else:
                # difference against 10-14 is that we cannot test tithi-masa date
                # because some festivals in this category depends on sankranti
                if self.findEventsText(strText) != 0:
                    return True
            return False
        else:
            return defaultRet
