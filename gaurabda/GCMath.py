import math
from . import GCUT as GCUT

# pi
PI = 3.1415926535897932385

# 2 * pi
PI2 = 6.2831853071795864769

# pi / 180
RADS = 0.0174532925199432958

# distance of Earth from Sun in km
AU = 149597869.0

# astronomy data
EARTH_RADIUS = 6378.15
MOON_RADIUS = 1737.4
SUN_RADIUS = 695500

# julian day constants
J1999 = 2451180.0
J2000 = 2451545.0

# input value: arc in degrees
def cosDeg(x):
	return math.cos(x * RADS)

# input value: arc in degrees
def sinDeg(x):
	return math.sin(x * RADS)

def arccosDeg(x):
	return math.acos(x) / RADS

def Abs(d):
	return math.fabs(d)

# input value: arc in degrees
# it is calculating arctan(x/y)
# with testing values
def arcTan2Deg(x,y):
	return math.atan2(x, y) / RADS

# input value: arc in degrees
# output value: tangens
def tanDeg(x):
	return math.tan(x * RADS)

# input value: -1.0 .. 1.0
# output value: -180 deg .. 180 deg
def arcSinDeg(x):
	return math.asin(x) / RADS

def arcTanDeg(x):
	return math.atan(x) / RADS

# modulo 1
def putIn1(v):
	v2 = v - math.floor(v)
	while (v2 < 0.0):
		v2 += 1.0;
	while (v2 > 1.0):
		v2 -= 1.0
	return v2

# modulo 24
def putIn24(id):
	d = id
	while(d >= 24.0):
		d -= 24.0
	while(d < 0.0):
		d += 24.0
	return d

# modulo 360
def putIn360(id):
	d = id
	while(d >= 360.0):
		d -= 360.0
	while(d < 0.0):
		d += 360.0
	return d

# modulo 360 but in range -180deg .. 180deg
# used for comparision values around 0deg
# so difference between 359deg and 1 deg
# is not 358 degrees, but 2 degrees (because 359deg = -1 deg)
def putIn180(in_d):
	d = in_d
	while d < -180.0:
		d += 360.0
	while d > 180.0:
		d -= 360.0;
	return d

# sign of the number
# -1: number is less than zero
# 0: number is zero
# +1: number is greater than zero
def getSign(d):
	if d > 0.0:
		return 1
	if d < 0.0:
		return -1
	return 0

def deg2rad(x):
	return x * RADS

def rad2deg(x):
	return x / RADS

def getFraction(x):
	return x - math.floor(x)

def Max(a,b):
	if a > b:
		return a
	return b

def Min(a,b):
	if a < b:
		return a
	return b

def arcDistance(lon1,lat1,lon2,lat2):
    lat1 = PI / 2 - lat1
    lat2 = PI / 2 - lat2
    return arccosDeg(cosDeg(lat1) * cosDeg(lat2) + sinDeg(lat1) * sinDeg(lat2) * cosDeg(lon1 - lon2))

def arcDistanceDeg(lon1, lat1, lon2, lat2):
    return rad2deg(arcDistance(deg2rad(lon1), deg2rad(lat1), deg2rad(lon2), deg2rad(lat2)))

def Floor(d):
	return math.floor(d)

def unittests():
    GCUT.info('gc math')
    GCUT.val(Max(1,2), 2, 'max')
    GCUT.val(sinDeg(90), 1.0, 'sin')
    GCUT.val(cosDeg(0), 1.0, 'cos')
    GCUT.val(putIn24(30), 6, 'putIn24')
    GCUT.val(Floor(1.3),1.0, 'Floor')
    GCUT.val(Floor(-1.3),-2.0, 'Floor')
