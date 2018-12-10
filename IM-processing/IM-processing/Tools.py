import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack


class Processing():

    def __init__(self):
        #self.data = data
        #self.trigger = trigger
        pass

    def BandPassFilter(self, data, Fpa=1, Fpb=50, fs=1024, order=5):
        '''
        # Detalhes do sinal e parâmetros para a construção dos filtros #       
        fs          # Frequência de amostragem do sinal.                      Default -> 1024 Hz
        Fpb = X   # Frequência para remover frequências abaixo de _X_ Hz.   Default -> 50 Hz
        Fpa = Y   # Frequência para remover frequências abaixo de _Y_ Hz.   Default -> 1 Hz
        '''
        Wpb = Fpb/(fs/2) # Para o filtro PASSA-BAIXA
        Wpa = Fpa/(fs/2) # Para o filtro PASSA-ALTA
        b2, a2 = signal.butter(order, Wpa, 'highpass') # Design butter filter - Fc = 10Hz
        b3, a3 = signal.butter(order, Wpb, 'lowpass') # Design butter filter - Fc = 20Hz
        passaAlta = signal.filtfilt(b2, a2, data) # Passa um filtro PASSA-ALTA para remover nível DC do SINAL
        passaBaixa = signal.filtfilt(b3, a3, passaAlta) # Passa um filtro PASSA-BAIXA no SINAL retificado
        return passaBaixa

    def NotchFilter(self, data, fc=60, fs=1024, order=5):


    def FFT(self, data, fs=1024):
        # Number of samplepoints
        N = len(data)
        # sample spacing
        T = 1.0 / float(fs)
        x = np.linspace(0.0, N*T, N)
        yf = scipy.fftpack.fft(data)
        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
        plt.subplot(2,1,1)
        plt.plot(np.array(range(N))/fs, data)
        plt.subplot(2,1,2)
        plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))


    def Amplificar(self, data, X):
        S = list(data)
        amp = [*map(lambda x: x*X,list(S))] #amplificar o sinal retificado
        return amp # amplifica um sinal em X vezes
