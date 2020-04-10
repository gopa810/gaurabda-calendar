import math
import datetime

import gaurabda.GCMath as GCMath
import gaurabda.GCUT as GCUT
import gaurabda.GCStrings as GCStrings

def GetMonthMaxDays(year, month):
    m_months = [ 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

    if IsLeapYear(year) and month==2: return 29
    return m_months[month]

def IsLeapYear(year):
    if (year % 4) != 0: return False
    if year % 100 == 0 and year % 400 != 0: return False
    return True

def NormalizedValues(date, tzone=False):
    d1 = date.day
    m1 = date.month
    y1 = date.year
    h1 = date.shour
    if tzone: h1 += date.tzone/24.0

    if h1 < 0.0:
        d1-=1
        h1 += 1.0
    elif h1 >= 1.0:
        h1 -= 1.0
        d1+=1

    if d1 < 1:
        m1-=1
        if m1 < 1:
            m1 = 12
            y1-=1
        d1 = GetMonthMaxDays(y1, m1)
    elif d1 > GetMonthMaxDays(y1, m1):
        m1+=1
        if m1 > 12:
            m1 = 1
            y1+=1
        d1 = 1
    return y1,m1,d1,h1

def CalculateJulianDay(year, month, day):
    yy = year - int((12 - month) / 10)
    mm = month + 9

    if mm >= 12:
        mm -= 12

    k1 = int (math.floor(365.25 * (yy + 4712)))
    k2 = int (math.floor(30.6 * mm + 0.5))
    k3 = int (math.floor(math.floor((yy/100.0)+49)*.75))-38
    j = k1 + k2 + day + 59
    if j > 2299160:
        j -= k3

    return j


class GCGregorianDate:
    def __init__(self,year=2000,month=1,day=1,shour=0.5,tzone=0.0,date=None,addDays=0):
        if date!=None:
            self.Set(date)
        else:
            self.year = year
            self.month = month
            self.day = day
            self.shour = shour
            self.tzone = tzone
            self.InitWeekDay()
        if addDays!=0:
            self.AddDays(addDays)

    def copy(self):
        return GCGregorianDate(date=self)

    def __str__(self):
        return '{} {} {:04d}'.format(self.day, GCStrings.GetMonthAbreviation(self.month), self.year)

    def __repr__(self):
        return "{:2d} {} {:04d}  {:02d}:{:02d}:{:02d}".format(self.day, GCStrings.GetMonthAbreviation(self.month), self.year, self.GetHour(), self.GetMinute(), self.GetSecond())

    def time_str(self):
        return "{:02d}:{:02d}:{:02d}".format(self.GetHour(), self.GetMinute(), self.GetSecond())

    def IsLessThan(self,date):
        y1,m1,d1,h1 = NormalizedValues(self,tzone=True)
        y2,m2,d2,h2 = NormalizedValues(date,tzone=True)

        if y1 > y2: return False
        if y1 < y2: return True

        if m1 > m2: return False
        if m1 < m2: return True

        if d1 < d2: return True
        return False

    def IsLessOrEqualTo(self,date):
        y1,m1,d1,h1 = NormalizedValues(self,tzone=True)
        y2,m2,d2,h2 = NormalizedValues(date,tzone=True)

        if y1 > y2: return False
        if y1 < y2: return True

        if m1 > m2: return False
        if m1 < m2: return True

        if d1 <= d2: return True
        return False

    def IsDateEqual(self,date):
        y1,m1,d1,h1 = NormalizedValues(self,tzone=True)
        y2,m2,d2,h2 = NormalizedValues(date,tzone=True)

        return y1 == y2 and m1 == m2 and d1 == d2

    def NormalizeValues(self):
        self.year,self.month,self.day,self.shour = NormalizedValues(self)

    def NormalizeHours(self):
        while self.shour < 0.0:
            self.shour += 1.0
            self.PreviousDay()
        while self.shour > 1.0:
            self.shour -= 1.0
            self.NextDay()

    def ChangeTimeZone(self,tZone):
        self.shour += (tZone - self.tzone)/24
        self.NormalizeValues()
        self.tzone = tZone

    def GetJulianInteger(self):
        return CalculateJulianDay(self.year,self.month,self.day)

    def GetJulian(self):
        return self.GetJulianInteger() * 1.0

    def PreviousDay(self):
        self.day-=1
        if self.day < 1:
            self.month-=1
            if self.month < 1:
                self.month = 12
                self.year-=1
            self.day = GetMonthMaxDays(self.year, self.month)
        self.dayOfWeek = (self.dayOfWeek + 6) % 7

    def NextDay(self):
        self.day+=1
        if self.day > GetMonthMaxDays(self.year, self.month):
            self.month+=1
            if self.month > 12:
                self.month = 1
                self.year+=1
            self.day = 1
        self.dayOfWeek = (self.dayOfWeek + 1) % 7

    def AddDays(self,n):
        if n>0:
            for i in range(n):
                self.NextDay()
        elif n<0:
            for i in range(-n):
                self.PreviousDay()

    def SubtractDays(self, n):
        self.AddDays(-n)

    def GetJulianDetailed(self):
        return self.GetJulian() - 0.5 + self.shour

    def GetJulianComplete(self):
        return self.GetJulian() - 0.5 + self.shour - self.tzone/24.0

    def InitWeekDay(self):
        self.dayOfWeek = (int(self.GetJulianInteger()) + 1) % 7;

    def SetFromJulian(self,jd):
        z = math.floor(jd + 0.5)
        f = (jd + 0.5) - z
        if z < 2299161.0:
            A = z
        else:
            alpha = math.floor((z - 1867216.25)/36524.25)
            A = z + 1.0 + alpha - math.floor(alpha/4.0)

        B = A + 1524
        C = math.floor((B - 122.1)/365.25)
        D = math.floor(365.25 * C)
        E = math.floor((B - D)/30.6001)
        self.day = int(math.floor(B - D - floor(30.6001 * E) + f))
        if E < 14:
            self.month = int(E - 1)
        else:
            self.month = int(E - 13)
        if self.month > 2:
            self.year = int(C - 4716)
        else:
            self.year = int(C - 4715)
        self.tzone = 0.0
        self.shour = GCMath.getFraction(jd + 0.5)

    def Clear(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.shour = 0.0
        self.tzone = 0.0

    def Set(self,ta):
        self.year = ta.year
        self.month = ta.month
        self.day = ta.day
        self.shour = ta.shour
        self.tzone = ta.tzone
        self.dayOfWeek = ta.dayOfWeek

    def IsBeforeThis(self,date):
        if self.year > date.year: return False
        if self.year < date.year: return True

        if self.month > date.month: return False
        if self.month < date.month: return True

        return self.day < date.day

    def Today(self):
        d = datetime.datetime.now()
        self.year = d.year
        self.month = d.month
        self.day = d.day
        self.shour = 0.5
        self.tzone = 0
        self.dayOfWeek = d.weekday()

    def CompareYMD(self,v):
        if v.year < self.year:
            return (self.year - v.year) * 365
        if v.year > self.year:
            return (self.year - v.year) * 365;

        if v.month < self.month:
            return (self.month - v.month)*31
        if v.month > self.month:
            return (self.month - v.month)*31

        return self.day - v.day

    def GetHour(self):
        return int(math.floor(self.shour*24))

    def GetMinute(self):
        return int(math.floor(GCMath.getFraction(self.shour*24) * 60))

    def GetMinuteRound(self):
        return int(math.floor(GCMath.getFraction(self.shour*24) * 60 + 0.5))

    def GetDayInteger(self):
        return self.year * 384 + self.month * 32 + self.day

    def GetSecond(self):
        return int(math.floor(GCMath.getFraction(self.shour*1440) * 60))

    def GetDateTextWithTodayExt(self):
        if (self.day > 0) and (self.day < 32) and (self.month > 0) \
            and (self.month < 13) and (self.year >= 1500) and (self.year < 4000):
            today = GCGregorianDate()
            diff = today.GetJulianInteger() - self.GetJulianInteger()
            if diff == 0:
                return str(self) + ' ' + GCStrings.getString(43)
            elif diff == -1:
                return str(self) + ' ' + GCStrings.getString(854)
            elif diff == 1:
                return str(self) + ' ' + GCStrings.getString(853)
            else:
                return str(self)

def Today():
    vc = GCGregorianDate()
    vc.Today()
    return vc

def unittests():
    GCUT.info('GCGregorianDate')
    t = GCGregorianDate()
    GCUT.val(t.day,0,'zero day')
    t.Today()
    GCUT.nval(t.day,0,'init day')
    GCUT.nval(t.month,0,'init month')
    GCUT.msg('Today: ' + str(t))
    GCUT.msg('Now: ' + repr(t))
