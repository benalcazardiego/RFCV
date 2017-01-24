from PyQt4 import QtGui
from lib.util.SweepType import SweepType
from lib.util.SourceType import SourceType
from lib.util.SourceMode import SourceMode
from lib.SMUSweep import SMUSweep #
from lib.SMUStep import SMUStep
from lib.SMUConstant import SMUConstant #
from lib.SMU import SMUConfigError
from lib.K4200 import K4200
from lib.SocketExecutor import SocketExecutor
import socket
import thread
import time

class MeasureHandler(QtGui.QMainWindow):

    def __init__(self, ip=None, port=None):
        pass


    def handle(self, event, ui, params):
        #Generates the configuration and triggers the measurement with the K4200 for each active SMU
        #Starts a threaded obtaining of data for each SMU
        print "U R in MeasureHandler -> handle" #flag 4 debug
        try:
            #The connection is established at initialization
            self.device = K4200(self.ip, self.port)   
            
        except socket.error as e:
            QtGui.QMessageBox.critical(ui.centralwidget, "No se pudo conectar",
                    "Verifique el IP y puerto y vuelva a intentar")

        ip = ui.ipField.text()
        #Create a list of active SMUs and another of inactive ones
        active = list()
        inactive = list()
        mapping = [{'combo': ui.smu1_combo, 'layout': ui.smu1_layout},
                   {'combo': ui.smu2_combo, 'layout': ui.smu2_layout},
                   {'combo': ui.smu3_combo, 'layout': ui.smu3_layout},
                   {'combo': ui.smu4_combo, 'layout': ui.smu4_layout}]
        #Get parameters out of the GUI
        for element in mapping:
            if "open" not in element['combo'].currentText().toLower():
                active.append(element)
            else:
                inactive.append(element)

        try:
            for element in active:
                combo = element['combo']
                layout = element['layout']
                groupbox = layout.itemAt(2).widget()
                ch = int(str(combo.objectName())[3:4])
                source_mode = SourceMode.CURRENT if "current" in combo.currentText().toLower() else SourceMode.VOLTAGE
                source_type = SourceType.CURRENT if "current" in combo.currentText().toLower() else SourceType.VOLTAGE


                if "constant" in combo.currentText().toLower():
                    print "U R in MeasureHandler 'try:' -> constant"#flag 4 debug
                    value = float(groupbox.findChild(QtGui.QLineEdit, "constant_textbox").text()) #Reads the value in the interface and transforms it in "float"
                    compliance = float(groupbox.findChild(QtGui.QLineEdit, "compliance_textbox").text()) #Reads the compliance in the interface and transforms it in "float"
                    smu = SMUConstant(ch, source_mode, source_type, value, compliance, "V%s"%ch, "I%s"%ch)

                    print value, compliance #Test 4 debug
                    
                    self.device.attach(smu)

                elif "list" in combo.currentText().toLower():
                    print "U R in MeasureHandler 'try:' -> list"#flag 4 debug
                    
                    # Current list sweep configuration for SMU
                    # Channel don't have a list sourcing function (!)
                    value_list = groupbox.findChild(QtGui.QLineEdit, "list_textedit").text()
                    print value_list
                    pass

                elif "sweep" in combo.currentText().toLower():
                    print "U R in MeasureHandler 'try:' -> sweep"#flag 4 debug
                    
                    # Current sweep configuration for SMU
                    stop = float(groupbox.findChild(QtGui.QLineEdit, "val_stop_field").text())
                    start = float(groupbox.findChild(QtGui.QLineEdit, "val_inicio_field").text())
                    step = float(groupbox.findChild(QtGui.QLineEdit, "step_field").text())
                    compliance = float(groupbox.findChild(QtGui.QLineEdit, "compliance_field").text())
                    st = str(groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").currentText())
                    if st == "Linear":
                        sweep_type = SweepType.LINEAR
                    elif st == "Log10":
                        sweep_type = SweepType.LOG10
                    elif st == "Log25":
                        sweep_type = SweepType.LOG25
                    elif st == "Log50":
                        sweep_type = SweepType.LOG50

                    smu = SMUSweep(ch, source_mode, source_type, start, stop, step, compliance,
                                   sweep_type, 'V%s' % ch, "I%s"%ch)
                    self.device.attach(smu)

                elif "step" in combo.currentText().toLower():
                    print "U R in MeasureHandler 'try:' -> step"#flag 4 debug

                    
                    # Current step configuration for SMU
                    start = float(groupbox.findChild(QtGui.QLineEdit, "start_lineedit").text())
                    step = float(groupbox.findChild(QtGui.QLineEdit, "step_lineedit").text())
                    steps = int(groupbox.findChild(QtGui.QLineEdit, "steps_lineedit").text())
                    compliance = float(groupbox.findChild(QtGui.QLineEdit, "compliance_lineedit").text())

                    smu = SMUStep(ch, source_mode, source_type, start, step, steps, compliance,
                                  voltage_name='V%s'%ch, current_name='I%s'%ch)
                    self.device.attach(smu)


            print "Attached SMUs: %s" % len(self.device.smus)
            try:
                self.device.configure(ui) # Configure for measure
                self.device.measure() # Measure
                self.device.executor.close() # Close socket
                thread.start_new_thread(poll_for_data, (self.ip, self.port, ui, active))
            except socket.error as e:
                QtGui.QMessageBox.critical(ui.centralwidget, "No se pudo conectar",
                        "Verifique el IP y puerto y vuelva a intentar")

        except SMUConfigError as e:
            QtGui.QMessageBox.information(ui.centralwidget, "Revisar valores",
                    "Verifique el IP y puerto y vuelva a intentar")

def poll_for_data(ip, port, ui, active): ####

    print "U R in poll_for_data" #Flag 4 debug
    
    executor = SocketExecutor(ip, port)
    while True:
        executor.execute_command("SP") #
        is_ready = executor.get_data()
        is_ready = is_ready.replace("\0","")
        if 0b00000001 & int(is_ready):
            # Data is ready. Break out of this loop
            break
        time.sleep(1)
    # Retrieve data and save it to file
    for element in active:
        print "Run once per channel"
        combo = element['combo']
        ch = int(str(combo.objectName())[3:4])
        template = "DO 'CH{ch}T'"
        cmd = template.format(ch=ch)
        data = executor.ask(cmd)
        with open(str(ui.fileField.text())+ str(ch) + ".csv",'w+') as f:
            data = data.split(",")
            for line in data:
                f.write(line+"\r\n")

    executor.close()
