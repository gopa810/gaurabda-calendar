from . import GCMath as GCMath
from . import GCUT as GCUT
import math

class GCTime:
    def __init__(self,hour=0,min=0,sec=0,milli=0):
        self.hour = hour
        self.min = min
        self.sec = sec
        self.milli = milli

    def __repr__(self):
        return '{:02d}:{:02d}:{:02d}.{:03d}'.format(self.hour, self.min, self.sec, self.milli%1000)

    # offset in seconds
    def short(self,offset=0):
        h,m,s = self.normalize(self.hour,self.min,self.sec + offset)
        return '{:02d}:{:02d}'.format(h,m)

    def normalize(self,h,m,s):
        while s>59:
            s-=60
            m+=1
        while s<0:
            s+=60
            m-=1
        while m>59:
            m-=60
            h+=1
        while m<0:
            m+=60
            h-=1
        return h,m,s

    def SetDayTime(self,d):
        time_hr = 0.0

        # hour
        time_hr = d * 24
        self.hour = int( math.floor(time_hr) )

        # minute
        time_hr -= self.hour
        time_hr *= 60
        self.min = int( math.floor(time_hr) )

        # second
        time_hr -= self.min
        time_hr *= 60
        self.sec = int( math.floor(time_hr) )

        # miliseconds
        time_hr -= self.sec
        time_hr *= 1000
        self.mili = int( math.floor(time_hr) )

    def SetValue(self,i):
        self.hour,self.min,self.sec = self.normalize(0,0,i)
        self.milli = i-math.floor(i)

    def Set(self,d,offset=0):
        self.hour = d.hour
        self.min = d.min
        self.sec = d.sec
        self.mili = d.mili
        if offset!=0:
            self.AddMinutes(offset)

    def IsGreaterThan(self,dt):
        return self.Seconds()>dt.Seconds()

    def IsLessThan(self, dt):
        return self.Seconds()<dt.Seconds()

    def IsGreaterOrEqualThan(self, dt):
        return self.Seconds()>=dt.Seconds()

    def IsLessOrEqualThan(self, dt):
        return self.Seconds()<=dt.Seconds()

    def Seconds(self):
        return self.hour*3600 + self.min*60 + self.sec + self.milli/1000

    def AddMinutes(self,mn):
        self.hour,self.min,self.sec = self.normalize(self.hour,self.min,self.sec + int(mn*60))

    def AddSeconds(self,sc):
        self.hour,self.min,self.sec = self.normalize(self.hour,self.min,self.sec + int(sc))

    def GetDayTime(self):
        return ((self.hour*60.0 + self.min)*60.0 + self.sec) / 86400.0

    #  Conversion time from DEGREE fromat to H:M:S:MS format
    #
    #  time - output
    #  time_deg - input time in range 0 deg to 360 deg
    #             where 0 deg = 0:00 AM and 360 deg = 12:00 PM
    #
    def SetDegTime(self, time_deg):
        time_hr = 0.0

        time_deg = GCMath.putIn360(time_deg)

        # hour
        time_hr = time_deg / 360 * 24
        self.hour = int( math.floor(time_hr) )

        # minute
        time_hr -= self.hour
        time_hr *= 60
        self.min = int( math.floor(time_hr) )

        # second
        time_hr -= self.min
        time_hr *= 60
        self.sec = int( math.floor(time_hr) )

        # miliseconds
        time_hr -= self.sec
        time_hr *= 1000
        self.mili = int( math.floor(time_hr) )

    def ToLongTimeString(self):
        return '{:02d}:{:02d}:{:02d}'.format(self.hour, self.min, self.sec)


def unittests():
    dt1 = GCTime(hour=1,min=23)
    dt2 = GCTime(hour=2,min=30)
    dt3 = GCTime(hour=5,min=10)

    GCUT.info('GCTime class')
    GCUT.val(dt1.ToLongTimeString(),'01:23:00','long time string')
    GCUT.val(dt3.IsGreaterThan(dt2),True,'greater than')

    dt2.AddMinutes(176)
    GCUT.val(dt2.ToLongTimeString(),'05:26:00', 'add minutes')
    GCUT.val(dt3.IsLessThan(dt2),True,'less than')
