from PyQt4 import QtGui
from ConAltMeasure import con_alt_measure 
from lib.util.VnaEnums import DataFormat

class ConAltHandler(object):
    def __init__(self, ui):
        print "U R in ConAltHandlers - '__init__' " #flag 4 debug        
        
        self.ui = ui
        self.executor = None
        self.ui.conalt_ui.conalt_measure.clicked.connect(self.measure_conalt)


    def measure_conalt(self):
        print "U R in ConAltHandlers - 'measure_conalt' " #flag 4 debug        
        
        self.smu_index = self.ui.conalt_ui.smu_combo.currentIndex()
        smu_combos = [self.ui.smu1_combo, self.ui.smu2_combo, self.ui.smu3_combo, self.ui.smu4_combo]
        smu_layouts = [self.ui.smu1_layout, self.ui.smu2_layout, self.ui.smu3_layout, self.ui.smu4_layout]
        self.current_combo = smu_combos[self.smu_index-1]
        self.smu_layout = smu_layouts[self.smu_index-1]
        self.smu_groupbox = self.smu_layout.itemAt(2).widget()
        
        try:
            self._validate_measure()
        except ConAltMeasureException as e:
            error_message = str(e) 
            QtGui.QMessageBox.critical(self.ui.centralwidget, "Error", error_message)
            return
        
        smu_params = self._get_smu_sweep_params() # validation passed, so this won't fail
        smu_params = [float(param) for param in smu_params] #

        #print smu_params
        
        if "current" in self.current_combo.currentText().toLower():
            smu_mode = "current"
        elif "voltage" in self.current_combo.currentText().toLower():
            smu_mode = "voltage"

        vna_parameters = self._get_vna_params()
        smu_parameters = {
            "index": self.smu_index - 1,
            "stop": smu_params[0],
            "start": smu_params[1],
            "step": smu_params[2],
            "compliance": smu_params[3],
            "steps": self._get_steps(), 
            "mode": smu_mode 
        }

        #print smu_parameters #Example output:{'index': 0, 'compliance': 0.01, 'stop': 2.0, 'start': 1.0, 'step': 0.5, 'steps': 3, 'mode': 'voltage'}
        
        delay = float(self.ui.conalt_ui.sweep_delay_field.text())
        puntosVNA = float(self.ui.points_field.text())
          
        ip_port_vna = str(self.ui.vna_ip_field.text()).split(":")
        ip_vna = ip_port_vna[0]
        port_vna = int(ip_port_vna[1])

        ip_port_keithley = str(self.ui.ipField.text()).split(":")
        ip_keithley = ip_port_keithley[0]
        port_keithley = int(ip_port_keithley[1])

        file_name_vna = str(self.ui.vna_file_field.text())
        file_name_keithley = str(self.ui.fileField.text())

        smu_parameters["file"] = file_name_keithley
        vna_parameters["file"] = file_name_vna

        #print vna_parameters
        GUI=self.ui
        con_alt_measure(smu_parameters, vna_parameters, delay, 
                (ip_keithley, port_keithley), (ip_vna, port_vna), puntosVNA, GUI)

    def _validate_measure(self):
    #Function "_validate_measure". Summary goes here:
    #   
    # Check if all the syntaxis of the input parametres of SMU, VNA and file location 
    #   are correct
        
        print "U R in ConAltHandlers - '_validate_measure' " #flag 4 debug        
        
        error_string = "Selected SMU is not configured for linear sweep in either voltage or current mode"


        if self.smu_index == 0:
            raise ConAltMeasureException("SMU must be selected")
        combo_text = self.current_combo.currentText().toLower()

        if "open" in combo_text:
            raise ConAltMeasureException(error_string)

        if "sweep" not in combo_text or "list" in combo_text:
            raise ConAltMeasureException(error_string)

        if not self._all_filled():
            raise ConAltMeasureException("All fields must be filled for the selected SMU")

        if not self._all_freq_filled():
            raise ConAltMeasureException("The frequency fields must be filled")

        if self.ui.conalt_ui.sweep_delay_field.text() == "":
            raise ConAltMeasureException("Specify a delay")

        try:
            ip_port_vna = str(self.ui.vna_ip_field.text()).split(":")
            ip_vna = ip_port_vna[0]
            port_vna = int(ip_port_vna[1])

            ip_port_keithley = str(self.ui.vna_ip_field.text()).split(":")
            ip_keithley = ip_port_keithley[0]
            port_keithley = int(ip_port_keithley[1])
        except IndexError as e:
            raise ConAltMeasureException("IP and port must be specified for VNA and K4200")

        file_name_vna = str(self.ui.vna_file_field.text())
        file_name_keithley = str(self.ui.fileField.text())

        if file_name_vna == "" or file_name_vna[-1] == "\\" or file_name_vna[-1] == "/":
            raise ConAltMeasureException("VNA file name must be set")
        
        if file_name_keithley == "" or file_name_keithley[-1] == "\\" or file_name_keithley[-1] == "/":
            raise ConAltMeasureException("K4200 file name must be set")

    def _all_freq_filled(self):
        print "U R in ConAltHandlers - '_all_freq_filled' " #flag 4 debug        
        
        groupbox = self.ui.bottom_layout.itemAt(3).widget()
        if self.ui.start_stop_radio.isChecked():
            freq_start = groupbox.findChild(QtGui.QLineEdit, "freqstart_field").text()
            freq_stop = groupbox.findChild(QtGui.QLineEdit, "freqstop_field").text()
            if freq_start == "" or freq_stop == "":
                return False
        
        if self.ui.center_span_radio.isChecked():
            freq_center = groupbox.findChild(QtGui.QLineEdit, "center_field").text()
            freq_span = groupbox.findChild(QtGui.QLineEdit, "span_field").text()
            if freq_center == "" or freq_span == "":
                return False

        return True

    def _all_filled(self):
        print "U R in ConAltHandlers - '_all_filled' " #flag 4 debug        
        
        smu_params = self._get_smu_sweep_params()
        smu_params = [param == "" for param in smu_params]
        return not any(smu_params)

    def _get_smu_sweep_params(self):
        print "U R in ConAltHandlers - '_get_smu_sweep_params' " #flag 4 debug        
        
        stop_qstr = self.smu_groupbox.findChild(QtGui.QLineEdit, "val_stop_field").text()
        start_qstr = self.smu_groupbox.findChild(QtGui.QLineEdit, "val_inicio_field").text()
        step_qstr = self.smu_groupbox.findChild(QtGui.QLineEdit, "step_field").text()
        compl_qstr = self.smu_groupbox.findChild(QtGui.QLineEdit, "compliance_field").text()
        stop_qstr=str(float(stop_qstr)+float(step_qstr))
        print stop_qstr
        start_qstr=str(float(start_qstr)-float(step_qstr))
        print start_qstr
        return [stop_qstr, start_qstr, step_qstr, compl_qstr]

    def _get_vna_params(self):
        print "U R in ConAltHandlers - '_get_vna_params' " #flag 4 debug        
        
        points = str(self.ui.points_field.text())
        fmat_index = self.ui.format_combobox.currentIndex()
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
        

        params = {}
        #params_puntos_vna = {}#---------
        groupbox = self.ui.bottom_layout.itemAt(3).widget()
        if self.ui.start_stop_radio.isChecked():
            freq_start = float(groupbox.findChild(QtGui.QLineEdit, "freqstart_field").text())
            freq_stop = float(groupbox.findChild(QtGui.QLineEdit, "freqstop_field").text())
        #   puntosVNA = float(ui.points_field.text())#---------
            params["format"] = fmat
            params["type"] = "start_stop"
            params["freq_start"] = freq_start
            params["freq_stop"] = freq_stop
        #  params_puntos_vna["puntosVNA"] = puntosVNA#---------
        elif self.ui.center_span_radio.isChecked():
            center_freq = float(groupbox.findChild(QtGui.QLineEdit, "center_field").text())
            span_freq = float(groupbox.findChild(QtGui.QLineEdit, "span_field").text())
            params["format"] = fmat
            params["type"] = "center_span"
            params["freq_center"] = center_freq
            params["freq_span"] = span_freq

        #print params #Example output: {'freq_stop': 20000000.0, 'type': 'start_stop', 'freq_start': 10000000.0, 'format': 2}
        return params#,params_puntos_vna


    def _get_steps(self):
    #Function "_get_steps". Summary goes here:
    #   
    # Calculate how many steps are in the SMU sweep.
    
        print "U R in ConAltHandlers - '_get_steps' " #flag 4 debug        
        
        sweep_params = self._get_smu_sweep_params()
        stop = float(sweep_params[0])
        start = float(sweep_params[1])
        step = float(sweep_params[2])

        steps = (stop-start)/step + 1.5
        print abs(int(steps))
        
        return abs(int(steps))


class ConAltMeasureException(Exception):
    pass
