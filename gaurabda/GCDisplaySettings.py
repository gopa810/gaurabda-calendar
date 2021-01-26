import json
from . import GCUT as GCUT

gss_default = [
    [0, 0, "ARTI", "Tithi at arunodaya"],#0
    [0, 0, "ARTM", "Arunodaya Time"],#1
    [0, 0, "SRTM", "Sunrise Time"],#2
    [0, 0, "SSTM", "Sunset Time"],#3
    [0, 0, "MRTM", "Moonrise Time"],#4
    [0, 0, "MSTM", "Moonset Time"],#5
    [1, 1, "FEST", "Festivals"],#6
    [0, 0, "KSAY", "Info about ksaya tithi"],#7
    [0, 0, "VRDH", "Info about vriddhi tithi"],#8
    [0, 0, "SLON", "Sun Longitude"],#9
    [0, 0, "MLON", "Moon Longitude"],#10
    [0, 0, "AYAN", "Ayanamsha value"],#11
    [0, 0, "JDAY", "Julian Day"],#12
    [1, 1, "CPUR", "Caturmasya Purnima System"], #13
    [0, 0, "CPRA", "Caturmasya Pratipat System"], #14
    [0, 0, "CEKA", "Caturmasya Ekadasi System"], #15
    [1, 1, "SANI", "Sankranti Info"], #16
    [1, 1, "EKAI", "Ekadasi Info"], #17
    [1, 1, "VHDR", "Masa Header Info"], #18
    [0, 0, "PHDR", "Month Header Info"], #19
    [0, 0, "EDNS", "Do not show empty days"], #20
    [0, 0, "SBEM", "Show begining of masa"], #21
    [1, 1, "F000", "Appearance days of the Lord"],#22
    [1, 1, "F001", "Events in the pastimes of the Lord"],#23
    [1, 1, "F002", "App, Disapp of Recent Acaryas"],#24
    [1, 1, "F003", "App, Disapp of Mahaprabhu's Associates and Other Acaryas"],#25
    [1, 1, "F004", "ISKCON's Historical Events"],#26
    [1, 1, "F005", "Bengal-specific Holidays"],#27
    [1, 1, "F006", "My Personal Events"], #28
    # BEGIN GCAL 1.4.3
    [1, 1, "TSSR", "Todat Sunrise"],  #29 Today sunrise
    [1, 1, "TSSN", "Today Noon"],  #30 today noon
    [1, 1, "TSSS", "Today Sunset"],  #31 today sunset
    [0, 0, "TSAN", "Sandhya Times"],  #32 today + sandhya times
    [1, 1, "TSIN", "Sunrise Info"],  #33 today sunrise info
    [0, 0, "ASIN", "Noon Time"],  #34 astro - noon time
    [1, 1, "NDST", "Notice about DST"], #35 notice about the change of the DST
    [1, 1, "DNAK", "Naksatra"], # 36 naksatra info for each day
    [1, 1, "DYOG", "Yoga"], #37 yoga info for each day
    [1, 1, "FFLG", "Fasting Flag"],#38
    [1, 1, "DPAK", "Paksa Info"],#39 paksa info
    [0, 0, "FDIW", "First Day in Week"],#40 first day in week
    [0, 0, "DRAS", "Rasi"], #41 moon rasi for each calendar day
    [0, 0, "OSFA", "Old Style Fasting text"], #42 old style fasting text
    [0, 0, "MLNT", "Name of month - type"], #43 month type name 0-vaisnava,1-bengal,2-hindu,3-vedic
    # END GCAL 1.4.3
    [0, 0, "EDBL", "Editable Default Events"], #44 editable default events
    [0, 0, "TSBM", "Today Brahma Muhurta"],     #45 brahma muhurta in today screen
    [0, 0, "TROM", "Today Rasi of the Moon"], # 46 rasi of the moon in today screen
    [0, 0, "TNPD", "Today Naksatra Pada details"], # 47 naksatra pada details in today screen
    [0, 0, "ADCS", "Child Names Suggestions"], # 48 child name suggestions in Appearance Day screen
    [0, 0, "MNFO", "Masa Name Format"], # 49 format of masa name
    [0, 0, "EPDR", "Ekadasi Parana details"], # 50 ekadasi parana details
    [0, 0, "ANIV", "Aniversary show format"], # 51 format of aniversary info
    [1, 1, "CE01", "Sun events"], # 52
    [1, 1, "CE02", "Tithi events"], #53
    [1, 1, "CE03", "Naksatra Events"], #54
    [1, 1, "CE04", "Sankranti Events"],#55
    [1, 1, "CE05", "Conjunction Events"],#56
    [0, 0, "CE06", "Rahu kalam"], #57
    [0, 0, "CE07", "Yama ghanti"], #58
    [0, 0, "CE08", "Guli kalam"], #59
    [0, 0, "CE09", "Moon events"], #60
    [0, 0, "CE10", "Moon rasi"], #61
    [0, 0, "CE11", "Ascendent"], #62
    [1, 1, "CE12", "Sort results core events"],#63
    [0, 0, "CE13", "Abhijit Muhurta"], #64
    [0, 0, "CE14", "Yoga Events"], #65
    [0, 0, "CE14", "Yoga Events"], #66
    [0, 0, "CE14", "Yoga Events"], #67
    [0, 0, "CE14", "Yoga Events"], #68
    [0, 0, "CE14", "Yoga Events"], #69
    [0, 0, "CE14", "Yoga Events"], #70
    [0, 0, "FKSP", "Festival on ksaya tithi: show on previous tithi"], #71
    [0, 0, None, None]
]

gss = gss_default

def getCount():
    return len(gss)

def getCountChanged():
    count = 0
    for a in gss:
        if a[0] != a[1]:
            count+=1
        a[1] = a[0]
    return count

def getSettingName(i):
    return gss[i][3]

def getValue(i):
    return gss[i][0]

def setValue(i,val):
    gss[i][0] = val
    gss[i][1] = val

def setValue(code,val):
    for a in gss:
        if a[2]==code:
            a[0] = val
            a[1] = val
            break

def readFile(fileName):
    default = True
    try:
        if os.path.exists(fileName):
            with open(fileName,'rt',encoding='utf-8') as json_file:
                gss = json.load(json_file)
                default = False
    except:
        default = True

    if default:
        gss = gss_default
    return default

def writeFile(fileName):
    try:
        with open(fileName,'wt',encoding='utf-8') as json_file:
            json_file.write(json.dumps(gss,indent=4))
    except:
        return False
    return True

def unittests():
    GCUT.info('display settings')
    GCUT.val(getValue(6),1,'get Value')
