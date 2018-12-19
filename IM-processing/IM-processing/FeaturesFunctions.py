import numpy as np
import scipy.fftpack
from scipy import signal

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
    def ALPHA_P(self, SINAL, fs=1024):

        # fft do sinal
        N = len(SINAL)
        T = 1.0 / float(fs)
        yf = scipy.fftpack.fft(SINAL)
        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
        a = list(2.0/N * np.abs(yf[:N//2]))

        nv = []
        for i, v in enumerate(xf):
            if v >= 8 and v <= 13:
                nv.append(a[i])
        alpha_p = np.sum(np.square(nv))
        return alpha_p