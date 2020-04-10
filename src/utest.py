import GCMath
import GCTime
import GCUT
import GCAyanamsha
from GCEnums import FastType,MahadvadasiType
import GCPancangaDate
import GCDisplaySettings
import GCStrings
import GCCountry
import GCGregorianDate
import GCTimeZone
import GCEarthData
import GCStringBuilder
import GCMoonData
import GCSunData
import GCConjunction
import GCNaksatra
import GCSankranti
import GCDayData
import GCTithi
import GCYoga
import GCLocationList
import GCEventList
import GCCalendar
import TMasaList
import TCalendar
import TAppDay
import TCoreEvents
import TToday
import os

os.mkdir('test')

GCMath.unittests()
GCTime.unittests()
GCUT.info('enums')
GCUT.val(FastType.FAST_NULL,0, 'FastType')
GCUT.val(MahadvadasiType.EV_VIJAYA,0x110, 'MahadvadasiType')
GCAyanamsha.unittests()
GCPancangaDate.unittests()
GCDisplaySettings.unittests()
GCStrings.unittests()
GCCountry.unittests()
GCGregorianDate.unittests()
GCTimeZone.unittests()
GCEarthData.unittests()
GCStringBuilder.unittests()
GCMoonData.unittests()
GCSunData.unittests()
GCConjunction.unittests()
GCNaksatra.unittests()
GCSankranti.unittests()
GCTithi.unittests()
GCDayData.unittests()
GCYoga.unittests()
GCLocationList.unittests()
GCEventList.unittests()
GCCalendar.unittests()
# retype to if True: ... in case you need unittests for specific engine
if True: TMasaList.unittests()
if True: TCalendar.unittests()
if True: TAppDay.unittests()
if True: TCoreEvents.unittests()
TToday.unittests()
