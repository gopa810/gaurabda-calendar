import os
import os.path
import json
import math
from .GCGregorianDate import GCGregorianDate,GetMonthMaxDays
from . import GCUT as GCUT

gzone = []

def LoadFile(fileName):
    global gzone
    if not os.path.exists(fileName):
        fileName = os.path.join(os.path.dirname(__file__), 'res', 'timezones.json')
    with open(fileName,'rt',encoding='utf-8') as json_file:
        gzone = json.load(json_file)

def ID2INDEX(_id):
    for i,t in enumerate(gzone):
        if t['id'] == _id:
            return i
    return None

def GetTimeZone(id=None,index=None,name=None):
    if name!=None:
        for tidx,t in enumerate(gzone):
            if t['name']==name:
                index = tidx
    if id!=None:
        index=ID2INDEX(id)
    if index==None:
        raise
    return gzone[index]

def GetTimeZones():
    return [g['name'] for g in gzone]

def GetTimeZoneName(id=None,index=None):
    if id!=None:
        index=ID2INDEX(id)
    if index==None:
        raise
    return gzone[index]['name']

def GetTimeZoneOffset(id=None,index=None):
    if id!=None:
        index=ID2INDEX(id)
    if index==None:
        raise
    return gzone[index]['offset']/60.0

def GetTimeZoneOffsetInteger(id=None,index=None):
    if id!=None:
        index=ID2INDEX(id)
    if index==None:
        raise
    return gzone[index]['offset']

def GetTimeZoneCount():
    return len(gzone)

def GetTimeZoneBias(id=None,index=None):
    if id!=None:
        index=ID2INDEX(id)
    if index==None:
        raise
    return gzone[index]['bias']

def GetDaylightTimeStartDate(nDst,nYear):
    nDst = ID2INDEX(nDst)
    a = gzone[nDst]

    vcStart = GCGregorianDate()
    vcStart.day = 1
    vcStart.month = a['startMonth']
    vcStart.year = nYear;
    if a['startType'] == 1:
        vcStart.day = a['startWeek']
    else:
        if a['startWeek'] == 5:
            vcStart.day = GetMonthMaxDays(nYear, a['startMonth'])
            vcStart.InitWeekDay()
            while vcStart.dayOfWeek != a['startDay']:
                vcStart.PreviousDay()
        else:
            vcStart.day = 1
            vcStart.InitWeekDay()
            while vcStart.dayOfWeek != a['startDay']:
                vcStart.NextDay()
            vcStart.day += a['startWeek'] * 7
    vcStart.shour = 1/24.0
    return vcStart


def GetNormalTimeStartDate(nDst,nYear):
    vcStart = GCGregorianDate()
    vcStart.day = 1
    vcStart.month = 10
    vcStart.year = nYear
    vcStart.shour = 3/24.0
    return vcStart


def GetID(p):
    for a in gzone:
        if a['name']==p:
            return a['id']
    for a in gzone:
        if a['name'].startswith(p):
            return a['id']
    return int(p)

def GetTimeZoneOffsetText(d):
    sig = 1
    if d < 0.0:
        sig = -1
        d = -d
    else:
        sig = 1
    a4 = int(math.floor(d))
    a5 = int(math.floor((d - a4)*60 + 0.5))
    ss = '+' if sig>0 else '-'

    return '{}{:d}:{:02d}'.format(ss, a4, a5)

def GetTimeZoneOffsetTextArg(d):
    sig = 1
    if d < 0.0:
        sig = -1
        d = -d
    else:
        sig = 1
    a4 = int(math.floor(d))
    a5 = int(math.floor((d - a4)*60 + 0.5))
    ss = 'E' if sig>0 else 'W'

    return '{:d}{}{:02d}'.format(a4, ss, a5)


# n - is order number of given day
# x - is number of day in week (0-sunday, 1-monday, ..6-saturday)
# if x >= 5, then is calculated whether day is after last x-day

def is_n_xday(vc, n, x):
    xx = [1, 7, 6, 5, 4, 3, 2]

    # prvy den mesiaca
    fdm = xx[ (7 + vc.day - vc.dayOfWeek) % 7 ]

    # 1. x-day v mesiaci ma datum
    fxdm = xx[ (fdm - x + 7) % 7 ]

    # n-ty x-day ma datum
    if (n < 0) or (n >= 5):
        nxdm = fxdm + 28
        max = GetMonthMaxDays(vc.year, vc.month)
        while nxdm > max:
            nxdm -= 7
    else:
        nxdm = fxdm + (n - 1)* 7

    if vc.day >= nxdm: return 1
    return 0

# This table has 8 items for each line:
#  [0]: starting month
#  [4]: ending month
#
#  [1]: type of day, 0-day is given as n-th x-day of month, 1- day is given as DATE
#  [2]: for [1]==1 this means day of month
#     : for [1]==0 this order number of occurance of the given day (1,2,3,4 is acceptable, 5 means *last*)
#  [3]: used only for [1]==0, and this means day of week (0=sunday,1=monday,2=tuesday,3=wednesday,...)
#     : [1] to [3] are used for starting month
#  [5] to [7] is used for ending month in the same way as [1] to [3] for starting month
#
# EXAMPLE: (first line)   3 0 5 0 10 0 5 0
# [0] == 3, that means starting month is March
# [1] == 0, that means starting system is (day of week)
# [2] == 5, that would mean that we are looking for 5th occurance of given day in the month, but 5 here means,
#           that we are looking for *LAST* occurance of given day
# [3] == 0, this is *GIVEN DAY*, and it is SUNDAY
#
#         so, DST is starting on last sunday of March
#
# similarly analysed, DST is ending on last sunday of October
#

def GetDaylightBias(vc,tz):
    bias = 1
    if vc.month == tz['startMonth']:
        if tz['startType'] == 0:
            return is_n_xday(vc, tz['startWeek'], tz['startDay']) * bias
        else:
            return bias if vc.day >= tz['startWeek'] else 0
    elif vc.month == tz['endMonth']:
        if tz['endType'] == 0:
            return (1 - is_n_xday(vc, tz['endWeek'], tz['endDay']))*bias
        else:
            return 0 if vc.day >= tz['endWeek'] else bias
    else:
        if tz['startMonth'] > tz['endMonth']:
            # zaciatocny mesiac ma vyssie cislo nez koncovy
            # napr. pre australiu
            if (vc.month > tz['startMonth']) or (vc.month < tz['endMonth']):
                return bias
        else:
            # zaciatocny mesiac ma nizsie cislo nez koncovy
            # usa, europa, asia
            if (vc.month > tz['startMonth']) or (vc.month < tz['endMonth']):
                return bias

        return 0


def determineDaylightStatus(vc, id=None,index=None):
    if id != None:
        index = ID2INDEX(id)
    if index==None: raise
    return GetDaylightBias(vc, gzone[index]);

# return values
# 0 - DST is off, yesterday was off
# 1 - DST is on, yesterday was off
# 2 - DST is on, yesterday was on
# 3 - DST is off, yesterday was on
def determineDaylightChange(vc2,nIndex):
    t2 = determineDaylightStatus(vc2, nIndex)
    vc3 = GCGregorianDate()
    vc3.Set(vc2)
    vc3.PreviousDay()
    t1 = determineDaylightStatus(vc3, nIndex)
    if t1:
        if t2:
            return 2
        else:
            return 3
    elif t2:
        return 1
    else:
        return 0


def unittests():
    GCUT.info('timezones')
    LoadFile('timezones.json')
    GCUT.msg('Timezones:' + str(len(gzone)))
    tz = GetTimeZone(id=321)
    vc = GCGregorianDate(year=2020,month=4,day=4)
    GCUT.val(GetDaylightBias(vc,tz),1,'daylight bias')
    GCUT.val(GetTimeZoneOffsetText(1.0),'+1:00','offset text')
