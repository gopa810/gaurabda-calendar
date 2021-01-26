from .GCTime import GCTime
from .GCEnums import KalaType
import math
import json
from . import GCMath as GCMath
from . import GCGregorianDate as GCGregorianDate
from . import GCEarthData as GCEarthData
from . import GCCoords as GCCoords
from . import GCUT as GCUT


def GetSunLongitude(vct):
    DG = GCMath.PI / 180
    RAD = 180 / GCMath.PI

    # mean ecliptic longitude of the sun
    mel = SunGetMeanLong(vct.year, vct.month, vct.day) + (360/365.25)*(vct.shour - 0.5 - vct.tzone/24.0)

    # ecliptic longitude of perigee
    elp = SunGetPerigee(vct.year, vct.month, vct.day)

    # mean anomaly of the sun
    mas = mel - elp

    # ecliptic longitude of the sun
    return  mel + 1.915 * math.sin(mas * DG) + 0.02 * math.sin (2 * DG * mas)


# find mean ecliptic longitude of the sun for your chosen day
def SunGetMeanLong(year,month,day):
    sun_long = [
        339.226,009.781,039.351,069.906,099.475,130.030,160.585,190.155,220.710,250.279,280.834,311.390,
        340.212,010.767,040.337,070.892,100.461,131.016,161.571,191.141,221.696,251.265,281.820,312.375,
        341.198,011.753,041.322,071.877,101.447,132.002,162.557,192.126,222.681,252.251,282.806,313.361,
        342.183,012.738,042.308,072.863,102.432,132.987,163.542,193.112,223.667,253.236,283.791,314.346,
        343.169,013.724,043.293,073.849,103.418,133.973,164.528,194.098,224.653,254.222,284.777,315.332,
        344.155,014.710,044.279,074.834,104.404,134.959,165.514,195.083,225.638,255.208,285.763,316.318,
        345.140,015.695,045.265,075.820,105.389,135.944,166.499,196.069,226.624,256.193,286.748,317.303,
        346.126,016.681,046.250,076.805,106.375,136.930,167.485,197.054,227.610,257.179,287.734,318.289,
        347.112,017.667,047.236,077.791,107.361,137.916,168.471,198.040,228.595,258.165,288.720,319.275,
        348.097,018.652,048.222,078.777,108.346,138.901,169.456,199.026,229.581,259.150,289.705,320.260,
        349.083,019.638,049.207,079.762,109.332,139.887,170.442,200.011,230.566,260.136,290.691,321.246,
        350.068,020.624,050.193,080.748,110.317,140.873,171.428,200.997,231.552,261.122,291.677,322.232,
        351.054,021.609,051.179,081.734,111.303,141.858,172.413,201.983,232.538,262.107,292.662,323.217,
        352.040,022.595,052.164,082.719,112.289,142.844,173.399,202.968,233.523,263.093,293.648,324.203,
        353.025,023.581,053.150,083.705,113.274,143.829,174.385,203.954,234.509,264.078,294.634,325.189,
        354.011,024.566,054.136,084.691,114.260,144.815,175.370,204.940,235.495,265.064,295.619,326.174,
        354.997,025.552,055.121,085.676,115.246,145.801,176.356,205.925,236.480,266.050,296.605,327.160,
        355.982,026.537,056.107,086.662,116.231,146.786,177.341,206.911,237.466,267.035,297.590,328.146,
        356.968,027.523,057.093,087.648,117.217,147.772,178.327,207.897,238.452,268.021,298.576,329.131,
        357.954,028.509,058.078,088.633,118.203,148.758,179.313,208.882,239.437,269.007,299.562,330.117,
        358.939,029.494,059.064,089.619,119.188,149.743,180.298,209.868,240.423,269.992,300.547,331.102,
        359.925,030.480,060.049,090.605,120.174,150.729,181.284,210.854,241.409,270.978,301.533,332.088,
        000.911,031.466,061.035,091.590,121.160,151.715,182.270,211.839,242.394,271.964,302.519,333.074,
        001.896,032.451,062.021,092.576,122.145,152.700,183.255,212.825,243.380,272.949,303.504,334.059,
        002.882,033.437,063.006,093.561,123.131,153.686,184.241,213.810,244.366,273.935,304.490,335.045,
        003.868,034.423,063.992,094.547,124.117,154.672,185.227,214.796,245.351,274.921,305.476,336.031,
        004.853,035.408,064.978,095.533,125.102,155.657,186.212,215.782,246.337,275.906,306.461,337.016,
        005.839,036.394,065.963,096.518,126.088,156.643,187.198,216.767,247.322,276.892,307.447,338.002,
        006.824,037.380,066.949,097.504,127.073,157.629,188.184,217.753,248.308,277.878,308.433,338.988,
        007.810,038.365,067.935,098.490,128.059,158.614,189.169,218.739,249.294,278.863,309.418,339.100,
        008.796,038.365,068.920,098.490,129.045,159.600,189.169,219.724,249.294,279.849,310.404,339.226,
        ]

    sun_1_col = [-001.157,-000.386,000.386,001.157 ]
    sun_1_row = [-001.070, 002.015, 005.101, 008.186, 011.271, 014.356, 017.441, 020.526, 023.611, 026.697 ]
    sun_2_col = [000.322,000.107,-000.107,-000.322 ]
    sun_2_row = [-000.577,-000.449,-000.320,-000.192,-000.064, 000.064, 000.192, 000.320, 000.449, 000.577 ]
    sun_3_row = [ -000.370,-000.339,-000.309,-000.278,-000.247, -000.216,-000.185,-000.154,-000.123,-000.093, -000.062,-000.031,+000.000,+000.031,+000.062, +000.093, +000.123,+000.154,+000.185,+000.216,+000.247,+000.278,+000.309,+000.339, +000.370 ]
    sun_3_col = [ +000.358,+000.119,-000.119,-000.358 ]

    mel = 0.0

    if (month > 12) or (month < 1) or (day < 1) or (day > 31):
        return -1.0
    mel = sun_long[(day - 1)*12 + (month + 9)%12]

    y = yy = 0

    if month < 3:
        year -= 1
    y = int(year / 100)
    yy = year % 100

    if y <= 15:
        mel += sun_1_col[y%4] + sun_1_row[int(y/4)]
    elif y < 40:
        mel += sun_2_col[y%4] + sun_2_row[int(y/4)]


    mel += sun_3_col[yy%4] + sun_3_row[int(yy/4)]

    return mel


# finds ecliptic longitude of perigee of the sun
# for the mean summer solstice of your chosen year
# (and effectively for the entire year)
def SunGetPerigee(year,month,day):
    sun_4_row = [251.97,258.85,265.73,272.61,279.49 ,286.37,293.25,300.14,307.02,313.90]
    sun_4_col = [-002.58,-000.86,000.86,002.58 ]
    sun_5_row = [-000.83,-000.76,-000.69,-000.62, -000.55,-000.48,-000.41,-000.34, -000.28,-000.21,-000.14,-000.07, +000.00,+000.07,+000.14,+000.21, +000.28,+000.34,+000.41,+000.48, +000.55,+000.62,+000.69,+000.76, +000.83 ]
    sun_5_col = [-000.03,-000.01,000.01,+000.03]

    per = 0.0

    if (month > 12) or (month < 1) or (day < 1) or (day > 31):
        return -1.0

    if month < 3: year -= 1
    y = int(year / 100)
    yy = year % 100

    per = sun_4_row[int(y / 4)] + sun_4_col[y % 4]
    per += sun_5_row[int(yy / 4)] + sun_5_col[yy % 4]

    return per

def CalculateKala(sunRise, sunSet, dayWeek, type):
    r1 = r2 = 0.0

    if type == KalaType.KT_RAHU_KALAM:
        a = [7,1,6,4,5,3,2]
        period = (sunSet - sunRise) / 8.0
        r1 = sunRise + a[dayWeek] * period
        r2 = r1 + period
    elif type == KalaType.KT_YAMA_GHANTI:
        a = [4,3,2,1,0,6,5]
        period = (sunSet - sunRise) / 8.0
        r1 = sunRise + a[dayWeek] * period
        r2 = r1 + period
    elif type == KalaType.KT_GULI_KALAM:
        a = [6,5,4,3,2,1,0]
        period = (sunSet - sunRise) / 8.0
        r1 = sunRise + a[dayWeek] * period
        r2 = r1 + period
    elif type == KalaType.KT_ABHIJIT:
        period = (sunSet - sunRise) / 15.0
        r1 = sunRise + 7 * period
        r2 = r1 + period
        if dayWeek == 3:
            r1 = r2 = -1
    return r1,r2

class SUNDATA:
    def __init__(self):
        self.length_deg = 0.0
        self.arunodaya_deg = 0.0
        self.sunrise_deg = 0.0
        self.sunset_deg = 0.0

        self.declination_deg = 0.0
        self.longitude_deg = 0.0
        self.longitude_set_deg = 0.0
        self.longitude_arun_deg = 0.0
        self.right_asc_deg = 0.0

        # time of arunodaya - 96 mins before sunrise
        self.arunodaya = GCTime()
        # time of sunrise
        self.rise = GCTime()
        # time of noon
        self.noon = GCTime()
        # time of sunset
        self.set = GCTime()
        # length of the day
        self.length = GCTime()

    def __iter__(self):
        yield 'rise_deg', self.sunrise_deg,
        yield 'noon_deg', (self.sunrise_deg + self.sunset_deg)/2,
        yield 'set_deg', self.sunset_deg,
        yield 'rise', repr(self.rise),
        yield 'noon', repr(self.noon),
        yield 'set', repr(self.set)

    def __repr__(self):
        d = {
            'rise_deg': self.sunrise_deg,
            'noon_deg': (self.sunrise_deg + self.sunset_deg)/2,
            'set_deg': self.sunset_deg,
            'rise': repr(self.rise),
            'noon': repr(self.noon),
            'set': repr(self.set)
        }
        return json.dumps(d)

    def SunPosition(self, vct, ed, dayHours):
        DG = GCMath.PI / 180
        RAD = 180 / GCMath.PI

        dLatitude = ed.latitude_deg
        dLongitude = ed.longitude_deg

        # mean ecliptic longitude of the sun
        mel = SunGetMeanLong(vct.year, vct.month, vct.day) + (360/365.25)*dayHours/360.0

        # ecliptic longitude of perigee
        elp = SunGetPerigee(vct.year, vct.month, vct.day)

        # mean anomaly of the sun
        mas = mel - elp

        # ecliptic longitude of the sun
        els = 0.0
        self.longitude_deg = els = mel + 1.915 * math.sin(mas * DG) + 0.02 * math.sin (2 * DG * mas)

        # declination of the sun
        self.declination_deg = RAD * math.asin (0.39777 * math.sin(els * DG))

        # right ascension of the sun
        self.right_asc_deg = els - RAD * math.atan2( math.sin(2*els*DG), 23.2377 + math.cos(2 * DG * els))

        # equation of time
        eqt = self.right_asc_deg - mel


        # definition of event
        # civil twilight                   eventdef = 0.10453;
        # nautical twilight                eventdef = 0.20791;
        # astronomical twilight            eventdef = 0.30902;
        # center of the sun on the horizont   eventdef = 0.01454;
        eventdef = 0.01454

        eventdef = (eventdef / math.cos(dLatitude * DG)) / math.cos(self.declination_deg * DG)

        x = math.tan(dLatitude * DG) * math.tan(self.declination_deg * DG) + eventdef

        # initial values for the case
        # that no rise no set for that day
        self.sunrise_deg = self.sunset_deg = -360.0

        if (x >= -1.0) and (x <= 1.0):
            # time of sunrise
            self.sunrise_deg = 90.0 - dLongitude - RAD * math.asin(x) + eqt
            # time of sunset
            self.sunset_deg = 270.0 - dLongitude + RAD * math.asin(x) + eqt





    #########################################
    #
    # return values are in sun.arunodaya, sun.rise, sun.set, sun.noon, sun.length
    # if values are less than zero, that means, no sunrise, no sunset in that day
    #
    # brahma 1 = calculation at brahma muhurta begining
    # brahma 0 = calculation at sunrise
    def SunCalc(self,vct,earth):
        s_rise = SUNDATA()
        s_set = SUNDATA()

        s_rise.sunrise_deg = 180
        s_set.sunrise_deg = 180

        for i in range(3):
            s_rise.SunPosition(vct, earth, s_rise.sunrise_deg - 180)
            s_set.SunPosition(vct, earth, s_set.sunset_deg - 180)

        # calculate times
        self.longitude_arun_deg = s_rise.longitude_deg - (24.0 / 365.25)
        self.longitude_deg = s_rise.longitude_deg
        self.longitude_set_deg = s_set.longitude_deg

        self.arunodaya_deg = s_rise.sunrise_deg - 24.0
        self.sunrise_deg = s_rise.sunrise_deg
        self.sunset_deg = s_set.sunset_deg
        self.length_deg = s_set.sunset_deg - s_rise.sunrise_deg

        # arunodaya is 96 min before sunrise
        #  sunrise_deg is from range 0-360 so 96min=24deg
        self.arunodaya.SetDegTime(self.arunodaya_deg + earth.tzone*15.0)
        # sunrise
        self.rise.SetDegTime(self.sunrise_deg + earth.tzone*15.0)
        # noon
        self.noon.SetDegTime((self.sunset_deg + self.sunrise_deg)/2  + earth.tzone*15.0)
        # sunset
        self.set.SetDegTime(self.sunset_deg + earth.tzone*15.0)
        # length
        self.length.SetDegTime(self.length_deg)


def unittests():
    GCUT.info('sundata')
    r1,r2 = CalculateKala(0.25, 0.75, 0, KalaType.KT_ABHIJIT)
    GCUT.msg('abhijit on sunday {} {}'.format(r1,r2))
    s = SUNDATA()
    e = GCEarthData.EARTHDATA()
    e.longitude_deg = 27.0
    e.latitude_deg = 45.0
    e.tzone = 1.0
    vc = GCGregorianDate.Today()
    s.SunCalc(vc,e)
    GCUT.msg(str(repr(s)))
