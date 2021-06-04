from .GCEvent import GCEvent
from . import GCUT as GCUT
from . import GCDisplaySettings as GCDS
import os
import os.path
import json

glist_events = []

def get_list():
    if len(glist_events)==0:
        OpenFile('events.json')
    return glist_events

def add():
    c = GCEvent()
    glist_events.append(c)
    return c

def OpenFile(fileName):
    #print('---------------- events loaded ----------------------')
    global glist_events
    if not os.path.exists(fileName):
        fileName = os.path.join(os.path.dirname(__file__), 'res', 'events.json')
    with open(fileName,'rt',encoding='utf-8') as rf:
        events = json.load(rf)
        for e in events:
            glist_events.append(GCEvent(data=e))
    #print(f'-------------setting fasting schema: {GCDS.getValue(42)} -----------------')
    SetOldStyleFasting(GCDS.getValue(42))
    return len(glist_events)

def SaveFile(fileName):
    with open(fileName,'wt',encoding='utf-8') as wf:
        events = [ce.data for ce in glist_events]
        wf.write(json.dumps(glist_events,indent=4))
    return len(glist_events)

def clear():
    glist_events = []

def SetOldStyleFasting(bOldStyle):
    locMatrix = []
    file_name = os.path.join(os.path.dirname(__file__), 'res', 'eventfast.json')
    with open(file_name,'rt',encoding='utf-8') as rf:
        locMatrix = json.load(rf)
    ret = 0
    key = 'fast' if bOldStyle else 'newfast'
    for a in locMatrix:
        for pce in glist_events:
            if pce.nMasa == a['masa'] and pce.nTithi == a['tithi'] and pce.nClass == a['cls']:
                if pce.nFastType != a[key]:
                    ret += 1
                    pce.nFastType = a[key]
                break
    return ret

def Count():
    return len(glist_events)

def EventAtIndex(index):
    return glist_events[index]

def SetFastingSchema(fs):
    GCDS.setValue(42, fs)
    get_list()
    SetOldStyleFasting(fs)

def unittests():
    GCUT.info('custom events')
    a = OpenFile('events.json')
    GCUT.nval(a,0,'open file')
    print(glist_events[0].data)
