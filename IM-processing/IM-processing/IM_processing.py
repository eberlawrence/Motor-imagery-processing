##################################################################################################################################################################################
        ### Importando os packages utilizados no código ###
##################################################################################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from OpenFile import SinalVoluntario
from Tools import Processing


##################################################################################################################################################################################
        ### Instanciando objetos ###
##################################################################################################################################################################################

P = Processing()
sVoluntario = SinalVoluntario("FHILLIPEE")


##################################################################################################################################################################################
        ### Carregando os dados de EEG, EMG e Trigger ###
##################################################################################################################################################################################

sEEG, tEEG = sVoluntario.CarregaEEG()
sEMG, tEMG = sVoluntario.CarregaEMG()

tEEG = P.Amplificar(tEEG, 50)
tEMG = Tools.Amplificar(tEMG, 500)






filtroEEG = P.BandPassFilter(sEEG)
filtro60Hz = P.NotchFilter(filtroEEG)

P.FFT(s, tEEG)
P.FFT(filtroEEG, tEEG)
P.FFT(filtro60Hz, tEEG)




#plt.plot(sEEG[10])
##plt.plot(filtroEEG,color='g')
##plt.plot(tEEG,color='r')
#plt.show()
            

##t = np.array(range(len(tEEG)))/1024
##plt.plot(t, tEEG)
##plt.show()
    
##for i, v in enumerate(sEEG):
##    plt.subplot(10,1,i+1)
##    plt.plot(sEEG[i])
##plt.show()




plt.subplot(2,1,1)
plt.plot(filtro60Hz)
plt.plot(tEEG,color='red')
plt.subplot(2,1,2)
plt.plot(sEMG[0])
plt.plot(sEMG[1])
plt.plot(P.Amplificar(tEMG,100),color='red')
plt.show()