##################################################################################################################################################################################
        ### Importando os packages utilizados no código ###
##################################################################################################################################################################################

import pywt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from OpenFile import SinalVoluntario
from Tools import Processing
import seaborn as sns
from TreinaValidacaoCruzada import TreinaValidacaoCruzada


##################################################################################################################################################################################
        ### Instanciando objetos ###
##################################################################################################################################################################################

P = Processing()
sVoluntario = SinalVoluntario("FHILLIPE-E")


##################################################################################################################################################################################
        ### Carregando os dados de EEG, EMG, Trigger e Respostas ###
##################################################################################################################################################################################


sEEG, tEEG = sVoluntario.CarregaEEG()
sEMG, tEMG = sVoluntario.CarregaEMG()
resp = sVoluntario.CarregaRESP()


##################################################################################################################################################################################
        ### Amplificando o valor do Trigger ###
##################################################################################################################################################################################

tEEG = P.Amplificar(tEEG, 50)
tEMG = P.Amplificar(tEMG, 500)


##################################################################################################################################################################################
        ### Filtrando os Dados com filtros Passa-Faixa (EEG -> 1 - 80 Hz , EMG -> 10 - 500 Hz) e Notch (60 Hz) ###
##################################################################################################################################################################################

pfEEG, pfEMG = P.BandPassFilter(sEEG, 1, 80, 1024), P.BandPassFilter(sEMG, 10, 500, 2000)
f_EEG, f_EMG = P.NotchFilter(pfEEG, 60, 1024), P.NotchFilter(pfEMG, 60, 2000)

sMov, sRep = P.VetorDeAmostras(tEEG, f_EEG[0])
P.FFT(sMov[15], tEEG, aux=False)

##################################################################################################################################################################################
        ### Carrega DataFrame com os atributos extraídos do sinal EEG ###
##################################################################################################################################################################################

A = P.DataFrameCarac(tEEG, f_EEG, 'RMS')
B = P.DataFrameCarac(tEEG, f_EEG, 'ZC')

AB = pd.concat([A, B], axis=1, ignore_index=True)

##################################################################################################################################################################################
        ### Treina o classicador - Validação cruzada - 10Fold ###
##################################################################################################################################################################################

Val1 = TreinaValidacaoCruzada(A, resp)
Val1.Parametros(mostraDivisao=False,group=False)
print(Val1.matrizDeConfusao)
print(Val1.tabelaDeClassificacao)







s = 0
P.FFT(f_EEG[s], tEEG)
plt.show()


##plt.plot(sEEG[10])
###plt.plot(filtroEEG,color='g')
###plt.plot(tEEG,color='r')
##plt.show()
            

###t = np.array(range(len(tEEG)))/1024
###plt.plot(t, tEEG)
###plt.show()
    
#for i, v in enumerate(sEEG):
#    plt.subplot(19,1,i+1)
#    plt.plot(sEEG[i])
#plt.show()




#plt.subplot(2,1,1)
#plt.plot(filtro60Hz)
#plt.plot(tEEG,color='red')
#plt.subplot(2,1,2)
#plt.plot(sEMG[0])
#plt.plot(sEMG[1])
#plt.plot(P.Amplificar(tEMG,100),color='red')
#plt.show()