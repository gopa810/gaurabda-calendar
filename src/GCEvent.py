
class GCEvent:
    def __init__(self,data=None):
        if data:
            self.data = data
        else:
            self.data = {
                'cls': 0,
                'tithi': 0,
                'masa': 0,
                'fast': 0,
                'visible': 1,
                'used': 1,
                'spec': 0
            }

    @property
    def nTithi(self):
        return self.data['tithi']

    @nTithi.setter
    def nTithi(self,val):
        self.data['tithi'] = val

    @property
    def nMasa(self):
        return self.data['masa']

    @nMasa.setter
    def nMasa(self,val):
        self.data['masa'] = val

    @property
    def nClass(self):
        return self.data['cls']

    @nClass.setter
    def nClass(self,val):
        self.data['cls'] = val

    @property
    def nFastType(self):
        return self.data['fast']

    @nFastType.setter
    def nFastType(self,val):
        self.data['fast'] = val

    #---------------------
    @property
    def nVisible(self):
        return self.data['visible']

    @nVisible.setter
    def nVisible(self,val):
        self.data['visible'] = val

    #---------------------
    @property
    def nStartYear(self):
        return self.data['start']

    @nStartYear.setter
    def nStartYear(self,val):
        self.data['start'] = val

    #---------------------
    @property
    def nUsed(self):
        return self.data['used']

    @nUsed.setter
    def nUsed(self,val):
        self.data['used'] = val

    #---------------------
    @property
    def nSpec(self):
        return self.data['spec']

    @nSpec.setter
    def nSpec(self,val):
        self.data['spec'] = val

    #---------------------
    @property
    def strFastSubject(self):
        return self.data['fastSubj']

    @strFastSubject.setter
    def strFastSubject(self,val):
        self.data['fastSubj'] = val

    #---------------------
    @property
    def strText(self):
        return self.data['text']

    @strText.setter
    def strText(self,val):
        self.data['text'] = val
