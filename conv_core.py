class Cal:
    def __init__(self,**kwargs):

        #temperature
        self.F = kwargs.get('F')
        self.C = kwargs.get('C')

        #velocity
        self.FPS = kwargs.get('FPS')
        self.mps = kwargs.get('mps')

        #flowrate
        self.CFM = kwargs.get('CFM')
        self.GPM = kwargs.get("GPM")
        self.lps = kwargs.get('lps')

        #pressure
        self.inwg = kwargs.get('inwg')
        self.pa = kwargs.get('pa')
        self.inwg_100ft = kwargs.get('inwg_100ft')
        self.pa_m = kwargs.get('pa_m')

    def temperature(self):
        if self.F != None:
            self.C = round((self.F - 32) * 5 /9,2)
            return self.C
        elif self.C != None:
            self.F = round(((self.C*9/5)+32),2)
            return self.F

    def velocity(self):
        if self.FPS != None:
            self.mps = round((self.FPS/3.281),2)
            return self.mps
        elif self.mps != None:
            self.FPS = round((self.mps*3.281),2)
            return self.FPS

    def airflow(self):
        if self.CFM != None:
            self.lps = round((self.CFM/2.12),2)
            return self.lps
        elif self.lps != None:
            self.CFM = round((self.lps*2.12),0)
            return self.CFM

    def waterflow(self):
        if self.GPM != None:
            self.lps = round((self.GPM/15.85),2)
            return self.lps
        elif self.lps != None:
            self.GPM = round((self.lps*15.85),1)
            return self.GPM

    def pressure(self):
        if self.inwg != None:
            self.pa = round((self.inwg*248.84),1)
            return self.pa
        elif self.pa != None:
            self.inwg = round((self.pa/248.84),3)
            return self.inwg
        elif self.inwg_100ft != None:
            self.pa_m = round((self.inwg_100ft*8.175),3)
            return self.pa_m
        elif self.pa_m != None:
            self.inwg_100ft = round((self.pa_m/8.175),3)
            return self.inwg_100ft


if __name__ =='__main__':
    p1 = Cal(F=20)
    result = p1.temp_conv()
    print(result)
