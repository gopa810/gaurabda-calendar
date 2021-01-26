import os
import os.path
import json

from . import GCDisplaySettings as GCDisplaySettings
from .GCEnums import MahadvadasiType,EkadasiParanaType,FastType,SpecialFestivalId
from . import GCUT as GCUT

gstr = {}
gstr_Modified = False

def GetMonthAbreviation(month):
    return getString(64 + month)

def GetTithiName(i):
    return getString(600 + i % 30)

def GetNaksatraName(n):
    return getString(630 + n % 27)

def GetNaksatraChildSylable(n,pada):
    i = (n * 4 + pada) % 108
    childsylable = [
        "chu", "che", "cho", "la", #asvini
        "li", "lu", "le", "lo", # bharani
        "a", "i", "u", "e", #krtika
        "o", "va", "vi", "vo", # rohini
        "ve", "vo", "ka", "ke", # mrgasira
        "ku","gha","ng","chha", # ardra
        "ke","ko","ha","hi", # punarvasu
        "hu","he","ho","da", # pushya
        "di","du","de","do", #aslesa
        "ma","mi","mu","me", #magha
        "mo","ta","ti","tu", #purvaphalguni
        "te","to","pa","pi", #uttaraphalguni
        "pu","sha","na","tha",#hasta
        "pe","po","ra","ri",#chitra
        "ru","re","ra","ta",#svati
        "ti","tu","te","to",#visakha
        "na","ni","nu","ne",# anuradha
        "no","ya","yi","yu",#jyestha
        "ye","yo","ba","bi",# mula
        "bu","dha","bha","dha",#purvasada
        "be","bo","ja","ji",# uttarasada
        "ju","je","jo","gha",#sravana
        "ga","gi","gu","ge",# dhanistha
        "go","sa","si","su",#satabhisda
        "se","so","da","di",#purvabhadra
        "du","tha","jna","da",#uttarabhadra
        "de","do","cha","chi"# revati
    ]

    return childsylable[i]

def GetRasiChildSylable(n):
    childsylable = [
        "a.. e.. la..",
        "u.. ba.. va..",
        "ka.. gha..",
        "da.. ha..",
        "ma..",
        "pa..",
        "ra.. ta..",
        "na.. ya..",
        "dha.. bha... pha..",
        "kha.. ja..",
        "ga.. sa.. sha..",
        "da.. ca.. tha.. jha.."
    ]

    return childsylable[n % 12]

def GetYogaName(n):
    return getString(660 + n % 27)

def GetSankrantiName(i):
    return getString(688 + i % 12)

def GetSankrantiNameEn(i):
    return getString(700 + i % 12)

def GetPaksaChar(i):
    return 'G' if i else 'K'

def GetPaksaName(i):
    if i: return getString(712)
    return getString(713)

def GetMasaName(i):
    masa_format = GCDisplaySettings.getValue(49)
    str_start = 720
    if masa_format==1:
        str_start=897
    elif masa_format==2:
        str_start=871
    elif masa_format==3:
        str_start=884
    return getString(str_start + i%13)

def GetMahadvadasiName(i):
    if i==MahadvadasiType.EV_NULL or i==MahadvadasiType.EV_SUDDHA:
        return None
    elif i==MahadvadasiType.EV_UNMILANI:
        return getString(733)
    elif i==MahadvadasiType.EV_TRISPRSA or i==MahadvadasiType.EV_UNMILANI_TRISPRSA:
        return getString(734)
    elif i==MahadvadasiType.EV_PAKSAVARDHINI:
        return getString(735)
    elif i==MahadvadasiType.EV_JAYA:
        return getString(736)
    elif i==MahadvadasiType.EV_VIJAYA:
        return getString(737)
    elif i==MahadvadasiType.EV_PAPA_NASINI:
        return getString(738)
    elif i==MahadvadasiType.EV_JAYANTI:
        return getString(739)
    elif i==MahadvadasiType.EV_VYANJULI:
        return getString(740)
    else:
        return None

def GetSpecFestivalName(i):
    if i==SpecialFestivalId.SPEC_JANMASTAMI:
        return getString(741)
    elif i==SpecialFestivalId.SPEC_GAURAPURNIMA:
        return getString(742)
    elif i==SpecialFestivalId.SPEC_RETURNRATHA:
        return getString(743)
    elif i==SpecialFestivalId.SPEC_HERAPANCAMI:
        return getString(744)
    elif i==SpecialFestivalId.SPEC_GUNDICAMARJANA:
        return getString(745)
    elif i==SpecialFestivalId.SPEC_GOVARDHANPUJA:
        return getString(746)
    elif i==SpecialFestivalId.SPEC_RAMANAVAMI:
        return getString(747)
    elif i==SpecialFestivalId.SPEC_RATHAYATRA:
        return getString(748)
    elif i==SpecialFestivalId.SPEC_NANDAUTSAVA:
        return getString(749)
    elif i==SpecialFestivalId.SPEC_PRABHAPP:
        return getString(759)
    elif i==SpecialFestivalId.SPEC_MISRAFESTIVAL:
        return getString(750)
    else:
        return getString(64)

def SetSpecFestivalName(i,szName):
    if i==SpecialFestivalId.SPEC_JANMASTAMI:
        setString(741, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_GAURAPURNIMA:
        setString(742, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_RETURNRATHA:
        setString(743, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_HERAPANCAMI:
        setString(744, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_GUNDICAMARJANA:
        setString(745, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_GOVARDHANPUJA:
        setString(746, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_RAMANAVAMI:
        setString(747, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_RATHAYATRA:
        setString(748, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_NANDAUTSAVA:
        setString(749, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_PRABHAPP:
        setString(759, szName)
        gstr_Modified = True
    elif i==SpecialFestivalId.SPEC_MISRAFESTIVAL:
        setString(750, szName)
        gstr_Modified = True

def GetFastingName(i):
    if i == FastType.FAST_NOON:
        return getString(751)
    if i == FastType.FAST_SUNSET:
        return getString(752)
    if i == FastType.FAST_MOONRISE:
        return getString(753)
    if i == FastType.FAST_DUSK:
        return getString(754)
    if i == FastType.FAST_MIDNIGHT:
        return getString(755)
    if i == FastType.FAST_DAY:
        return getString(756)
    return None

def getString(i):
    if isinstance(i,int):
        i = str(i)
    if i in gstr:
        return gstr[i]
    return ''

def GetEkadasiName(nMasa,nPaksa):
    return getString(560 + nMasa*2 + nPaksa)

def GetDSTSignature(nDST):
    if nDST: return 'DST'
    return 'LT'

def GetParanaReasonText(eparana_type):
    if eparana_type == EkadasiParanaType.EP_TYPE_3DAY:
        return getString(165)
    if eparana_type == EkadasiParanaType.EP_TYPE_4TITHI:
        return getString(166)
    if eparana_type == EkadasiParanaType.EP_TYPE_SUNRISE:
        return getString(169)
    if eparana_type == EkadasiParanaType.EP_TYPE_TEND:
        return getString(167)
    if eparana_type == EkadasiParanaType.EP_TYPE_NAKEND:
        return getString(168)
    return ''

def GetVersionText():
    return getString(131)

def setString(i,value):
    if isinstance(i,int):
        i = str(i)
    gstr[i]=value
    gstr_Modified=True

def GetEventClassText(i):
    ect = {
        0: "Appearance Days of the Lord and His Incarnations",
        1: "Events in the Pastimes of the Lord and His Associates",
        2: "Appearance and Disappearance Days of Recent Acaryas",
        3: "Appearance and Disappearance Days of Mahaprabhu's Associates and Other Acaryas",
        4: "ISKCON's Historical Events",
        5: "Bengal-specific Holidays",
        6: "My Personal Events"
    }
    if i in ect: return ect[i]
    return None

def GetDayOfWeek(i):
    return getString(i)

def readFile(pszFile):
    global gstr

    if not os.path.exists(pszFile):
        pszFile = os.path.join(os.path.dirname(__file__), 'res', 'strings.json')
    with open(pszFile,'rt',encoding='utf-8') as json_file:
        gstr = json.load(json_file)

    version = "11, Build 5"
    gstr['130'] = version
    gstr['131'] = 'GCal ' + version
    gstr['132'] = 'Gaurabda Calendar ' + version

def writeFile(pszFile):
    with open(pszFile,'wt',encoding='utf-8') as json_file:
        json_file.write(json.dumps(gstr))

def GetKalaName(i):
    if i == KalaType.KT_RAHU_KALAM:
        return "Rahu kalam"
    if i == KalaType.KT_YAMA_GHANTI:
        return "Yama ghanti"
    if i == KalaType.KT_GULI_KALAM:
        return "Guli kalam"
    if i == KalaType.KT_ABHIJIT:
        return "Abhijit muhurta"
    return ""

def getLongitudeDirectionName(d):
    if d < 0.0:
        return "West"
    return "East"

def getLatitudeDirectionName(d):
    if d < 0.0:
        return "South"
    return "North"

def InitLanguageOutputFromFile(pszFile):
    global gstr
    if os.path.exists(pszFile):
        with open(pszFile,'rt',encoding='utf-8') as json_file:
            g = json.load(json_file)
            for k,v in g.items():
                gstr[k] = v

def getCount():
    return len(gstr)


def unittests():
    GCUT.info('strings')
    readFile('strings.json')
    GCUT.nval(len(gstr),0,'read strings')
    GCUT.val(GetDayOfWeek(0),'Sunday','day of week')
    GCUT.val(GetMasaName(0),'Madhusudana','masa name')
