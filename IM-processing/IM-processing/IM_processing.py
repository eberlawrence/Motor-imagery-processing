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
        count = 0
        for i, v in enumerate(triggerSinal):
            count = count + 1
            if v > 10 and count < 4500:
                triggerSinal[i] = 8 
            elif v > 10:
                count = 0
        for i, v in enumerate(triggerSinal):
            more, less = False, False
            if v > 10:
                if not any(triggerSinal[i - 8500 : i] > 10):
                    less = True
                if not any(triggerSinal[i + 1 : i + 8500] > 10):
                    more = True
                if more and less:
                    triggerSinal[i] = 8
        return eegSinal, triggerSinal    
    
    def CarregaEMG(self):
        dataEMG = open("EMG_coleta\\"+self.nome+"3.txt")
        rl = dataEMG.readlines()
        dataEMG.close()
        k = 0
        c1, c2, c3 = [], [], []

        while rl[k] != '[Dados]\n':
            k = k + 1
        k = k + 1
        while k < len(rl) - 1:
            a, b, c = rl[k].split()
            c1.append(float(a))
            c2.append(float(b))
            c3.append(float(c))
            k = k + 1
        return np.array([np.array(c1), np.array(c2), np.array(c3)])

           


sVoluntario = SinalVoluntario("FHILLIPE-E")
#sEEG, tEEG = sVoluntario.CarregaEEG()
EMG = sVoluntario.CarregaEMG()
plt.plot(EMG[0])
plt.plot(EMG[2],color='red')
plt.show()


            

#t = np.array(range(len(tEEG)))/1024
#plt.plot(t, tEEG)
#plt.show()
    
#for i, v in enumerate(sEEG):
#    plt.subplot(10,1,i+1)
#    plt.plot(sEEG[i])
#plt.show()

