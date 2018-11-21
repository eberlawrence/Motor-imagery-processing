import pyedflib
import numpy as np

f = pyedflib.EdfReader("C:\\Users\\BioLab\\Desktop\\GitHub\\Motor-imagery-processing\\EEG_coleta\\FHILLIPE-E.edf")
n = f.signals_in_file
signal_labels = f.getSignalLabels()
sigbufs = np.zeros((n, f.getNSamples()[0]))
for i in np.arange(n):
    sigbufs[i, :] = f.readSignal(i)