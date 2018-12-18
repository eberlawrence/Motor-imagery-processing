import numpy as np


class Features:

    def __init__(self):
        pass

    def MAV(self, SINAL):
        mav = np.sum(SINAL)/len(SINAL)
        return float(mav)
    def SSC(self, SINAL):
        ssc = np.count_nonzero(np.diff(np.sign(np.diff(SINAL))))
        return float(ssc)
    def WL(self, SINAL):
        wl = np.sum(np.abs(np.diff(SINAL)))
        return float(wl)
    def RMS(self, SINAL): 
        rms = np.sqrt(np.mean(np.square(SINAL)))
        return float(rms) 
    def VAR(self, SINAL):
        var = np.var(SINAL)
        return var
    def ZC(self, SINAL):
        zc = ((SINAL[:-1] * SINAL[1:]) < 0).sum()
        return float(zc)