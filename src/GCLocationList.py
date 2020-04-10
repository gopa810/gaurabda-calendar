from GCLocation import GCLocation
import GCCountry
import GCTimeZone
import os
import os.path
import json
import GCUT

locationList = []
m_bModified = True

def OpenFile(pszFileList):
    if not os.path.exists(pszFileList):
        pszFileList = 'res/locations.json'
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
