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

           


sVoluntario = SinalVoluntario("FHILLIPE-E")
sEEG, tEEG = sVoluntario.CarregaEEG();
count = 0
for i, v in enumerate(tEEG):
    count = count + 1
    if v > 10 and count < 5000:
        tEEG[i] = 8 
    elif v > 10:
        count = 0
count2 = 0
flag = False
for i, v in enumerate(tEEG):
    count2 = count2 + 1
    if v > 10  and count2 > 8500:
        j = i
        flag = True
        count2 = 0
    elif v > 10:
        flag = False
        count2 = 0
    elif v > 10 and flag == True:
        tEEG[j] = 8

        






t = np.array(range(len(tEEG)))/1024
plt.plot(tEEG)
plt.show()