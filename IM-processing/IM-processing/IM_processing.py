import numpy as np
import matplotlib.pyplot as plt
from OpenFile import SinalVoluntario
import Tools 

sVoluntario = SinalVoluntario("FHILLIPE-E")
sEEG, tEEG = sVoluntario.CarregaEEG()
sEMG, tEMG = sVoluntario.CarregaEMG()


tEMG = Tools.Amplificar(tEMG, 500)
plt.plot(sEMG[0])
plt.plot(sEMG[1],color='g')
plt.plot(tEMG,color='r')
plt.show()

tEEG = Tools.Amplificar(tEEG, 500)
plt.plot(sEEG[0])
plt.plot(sEEG[1],color='g')
plt.plot(tEEG,color='r')
plt.show()
            

#t = np.array(range(len(tEEG)))/1024
#plt.plot(t, tEEG)
#plt.show()
    
#for i, v in enumerate(sEEG):
#    plt.subplot(10,1,i+1)
#    plt.plot(sEEG[i])
#plt.show()

