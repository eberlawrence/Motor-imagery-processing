import numpy as np
from scipy import signal
import pandas as pd


class Processing():

    def __init__(self, data, trigger):
        self.data = data
        self.trigger = trigger
        #if str(type(self.data)) != "<class 'pandas.core.frame.Series'>":        
        #    self.data = pd.Series(self.data)

    def BandPassFilter(self, Fpa=1, Fpb=50, fs=1024, order=5):
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
        passaAlta = signal.filtfilt(b2, a2, self.data) # Passa um filtro PASSA-ALTA para remover nível DC do SINAL
        passaBaixa = signal.filtfilt(b3, a3, passaAlta) # Passa um filtro PASSA-BAIXA no SINAL retificado
        return passaBaixa
    

    def Amplificar(self, X):
        S = list(self.trigger)
        amp = [*map(lambda x: x*X,list(S))] #amplificar o sinal retificado
        return amp # amplifica um sinal em X vezes
