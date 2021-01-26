from . import GCUT as GCUT

ayamashaType = 1;

# precession of the equinoxes http://en.wikipedia.org/wiki/Precession_%28astronomy%29
def GetAyanamsa(jdate):
    t = d = 0.0
    a1 = 0.0
    # progress of ayanamsa from 1950 to 2000
    t = (jdate - 2451545.0) / 36525.0
    d = (5028.796195 - 1.1054348*t)*t / 3600.0
    if ayamashaType==0: # Fagan-Bradley
        a1 = 24.8361111111 -0.095268987143399+ d
    elif ayamashaType==1: # Lahiri
        a1 = 23.85305555555 + d
    elif ayamashaType==2: # Krishnamurti
        a1 = 23.8561111111 -0.095268987143399+ d
    elif ayamashaType==3: # Raman
        a1 = 22.5066666666 -0.095268987143399+ d

    return a1

def GetAyanamsaName(nType):
    pNames = [
        "Fagan/Bradley",
        "Lahiri",
        "Krishnamurti",
        "Raman"
    ]

    if nType > 3:
        return ""

    return pNames[nType]


def GetAyanamsaType():
    return ayamashaType


def SetAyanamsaType(i):
    prev = ayamashaType
    ayamashaType = i
    return prev


# Value of Ayanamsha for given Julian day
#
# 27.8.1900     22-27-54  2415259.000000 22,475
# 23.7.1950     23-09-53  2433486.000000 23,16472
# 03.9.2000     23-52-13  2451791.000000 23,870277778
# 28.8.2010     24-00-04  2455437.000000 24,001111111
# 21.6.2050     24-33-29  2469979.000000 24,558055556
# 14.6.2100     25-15-29  2488234.000000 25,258055556*/

def GetLahiriAyanamsa(d):
    h = [ 2415259.000000,22.475,
        2433486.000000,23.16472,
        2451791.000000,23.870277778,
        2455437.000000,24.001111111,
        2469979.000000,24.558055556,
        2488234.000000,25.258055556 ]

    if d > h[10]:
        return (d - h[10]) * ((h[11] - h[9]) / (h[10] - h[8])) + h[11]
    elif d > h[8]:
        return (d - h[8]) * ((h[11] - h[9]) / (h[10] - h[8])) + h[9]
    elif d > h[6]:
        return (d - h[6]) * ((h[9] - h[7]) / (h[8] - h[6])) + h[7]
    elif d > h[4]:
        return (d - h[4]) * ((h[7] - h[5]) / (h[6] - h[4])) + h[5]
    elif d > h[2]:
        return (d - h[2]) * ((h[5] - h[3]) / (h[4] - h[2])) + h[3]
    elif d > h[0]:
        return (d - h[0]) * ((h[3] - h[1]) / (h[2] - h[0])) + h[1]
    else:
        return (d - h[0]) * ((h[3] - h[1]) / (h[2] - h[0])) + h[1]

def unittests():
    GCUT.info('ayanamsha')
    GCUT.nval(len(GetAyanamsaName(ayamashaType)),0,'ayanamsa name')
    GCUT.nval(GetAyanamsa(2000000),0.0,'ayanamsha value')
