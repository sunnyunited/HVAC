class Cal:
    def __init__(self,**kwargs):

        self.F = kwargs.get('F')
        self.C = kwargs.get('C')
        self.FPS = kwargs.get('FPS')
        self.mps = kwargs.get('mps')
        self.CFM = kwargs.get('CFM')
        self.lps = kwargs.get('lps')
        self.inwg = kwargs.get('inwg')
        self.pa = kwargs.get('pa')

    def temp_conv(self):
        if self.F != None:
            self.C = round((self.F - 32) * 5 / 9,2)
            return self.C
        elif self.C != None:
            self.F = round(((self.C*9/5)+32),2)
            return self.F

    def velocity_conv(self):
        if self.FPS != None:
            self.mps = round((self.FPS/3.281),2)
            return self.mps
        elif self.mps != None:
            self.FPS = round((self.mps*3.281),2)
            return self.FPS

    def airflow_conv(self):
        if self.CFM != None:
            self.lps = round((self.CFM/2.12),2)
            return self.lps
        elif self.lps != None:
            self.CFM = round((self.lps*2.12),2)
            return self.CFM

    def pressure_conv(self):
        if self.inwg != None:
            self.pa = round((self.inwg*248.84),2)
            return self.pa
        elif self.pa != None:
            self.inwg = round((self.pa/248.84),2)
            return self.inwg

if __name__ =='__main__':
    p1 = Cal(F=20)
    result = p1.temp_conv()
    print(result)
