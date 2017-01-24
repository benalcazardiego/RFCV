#Description: Establish the commands to the VNA.
#             Do the measures and returns a "csv." or "excel" file       

import thread
from xlwt import Workbook
from PyQt4 import QtGui
from lib.VnaChannel import VnaChannel
from lib.util.VnaEnums import SParameters
from lib.util.VnaEnums import SweepType
from lib.util.VnaEnums import DataFormat
from lib.util.DataTransformers import z_from_s, y_from_s, cga_from_s, cgs_from_s
from lib.SocketExecutor import SocketExecutor
import time
sdata = [] # Initializing an empty array for the "S-Matrix"

def chunker(seq, size):
#Creates a generator object based on the elements in seq with with a size "size"

    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def VnaMeasureThreaded(ui):
    #Function "VnaMeasureThreaded". Summary goes here:
    #
    #Realizes the measurement into a thread   
    # Check if the ip and port are correct. And also if the 'box' for the
    #   measure of the 'S' Matrix is checked ("VnaMeasure") or not ("VnaMeasureSingle")
    
    print "U R in VnaMeasure - VnaMeasureThreaded" #FLAG FOR DEBUGGING
    print "STARTING A NEW MEASURE OF VNA!!!!!!!!!!!!!!!" #FLAG FOR DEBUGGING
    try:
        ip_port = str(ui.vna_ip_field.text()).split(":")
        ip = ip_port[0]
        port = int(ip_port[1])
    except IndexError as e:
        QtGui.QMessageBox.information(ui.centralwidget,"IP", "Se debe especificar un puerto y un IP en formato IP:puerto")
    if ui.all_checkbox.isChecked():
        thread.start_new_thread(VnaMeasure, (ui,ip, port))
    else:
        thread.start_new_thread(VnaMeasureSingle, (ui,ip, port))


def VnaMeasureSingle(ui, ip, port):
    #Function "VnaMeasureSingle". Summary goes here:
    #
    # THIS FUNCTION IS NOT WORKING RIGTH.
    
    print "U R in VnaMeasure - VnaMeasureSingle" #FLAG FOR DEBUGGING
    ui.measure_vna.setEnabled(False)
    ui.left_button.setEnabled(False)
    ui.right_button.setEnabled(False)

    channel = VnaChannel(ip, port, 1) # One channel
    # channel.reset()
    channel.set_sweep_type(SweepType.LINEAR)
    if ui.s11_radio.isChecked():
        spar = SParameters.S11
    elif ui.s12_radio.isChecked():
        spar = SParameters.S12
    elif ui.s21_radio.isChecked():
        spar = SParameters.S21
    elif ui.s22_radio.isChecked():
        spar = SParameters.S22
    points = str(ui.points_field.text())
    fmat = DataFormat.LOG # By default we use MLOG
    fmat_index = ui.format_combobox.currentIndex()
    formats = [DataFormat.LOG, 
               DataFormat.LIN, 
               DataFormat.LIN_PHASE, 
               DataFormat.PHASE, 
               DataFormat.GDELAY, 
               DataFormat.SMITH_LIN_PHASE, 
               DataFormat.SMITH_LOG_PHASE, 
               DataFormat.SMITH_RE_IM, 
               DataFormat.SMITH_R_JX, 
               DataFormat.SMITH_G_JB]

    fmat = formats[fmat_index]
    channel.set_one_channel()
    if ui.center_span_radio.isChecked():
        groupbox = ui.bottom_layout.itemAt(3).widget()
        center_freq = float(groupbox.findChild(QtGui.QLineEdit, "center_field").text())
        span_freq = float(groupbox.findChild(QtGui.QLineEdit, "span_field").text())
        channel.set_center_span(center_freq, span_freq)
        channel.set_traces(1)
        channel.set_points(points)
        channel.set_sparam(1, spar)
        channel.set_format(fmat) # set the selected format
        channel.activate_channel()
        channel.activate_trace(1)
        channel.set_continuous(True)
        
    elif ui.start_stop_radio.isChecked():
        groupbox = ui.bottom_layout.itemAt(3).widget()
        freq_start = float(groupbox.findChild(QtGui.QLineEdit, "freqstart_field").text())
        freq_stop = float(groupbox.findChild(QtGui.QLineEdit, "freqstop_field").text())
        channel.set_start_stop(freq_start, freq_stop)
        channel.set_traces(1)
        channel.set_points(points)
        channel.set_sparam(1, spar)
        channel.set_format(fmat) # set the selected format
        channel.activate_channel()
        channel.activate_trace(1)
        channel.set_continuous(True)

    if ui.autoscale_checkbox.isChecked():
        channel.auto_scale() # Autoscale

    f = str(ui.vna_file_field.text())
    channel.executor.close()
    # Reenable buttons once measure has finished
    ui.measure_vna.setEnabled(True)
    ui.left_button.setEnabled(True)
    ui.right_button.setEnabled(True)

    thread.start_new_thread(retrieve_data_single, (ip, port, f))  

def VnaMeasure(ui, ip, port):
    #Function "VnaMeasure". Summary goes here:
    #
    #Configure parameters for the VNA measurement of the four parameters
    #Measure of the four parametres of 'S' Matrix and save the data
    
    
    print "U R in VnaMeasure - VnaMeasure" #FLAG FOR DEBUGGING
    # Disable button after click:
    ui.measure_vna.setEnabled(False)
    ui.left_button.setEnabled(False)
    ui.right_button.setEnabled(False)
    #-------------------------------

    channel = VnaChannel(ip, port, 1) # One channel
    channel.set_four_channels()
    channel.set_bus_trigger()
    sdata = [] # Clean sdata for each measure
    for idx, spar in enumerate([SParameters.S11, SParameters.S12, SParameters.S21, SParameters.S22]):
        print "Now measuring: " + str(spar)
        channel.set_sweep_type(SweepType.LINEAR)
        channel.channel = idx + 1
        points = str(ui.points_field.text())
        fmat = DataFormat.LOG # By default we use MLOG
        fmat_index = ui.format_combobox.currentIndex()
        formats = [DataFormat.LOG, 
                   DataFormat.LIN, 
                   DataFormat.LIN_PHASE, 
                   DataFormat.PHASE, 
                   DataFormat.GDELAY, 
                   DataFormat.SMITH_LIN_PHASE, 
                   DataFormat.SMITH_LOG_PHASE, 
                   DataFormat.SMITH_RE_IM, 
                   DataFormat.SMITH_R_JX, 
                   DataFormat.SMITH_G_JB]

        fmat = formats[fmat_index]
        
        #Configure of the parameters for center-span
        if ui.center_span_radio.isChecked():
            groupbox = ui.bottom_layout.itemAt(3).widget()
            center_freq = float(groupbox.findChild(QtGui.QLineEdit, "center_field").text())
            span_freq = float(groupbox.findChild(QtGui.QLineEdit, "span_field").text())
            channel.set_center_span(center_freq, span_freq)
            channel.set_traces(1)
            channel.set_points(points)
            channel.set_sparam(1, spar)
            channel.set_format(fmat) # set the selected format
            channel.activate_channel()
            channel.activate_trace(1)
            channel.set_continuous(False)
            channel.set_immediate()
            channel.trigger()
        
        #Configure of the parameters for start-stop    
        elif ui.start_stop_radio.isChecked():
            groupbox = ui.bottom_layout.itemAt(3).widget()
            freq_start = float(groupbox.findChild(QtGui.QLineEdit, "freqstart_field").text())
            freq_stop = float(groupbox.findChild(QtGui.QLineEdit, "freqstop_field").text())
            channel.set_start_stop(freq_start, freq_stop)
            channel.set_traces(1)
            channel.set_points(points)
            channel.set_sparam(1, spar)
            channel.set_format(fmat) # set the selected format
            channel.activate_channel()
            channel.activate_trace(1)
            channel.set_continuous(False)
            channel.set_immediate()
            channel.trigger()

        if ui.autoscale_checkbox.isChecked():
            channel.auto_scale() # Autoscale
        while True:
            vna_ready = channel.is_ready()  
            if vna_ready:
                break
            time.sleep(1)
        f = str(ui.vna_file_field.text()) # Direction introduced by the user.
        # If the field is not specified, the direction by default is the directory of the "app.py"
        retrieve_data(ip, port, f, fmat, channel.executor) #Get the data
    while True:
            vna_ready = channel.is_ready()  
            if vna_ready:
                break
            time.sleep(1)
    
    for ch, sparam in zip([1,2,3,4], [SParameters.S11, SParameters.S12, SParameters.S21, SParameters.S22]):
        channel.channel = ch
        channel.set_sparam(1, sparam) #Set the four parameters

    channel.channel = 1
    channel.executor.close()
    
    # Reenable buttons once measure has finished
    ui.measure_vna.setEnabled(True)
    ui.left_button.setEnabled(True)
    ui.right_button.setEnabled(True)


def write_4vectors(lvectors, fname):
    #Function "retrieve_data". Summary goes here:
    #   
    #   lvectors = Data input. Always its the S,X,Y - Matrix
    #   fname = Direction introduced by the user.
    #            If the field is not specified, the direction by default is the directory of the "app.py"
    
    print "U R in write_4vectors" #FLAG FOR DEBUGGING
    
    def ctos(cmx):
    #Function "ctos". Summary goes here:
    #
    #   Description: Calculate the imaginary and real part.
    #   cmx = The input parameter        
        if cmx.imag == 0: # Float comparison. This might be bad
            return str(cmx.real) # Writing only the real part
        else: # write complex to number to a string
            return str(cmx.real) + "+" + str(cmx.imag) + "j" # Writing in the format '0.0+2.0j' (Example)

    with open("{fname}.csv".format(fname=fname), "w+") as f:
        for idx, d in enumerate(lvectors[0]):
            f.write(ctos(lvectors[0][idx])+","+ctos(lvectors[1][idx])+","+ctos(lvectors[2][idx])+","+ctos(lvectors[3][idx])+"\r\n")

def write_2vectors(lvectors, fname):
    #Function "retrieve_data". Summary goes here:
    #   
    #   lvectors = Data input. Always its the S,X,Y - Matrix
    #   fname = Direction introduced by the user.
    #            If the field is not specified, the direction by default is the directory of the "app.py"
    
    print "U R in write_2vectors" #FLAG FOR DEBUGGING
    
    def ctos(cmx):
    #Function "ctos". Summary goes here:
    #
    #   Description: Calculate the imaginary and real part.
    #   cmx = The input parameter          
        if cmx.imag == 0: # Float comparison. This might be bad
            return str(cmx.real) # Writing only the real part
        else: # write complex to number to a string
            return str(cmx.real) + "+" + str(cmx.imag) + "j" # Writing in the format '0.0+2.0j' (Example)

    with open("{fname}.csv".format(fname=fname), "w+") as f: #Storing results
        for idx, d in enumerate(lvectors[0]):
            try:
                f.write(ctos(lvectors[0][idx])+","+ctos(lvectors[1][idx])+"\r\n")
            except IndexError as e:
                print "Index mismatch"


def write_vector(vector, fname):
    print "U R in write_vector" #FLAG FOR DEBUGGING
    def ctos(cmx):
    #Function "ctos". Summary goes here:
    #
    #   Description: Calculate the imaginary and real part.
    #   cmx = The input parameter
        if cmx.imag == 0: # Float comparison. This might be bad
            return str(cmx.real) # Writing only the real part
        else: # write complex to number to a string
            return str(cmx.real) + "+" + str(cmx.imag) + "j" # Writing in the format '0.0+2.0j' (Example)

    with open(fname + ".csv", "w+") as f: #Storing results
        for line in vector:
            f.write(ctos(line)+"\r\n")


def retrieve_data_single(ip, port, fname):
    #Function "retrieve_data". Summary goes here:
    #
    #This function doesn't work
    print "U R in retrieve_data_single" #FLAG FOR DEBUGGING
    executor = SocketExecutor(ip, port, expect_reply=False, endline="\n")
    executor.execute_command(":FORM:DATA ASC") # Set data to ASCII

    data = executor.ask(":CALC1:DATA:FDAT?")
    data = data.split(",")
    data = [float(i) for i in data]
    write_vector(data, fname + "_sdata.csv")
    
    freq_data = executor.ask(":SENS1:FREQ:DATA?")
    freq_data = freq_data.split(",")
    freq_data = [float(i) for i in freq_data]
    write_vector(freq_data, fname + "_freqdata.csv")

    executor.close()


def save_data(S,freq_data):
    #Function "save_data". Summary goes here:
    #
    #This function save the data in an excel file.

    def ctos(cmx):
    #Function "ctos". Summary goes here:
    #
    #   Description: Calculate the imaginary and real part.
    #   cmx = The input parameter
        if cmx.imag == 0: # Float comparison. This might be bad
            return str(cmx.real) # Writing only the real part
        else: # write complex to number to a string
            return str(cmx.real) + "+" + str(cmx.imag) + "j" # Writing in the format '0.0+2.0j' (Example)
    
    wb = Workbook()
    sheet1 = wb.add_sheet('Resultados') #Adding a page to the excel doc
    #Adding label for the results:
    FVC_label = ["Frequency","Voltage","Cga","Cgs"]
    S_label = ["S11","S12","S21","S22"]
    Y_label = ["Y11","Y12","Y21","Y22"]
    Z_label = ["Z11","Z12","Z21","Z22"]
    for idx, d in enumerate(FVC_label):
        sheet1.write(0,idx,d)
    for idx, d in enumerate(S_label):
        sheet1.write(0,idx+4,d)
    for idx, d in enumerate(Y_label):
        sheet1.write(0,idx+4+4,d)
    for idx, d in enumerate(Z_label):
        sheet1.write(0,idx+8+4,d)
    #-----------------------------
        
    #Resizing the width of sheet columns
    for i in xrange(12+4): #12 due to the 4 elements of the 3 matrix
        sheet1.col(i).width = 4000;
    #-----------------------------------

    #Obtaining the Y and Z matrixm, and the capacitances:
    Y = y_from_s(S)
    Z = z_from_s(S)
    Cga = cga_from_s(freq_data,S)
    Cgs = cgs_from_s(freq_data,S)    
    #----------------------------------------------------

    #Writing the data in the excel file:       
    for idx,d in enumerate(freq_data):
        sheet1.write(idx+1,0,d)
    for idx,d in enumerate(Cga):
        sheet1.write(idx+1,2,d)
    for idx,d in enumerate(Cgs):
        sheet1.write(idx+1,3,d)     
    for idx, d in enumerate(S[0]):
        for i in xrange(4):
            sheet1.write(idx+1,i+4,ctos(S[i][idx]))
            sheet1.write(idx+1,i+4+4,ctos(Y[i][idx]))
            sheet1.write(idx+1,i+8+4,ctos(Z[i][idx]))
    wb.save('ResultadosExcel.xls')
    #-----------------------------------

    #Graph:
    '''
    plt.plot(freq_data,Cga,label='Cga')
    plt.plot(freq_data,Cgs,label='Cgs')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Capacitance [C]')
    plt.title('Frequency vs Capacitance')
    plt.legend()
    plt.show()
    '''
    #------
    
        
def retrieve_data(ip, port, fname, fmat, executor):
    #Function "retrieve_data". Summary goes here:
    #
    #   ip = Corresponds to the ip of the VNA. (In the case of my LAN network is 192.168.0.11)
    #   port = Corresponds to the port. (The configuration was made by port = 5025)
    #   fname = Direction introduced by the user.
    #            If the field is not specified, the direction by default is the directory of the "app.py"
    #   fmat = Format specifies by the user. For example: in the VNA interface we have formats like: SMITH, LOG, LIN, etc.
    #   executor = Corresponds to 'channel.executor'. The channel where the VNA is going to receive the instructios
    
    print "U R in retrieve_data" #FLAG FOR DEBUGGING
        
    def ctos(cmx):
    #Function "ctos". Summary goes here:
    #
    #   Description: Calculate the imaginary and real part.
    #   cmx = The input parameter
        if cmx.imag == 0: # Float comparison. This might be bad
            return str(cmx.real) # Writing only the real part
        else: # write complex to number to a string
            return str(cmx.real) + "+" + str(cmx.imag) + "j" # Writing in the format '0.0+2.0j' (Example)
            
    executor.execute_command(":FORM:DATA ASC") # Set data to ASCII
    data = executor.ask(":CALC1:DATA:FDAT?") # Call the VNA and make the respective operation
    data = data.split(",") # Make an array of string 'data'
    data = [complex(float(pair[0]), float(pair[1])) for pair in chunker(data, 2)] # Dealing with complex values, convert pairs into complex numbers even when
    #   returning reals, the VNA responds with rows of zeros for the imaginary part
    sdata.append(data) #Concatenate the information of 'data' in an array of 'sdata'

    
    #Imprimiendo los resultados en la pantalla: (Borrar despues)
    print '-----------------MATRIZ S--------------------'
    print sdata
    #-----------------------------------------

    if len(sdata) == 4: #Check if the 4 parametres of the 'S Matrix' were measured

        #Imprimiendo los resultados en pantalla:  (Borrar despues)
        print '-----------------MATRIZ Z--------------------'
        print z_from_s(sdata)
        print '-----------------MATRIZ Y--------------------'
        print y_from_s(sdata)
        #--------------------------------------
        
        
        #write_4vectors(sdata, fname+"_vna_s") # write 4 parameters S11, S12, S21, S22 of the 'S-Matrix' in a ".csv" file
        #write_4vectors(z_from_s(sdata), fname+"_vna_z") # write 4 parameters Z11, Z12, Z21, Z22 of the 'Z-Matrix' in a ".csv" file
        #write_4vectors(y_from_s(sdata), fname+"_vna_y") # write 4 parameters Y11, Y12, Y21, Y22 of the 'Y-Matrix' in a ".csv" file
        freq_data = executor.ask(":SENS1:FREQ:DATA?") # Ask VNA to do an operation
        #OP = executor.ask("*OPC?")  (Borrar despues)
        #print OP  (Borrar despues)
        print freq_data
        freq_data = freq_data.split(",") # Make an array of string 'data'
        
        freq_data = [float(i) for i in freq_data]
        
        save_data(sdata,freq_data)
        '''
        #write_2vectors([cga_from_s(freq_data, sdata),cgs_from_s(freq_data, sdata)], fname+"_cap") #Aditional parametres extracting from the 'S' matrix
        with open(fname + "_freqdata.csv", "w+") as f: #Storing the results in '.csv' file
            #for idx, d in enumerate(sdata[0]):
             #   f.write(str(freq_data[idx])+","+ctos(sdata[0][idx])+","+ctos(sdata[1][idx])+","+ctos(sdata[2][idx])+","+ctos(sdata[3][idx])+"\r\n")
            for line in freq_data:
                f.write(str(line)+"\r\n")
        '''         
        del sdata[0:len(sdata)]# Clean sdata
