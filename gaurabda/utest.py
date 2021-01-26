from . import GCMath as GCMath
from . import GCTime as GCTime
from . import GCUT as GCUT
from . import GCAyanamsha as GCAyanamsha
from .GCEnums import FastType,MahadvadasiType
from . import GCPancangaDate as GCPancangaDate
from . import GCDisplaySettings as GCDisplaySettings
from . import GCStrings as GCStrings
from . import GCCountry as GCCountry
from . import GCGregorianDate as GCGregorianDate
from . import GCTimeZone as GCTimeZone
from . import GCEarthData as GCEarthData
from . import GCStringBuilder as GCStringBuilder
from . import GCMoonData as GCMoonData
from . import GCSunData as GCSunData
from . import GCConjunction as GCConjunction
from . import GCNaksatra as GCNaksatra
from . import GCSankranti as GCSankranti
from . import GCDayData as GCDayData
from . import GCTithi as GCTithi
from . import GCYoga as GCYoga
from . import GCLocationList as GCLocationList
from . import GCEventList as GCEventList
from . import GCCalendar as GCCalendar
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
