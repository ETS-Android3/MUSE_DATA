from datetime import datetime
import pandas as pd
import numpy as np
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import dispatcher
from pythonosc import osc_server

from os.path import dirname, join
from com.chaquo.python import Python

port = 5000
start = 0

files_dir = str(Python.getPlatform().getApplication().getFilesDir())
filePath = join(dirname(files_dir), 'OSC-Python-Recording.csv')
recording = False
enable = False
count_row = 1
col1 = []
col2 = []
server = None
f = open(filePath, 'w+')

def eeg_accel(address: str, *args):
    global recording
    if recording:
        for arg in args:
            f.write("," + str(arg))
        f.write("\n")


def muse_handler(address, *args):
    """handle all muse data"""
    global recording
    global count_row
    global enable
    global col1
    global col2
    media = 0.00000000000

    if recording:
        if not enable and address == "/muse/acc":
            print("Enable")
            enable = True
        if enable:
            l = []
            if address == "/muse/acc":
                for arg in args:
                    l.append(float(arg))
                col1.append(l)
            else:
                for arg in args:
                    l.append(float(arg))
                col2.append(l)

            if len(col1) > 128 and len(col2) > 128:
                tot = np.concatenate((col1[0:128], col2[0:128]), axis=1)
                df = pd.DataFrame(tot, columns=['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z'])
                df = df.set_index('Accelerometer_X')
                df.iloc[1:129, :].to_csv(filePath, mode='w')#, header=False) mode='a'
                time.sleep(0.5)
                f.close()
                col1 = []
                col2 = []
                print("Shutdown")
                recording = False
                server.shutdown()   #The file is written, then stop the recording

            if (time.time() - start) > 3 :
                server.shutdown()
    else :
        server.shutdown()



def marker_handler(address: str, i):
    global recording
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    markerNum = address[-1]
    recording = True
    print("Recording Started.")
    if markerNum == "2":
        f.close()
        server.shutdown()


def main(ip):
    global recording
    global server
    global start

    df_acc = pd.DataFrame(columns=['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z'])
    df_gyro = pd.DataFrame(columns=['Gyro_X', 'Gyro_Y', 'Gyro_Z'])
    dispatche = dispatcher.Dispatcher()
    dispatche.map("/debug", print)
    dispatche.map("/muse/acc", muse_handler)
    dispatche.map("/muse/gyro", muse_handler)
    recording = True
    #dispatcher.map("/Marker/*", marker_handler)
    if server == None:
        server = osc_server.ThreadingOSCUDPServer((ip, port), dispatche)  # Sostituire con il tuo IP

    start = time.time()
    server.serve_forever()


if __name__ == "__main__":
    main()