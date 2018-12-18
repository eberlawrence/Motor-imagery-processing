import numpy as np
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack
from FeaturesFunctions import Features


class Processing():

    def __init__(self):
        #self.data = data
        #self.trigger = trigger
        pass

    def BandPassFilter(self, data, Fpa=1, Fpb=60, fs=1024, order=5):
        '''
        # Detalhes do sinal e parâmetros para a construção dos filtros #       
        fs          # Frequência de amostragem do sinal.                      Default -> 1024 Hz
        Fpb = X   # Frequência para remover frequências abaixo de _X_ Hz.   Default -> 50 Hz
        Fpa = Y   # Frequência para remover frequências abaixo de _Y_ Hz.   Default -> 1 Hz
        '''
        passaFaixa = []
        for i in data:
            Wpb = Fpb/(fs/2) # Para o filtro PASSA-BAIXA
            Wpa = Fpa/(fs/2) # Para o filtro PASSA-ALTA
            b2, a2 = signal.butter(order, Wpa, 'highpass') # Design butter filter - Fc = 10Hz
            b3, a3 = signal.butter(order, Wpb, 'lowpass') # Design butter filter - Fc = 20Hz
            passaAlta = signal.filtfilt(b2, a2, i) # Passa um filtro PASSA-ALTA para remover nível DC do SINAL
            passaBaixa = signal.filtfilt(b3, a3, passaAlta) # Passa um filtro PASSA-BAIXA no SINAL retificado
            passaFaixa.append(passaBaixa)
        return np.array(passaFaixa)

    def NotchFilter(self, data, fc=60, fs=1024, order=5, Q=1):
        # Frequência normalizada:
        notch = []
        for i in data:
            wn = fc/(fs/2) # Para o filtro NOTCH 60 Hz
            b11, a11 = signal.iirnotch(wn, Q) # Design notch filter - Fc = 60Hz
            filtradoRede = signal.filtfilt(b11, a11, i) # Passa um filtro NOTCH no SINAL para remover 60Hz
            notch.append(filtradoRede)
        return np.array(notch)

    def FFT(self, data, trigger, fs=1024, aux=True):
        # Number of samplepoints
        N = len(data)
        t = np.array(range(N))/fs
        # sample spacing
        T = 1.0 / float(fs)
        x = np.linspace(0.0, N*T, N)
        yf = scipy.fftpack.fft(data)
        xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
        plt.subplot(2,1,1)
        plt.plot(t, data)
        if aux:
            plt.plot(t, trigger)
        plt.subplot(2,1,2)
        plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))

    def Amplificar(self, data, X):
        S = list(data)
        amp = [*map(lambda x: x*X,list(S))] #amplificar o sinal retificado
        return amp # amplifica um sinal em X vezes


    def Amostras(self, TriggerFinal, SINAL):
        '''
        Remove o tempo de repouso
        Retorna um vetor com todas as contrações. 
        '''
        T = list(TriggerFinal)
        S = list(SINAL)    
        vetorMov, vetorRep = [], []

        flagMov = True
        tJ = int(4096)
        count = 0
        while count < 120:
            for i, v in enumerate(T):
                if v > 10 and flagMov == True:
                    vetorMov.extend(S[i:i+tJ])
                    flagMov = False
                    count += 1
                if v < 10 and flagMov == False:
                    vetorRep.extend(S[i:i+tJ])
                    flagMov = True
                    count += 1
        return vetorMov, vetorRep

    def VetorDeAmostras(self, TriggerFinal, SINAL):
        '''
        Retorna o vetor com os SINAIS DE CONTRAÇÃO separados.
        Contem uma lista com N listas. Cada lista N é uma janela de contração.
        '''
        sMov, sRep = self.Amostras(TriggerFinal, SINAL)
        AmostraMov, AmostraRep = [], []
        tJ = int(4096)
        for T in range(120):
            AmostraMov.append(sMov[0:tJ])
            AmostraRep.append(sRep[0:tJ])
            del sMov[0:tJ]
            del sRep[0:tJ]
        return AmostraMov, AmostraRep

    def VetorATRIBUTOS(self, TriggerFinal, SINAL, Atributo, sRep=False):
        '''
        Retorna um vetor com os valores RMS de cada SINAL DE CONTRAÇÃO. 
        Retorna como -Pandas.Series-
        '''
        aMov, aRep = self.VetorDeAmostras(TriggerFinal, SINAL)
        ListaAtributos = []
        F = Features()

        if sRep == False:
            A = aMov
        elif sRep == True:
            A = aRep

        if Atributo == 'RMS':
            for i, v in enumerate(A):
                ListaAtributos.append(F.RMS(A[i]))
            rms = pd.Series(ListaAtributos)
            return rms 
        if Atributo == 'ZC':
            for i, v in enumerate(A):
                ListaAtributos.append(F.ZC(np.array(A[i])))
            zc = pd.Series(ListaAtributos)
            return zc 
        if Atributo == 'VAR':
            for i, v in enumerate(A):
                ListaAtributos.append(F.VAR(np.array(A[i])))
            var = pd.Series(ListaAtributos)
            return var 
        if Atributo == 'SSC':
            for i, v in enumerate(A):
                ListaAtributos.append(F.SSC(np.array(A[i])))
            ssc = pd.Series(ListaAtributos)
            return ssc 
        if Atributo == 'MAV':
            for i, v in enumerate(A):
                ListaAtributos.append(F.MAV(np.array(A[i])))
            mav = pd.Series(ListaAtributos)
            return mav 
        if Atributo == 'WL':
            for i, v in enumerate(A):
                ListaAtributos.append(F.WL(np.array(A[i])))
            wl = pd.Series(ListaAtributos)
            return wl
        pass

    def DataFrameCarac(self, TRIGGER, SINAL, a, sRep=False):
        FeaturesEEG = pd.DataFrame()
        for i in range(len(SINAL)):
            atributo = self.VetorATRIBUTOS(TRIGGER, SINAL[i], a, sRep)
            FeaturesEEG['CH'+str(i)+'_'+a] = atributo

        return FeaturesEEG