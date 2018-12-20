import numpy as np
import scipy.fftpack
from scipy import signal

class Features:

    def __init__(self):
        pass

    def FFT(self, data, fs=1024):
        N = len(data)
        T = 1.0 / float(fs)
        yf = scipy.fftpack.fft(data)
        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
        a = list(2.0/N * np.abs(yf[:N//2]))
        return a, xf

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



    def DELTA_P(self, SINAL, fs=1024):
        # fft do sinal
        a, xf = self.FFT(SINAL)
        nv = []
        for i, v in enumerate(xf):
            if v >= 0 and v <= 3.5:
                nv.append(a[i])
        delta_p = np.sum(np.square(nv))
        return delta_p

    def THETA_P(self, SINAL, fs=1024):
        # fft do sinal
        a, xf = self.FFT(SINAL)
        nv = []
        for i, v in enumerate(xf):
            if v >= 4 and v <= 7:
                nv.append(a[i])
        theta_p = np.sum(np.square(nv))
        return theta_p

    def ALPHA_P(self, SINAL, fs=1024):
        # fft do sinal
        a, xf = self.FFT(SINAL)
        nv = []
        for i, v in enumerate(xf):
            if v >= 8 and v <= 13:
                nv.append(a[i])
        alpha_p = np.sum(np.square(nv))
        return alpha_p

    def BETA_P(self, SINAL, fs=1024):
        # fft do sinal
        a, xf = self.FFT(SINAL)
        nv = []
        for i, v in enumerate(xf):
            if v >= 14 and v <= 30:
                nv.append(a[i])
        beta_p = np.sum(np.square(nv))
        return beta_p

    def POT(self, SINAL, fs=1024):
        # fft do sinal
        a, xf = self.FFT(SINAL)
        pot = np.sum(np.square(a))
        return pot
