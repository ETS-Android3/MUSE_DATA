import pandas as pd
import numpy as np
from numpy import mean, var, fft, diff, sign, correlate
from scipy.stats import kurtosis, skew
from os.path import dirname, join
from com.chaquo.python import Python
import csv
import math
from sklearn.preprocessing import MinMaxScaler

stringSens = "Accelerometer Gyro".split()
stringAx = "X Y Z".split()
stringFeature = "max min avg var skew kurt aut pks fpk".split()

clm2 = []
for s in range(2):
    for a in range(3):
        for f in range(9):
            if stringFeature[f] == "aut":
                for u in range(1, 11):
                    clm2.append(stringSens[s] + "-" + stringAx[a] + "-" + stringFeature[f] + str(u))
            else:
                if stringFeature[f] == "pks" or stringFeature[f] == "fpk":
                    for u in range(1, 6):
                        clm2.append(stringSens[s] + "-" + stringAx[a] + "-" + stringFeature[f] + str(u))
                else:
                    clm2.append(stringSens[s] + "-" + stringAx[a] + "-" + stringFeature[f])


def main():
    clm = ["Accelerometer_X", "Accelerometer_Y", "Accelerometer_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"]

    j = 0
    count_row = 0
    count_errors = 0

    files_dir = str(Python.getPlatform().getApplication().getFilesDir())
    #stringPathFile = join(dirname(__file__), 'OSC-Python-Recording.csv')
    stringPathFile = join(dirname(files_dir), 'OSC-Python-Recording.csv')
    list = [[]]#[[1.0,2.0,3.0,4.0,5.0,6.0], [1.0,2.0,3.0,4.0,5.0,6.0]]

    df = pd.read_csv(stringPathFile, header=1)#, usecols = clm)#, sep=",", header=1)#, chunksize=1, error_bad_lines=False)
    #for c,r in df.iterrows():

    row = []
        #for c in range(26, 32):
        #if c in clm:
        #try:
        #print(r)
        #row.append(r)#.astype(float))#.iloc[:, i]).astype(float).name)

        #except AttributeError:
        #    count_errors += 1
        #    print(count_errors, ' Error!')
        #    continue

        #if len(clm) == len(row):
            #list.append(row)   #return list(row)


        #else:
        #   print("Error")

    #return df.iloc[109].values

    for i in range(0, df.shape[1]):
        aux = []
        # Valore massimo
        aux.append(max(df.iloc[:, i]))  # mean(X.iloc[:, i]

        # Valore minimo
        aux.append(max(df.iloc[:, i]))

        # Valore medio
        aux.append(mean(df.iloc[:, i]))

        # Varianza
        aux.append(var(df.iloc[:, i], ddof=1))

        # Assimetria
        aux.append(skew(df.iloc[:, i]))

        # Curtosi
        aux.append(kurtosis(df.iloc[:, i]))

        # Autocorrelazione
        # acf = correlate(df[i], df[i], 'full')[-len(X[0]):]
        acf = correlate(df.iloc[:, i], df.iloc[:, i], 'full')[-len(df.iloc[:, 0]):]
        aut = []
        for j in range(acf.size):
            if j % 15 == 0:
                aut.append(acf[j])

        while len(aut) < 10:
            aut.append(acf[df.iloc[:, i].size - (10 - len(aut))])
        aux.extend(aut)

        # Trasformata discreta di Fourier
        fourier = (fft.rfft(df.iloc[:, i] - df.iloc[:, i].mean()))
        freq = fft.rfftfreq(df.iloc[:, i].size, d=1. / 15)
        inflection = diff(sign(diff(fourier)))
        peaks = (inflection < 0).nonzero()[0] + 1

        # primi 5 picchi trasformata di fourier
        peak = fourier[peaks]

        # Frequenza dei picchi della trasformata discreta di fourier
        signal_freq = freq[peaks]

        aux.extend(peak[:5])
        aux.extend(signal_freq[:5])
        # print("Len_peak ", len(peak[:5]), " Len_sig", len(signal_freq[:5]))
        row.extend(aux)

    print("lll:", len(row))

    #Normalization

    index = []

    clm2 = ['Accelerometer-X-max','Accelerometer-X-min','Accelerometer-X-avg','Accelerometer-X-var','Accelerometer-X-skew','Accelerometer-X-kurt',
        'Accelerometer-X-aut1','Accelerometer-X-aut2','Accelerometer-X-aut3','Accelerometer-X-aut4','Accelerometer-X-aut5','Accelerometer-X-aut6',
        'Accelerometer-X-aut7','Accelerometer-X-aut8','Accelerometer-X-aut9','Accelerometer-X-aut10','Accelerometer-X-pks1','Accelerometer-X-pks2',
        'Accelerometer-X-pks3','Accelerometer-X-pks4','Accelerometer-X-pks5','Accelerometer-X-fpk1','Accelerometer-X-fpk2','Accelerometer-X-fpk3',
        'Accelerometer-X-fpk4','Accelerometer-X-fpk5','Accelerometer-Y-max','Accelerometer-Y-min','Accelerometer-Y-avg','Accelerometer-Y-var',
        'Accelerometer-Y-skew','Accelerometer-Y-kurt','Accelerometer-Y-aut1','Accelerometer-Y-aut2','Accelerometer-Y-aut3','Accelerometer-Y-aut4',
        'Accelerometer-Y-aut5','Accelerometer-Y-aut6','Accelerometer-Y-aut7','Accelerometer-Y-aut8','Accelerometer-Y-aut9','Accelerometer-Y-aut10',
        'Accelerometer-Y-pks1','Accelerometer-Y-pks2','Accelerometer-Y-pks3','Accelerometer-Y-pks4','Accelerometer-Y-pks5','Accelerometer-Y-fpk1',
        'Accelerometer-Y-fpk2','Accelerometer-Y-fpk3','Accelerometer-Y-fpk4','Accelerometer-Y-fpk5','Accelerometer-Z-max','Accelerometer-Z-min',
        'Accelerometer-Z-avg','Accelerometer-Z-var','Accelerometer-Z-skew','Accelerometer-Z-kurt','Accelerometer-Z-aut1','Accelerometer-Z-aut2',
        'Accelerometer-Z-aut3','Accelerometer-Z-aut4','Accelerometer-Z-aut5','Accelerometer-Z-aut6','Accelerometer-Z-aut7','Accelerometer-Z-aut8',
        'Accelerometer-Z-aut9','Accelerometer-Z-aut10','Accelerometer-Z-pks1','Accelerometer-Z-pks2','Accelerometer-Z-pks3','Accelerometer-Z-pks4',
        'Accelerometer-Z-pks5','Accelerometer-Z-fpk1','Accelerometer-Z-fpk2','Accelerometer-Z-fpk3','Accelerometer-Z-fpk4','Accelerometer-Z-fpk5',
        'Gyro-X-max','Gyro-X-min','Gyro-X-avg','Gyro-X-var','Gyro-X-skew','Gyro-X-kurt','Gyro-X-aut1','Gyro-X-aut2','Gyro-X-aut3','Gyro-X-aut4',
        'Gyro-X-aut5','Gyro-X-aut6','Gyro-X-aut7','Gyro-X-aut8','Gyro-X-aut9','Gyro-X-aut10','Gyro-X-pks1','Gyro-X-pks2','Gyro-X-pks3','Gyro-X-pks4',
        'Gyro-X-pks5','Gyro-X-fpk1','Gyro-X-fpk2','Gyro-X-fpk3','Gyro-X-fpk4','Gyro-X-fpk5','Gyro-Y-max','Gyro-Y-min','Gyro-Y-avg','Gyro-Y-var',
        'Gyro-Y-skew','Gyro-Y-kurt','Gyro-Y-aut1','Gyro-Y-aut2','Gyro-Y-aut3','Gyro-Y-aut4','Gyro-Y-aut5','Gyro-Y-aut6','Gyro-Y-aut7','Gyro-Y-aut8',
        'Gyro-Y-aut9','Gyro-Y-aut10','Gyro-Y-pks1','Gyro-Y-pks2','Gyro-Y-pks3','Gyro-Y-pks4','Gyro-Y-pks5','Gyro-Y-fpk1','Gyro-Y-fpk2','Gyro-Y-fpk3',
        'Gyro-Y-fpk4','Gyro-Y-fpk5','Gyro-Z-max','Gyro-Z-min','Gyro-Z-avg','Gyro-Z-var','Gyro-Z-skew','Gyro-Z-kurt','Gyro-Z-aut1','Gyro-Z-aut2',
        'Gyro-Z-aut3','Gyro-Z-aut4','Gyro-Z-aut5','Gyro-Z-aut6','Gyro-Z-aut7','Gyro-Z-aut8','Gyro-Z-aut9','Gyro-Z-aut10','Gyro-Z-pks1','Gyro-Z-pks2',
        'Gyro-Z-pks3','Gyro-Z-pks4','Gyro-Z-pks5','Gyro-Z-fpk1','Gyro-Z-fpk2','Gyro-Z-fpk3','Gyro-Z-fpk4','Gyro-Z-fpk5']

        # Creazione matrice contenente i dati in un unico formato
    matrix1 = []
    j = 0
    for i in range(len(clm2)):
        con = 0
        if "pks" not in clm2[i]:
            values = row[i]
            #j = j+1
        else:
            values = absolute_value_complex_arr(row[i])
            #j = j+1
        #values = values.reshape((len(values), 1))
        matrix1.append(values)

    #matrix2 = []
    #for i in range(0, len(matrix1[0])):
    #rowStamp = []
    #for k in range(0, len(matrix1)):
    #    app = matrix1[k]
    #    rowStamp.extend(app)
    #    matrix2.append(rowStamp)
    matrix2 = matrix1


    for k in range(0, len(matrix2)):
        #for i in range(0, len(matrix2[0])):
        if isinstance(matrix2[k], str):
            matrix2[k] = float(matrix2[k])

       # Normalizzazione dei dati
    scaler = MinMaxScaler(feature_range=(0, 1))
    matrix2 = np.reshape(matrix2, [1,-1])
    #scaler = scaler.fit(matrix2)

    matrixFin = scaler.fit_transform(matrix2.T)
    #print(matrix2)
    #matrix2 = np.reshape(matrix2, [1,-1])

    #print(matrix2)

    for i in range(0, len(matrixFin)):
        #for k in range(0, len(matrixFin[0])):
        matrixFin[i] = matrixFin[i] * 1

    # Creazione del dataset Normalizzato
    #print(matrixFin)
    return matrixFin.T


# Funzione per il calcolo del valore assoluto dei numeri complessi
def absolute_value_complex_arr(parameter):
    auxC = []
    #for j in parameter:
    j = str(parameter)
    j = j.replace('(', '')
    j = j.replace(')', '')
    compl = complex(j)
    auxC.append(compl)

    real_part = list(np.real(auxC))
    imagin_part = list(np.imag(auxC))

    result = []
    for j in range(0, len(real_part)):
        res = math.sqrt(pow(real_part[j], 2) + pow(imagin_part[j], 2))
        result.extend([res])

    return np.asarray(result)