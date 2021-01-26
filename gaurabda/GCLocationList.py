from .GCLocation import GCLocation
from . import GCCountry
from . import GCTimeZone
from . import GCUT

import os
import os.path
import json

locationList = []
m_bModified = True

def OpenFile(pszFileList):
    if not os.path.exists(pszFileList):
        pszFileList = os.path.join(os.path.dirname(__file__), 'res', 'locations.json')
    ImportFile(pszFileList,True)

def IsModified():
    return m_bModified

def SaveAs(lpszFileName):
    locations = [a.data() for a in locationList]
    with open(lpszFileName,'wt',encoding='utf-8') as json_file:
        json_file.write(json.dumps(locations))

def ImportFile(pszFile, bDeleteCurrent=False):
    global locationList
    with open(pszFile,'rt',encoding='utf-8') as json_file:
        locations = json.load(json_file)
        if bDeleteCurrent:
            locationList=[]
        for a in locations:
            locationList.append(GCLocation(data=a))
        m_bModified = True

def RemoveAll():
    locationList=[]
    m_bModified=True

def Add(loc):
    locationList.append(loc)
    m_bModified = True

def FindLocation(city=None,country=None):
    c = None if city is None else city.lower()
    cn = None if country is None else country.lower()
    for L in locationList:
        if c is None or c==L.m_strCity.lower():
            if cn is None or cn==L.m_strCountry.lower():
                return L
    return None

def FindLocations(city=None,country=None, limit=200):
    equals1 = []
    starting1 = []
    contains2 = []
    if city is not None:
        city = city.lower()
        # city is valid
        if country is not None:
            # country is valid
            print('1')
            country = country.lower()
            for L in locationList:
                if country != L.m_strCountry.lower():
                    continue
                c2 = L.m_strCity.lower()
                if c2 == city:
                    equals1.append(L)
                elif c2.startswith(city):
                    starting1.append(L)
                elif city in c2:
                    contains2.append(L)
                if len(equals1) + len(starting1) + len(contains2) >= limit:
                    return equals1, starting1, contains2
        else:
            # country is omitted
            print('2')
            for L in locationList:
                c2 = L.m_strCity.lower()
                if c2 == city:
                    equals1.append(L)
                elif c2.startswith(city):
                    starting1.append(L)
                elif city in c2:
                    contains2.append(L)
                if len(equals1) + len(starting1) + len(contains2) >= limit:
                    return equals1, starting1, contains2
    else:
        # city is omitted
        if country is not None:
            print('3')
            # country is valid
            country = country.lower()
            for L in locationList:
                c3 = L.m_strCountry.lower()
                if c3 == country:
                    equals1.append(L)
                elif c3.startswith(country):
                    starting1.append(L)
                elif country in c3:
                    contains2.append(L)
                if len(equals1) + len(starting1) + len(contains2) >= limit:
                    return equals1, starting1, contains2
        else:
            print('4')
            # country is omitted
            for L in locationList:
                equals1.append(L)
            if len(starting1) >= limit:
                return equals1, starting1, contains2
    return equals1, starting1, contains2

def GetLocationsForCountry(country=None,limit=-1):
    rv = []
    for L in locationList:
        if country==None or country==L.m_strCountry:
            if len(rv)<limit or limit<0:
                rv.append(L)
    return rv


def RemoveAt(index):
    del locationList[index]
    m_bModified = True

def RenameCountry(pszOld, pszNew):
    for loc in locationList:
        if loc.m_strCountry==pszOld:
            loc.m_strCountry = pszNew
            m_pModified = True

def LocationCount():
    return len(locationList)

def LocationAtIndex(index):
    return locationList[index]

def unittests():
    GCUT.info('location list')
    OpenFile('locations.json')
    GCUT.nval(LocationCount(),0,'location count')
    lc = LocationAtIndex(0)
    print(lc.data())
