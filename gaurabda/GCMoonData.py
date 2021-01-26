import math

from . import GCEarthData as GCEarthData
from . import GCGregorianDate as GCGregorianDate
from . import GCTime as GCTime
from . import GCCoords as GCCoords
from . import GCUT as GCUT
from . import GCMath as GCMath
from . import GCAyanamsha as GCAyanamsha

class MOONDATA:
    def __init__(self):
        #   latitude from nodal (draconic) phase
        self.latitude_deg = 0.0
        #   longitude from sidereal motion
        self.longitude_deg = 0.0
        self.radius = 0.0
        self.rektaszension = 0.0
        self.declination = 0.0
        self.parallax = 0.0
        self.elevation = 0.0
        self.azimuth = 0.0

    def CalculateEcliptical(self,jdate):
        arg_lr = [
             [ 0, 0, 1, 0], [ 2, 0,-1, 0],     [ 2, 0, 0, 0],     [ 0, 0, 2, 0],
             [ 0, 1, 0, 0],     [ 0, 0, 0, 2],     [ 2, 0,-2, 0],     [ 2,-1,-1, 0],
             [ 2, 0, 1, 0],     [ 2,-1, 0, 0],     [ 0, 1,-1, 0],     [ 1, 0, 0, 0],
             [ 0, 1, 1, 0],     [ 2, 0, 0,-2],     [ 0, 0, 1, 2],     [ 0, 0, 1,-2],
             [ 4, 0,-1, 0],     [ 0, 0, 3, 0],     [ 4, 0,-2, 0],     [ 2, 1,-1, 0],
             [ 2, 1, 0, 0],     [ 1, 0,-1, 0],     [ 1, 1, 0, 0],     [ 2,-1, 1, 0],
             [ 2, 0, 2, 0],     [ 4, 0, 0, 0],     [ 2, 0,-3, 0],     [ 0, 1,-2, 0],
             [ 2, 0,-1, 2],     [ 2,-1,-2, 0],     [ 1, 0, 1, 0],     [ 2,-2, 0, 0],
             [ 0, 1, 2, 0],     [ 0, 2, 0, 0],     [ 2,-2,-1, 0],     [ 2, 0, 1,-2],
             [ 2, 0, 0, 2],     [ 4,-1,-1, 0],     [ 0, 0, 2, 2],     [ 3, 0,-1, 0],
             [ 2, 1, 1, 0],     [ 4,-1,-2, 0],     [ 0, 2,-1, 0],     [ 2, 2,-1, 0],
             [ 2, 1,-2, 0],     [ 2,-1, 0,-2],     [ 4, 0, 1, 0],     [ 0, 0, 4, 0],
             [ 4,-1, 0, 0],     [ 1, 0,-2, 0],     [ 2, 1, 0,-2],     [ 0, 0, 2,-2],
             [ 1, 1, 1, 0],     [ 3, 0,-2, 0],     [ 4, 0,-3, 0],     [ 2,-1, 2, 0],
             [ 0, 2, 1, 0],     [ 1, 1,-1, 0],     [ 2, 0, 3, 0],     [ 2, 0,-1,-2]]

        arg_b = [[ 0, 0, 0, 1],     [ 0, 0, 1, 1],     [ 0, 0, 1,-1],     [ 2, 0, 0,-1],
                [ 2, 0,-1, 1],     [ 2, 0,-1,-1],     [ 2, 0, 0, 1],     [ 0, 0, 2, 1],
                [ 2, 0, 1,-1],     [ 0, 0, 2,-1],  [ 2,-1, 0,-1],     [ 2, 0,-2,-1],
                [ 2, 0, 1, 1],     [ 2, 1, 0,-1],     [ 2,-1,-1, 1],     [ 2,-1, 0, 1],
                [ 2,-1,-1,-1],     [ 0, 1,-1,-1],     [ 4, 0,-1,-1],     [ 0, 1, 0, 1],
                [ 0, 0, 0, 3],     [ 0, 1,-1, 1],     [ 1, 0, 0, 1],     [ 0, 1, 1, 1],
                [ 0, 1, 1,-1],     [ 0, 1, 0,-1],     [ 1, 0, 0,-1],     [ 0, 0, 3, 1],
                [ 4, 0, 0,-1],     [ 4, 0,-1, 1],     [ 0, 0, 1,-3],     [ 4, 0,-2, 1],
                [ 2, 0, 0,-3],     [ 2, 0, 2,-1],     [ 2,-1, 1,-1],     [ 2, 0,-2, 1],
                [ 0, 0, 3,-1],     [ 2, 0, 2, 1],     [ 2, 0,-3,-1],     [ 2, 1,-1, 1],
                [ 2, 1, 0, 1],     [ 4, 0, 0, 1],     [ 2,-1, 1, 1],     [ 2,-2, 0,-1],
                [ 0, 0, 1, 3],     [ 2, 1, 1,-1],     [ 1, 1, 0,-1],     [ 1, 1, 0, 1],
                [ 0, 1,-2,-1],     [ 2, 1,-1,-1],     [ 1, 0, 1, 1],     [ 2,-1,-2,-1],
                [ 0, 1, 2, 1],     [ 4, 0,-2,-1],     [ 4,-1,-1,-1],     [ 1, 0, 1,-1],
                [ 4, 0, 1,-1],     [ 1, 0,-1,-1],     [ 4,-1, 0,-1],     [ 2,-2, 0, 1]]
        sigma_r = [-20905355, -3699111, -2955968,  -569925,
               48888,    -3149,   246158,  -152138,
             -170733,  -204586,  -129620,   108743,
              104755,    10321,        0,    79661,
              -34782,   -23210,   -21636,    24208,
               30824,    -8379,   -16675,   -12831,
              -10445,   -11650,    14403,    -7003,
                   0,    10056,     6322,    -9884,
                5751,        0,    -4950,     4130,
                   0,    -3958,        0,     3258,
                2616,    -1897,    -2117,     2354,
                   0,        0,    -1423,    -1117,
               -1571,    -1739,        0,    -4421,
                   0,        0,        0,        0,
                1165,        0,        0,     8752]

        sigma_l = [6288774, 1274027,  658314,  213618,
            -185116, -114332,   58793,   57066,
              53322,   45758,  -40923,  -34720,
             -30383,   15327,  -12528,   10980,
              10675,   10034,    8548,   -7888,
              -6766,   -5163,    4987,    4036,
               3994,    3861,    3665,   -2689,
              -2602,    2390,   -2348,    2236,
              -2120,   -2069,    2048,   -1773,
              -1595,    1215,   -1110,    -892,
               -810,     759,    -713,    -700,
                691,     596,     549,     537,
                520,    -487,    -399,    -381,
                351,    -340,     330,     327,
               -323,     299,     294,       0]

        sigma_b = [5128122,  280602,  277693,  173237,
              55413,   46271,   32573,   17198,
               9266,    8822,    8216,    4324,
               4200,   -3359,    2463,    2211,
               2065,   -1870,    1828,   -1794,
              -1749,   -1565,   -1491,   -1475,
              -1410,   -1344,   -1335,    1107,
               1021,     833,     777,     671,
                607,     596,     491,    -451,
                439,     422,     421,    -366,
               -351,     331,     315,     302,
               -283,    -229,     223,     223,
               -220,    -220,    -185,     181,
               -177,     176,     166,    -164,
                132,    -119,     115,     107]

        t = (jdate - 2451545.0)/36525.0

        #  (* mean elongation of the moon
        d = 297.8502042+(445267.1115168+(-0.0016300+(1.0/545868-1.0/113065000*t)*t)*t)*t

        #  (* mean anomaly of the sun
        m = 357.5291092+(35999.0502909+(-0.0001536+1.0/24490000*t)*t)*t

        #  (* mean anomaly of the moon
        ms = 134.9634114+(477198.8676313+(0.0089970+(1.0/69699-1.0/1471200*t)*t)*t)*t

        #  (* argument of the longitude of the moon
        f = 93.2720993+(483202.0175273+(-0.0034029+(-1.0/3526000+1.0/863310000*t)*t)*t)*t

        #  (* correction term due to excentricity of the earth orbit
        e = 1.0+(-0.002516-0.0000074*t)*t

        #  (* mean longitude of the moon
        ls = 218.3164591+(481267.88134236+(-0.0013268+(1.0/538841-1.0/65194000*t)*t)*t)*t

        #  (* arguments of correction terms
        a1 = 119.75+131.849*t
        a2 = 53.09+479264.290*t
        a3 = 313.45+481266.484*t

        sr = 0
        for i in range(60):
            temp =sigma_r[i]*GCMath.cosDeg( arg_lr[i][0]*d +arg_lr[i][1]*m +arg_lr[i][2]*ms +arg_lr[i][3]*f)
            if math.fabs(arg_lr[i][1])==1: temp = temp*e
            if math.fabs(arg_lr[i][1])==2: temp = temp*e*e
            sr =sr+temp

        sl = 0
        for i in range(60):
            temp =sigma_l[i]*GCMath.sinDeg( arg_lr[i][0]*d +arg_lr[i][1]*m +arg_lr[i][2]*ms +arg_lr[i][3]*f)
            if math.fabs(arg_lr[i][1])==1: temp =temp*e
            if math.fabs(arg_lr[i][1])==2: temp =temp*e*e
            sl =sl+temp

        #  (* correction terms
        sl =sl +3958*GCMath.sinDeg(a1) \
            +1962*GCMath.sinDeg(ls-f) \
            +318*GCMath.sinDeg(a2)
        sb = 0
        for i in range(60):
            temp = sigma_b[i]*GCMath.sinDeg( arg_b[i][0]*d + arg_b[i][1]*m + arg_b[i][2]*ms + arg_b[i][3]*f)
            if math.fabs(arg_b[i][1])==1: temp=temp*e
            if math.fabs(arg_b[i][1])==2: temp=temp*e*e
            sb=sb+temp

        #  (* correction terms
        sb =sb - 2235*GCMath.sinDeg(ls) + 382*GCMath.sinDeg(a3)  + 175*GCMath.sinDeg(a1-f) + 175*GCMath.sinDeg(a1+f)  +127*GCMath.sinDeg(ls-ms) - 115*GCMath.sinDeg(ls+ms)

        coords = GCCoords.GCEclipticalCoords()

        coords.longitude = ls+sl/1000000
        coords.latitude = sb/1000000
        coords.distance = 385000.56+sr/1000

        return coords

    def Calculate(self,jdate,earth):
        crd = self.CalculateEcliptical(jdate)
        eqc,crd = GCEarthData.eclipticalToEquatorialCoords(crd, jdate)

        self.radius = crd.distance
        self.longitude_deg =crd.longitude
        self.latitude_deg = crd.latitude

        self.rektaszension = eqc.rightAscension
        self.declination = eqc.declination

    def calc_horizontal(self,date, longitude, latitude):
        h = GCMath.putIn360(GCEarthData.star_time(date) - self.rektaszension+longitude)

        self.azimuth = GCMath.rad2deg( math.atan2(GCMath.sinDeg(h), GCMath.cosDeg(h)*GCMath.sinDeg(latitude) - GCMath.tanDeg(self.declination)*GCMath.cosDeg(latitude) ))

        self.elevation = GCMath.rad2deg( math.asin( GCMath.sinDeg(latitude) * GCMath.sinDeg(self.declination) + GCMath.cosDeg(latitude) * GCMath.cosDeg(self.declination) * GCMath.cosDeg(h)))

    def  correct_position(self, jdate, latitude, longitude, height):
        b_a=0.99664719

        u =GCMath.arcTanDeg(b_a*b_a*GCMath.tanDeg(latitude))
        rho_sin =b_a*GCMath.sinDeg(u)+height/6378140.0*GCMath.sinDeg(latitude)
        rho_cos =GCMath.cosDeg(u)+height/6378140.0*GCMath.cosDeg(latitude)

        self.parallax = GCMath.arcSinDeg(GCMath.sinDeg(8.794/3600)/(MoonDistance(jdate) / GCMath.AU))

        h = GCEarthData.star_time(jdate) - longitude - self.rektaszension;
        delta_alpha = GCMath.arcTanDeg( (-rho_cos*GCMath.sinDeg(self.parallax)*GCMath.sinDeg(h)) / (GCMath.cosDeg(self.declination) - rho_cos*GCMath.sinDeg(self.parallax)*GCMath.cosDeg(h)))
        self.rektaszension = self.rektaszension+delta_alpha
        self.declination =GCMath.arcTanDeg( (( GCMath.sinDeg(self.declination) -rho_sin*GCMath.sinDeg(self.parallax))*GCMath.cosDeg(delta_alpha))/ ( GCMath.cosDeg(self.declination) -rho_cos*GCMath.sinDeg(self.parallax)*GCMath.cosDeg(h)))

    def getTopocentricEquatorial(self, obs, jdate):
        b_a = 0.99664719
        tec = GCCoords.GCEquatorialCoords()

        altitude = 0

        #   geocentric position of observer on the earth surface
        #   10.1 - 10.3
        u = GCMath.arcTanDeg(b_a * b_a * GCMath.tanDeg(obs.latitude_deg))
        rho_sin = b_a * GCMath.sinDeg(u) + altitude / 6378140.0 * GCMath.sinDeg(obs.latitude_deg)
        rho_cos = GCMath.cosDeg(u) + altitude / 6378140.0 * GCMath.cosDeg(obs.latitude_deg)

        #   equatorial horizontal paralax
        #   39.1
        parallax = GCMath.arcSinDeg(GCMath.sinDeg(8.794 / 3600) / (self.radius / GCMath.AU))

        #   geocentric hour angle of the body
        h = GCEarthData.star_time(jdate) + obs.longitude_deg - self.rektaszension


        #   39.2
        delta_alpha = GCMath.arcTanDeg( (-rho_cos * GCMath.sinDeg(self.parallax) * GCMath.sinDeg(h)) / (GCMath.cosDeg(self.declination) - rho_cos * GCMath.sinDeg(self.parallax) * GCMath.cosDeg(h)))
        tec.rightAscension = self.rektaszension + delta_alpha
        tec.declination = GCMath.arcTanDeg( ((GCMath.sinDeg(self.declination) - rho_sin * GCMath.sinDeg(self.parallax)) * GCMath.cosDeg(delta_alpha)) / (GCMath.cosDeg(self.declination) - rho_cos * GCMath.sinDeg(self.parallax) * GCMath.cosDeg(h)))

        return tec



def MoonCalcElevation(e,vc):
    moon = MOONDATA()
    d = vc.GetJulianComplete()
    moon.Calculate(d, e)
    moon.correct_position(d, e.latitude_deg, e.longitude_deg, 0)
    moon.calc_horizontal(d, e.longitude_deg, e.latitude_deg)

    return moon.elevation

def CalcMoonTimes(e,vc,nDaylightSavingShift):
    rise = GCTime.GCTime()
    set = GCTime.GCTime()

    UT = 0.0
    i = 0
    prev_elev = 0.0
    nType = 0
    nFound = 0

    rise.SetValue(-1)
    set.SetValue(-1)

    #   inicializacia prvej hodnoty ELEVATION
    vc.shour = (-nDaylightSavingShift - 1.0) / 24.0
    prev_elev = MoonCalcElevation(e, vc)

    #   prechod cez vsetky hodiny
    UT = - 0.1 - nDaylightSavingShift
    while UT <= (24.1 - nDaylightSavingShift):
        vc.shour = UT / 24.0
        elev = MoonCalcElevation(e, vc)
        if prev_elev * elev <= 0.0:
            if prev_elev <= 0.0:
                nType = 0x1
            else:
                nType = 0x2

            a = UT - 1.0
            ae = prev_elev
            b = UT
            be = elev
            for i in range(20):
                c = (a + b) / 2.0
                vc.shour = c / 24.0
                ce = MoonCalcElevation(e, vc)
                if ae*ce <= 0.0:
                    be = ce
                    b = c
                else:
                    ae = ce
                    a = c

            if nType == 1:
                rise.SetDayTime((c + nDaylightSavingShift)/24.0)
            else:
                set.SetDayTime((c + nDaylightSavingShift)/24.0)
            nFound |= nType
            if nFound == 0x3: break
        prev_elev = elev
        UT+=1.0
    return rise,set

def GetNextMoonRasi(ed,startDate):
    nextDate = GCGregorianDate.GCGregorianDate(date=startDate)
    phi = 30.0
    jday = startDate.GetJulianComplete()
    moon = MOONDATA()
    d = GCGregorianDate.GCGregorianDate(date=startDate)
    ayanamsa = GCAyanamsha.GetAyanamsa(jday)
    scan_step = 0.5
    prev_naks = 0
    new_naks = -1

    xj = 0.0
    xd = GCGregorianDate.GCGregorianDate()

    moon.Calculate(jday, ed)
    l1 = GCMath.putIn360(moon.longitude_deg - ayanamsa)
    prev_naks = int(GCMath.Floor(l1 / phi))

    counter = 0
    while counter < 20:
        xj = jday
        xd.Set(d)

        jday += scan_step
        d.shour += scan_step
        if d.shour > 1.0:
            d.shour -= 1.0
            d.NextDay()

        moon.Calculate(jday, ed)
        l2 = GCMath.putIn360(moon.longitude_deg - ayanamsa);
        new_naks = int(GCMath.Floor(l2/phi))
        if prev_naks != new_naks:
            jday = xj
            d.Set(xd)
            scan_step *= 0.5
            counter+=1
            continue
        else:
            l1 = l2
    nextDate.Set(d)
    return new_naks,nextDate


def GetNextRise(e, vc, bRise):
    nFound = 0
    h = [0, 0, 0]
    hour = 1/24.0
    startHour = vc.shour

    track = GCGregorianDate.GCGregorianDate(date = vc)
    track.NormalizeValues()

    #   inicializacia prvej hodnoty ELEVATION
    h[0] = MoonCalcElevation(e, track)
    track.shour += hour
    h[1] = MoonCalcElevation(e, track)
    track.shour += hour
    h[2] = MoonCalcElevation(e, track)

    for c in range(24):
        has_change = False
        if bRise:
            has_change = h[1] < 0.0 and h[2] > 0.0
        else:
            has_change = h[1] > 0.0 and h[2] < 0.0
        if has_change:
            a = (h[2] - h[1]) / hour
            b = h[2] - a * track.shour
            track.shour = - b / a
            track.NormalizeValues()
            return track

        h[0] = h[1]
        h[1] = h[2]
        track.shour += hour
        h[2] = MoonCalcElevation(e, track)

    return track



def MoonDistance(jdate):
    arg_lr = [
         [ 0, 0, 1, 0], [ 2, 0,-1, 0], [ 2, 0, 0, 0], [ 0, 0, 2, 0], [ 0, 1, 0, 0],
         [ 0, 0, 0, 2], [ 2, 0,-2, 0], [ 2,-1,-1, 0], [ 2, 0, 1, 0], [ 2,-1, 0, 0],
         [ 0, 1,-1, 0], [ 1, 0, 0, 0], [ 0, 1, 1, 0], [ 2, 0, 0,-2], [ 0, 0, 1, 2],
         [ 0, 0, 1,-2], [ 4, 0,-1, 0], [ 0, 0, 3, 0], [ 4, 0,-2, 0], [ 2, 1,-1, 0],
         [ 2, 1, 0, 0], [ 1, 0,-1, 0], [ 1, 1, 0, 0], [ 2,-1, 1, 0], [ 2, 0, 2, 0],
         [ 4, 0, 0, 0], [ 2, 0,-3, 0], [ 0, 1,-2, 0], [ 2, 0,-1, 2], [ 2,-1,-2, 0],
         [ 1, 0, 1, 0], [ 2,-2, 0, 0], [ 0, 1, 2, 0], [ 0, 2, 0, 0], [ 2,-2,-1, 0],
         [ 2, 0, 1,-2], [ 2, 0, 0, 2], [ 4,-1,-1, 0], [ 0, 0, 2, 2], [ 3, 0,-1, 0],
         [ 2, 1, 1, 0], [ 4,-1,-2, 0], [ 0, 2,-1, 0], [ 2, 2,-1, 0], [ 2, 1,-2, 0],
         [ 2,-1, 0,-2], [ 4, 0, 1, 0], [ 0, 0, 4, 0], [ 4,-1, 0, 0], [ 1, 0,-2, 0],
         [ 2, 1, 0,-2], [ 0, 0, 2,-2], [ 1, 1, 1, 0], [ 3, 0,-2, 0], [ 4, 0,-3, 0],
         [ 2,-1, 2, 0], [ 0, 2, 1, 0], [ 1, 1,-1, 0], [ 2, 0, 3, 0], [ 2, 0,-1,-2]
       ]

    sigma_r = [
       -20905355, -3699111, -2955968,  -569925,    48888,    -3149,   246158,
         -152138,  -170733,  -204586,  -129620,   108743,   104755,    10321,
               0,    79661,   -34782,   -23210,   -21636,    24208,    30824,
           -8379,   -16675,   -12831,   -10445,   -11650,    14403,    -7003,
               0,    10056,     6322,    -9884,     5751,        0,    -4950,
            4130,        0,    -3958,        0,     3258,     2616,    -1897,
           -2117,     2354,        0,        0,    -1423,    -1117,    -1571,
           -1739,        0,    -4421,        0,        0,        0,        0,
            1165,        0,        0,     8752
      ]


    t = (jdate - 2451545.0)/36525.0

    #  (* mean elongation of the moon
    d = 297.8502042+(445267.1115168+(-0.0016300+(1.0/545868-1.0/113065000*t)*t)*t)*t

    #  (* mean anomaly of the sun
    m = 357.5291092+(35999.0502909+(-0.0001536+1.0/24490000*t)*t)*t

    #  (* mean anomaly of the moon
    ms = 134.9634114+(477198.8676313+(0.0089970+(1.0/69699-1.0/1471200*t)*t)*t)*t

    #  (* argument of the longitude of the moon
    f = 93.2720993+(483202.0175273+(-0.0034029+(-1.0/3526000+1.0/863310000*t)*t)*t)*t

    #  (* correction term due to excentricity of the earth orbit
    e = 1.0+(-0.002516-0.0000074*t)*t

    #  (* mean longitude of the moon
    ls = 218.3164591+(481267.88134236+(-0.0013268+(1.0/538841-1.0/65194000*t)*t)*t)*t

    sr = 0

    for i in range(60):
        temp =sigma_r[i]*GCMath.cosDeg( arg_lr[i][0]*d + arg_lr[i][1]*m + arg_lr[i][2]*ms + arg_lr[i][3]*f)
        if math.fabs(arg_lr[i][1])==1: temp = temp*e
        if math.fabs(arg_lr[i][1])==2: temp = temp*e*e
        sr =sr+temp


    return 385000.56+sr/1000


def unittests():
    GCUT.info('moon data')
    ed = GCEarthData.EARTHDATA()
    ed.longitude_deg = 20.0
    ed.latitude_deg = 45.0
    ed.tzone = 1.0
    vc = GCGregorianDate.GCGregorianDate(2000,1,1,0.5)
    GCUT.msg('Moon distance: ' + str(MoonDistance(vc.GetJulianComplete())))
    nd = GetNextRise(ed,vc,True)
    GCUT.msg('Next rise: ' + repr(nd))
    nd = GetNextRise(ed, vc, False)
    GCUT.msg('Next set: ' + repr(nd))
    a,b = GetNextMoonRasi(ed,vc)
    GCUT.msg('next moon rasi: {} {}'.format(a,b))
    a,b = CalcMoonTimes(ed,vc,1.0)
    GCUT.msg('moon times: {} {}'.format(repr(a),repr(b)))
