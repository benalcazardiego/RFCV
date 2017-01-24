#Continuous_alternate_GUI_creation
#Description: This module is the core of the sincronization process.
#The main function is con_alt_measure which is called in the module ConAltHandlers.py

from lib.util.SweepType import SweepType
from lib.util.SourceType import SourceType
from lib.util.SourceMode import SourceMode
from lib.SMUSweep import SMUSweep
from lib.SMUConstant import SMUConstant
from lib.K4200 import K4200
from lib.VnaChannel import VnaChannel
from lib.util.DataTransformers import z_from_s, y_from_s, cga_from_y, cgs_from_y, cga_from_s, cgs_from_s
from gui.VnaMeasure import chunker, write_vector, write_4vectors
from threading import RLock, Thread
from lib.util.VnaEnums import SParameters
import time
import pprint
import numpy
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PyQt4 import QtCore, QtGui
import MedicionesContinuoAlterno
from PyQt4.QtGui import QDialog
import csv

"""
    Prevent that the data dont overlap itself. Due the synchronization between
    K4200 & the Agilent (VNA), we need to be sure that the data is arriving correctly.
"""
#Definition of the blocks needed for the sincronization process
vlock = RLock()
klock = RLock()
gdata = {}  
params = [] 

"""
main function con_alt_measure
Inputs: smu_parameters, vna_parameters, delay, connection_keithley, connection_vna, puntosVNA, GUI object
*delay is the time the SMU is at each step
*Points are the number of steps made during the measurement
#conn is a list with the IP and the port 
"""

def con_alt_measure(smu_params, vna_params, delay, conn_keithley, conn_vna, puntosVNA, GUI):
    #Global variables used for the de-embedding process
    global yopen_path
    global alpha
    print "U R in ConAltMeasure - 'con_alt_measure' " 
    
    #Parameters obtaining fom the inputs
    points = smu_params["steps"]    
    sweep_time_SMU = delay*points  
    params.append(smu_params)   
    ch = smu_params["index"] + 1
    ch2 = ch + 1
    if smu_params["mode"] == "voltage":
        source_mode = SourceMode.VOLTAGE
        source_type = SourceType.VOLTAGE
    if smu_params["mode"] == "current":
        source_mode = SourceMode.CURRENT
        source_type = SourceType.CURRENT
    start = smu_params["start"]
    stop = smu_params["stop"]
    step = smu_params["step"]
    compliance = smu_params["compliance"]
    sweep_type = SweepType.LINEAR   # Always linear!
    
    # Voltage for the second SMU is always 0 (grounded)
    Output = 0
    
    #Creation of the SMUs objects  
    smu = SMUSweep(ch, source_mode, source_type, start, stop, step, 
            compliance, sweep_type, 'V%s' % ch, "I%s"%ch)
    smu2 = SMUConstant(ch2, source_mode, source_type, Output, compliance, 'V%s' % ch2, "I%s" %ch2)
    yx = numpy.linspace(start,stop,points)  #points include the limits points
    
    #Saving voltages vector
    smu_Vlist = []
    for i in range(1,points+1): 
        smu_Vlist.append(float(yx[i-1]))
    write_vector(smu_Vlist[1:-1], vna_params["file"] + "_V")    
    
    #Define function to measure the SCS (unnecessary)
    def measure_keithley(keithley): #Keithley is a K4200 instance object
        print "U R in ConAltMeasure - 'measure_keithley' " #flag 4 debug        
        klock.acquire()
        keithley.measure() 
        klock.release()         
    params.append(vna_params)
    
    #Saving frecuency vector 
    VNA_list = []    
    final = vna_params['freq_stop']
    ini = vna_params['freq_start']
    yx_VNA = numpy.linspace(ini,final,puntosVNA)
    for i in range(1,int(puntosVNA)+1): 
        VNA_list.append(float(yx_VNA[i-1]))
    write_vector(VNA_list, vna_params["file"] + "_F")    
    
    #Define function to measure the VNA
    def measure_vna(vna):
        print "U R in ConAltMeasure - 'measure_vna' "     
        vlock.acquire()    
        vna.beep()
        vna.trigger()
        vna.beep()
        vlock.release()
    
    #Initialization of the y_open_pad matrix 
    vector_zeros_open=[0]*3*points
    y_pad_flag=[vector_zeros_open,vector_zeros_open,vector_zeros_open,vector_zeros_open]
    yopen_path=[]
    for idx_freq in xrange(len(VNA_list)):
        yopen_path.append(y_pad_flag)
    alpha=1
    
    #Definition of the setup function, needed to communicate with the VNA, get the data and add it to the corresponding matrix.  
    def setup(execution_flag, idx_freq):
        global yopen_device
        global yopen_path
        global yshort
        global graf_cga
        global graf_cgs
        global cga
        global cgs
        global matriz_z11
        global vector_z11
        print "U R in con_alt_measure - Parametros previos del keithley"
        
        #Configuration of the SCS
        device = K4200(conn_keithley[0], conn_keithley[1])
        device.attach(smu)
        device.attach(smu2)
        device.configure()
        device.executor.execute_command("SS DT {time}".format(time=delay)) #Force a delay time "time" seconds
        device.executor.execute_command("SS HT {timeH}".format(timeH=0.0)) #Force a hold time "time" seconds
        
        print "U R in con_alt_measure - Dentro del LOOP de frecuencias"
        
        #Configuration of the VNA
        vna = VnaChannel(conn_vna[0], conn_vna[1], 1)
        vna.set_one_channel()
        vna.set_bus_trigger()
        vna.channel = 1
        vna.set_continuous(False)
        vna.set_immediate()
        vna.activate_channel()
        vna.set_traces(4) #Activate 4 traces
        sparamList = [None, SParameters.S11, SParameters.S12, SParameters.S21, SParameters.S22]
        for j in range(1,5):
            vna.set_sparam(j, sparamList[j]) 
            vna.activate_trace(j)
            vna.set_format(vna_params["format"])
        N=3     #measurement resolution
        vna.set_points(N*points) #Keithley points
        vna.set_sweep_time(sweep_time_SMU) 
        vna.set_sweep_delay(0.000)
        if vna_params["type"] == "center_span":
            vna.set_center_span(VNA_list[idx_freq], VNA_list[idx_freq])
        elif vna_params["type"] == "start_stop":
            vna.set_start_stop(VNA_list[idx_freq], VNA_list[idx_freq])
       
        #First sincronization loop assuming different configuration times
        while True:
            vlock.acquire()
            vna_ready = vna.is_ready()  
            vlock.release()
            if vna_ready:
                break
            time.sleep(1)
        
        #Definition of the threads
        threads = []
        measure_vna_t = Thread(target=measure_vna, args=(vna,))
        measure_keithley_t = Thread(target=measure_keithley, args=(device,))
        
        #Beginning of the measurement
        measure_vna_t.start()  
        measure_keithley_t.start()
        threads.append(measure_vna_t)  
        threads.append(measure_keithley_t)
        for t in threads:
            t.join()
        while True:
            vlock.acquire()
            vna_ready = vna.is_ready()  
            vlock.release()
            if vna_ready:
                break
            time.sleep(1)
        
        #Beginning of the data obtaining. The data from the SCS is not being recovered    
        threads = []
        check_keithley_t = Thread(target=check_keithley, args=(device,smu_params,sweep_time_SMU,))
        check_keithley_t.start()
        threads.append(check_keithley_t)
        for t in threads:
            t.join()
        threads = []
        
        #The data obteined from the VNA is saved into a different matrix depending on the button pushed    
        if execution_flag in [0,1,2]:
            check_vna_t = Thread(target=check_vna_short_open, args=(vna,vna_params,idx_freq,points, N, execution_flag,))
        elif execution_flag==3:
            yopen_device_single=yopen_device[idx_freq]
            yopen_path_single=yopen_path[idx_freq]
            yshort_single=yshort[idx_freq]
            check_vna_t = Thread(target=check_vna, args=(vna,vna_params,idx_freq,points, N, yopen_device_single, yopen_path_single, yshort_single,))
        elif execution_flag==4:
            check_vna_t = Thread(target=check_vna_no_deembedding, args=(vna, vna_params, idx_freq, points, N,))
        check_vna_t.start()
        
        threads.append(check_vna_t)
        for t in threads:
            t.join()
            
        #Addition of a curve to the graph and of a impedance vector to the impedance matrix    
        if execution_flag in [3,4]:
            graf_cga.append(cga)   
            graf_cgs.append(cgs)
            matriz_z11.append(vector_z11)
        time.sleep(2)
    
    #Definition of the slots for each option related to each button    
    def Slot0():
        global yopen_device
        QtGui.QMessageBox.information(GUI.centralwidget,"Open", "Conectar open - device")
        yopen_device=[]
        execution_flag=0
        for idx_freq in xrange(len(VNA_list)):
            setup(execution_flag, idx_freq)
    def Slot1():
        global yopen_path
        global alpha
        QtGui.QMessageBox.information(GUI.centralwidget,"Open", "Conectar open - pad")
        yopen_path=[]
        alpha=0.5
        execution_flag=1
        for idx_freq in xrange(len(VNA_list)):
            setup(execution_flag, idx_freq)
    def Slot2():
        global yshort
        QtGui.QMessageBox.information(GUI.centralwidget,"Short", "Conectar short")
        yshort=[]
        execution_flag=2
        for idx_freq in xrange(len(VNA_list)):
            setup(execution_flag, idx_freq)
    def Slot3():
        global matriz_z11
        global vector_z11
        global graf_cga
        global graf_cgs
        global cga
        global cgs
        execution_flag=3
        QtGui.QMessageBox.information(GUI.centralwidget,"DUT", "Conectar DUT")
        matriz_z11=[]
        graf_cga=[]
        graf_cgs=[]
        for idx_freq in xrange(len(VNA_list)):
            cga=[]
            cgs=[]
            vector_z11=[]
            setup(execution_flag, idx_freq)
        save_matrix(matriz_z11, 'Matriz_z11')
        graf_v=smu_Vlist[1:-1]
        print graf_v
        fig=plt.figure()
        gs = gridspec.GridSpec(1, 2)
        ax1=fig.add_subplot(gs[0])
        for i in graf_cga:
            print i
            ax1.plot(graf_v, i)
        ax2=fig.add_subplot(gs[1])
        for i in graf_cgs:
            ax2.plot(graf_v, i)
            print i
        plt.show()
    def Slot4():
        global matriz_z11
        global vector_z11
        global graf_cga
        global graf_cgs
        global cga
        global cgs
        execution_flag=4
        QtGui.QMessageBox.information(GUI.centralwidget,"DUT", "Conectar DUT")
        graf_cga=[]
        graf_cgs=[]
        matriz_z11=[]
        for idx_freq in xrange(len(VNA_list)):
            cga=[]
            cgs=[]
            vector_z11=[]
            setup(execution_flag, idx_freq)       
        save_matrix(matriz_z11, 'Matriz_z11_nd')
        graf_v=smu_Vlist[1:-1]
        print graf_v
        fig=plt.figure()
        gs = gridspec.GridSpec(1, 2)
        ax1=fig.add_subplot(gs[0])
        for i in graf_cga:
            print i
            ax1.plot(graf_v, i)
        ax2=fig.add_subplot(gs[1])
        for i in graf_cgs:
            ax2.plot(graf_v, i)
            print i
        plt.show()
    
    #Creation of the GUI and connection between the slots and the buttons.
    GUI.Medui_ui=MedicionesContinuoAlterno.Ui_Medicionescontinuoalterno()
    dialog = QDialog()
    dialog.ui = GUI.Medui_ui
    dialog.ui.setupUi(dialog, Slot0, Slot1, Slot2, Slot3, Slot4)
    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog.exec_()

#Definition of the functions used to check if the VNA is done with its actions    
def check_vna_short_open(vna, vna_params, idx_freq, points, N, shortoopen):
    print "U R in ConAltMeasure - 'check_vna' " #flag 4 debug        
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
        print "Waiting for VNA"
    print "VNA is ready"
    vna.beep()
    retrieve_short_open(vna, vna_params, idx_freq, points, N, shortoopen)
    reset_config(vna)
    vna.executor.close()
def check_vna(vna, vna_params, idx_freq, points, N, yopen_device, yopen_path, yshort):
    print "U R in ConAltMeasure - 'check_vna' " #flag 4 debug        
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
        print "Waiting for VNA"
    print "VNA is ready"
    vna.beep()
    retrieve_vna_data(vna, vna_params, idx_freq, points, N, yopen_device, yopen_path, yshort)
    reset_config(vna)
    vna.executor.close()
def check_vna_no_deembedding(vna, vna_params, idx_freq, points, N):
    print "U R in ConAltMeasure - 'check_vna' " #flag 4 debug        
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
        print "Waiting for VNA"
    print "VNA is ready"
    vna.beep()
    retrieve_vna_data_no_deembedding(vna, vna_params, idx_freq, points, N)
    reset_config(vna)
    vna.executor.close()

#Definition of the functions used to retrieve data from the VNA and save it to the corresponding matrix
def retrieve_short_open(vna, vna_params, idx_freq, points, N, shortoopen):
    global yopen_device
    global yopen_path
    global yshort
    sdata = []
    #freq_data = []
    template = ":CALC{ch}:TRAC{trace}:DATA:FDAT?" #template = "CALC:SEL:DATA:FDAT"
    channel = 1 # [S11,S12,S21,S22]
    for trac in range(1,5):
        data = vna.executor.ask(template.format(ch=str(channel),trace=str(trac)))
        data = data.split(',')
        data = [complex(float(pair[0]), float(pair[1])) for pair in chunker(data, 2)]
        sdata.append(data)
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
    print sdata
    if len(sdata) == 4:
        print "----Sdata----"
        print sdata
        while True:
            vlock.acquire()
            is_ready = vna.is_ready() #ask *OPC?
            vlock.release()
            if is_ready:
                break
            time.sleep(1)
        ydata = y_from_s(sdata)
        print ydata
        yguardar=[]
        for data in ydata:
            b7=data[N:N*(points-1)]
            c7=[]
            for i in range(0,points-2):
                c7.append(b7[N/2+N*i])
            yguardar.append(c7)
        if shortoopen == 0:
            yopen_device.append(ydata)
            write_4vectors(yguardar, vna_params["file"] + "_open_device" + str(idx_freq))
        if shortoopen == 1:
            yopen_path.append(ydata)
            write_4vectors(yguardar, vna_params["file"] + "_open_pad" + str(idx_freq))
        if shortoopen == 2:
            yshort.append(ydata)
            write_4vectors(yguardar, vna_params["file"] + "_short" + str(idx_freq))
def retrieve_vna_data(vna, vna_params, idx_freq, points, N, yopen_device, yopen_path, yshort):
    global alpha
    global cga
    global cgs
    global vector_z11
    print "U R in ConAltMeasure - 'retrieve_vna_data' " #flag 4 debug
    sdata = []
    freq_data = []
    template = ":CALC{ch}:TRAC{trace}:DATA:FDAT?" #template = "CALC:SEL:DATA:FDAT"
    channel = 1 #1 #El orden correcto es [S11,S12,S21,S22]
    for trac in range(1,5):
        data = vna.executor.ask(template.format(ch=str(channel),trace=str(trac)))
        data = data.split(',')
        data = [complex(float(pair[0]), float(pair[1])) for pair in chunker(data, 2)]
        sdata.append(data)
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
    print sdata
    if len(sdata) == 4:
        print "----Sdata----"
        print sdata
        template_freq = ":SENS{ch}:FREQ:DATA?"
        while True:
            vlock.acquire()
            is_ready = vna.is_ready() #ask *OPC?
            vlock.release()
            if is_ready:
                break
            time.sleep(1)
        freq_data = vna.executor.ask(template_freq.format(ch=1))
        freq_data = freq_data.split(',')
        freq_data = [float(fdatum) for fdatum in freq_data]
        print freq_data
        ydata = y_from_s(sdata)
        zdata = z_from_s(sdata)
        print "----ydata----"
        print ydata
        print "----zdata----"    
        print zdata
        y_tran_data=[[],[],[],[]]
        for indice in range(len(sdata[0])):
            y_open_device=numpy.matrix([[yopen_device[0][indice], yopen_device[1][indice]],[yopen_device[2][indice], yopen_device[3][indice]]])
            y_open_path=numpy.matrix([[yopen_path[0][indice], yopen_path[1][indice]],[yopen_path[2][indice], yopen_path[3][indice]]])
            y_short=numpy.matrix([[yshort[0][indice], yshort[1][indice]],[yshort[2][indice], yshort[3][indice]]])
            y_dut=numpy.matrix([[ydata[0][indice], ydata[1][indice]],[ydata[2][indice], ydata[3][indice]]])
            y_tran=((((y_dut-(alpha*(y_open_device-y_open_path)))**-1)-((y_short-(alpha*(y_open_device-y_open_path)))**-1))**-1)-((1-alpha)*(y_open_device-y_open_path))
            y_tran_data[0].append(y_tran.item(0,0))
            y_tran_data[1].append(y_tran.item(0,1))
            y_tran_data[2].append(y_tran.item(1,0))
            y_tran_data[3].append(y_tran.item(1,1))
        
        print "----freqdata----"
        print freq_data
        print "----ytrandata----"
        print y_tran_data
        cga_data = cga_from_y(freq_data, y_tran_data)
        cgs_data = cgs_from_y(freq_data, y_tran_data)
       
        b4=cga_data[N:N*(points-1)]
        c4=[]
        for i in range(0,points-2):
            c4.append(b4[N/2+N*i])
        cga_data=c4
            
        b5=cgs_data[N:N*(points-1)]
        c5=[]
        for i in range(0,points-2):
            c5.append(b5[N/2+N*i])
        cgs_data=c5
            
        print "----CGA----data----"
        print cga_data
        print "----CGS----data----"    
        print cgs_data
        
        cga=cga_data
        cgs=cgs_data
        
    
        sdataflag=[]
        for data in sdata:
            b1=data[N:N*(points-1)]
            c1=[]
            for i in range(0,points-2):
                c1.append(b1[N/2+N*i])
            sdataflag.append(c1)
        sdata=sdataflag
            
        zdataflag=[]
        for data in zdata:
            b2=data[N:N*(points-1)]
            c2=[]
            for i in range(0,points-2):
                c2.append(b2[N/2+N*i])
            zdataflag.append(c2)
        zdata=zdataflag
        vector_z11=zdata[0]
            
        ydataflag=[]
        for data in ydata:
            b3=data[N:N*(points-1)]
            c3=[]
            for i in range(0,points-2):
                c3.append(b3[N/2+N*i])
            ydataflag.append(c3)
        ydata=ydataflag
            
        ytrandataflag=[]
        for data in y_tran_data:
            b6=data[N:N*(points-1)]
            c6=[]
            for i in range(0,points-2):
                c6.append(b6[N/2+N*i])
            ytrandataflag.append(c6)
        y_tran_data=ytrandataflag
        print "----ytrandatacorto----"
        print y_tran_data
        
        
        #Inicializando arreglos para guardar sweep de resultados:
        write_vector(freq_data, vna_params["file"] + "_freqs" + str(idx_freq))
        write_4vectors(sdata, vna_params["file"] + "_s" + str(idx_freq))
        write_4vectors(zdata, vna_params["file"] + "_z" + str(idx_freq))
        write_4vectors(ydata, vna_params["file"] + "_y" + str(idx_freq))
        write_4vectors(y_tran_data, vna_params["file"] + "_y_transistor" + str(idx_freq))
        write_vector(cga_data, vna_params["file"] + "_CGA" + str(idx_freq))
        write_vector(cgs_data, vna_params["file"] + "_CGS" + str(idx_freq))
def retrieve_vna_data_no_deembedding(vna, vna_params, idx_freq, points, N):
    global cga
    global cgs
    global vector_z11
    print "U R in ConAltMeasure - 'retrieve_vna_data' " #flag 4 debug
    sdata = []
    freq_data = []
    template = ":CALC{ch}:TRAC{trace}:DATA:FDAT?" #template = "CALC:SEL:DATA:FDAT"
    channel = 1 # [S11,S12,S21,S22]
    for trac in range(1,5):
        data = vna.executor.ask(template.format(ch=str(channel),trace=str(trac)))
        data = data.split(',')
        data = [complex(float(pair[0]), float(pair[1])) for pair in chunker(data, 2)]
        sdata.append(data)
    while True:
        vlock.acquire()
        is_ready = vna.is_ready() #ask *OPC?
        vlock.release()
        if is_ready:
            break
        time.sleep(1)
    if len(sdata) == 4:
        print "----Sdata----"
        print sdata
        template_freq = ":SENS{ch}:FREQ:DATA?"
        while True:
            vlock.acquire()
            is_ready = vna.is_ready() #ask *OPC?
            vlock.release()
            if is_ready:
                break
            time.sleep(1)
        freq_data = vna.executor.ask(template_freq.format(ch=1))
        freq_data = freq_data.split(',')
        freq_data = [float(fdatum) for fdatum in freq_data]
        print freq_data
        ydata = y_from_s(sdata)
        zdata = z_from_s(sdata)
        print "----ydata----"
        print ydata
        print "----zdata----"    
        print zdata
                
        cga_data = cga_from_s(freq_data, sdata)
        cgs_data = cgs_from_s(freq_data, sdata)
        print "----CGA----data----"
        print cga_data
        print "----CGS----data----"    
        print cgs_data
        
               
        b4=cga_data[N:N*(points-1)]
        c4=[]
        for i in range(0,points-2):
            c4.append(b4[N/2+N*i])
        cga_data=c4
        
        b5=cgs_data[N:N*(points-1)]
        c5=[]
        for i in range(0,points-2):
            c5.append(b5[N/2+N*i])
        cgs_data=c5
        
        print "----CGA----data----"
        print cga_data
        print "----CGS----data----"    
        print cgs_data
        
        cga=cga_data
        cgs=cgs_data
        
        sdataflag=[]
        for data in sdata:
            b1=data[N:N*(points-1)]
            c1=[]
            for i in range(0,points-2):
                c1.append(b1[N/2+N*i])
            sdataflag.append(c1)
        sdata=sdataflag
        
        zdataflag=[]
        for data in zdata:
            b2=data[N:N*(points-1)]
            c2=[]
            for i in range(0,points-2):
                c2.append(b2[N/2+N*i])
            zdataflag.append(c2)
        zdata=zdataflag
        vector_z11=zdata[0]
        

        ydataflag=[]
        for data in ydata:
            b3=data[N:N*(points-1)]
            c3=[]
            for i in range(0,points-2):
                c3.append(b3[N/2+N*i])
            ydataflag.append(c3)
        ydata=ydataflag
    
        #Inicializando arreglos para guardar sweep de resultados:
        write_vector(freq_data, vna_params["file"] + "_freqs_nd" + str(idx_freq))
        write_4vectors(sdata, vna_params["file"] + "_s_nd" + str(idx_freq))
        write_4vectors(zdata, vna_params["file"] + "_z_nd" + str(idx_freq))
        write_4vectors(ydata, vna_params["file"] + "_y_nd" + str(idx_freq))
        write_vector(cga_data, vna_params["file"] + "_CGA_nd" + str(idx_freq))
        write_vector(cgs_data, vna_params["file"] + "_CGS_nd" + str(idx_freq))

#Definition of the functions used to check if the SCS is done with its actions
def check_keithley(device, smu_params,sweep_time_SMU):
    print "U R in ConAltMeasure - 'check_keithley' " #flag 4 debug        
    while True:
        klock.acquire()
        is_ready = device.is_ready()
        klock.release()
        if is_ready:
            break
        time.sleep(1)
        print "Waiting for K4200"
    print "K4200 is ready"
    #retrieve_keithley_data(device, smu_params)
    device.executor.close()
    time.sleep(sweep_time_SMU) 

#Definition of the functions used to retrieve data from the SCS and save it to the corresponding matrix (not used)
def retrieve_keithley_data(device, smu_params):
    print "U R in ConAltMeasure - 'retrieve_keithley_data' " #flag 4 debug        
    ch = smu_params["index"] + 1
    cmd = "DO 'CH{ch}T'".format(ch=ch)
    data = device.executor.ask(cmd)
    print "Keithley Data:"
    pprint.pprint(data)
    data = data.split(",")
    gdata["pol"] = data
    print "----Keithley----data----"    
    print data

#Definition of the function used to save an impedance matrix
def save_matrix(matrix,filename):
    c1=[]
    for item in matrix:
        c2=[]
        for subitem in item:
            subitem=str(subitem.real)+"+"+str(subitem.imag)+"j"
            c2.append(subitem)
        c1.append(c2)
    matrix=c1
    ar=zip(*matrix)
    ar = numpy.array(ar)
    fl = open(filename+'.csv', 'w')
    writer = csv.writer(fl)
    for values in ar:
        writer.writerow(values)
    fl.close()
    
#Definition of the function used to reset the configuration of the VNA
def reset_config(vna):
    print "U R in ConAltMeasure - 'reset_config' " #flag 4 debug        
    vna.set_internal_trigger()
    vna.set_one_channel()
    for ch in [1,2,3,4]:
        vna.channel = ch
        vna.set_immediate()