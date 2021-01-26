from . import GCUT as GCUT
from . import GCStrings as GCStrings

class GCGaurabdaDate:
    def __init__(self,t=0,m=0,y=520):
        self.tithi = t
        self.masa = m
        self.gyear = y

    def __str__(self):
        return '{} {}, {} Masa, {}'.format(GCStrings.GetTithiName(self.tithi), GCStrings.GetPaksaName(self.paksa), GCStrings.GetMasaName(self.masa), self.gyear)

    @property
    def paksa(self):
        return 1 if self.tithi>=15 else 0

    def next(self):
        self.tithi+=1
        if self.tithi >= 30:
            self.tithi %= 30
            self.nextMasa()

    def nextMasa(self):
        self.masa+=1
        if self.masa >= 12:
            self.masa %= 12
            self.gyear+=1

    def prev(self):
        if self.tithi == 0:
            self.tithi = 29
            self.prevMasa()
        else:
            self.tithi-=1

    def prevMasa(self):
        if self.masa == 0:
            self.masa = 11
            self.gyear -= 1
        else:
            self.masa-=1

    def Set(self,va):
        self.tithi = va.tithi;
        self.masa = va.masa;
        self.gyear = va.gyear;

def unittests():
    GCUT.info('GCGaurabdaDate')
    va = GCGaurabdaDate()
    GCUT.val(va.tithi,0,'day')
    va.next()
    GCUT.val(va.tithi,1,'next')
    va.prev()
    va.prev()
    GCUT.val(va.tithi,29,'prev-tithi')
    GCUT.val(va.masa,11,'prev-masa')
    GCUT.val(va.gyear,519,'prev-gyear')
