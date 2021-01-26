import os
import os.path
import json

from . import GCUT

gcontinents = [
        "",
        "Europe", #1
        "Asia",   #2
        "Africa", #3
        "America",#4
        "Pacific",#5
        "Indiana",#6
        "Atlantic",#7
        ""
]

_modified = 0

gcountries = []

def InitWithFile(strFile):
    global gcountries
    if not os.path.exists(strFile):
        strFile = os.path.join(os.path.dirname(__file__), 'res', 'countries.json')
    with open(strFile,'rt',encoding='utf-8') as json_file:
        gcountries = json.load(json_file)
    return len(gcountries)

def FindCountry(name=None,abbr=None):
    if name!=None:
        for a in gcountries:
            if a['name']==name:
                return a
    elif abbr!=None:
        for a in gcountries:
            if a['abbr']==abbr:
                return a
    return None

def GetCountries():
    return [a['name'] for a in gcountries]

def GetCountryName(w):
    bytes = int(w).to_bytes(2,byteorder='little',signed=False)
    abbr = chr(bytes[0]) + chr(bytes[1])
    for a in gcountries:
        if a['abbr'] == abbr:
            return a['name']
    return ""

def GetCountryContinentName(w):
    bytes = int(w).to_bytes(2,byteorder='little',signed=False)
    abbr = chr(bytes[0]) + chr(bytes[1])
    for a in gcountries:
        if a['abbr'] == abbr:
            return gcontinents[a['continent']]
    return ""

def GetCountryCount():
    return len(gcountries)

def GetCountryNameByIndex(nIndex):
    return gcountries[nIndex]['name']

def GetCountryContinentNameByIndex(nIndex):
    return gcontinents[gcountries[nIndex]['continent']]

def GetCountryAcronymByIndex(nIndex):
    return gcountries[nIndex]['abbr']

def SaveToFile(szFile):
    with open(szFile,'wt',encoding='utf-8') as json_file:
        json_file.write(json.dumps(gcountries,indent=4))

def AddCountry(abbr, name, continent):
    gcountries.append({
        'abbr': abbr,
        'name': name,
        'continent': continent
    })
    return len(gcountries)

def SetCountryName(index,name):
    if index>=0 and index<len(gcountries):
        gcountries[index]['name'] = name
    _modified = 1
    return 1

def GetCountryCode(index):
    return gcountries[index]['code']

def IsModified():
    return _modified

def unittests():
    GCUT.info('countries')
    GCUT.nval(InitWithFile('countries.json'),0,'load countries')
    GCUT.msg('count:' + str(len(gcountries)))
    country = FindCountry(name='India')
    GCUT.val(country['abbr'],'IN','find country')
