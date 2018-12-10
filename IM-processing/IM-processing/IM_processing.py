import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from OpenFile import SinalVoluntario
from Tools import Processing

sVoluntario = SinalVoluntario("FHILLIPE-E")
sEEG, tEEG = sVoluntario.CarregaEEG()
sEMG, tEMG = sVoluntario.CarregaEMG()


#tEMG = Tools.Amplificar(tEMG, 500)
#plt.plot(sEMG[0])
#plt.plot(sEMG[1],color='g')
#plt.plot(tEMG,color='r')
#plt.show()

P = Processing()
tEEG = P.Amplificar(tEEG, 50)
df = pd.DataFrame(sEEG)
filtroEEG = P.BandPassFilter(sEEG[0])

P.FFT(sEEG[0])
P.FFT(filtroEEG)

plt.plot(sEEG[0])
plt.plot(filtroEEG,color='g')
plt.plot(tEEG,color='r')
plt.show()
            

#t = np.array(range(len(tEEG)))/1024
#plt.plot(t, tEEG)
#plt.show()
    
#for i, v in enumerate(sEEG):
#    plt.subplot(10,1,i+1)
#    plt.plot(sEEG[i])
#plt.show()





