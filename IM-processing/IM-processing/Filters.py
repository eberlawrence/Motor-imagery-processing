import numpy as np
from scipy import signal


def PassaFiltros(DataFrameCH, F):
    '''    
    Retorna o SINAL filtrado:
    1 - Filtra sinal DC - Passa-Alta
    2 - Filtra sinal 60Hz, 120Hz e 180Hz
    3 - Retifica sinal
    4 - Filtra o sinal com um filtro Passa-Baixa
    '''
    #
    # Detalhes do sinal e parâmetros para a construção dos filtros
    #
    fs = 2000  # Frequência de amostragem (Hz)
    Fn60Hz = 60.0  # Frequência para remoer com o filtro NOTCH - Remover interferência da rede 60 HZ
    Fn120Hz = 120.0  # Frequência para remoer com o filtro NOTCH - Remover interferência da rede 120 HZ
    Fn180Hz = 180.0  # Frequência para remoer com o filtro NOTCH - Remover interferência da rede 180 HZ
    Fpa = 10.0 # Frequência de corte do filtro PASSA-ALTA - Remoção do Offset gerado pelo sinal DC
    Fpb = 10.0 # Frequência de corte do filtro PASSA-BAIXA - Suavização do sinal
    Q = 1  # Fator de qualidade do filtro NOTCH

    # Frequência normalizada:
    Wn60Hz = Fn60Hz/(fs/2) # Para o filtro NOTCH 60 Hz
    Wn120Hz = Fn120Hz/(fs/2) # Para o filtro NOTCH 120 Hz
    Wn180Hz = Fn180Hz/(fs/2) # Para o filtro NOTCH 180 HZ
    Wpb = Fpb/(fs/2) # Para o filtro PASSA-BAIXA
    Wpa = Fpa/(fs/2) # Para o filtro PASSA-ALTA

    #
    # Construção de filtros
    #
    b11, a11 = signal.iirnotch(Wn60Hz, Q) # Design notch filter - Fc = 60Hz
    b12, a12 = signal.iirnotch(Wn120Hz, Q) # Design notch filter - Fc = 120Hz
    b13, a13 = signal.iirnotch(Wn180Hz, Q) # Design notch filter - Fc = 180Hz
    b2, a2 = signal.butter(2, Wpa, 'highpass') # Design butter filter - Fc = 10Hz
    b3, a3 = signal.butter(6, Wpb, 'lowpass') # Design butter filter - Fc = 20Hz

    filtradoDC = signal.filtfilt(b2, a2, DataFrameCH) # Passa um filtro PASSA-ALTA para remover nível DC do SINAL
    filtradoRede = signal.filtfilt(b11, a11, filtradoDC) # Passa um filtro NOTCH no SINAL para remover 60Hz
    #filtradoRede2 = signal.filtfilt(b12, a12, filtradoRede1) # Passa um filtro NOTCH no SINAL para remover 60Hz
    #filtradoRede3 = signal.filtfilt(b13, a13, filtradoRede2) # Passa um filtro NOTCH no SINAL para remover 60Hz
    
    retificado = np.abs(filtradoRede) # Retifica o SINAL filtrado
    passaBaixa = signal.filtfilt(b3, a3, retificado) # Passa um filtro PASSA-BAIXA no SINAL retificado
    if F == 1:
        return filtradoDC
    if F == 2:
        return filtradoRede
    if F == 3:
        return retificado
    if F == 4:
        return passaBaixa 
    pass



