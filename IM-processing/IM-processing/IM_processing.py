import numpy as np
import matplotlib.pyplot as plt
from OpenFile import SinalVoluntario

sVoluntario = SinalVoluntario("FHILLIPE-E")
#sEEG, tEEG = sVoluntario.CarregaEEG()
EMG = sVoluntario.CarregaEMG()
plt.plot(EMG[0])
plt.plot(EMG[1],color='g')
plt.plot(EMG[2],color='r')
plt.show()


            

#t = np.array(range(len(tEEG)))/1024
#plt.plot(t, tEEG)
#plt.show()
    
#for i, v in enumerate(sEEG):
#    plt.subplot(10,1,i+1)
#    plt.plot(sEEG[i])
#plt.show()

