import gaurabda.GCMath as GCMath
import gaurabda.GCTime as GCTime
import gaurabda.GCUT as GCUT
import gaurabda.GCAyanamsha as GCAyanamsha
from gaurabda.GCEnums import FastType,MahadvadasiType
import gaurabda.GCPancangaDate as GCPancangaDate
import gaurabda.GCDisplaySettings as GCDisplaySettings
import gaurabda.GCStrings as GCStrings
import gaurabda.GCCountry as GCCountry
import gaurabda.GCGregorianDate as GCGregorianDate
import gaurabda.GCTimeZone as GCTimeZone
import gaurabda.GCEarthData as GCEarthData
import gaurabda.GCStringBuilder as GCStringBuilder
import gaurabda.GCMoonData as GCMoonData
import gaurabda.GCSunData as GCSunData
import gaurabda.GCConjunction as GCConjunction
import gaurabda.GCNaksatra as GCNaksatra
import gaurabda.GCSankranti as GCSankranti
import gaurabda.GCDayData as GCDayData
import gaurabda.GCTithi as GCTithi
import gaurabda.GCYoga as GCYoga
import gaurabda.GCLocationList as GCLocationList
import gaurabda.GCEventList as GCEventList
import gaurabda.GCCalendar as GCCalendar
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
