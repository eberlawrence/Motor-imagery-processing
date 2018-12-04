import pyedflib
import numpy as np
import matplotlib.pyplot as plt

class SinalVoluntario():

    def __init__(self, nome):
        self.nome = nome

    def CarregaEEG(self):
        eegFile = pyedflib.EdfReader("EEG_coleta\\"+self.nome+".edf")
        n = eegFile.signals_in_file
        signal_labels = eegFile.getSignalLabels()
        eegSinal = np.zeros((n, eegFile.getNSamples()[0]))
        for i in np.arange(n):
            eegSinal[i, :] = eegFile.readSignal(i)
        triggerSinal = eegSinal[19].copy()
        eegSinal = np.delete(eegSinal, 19, 0)
        return eegSinal, triggerSinal
    
    
    def CarregaEMG(self):
        pass

           


sVoluntario = SinalVoluntario("FHILLIPE-I")
sEEG, tEEG = sVoluntario.CarregaEEG();
count = 0
for i, v in enumerate(tEEG):
    count = count + 1
    if v > 10 and count < 4500:
        tEEG[i] = 8 
    elif v > 10:
        count = 0
for i, v in enumerate(tEEG):
    more = False
    less = False
    if v > 10:
        if not any(tEEG[i - 8500 : i] > 10):
            less = True
        if not any(tEEG[i + 1 : i + 8500] > 10):
            more = True
        if more and less:
            tEEG[i] = 8
            



            

t = np.array(range(len(tEEG)))/1024
plt.plot(tEEG)
plt.show()

for i, v in enumerate(sEEG):
    plt.subplot(20,1,i+1)
    plt.plot(sEEG[i])
plt.show()

