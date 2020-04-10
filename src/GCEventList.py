from GCEvent import GCEvent
import GCUT
import os
import os.path
import json

list = []

def add():
    c = GCEvent()
    list.append(c)
    return c

def OpenFile(fileName):
    global list
    if not os.path.exists(fileName):
        fileName = 'res/events.json'
    with open(fileName,'rt',encoding='utf-8') as rf:
        events = json.load(rf)
        for e in events:
            list.append(GCEvent(data=e))
    return len(list)

def SaveFile(fileName):
    with open(fileName,'wt',encoding='utf-8') as wf:
        events = [ce.data for ce in list]
        wf.write(json.dumps(list,indent=4))
    return len(list)

def clear():
    list = []

def SetOldStyleFasting(bOldStyle):
    locMatrix = []
    with open('res/eventfast.json','rt',encoding='utf-8') as rf:
        locMatrix = json.load(rf)
    ret = 0
    key = 'fast' if bOldStyle else 'newfast'
    for a in locMatrix:
        for pce in list:
            if pce.nMasa == a['masa'] and pce.nTithi == a['tithi'] and pce.nClass == a['cls']:
                if pce.nFastType != a[key]:
                    ret += 1
                    pce.nFastType = a[key]
                break
    return ret

def Count():
    return len(list)

def EventAtIndex(index):
    return list[index]


def unittests():
    GCUT.info('custom events')
    a = OpenFile('events.json')
    GCUT.nval(a,0,'open file')
    print(list[0].data)
