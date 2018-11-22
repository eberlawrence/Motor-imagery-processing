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
        return eegSinal