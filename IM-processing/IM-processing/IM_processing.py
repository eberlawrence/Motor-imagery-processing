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
from FeaturesFunctions import Features

##################################################################################################################################################################################
        ### Instanciando objetos ###
##################################################################################################################################################################################

P = Processing()
sVoluntario = SinalVoluntario("VINICIUS-I")


##################################################################################################################################################################################
        ### Carregando os dados de EEG, EMG, Trigger e Respostas ###
##################################################################################################################################################################################


sEEG, tEEG = sVoluntario.CarregaEEG()
#sEMG, tEMG = sVoluntario.CarregaEMG()
resp = sVoluntario.CarregaRESP()
respDF = pd.Series(resp)
r = list(np.zeros(60))
r2 = list(np.zeros(60))
p = list(np.ones(60))
s = list(np.ones(60)*2)
r.extend(p)
r.extend(s)
r2.extend(s)

RESP = []
for i in range(60):
    RESP.append('Esquerda')
for i in range(60):
    RESP.append('Direita')
for i in range(60):
    RESP.append('Repouso')

RESP = np.array(RESP)

##################################################################################################################################################################################
        ### Amplificando o valor do Trigger ###
##################################################################################################################################################################################

tEEG[157038] = 16
tEEG[699563] = 16
tEEG = P.Amplificar(tEEG, 50)
#tEMG = P.Amplificar(tEMG, 500)


##################################################################################################################################################################################
        ### Filtrando os Dados com filtros Passa-Faixa (EEG -> 1 - 80 Hz , EMG -> 10 - 500 Hz) e Notch (60 Hz) ###
##################################################################################################################################################################################

pfEEG = P.BandPassFilter(sEEG, 1, 80, 1024)
#pfEMG = P.BandPassFilter(sEMG, 10, 500, 2000)
f_EEG = P.NotchFilter(pfEEG, 60, 1024)
#f_EMG = P.NotchFilter(pfEMG, 60, 2000)

##################################################################################################################################################################################
        ### Carrega DataFrame com os atributos extraídos do sinal EEG ###
##################################################################################################################################################################################

R = P.DataFrameCarac(tEEG, f_EEG, 'RMS', resp, flagResp=True)
R = R.sort_values('Resposta').drop('Resposta', 1)
RR = P.DataFrameCarac(tEEG, f_EEG, 'RMS', sRep=True)
RMS = pd.concat([R,RR[:60]]).reset_index(drop=True)



aM = P.DataFrameCarac(tEEG, f_EEG, 'DELTA_P', resp, flagResp=True)
aM = aM.sort_values('Resposta').drop('Resposta', 1)
aR = P.DataFrameCarac(tEEG, f_EEG, 'DELTA_P', sRep=True)
a = pd.concat([aM,aR[:60]]).reset_index(drop=True)

bM= P.DataFrameCarac(tEEG, f_EEG, 'THETA_P', resp, flagResp=True)
bM = bM.sort_values('Resposta').drop('Resposta', 1)
bR = P.DataFrameCarac(tEEG, f_EEG, 'THETA_P', sRep=True)
b = pd.concat([bM,bR[:60]]).reset_index(drop=True)

cM= P.DataFrameCarac(tEEG, f_EEG, 'ALPHA_P', resp, flagResp=True)
cM = cM.sort_values('Resposta').drop('Resposta', 1)
cR = P.DataFrameCarac(tEEG, f_EEG, 'ALPHA_P', sRep=True)
c = pd.concat([cM,cR[:60]]).reset_index(drop=True)

dM= P.DataFrameCarac(tEEG, f_EEG, 'BETA_P', resp, flagResp=True)
dM = dM.sort_values('Resposta').drop('Resposta', 1)
dR = P.DataFrameCarac(tEEG, f_EEG, 'BETA_P', sRep=True)
d = pd.concat([dM,dR[:60]]).reset_index(drop=True)

#eM= P.DataFrameCarac(tEEG, f_EEG, 'POT', resp, flagResp=True)
#eM = eM.sort_values('Resposta').drop('Resposta', 1)
#eR = P.DataFrameCarac(tEEG, f_EEG, 'POT', sRep=True)
#e = pd.concat([eM,eR[:60]]).reset_index(drop=True)

AB = pd.concat([RMS,a,b,c,d], axis=1, sort=False)
#AB.to_csv("C:\\Users\\BioLab\\Desktop\\GitHub\\Motor-imagery-processing\\IM-processing\\IM-processing\\VINICIUS-I.csv", sep=';', decimal=',')


ED = P.NormalizaDadosCOLUNA(AB.iloc[:120].copy())
ER = P.NormalizaDadosCOLUNA(pd.concat([AB.iloc[:60], AB.iloc[120:]]).reset_index(drop=True))
DR = P.NormalizaDadosCOLUNA(AB.iloc[60:180].reset_index(drop=True).copy())

t = pd.concat([R[:60],RR[:60]]).reset_index(drop=True)

##################################################################################################################################################################################
        ### Treina o classicador - Validação cruzada - 10Fold ###
##################################################################################################################################################################################
f = pd.concat([ED.iloc[:,(11-2)],ED.iloc[:,(47-2)]], axis=1, sort=False)
plt.scatter(ED.iloc[:,(11-2)],ED.iloc[:,(47-2)],c=r[:120])
plt.show()

# FHILLIPE
#ED1 = ED.iloc[:,[53, 68 ]]
#ER1 = ER.iloc[:,[45,55, 56, 76, 78, 84, 88, 89, 93]]
#DR1 = DR.iloc[:,[76, 78, 82]]
#ED1 = ED.iloc[:,[42, 44, 47, 54, 85]]
#ER1 = ER.iloc[:,[10, 15, 29, 34, 48, 53, 72]]
#DR1 = DR.iloc[:,[10, 15, 29, 34, 41, 48, 53, 72, 78, 91]]

# Vinicius
#ED1 = ED.iloc[:,[8, 9, 50, 53]]
#ER1 = ER.iloc[:,[0, 1, 2, 3, 4, 5, 19, 20, 21, 22, 23, 25, 38, 39, 40, 85]]
#DR1 = DR.iloc[:,[0, 1, 2, 3, 4, 5, 6, 16, 19, 20, 21, 22, 23, 24, 25, 26, 35, 38, 39, 40, 41, 42, 43, 44, 50, 51, 53,54,56,57, 85]]
#ED1 = ED.iloc[:,[14, 27, 31, 34, 86, 94]]
#ER1 = ER.iloc[:,[14, 76, 77, 80]]
#DR1 = DR.iloc[:,[8, 9, 76, 77, 83]]

Val1 = TreinaValidacaoCruzada(DR1, RESP[:120])
Val1.Parametros(group=True, nA=False)
print(Val1.matrizDeConfusao)
print(Val1.tabelaDeClassificacao)
#





from sklearn.model_selection import train_test_split  
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.model_selection import cross_val_score, GridSearchCV

X_train, X_test, y_train, y_test = train_test_split(AB, r, test_size = 0.40)   
svclassifier = SVC(kernel='linear')  
svclassifier.fit(X_train, y_train)
y_pred = svclassifier.predict(X_test)   
print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))  
scores = cross_val_score(svclassifier,aM, resp, cv=2)

X_train, X_test, y_train, y_test = train_test_split(aM, r, test_size = 0.40)   
param_grid = {'C':[0.1,1,10,100,1000], 'gamma':[1,0.1,0.01,0.001]}
grid_cv = GridSearchCV(SVC(kernel='linear'), param_grid, refit=True, verbose=2)
grid_cv.fit(X_train, y_train)
pred = grid_cv.predict(X_test)
print(confusion_matrix(y_test,pred)) 
print(classification_report(y_test,pred)) 




s = 2
P.PlotFFT(f_EEG[s], tEEG)
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





sMov, sRep = P.VetorDeAmostras(tEEG, f_EEG[0])
F = Features()
a = F.ALPHA_P(sMov[0])
P.PlotFFT(sMov[0], tEEG, aux=False)


plt.plot(sRep[3])
plt.plot(sMov[3])
plt.show()







#bM, bR = P.DataFrameCarac(tEEG, f_EEG, 'THETA_P'), P.DataFrameCarac(tEEG, f_EEG, 'THETA_P',sRep=True)
#cM, cR = P.DataFrameCarac(tEEG, f_EEG, 'ALPHA_P'), P.DataFrameCarac(tEEG, f_EEG, 'ALPHA_P',sRep=True)
#dM, dR = P.DataFrameCarac(tEEG, f_EEG, 'BETA_P'), P.DataFrameCarac(tEEG, f_EEG, 'BETA_P',sRep=True)
#eM, eR = P.DataFrameCarac(tEEG, f_EEG, 'POT'), P.DataFrameCarac(tEEG, f_EEG, 'POT',sRep=True)