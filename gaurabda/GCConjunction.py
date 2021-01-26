from .GCGregorianDate import GCGregorianDate,Today
from . import GCEarthData as GCEarthData
from . import GCMath as GCMath
import math
from . import GCUT as GCUT
from . import GCMoonData as GCMoonData
from . import GCSunData as GCSunData



#********************************************************************/
#                                                                   */
#  m1 - previous moon position                                      */
#  m2 - next moon position                                          */
#  s1 - previous sun position                                       */
#  s2 - next sun position                                           */
#                                                                   */
#  Test for conjunction of the sun and moon                         */
#  m1,s1 is in one time moment                                      */
#  m2,s2 is in second time moment                                   */
#                                                                   */
#  this function tests whether conjunction occurs between           */
#  these two moments                                                */
#                                                                   */
#********************************************************************/

def IsConjunction(m1, s1, s2, m2):
    if m2 < m1: m2 += 360.0
    if s2 < s1: s2 += 360.0
    if (m1 <= s1) and (s1 < s2) and (s2 <= m2):
        return True

    m1 = GCMath.putIn180(m1)
    m2 = GCMath.putIn180(m2)
    s1 = GCMath.putIn180(s1)
    s2 = GCMath.putIn180(s2)

    return (m1 <= s1) and (s1 < s2) and (s2 <= m2)

###################################/
# GET PREVIOUS CONJUNCTION OF THE SUN AND MOON
#
# THIS IS HELP FUNCTION FOR GetPrevConjunction(GCGregorianDate test_date,
#                                         GCGregorianDate &found, bool this_day, EARTHDATA earth)
#
# looking for previous sun-moon conjunction
# it starts from input day from 12:00 AM (noon) UTC
# so output can be the same day
# if output is the same day, then conjunction occurs between 00:00 AM and noon of this day
#
# date - input / output
# earth - input
# return value - sun longitude in degs
#
# error is when return value is greater than 999.0 deg

def GetPrevConjunction(date, earth, forward=False):
    prevSun = 0.0
    prevMoon = 0.0
    prevDiff = 0.0
    nowSun = 0.0
    nowMoon = 0.0
    nowDiff = 0.0
    dir = 1.0 if forward else -1.0
    moon = GCMoonData.MOONDATA()


    d = GCGregorianDate(date=date)
    d.shour = 0.5
    d.tzone = 0.0
    jd = d.GetJulian()

    # set initial data for input day
    # NOTE: for grenwich
    moon.Calculate(jd, earth)
    prevSun = GCSunData.GetSunLongitude(d)
    prevMoon = moon.longitude_deg
    prevDiff = GCMath.putIn180(prevSun - prevMoon)

    for bCont in range(32):
        if forward:
            d.NextDay()
        else:
            d.PreviousDay()
        jd += dir
        moon.Calculate(jd, earth)
        nowSun = GCSunData.GetSunLongitude(d)
        nowMoon = moon.longitude_deg
        nowDiff = GCMath.putIn180(nowSun - nowMoon)

        if IsConjunction(nowMoon, nowSun, prevSun, prevMoon):
            # now it calculates actual time and zodiac of conjunction
            if prevDiff == nowDiff: return 0
            x = math.fabs(nowDiff) / math.fabs(prevDiff - nowDiff)
            if x < 0.5:
                if forward: d.PreviousDay()
                d.shour = x + 0.5
            else:
                if not forward: d.NextDay()
                d.shour = x - 0.5
            date.Set(d)
            prevSun = GCMath.putIn360(prevSun)
            nowSun = GCMath.putIn360(nowSun)
            if math.fabs(prevSun - nowSun) > 10.0:
                return GCMath.putIn180(nowSun) + (GCMath.putIn180(prevSun) - GCMath.putIn180(nowSun))*x
            else:
                return nowSun + (prevSun - nowSun)*x
        prevSun = nowSun
        prevMoon = nowMoon
        prevDiff = nowDiff

    return 1000.0

###################################/
# GET NEXT CONJUNCTION OF THE SUN AND MOON
#
# Help function for GetNextConjunction(GCGregorianDate test_date, GCGregorianDate &found,
#                                      bool this_day, EARTHDATA earth)
#
# looking for next sun-moon conjunction
# it starts from input day from 12:00 AM (noon) UTC
# so output can be the same day
# if output is the same day, then conjunction occurs
# between noon and midnight of this day
#
# date - input / output
# earth - input
# return value - sun longitude
#
# error is when return value is greater than 999.0 deg

def GetNextConjunction(date, earth):
    return GetPrevConjunction(date, earth, forward=True)

#********************************************************************/
#                                                                   */
#                                                                   */
#                                                                   */
#                                                                   */
#                                                                   */
#********************************************************************/

def GetPrevConjunctionEx(test_date, found, this_conj, earth, forward = False):
    phi = 12.0
    dir = 1.0 if forward else -1.0
    if this_conj:
        test_date.shour += 0.2 * dir
        test_date.NormalizeHours()


    jday = test_date.GetJulianComplete()
    moon = GCMoonData.MOONDATA()
    d = GCGregorianDate(date = test_date)
    xd = GCGregorianDate()
    scan_step = 1.0
    prev_tit = 0
    new_tit = -1

    moon.Calculate(jday, earth)
    sunl = GCSunData.GetSunLongitude(d)
    l1 = GCMath.putIn180(moon.longitude_deg - sunl)
    prev_tit = int(math.floor(l1/phi))

    counter=0
    while counter<20:
        xj = jday
        xd.Set(d)

        jday += scan_step*dir
        d.shour += scan_step*dir
        d.NormalizeHours()

        moon.Calculate(jday, earth)
        sunl = GCSunData.GetSunLongitude(d)
        l2 = GCMath.putIn180(moon.longitude_deg - sunl)
        new_tit = int(math.floor(l2/phi))

        if forward:
            is_change = prev_tit < 0 and new_tit >= 0
        else:
            is_change = prev_tit >= 0 and new_tit < 0

        if is_change:
            jday = xj
            d.Set(xd)
            scan_step *= 0.5
            counter+=1
        else:
            l1 = l2
            prev_tit = new_tit

    found.Set(d)
    return sunl

#********************************************************************/
#                                                                   */
#                                                                   */
#                                                                   */
#                                                                   */
#                                                                   */
#********************************************************************/

def GetNextConjunctionEx(test_date, found, this_conj, earth):
    return GetPrevConjunctionEx(test_date, found, this_conj, earth, forward = True)


def unittests():
    GCUT.info('conjunctions')
    b = IsConjunction(10, 11, 12, 20)
    GCUT.val(b,True,'is conjunction')

    e = GCEarthData.EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = Today()
    vc2 = GCGregorianDate(date = vc)
    vc3 = GCGregorianDate(date = vc)

    l = GetPrevConjunction(vc2,e)
    GCUT.msg('Conjunction on: {}'.format(repr(vc2)))
    vc2.Set(vc)
    l = GetNextConjunctionEx(vc2,vc3,True,e)
    GCUT.msg('Conjunction on: {}'.format(repr(vc3)))
