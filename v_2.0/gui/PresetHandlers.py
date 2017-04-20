from lib.VnaChannel import VnaChannel
from lib.util.VnaEnums import CalType
from PyQt4 import QtGui
from lib.util.VnaEnums import DataFormat


class PresetHandler(object):

    def __init__(self, ui):
        self.ui = ui
        self.ui.cal_presets_ui.full_2port_button.clicked.connect(self.full_2port_cal)
        self.ui.cal_presets_ui.trl_2port_button.clicked.connect(self.trl_2port_cal)
        self.ui.cal_presets_ui.cal_kit_combo.currentIndexChanged.connect(self.toggle_buttons)
        self.executor = None

    def toggle_buttons(self):
        if self.ui.cal_presets_ui.cal_kit_combo.currentIndex() == 0:
            self.ui.cal_presets_ui.trl_2port_button.setEnabled(True)
        if self.ui.cal_presets_ui.cal_kit_combo.currentIndex() == 1:
            self.ui.cal_presets_ui.trl_2port_button.setEnabled(False)

    def _set_cal_kit(self):
        if self.ui.cal_presets_ui.cal_kit_combo.currentIndex() == 0:
            self.channel.set_cal_kit(1)
        elif self.ui.cal_presets_ui.cal_kit_combo.currentIndex() == 1:
            self.channel.set_cs5()
            self.channel.set_cal_kit(30)

    def _connect(self):
        if self.executor is not None:
            return self.channel # Reuse previously opened object (and socket)
        try:
            chan_number = int(self.ui.cal_presets_ui.channel_combo.currentText())
            self.channels = range(1,chan_number+1)
            ip_port = str(self.ui.vna_ip_field.text()).split(":")
            ip = ip_port[0]
            port = int(ip_port[1])
            self.channel = VnaChannel(ip, port, 1) # Do connection
        except IndexError:
            QtGui.QMessageBox.information(self.ui.centralwidget,
                    "IP no especificado",
                    "Es necesario especificar un IP y puerto en el formato IP:puerto")

    
    def initialize(self):
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
        return [params, points]
    
    def configure_channel(self, ka):
        vna=self.channel
        params=ka[0]
        points=ka[1]
        if params["type"] == "center_span":
            vna.set_center_span(params["freq_center"], params["freq_span"] )
        elif params["type"] == "start_stop":
            vna.set_start_stop(params["freq_start"], params["freq_stop"])
        vna.set_points(points)
    
    def configure_trace(self, ka, trace):
        params=ka[0]
        vna=self.channel
        vna.activate_trace(trace)
        vna.set_format(params["format"])
        #vna.executor.execute_command(":SENS{cha}:CORR:IMP:INP:MAGN 1".format(cha=ch))
        
    def impedance_recovery(self):
        vna=self.channel
        for ch in self.channels:
            vna.executor.execute_command(":SENS{cha}:CORR:IMP:INP:MAGN 50".format(cha=ch))
        
    def full_2port_cal(self):
        self._connect()                                 #Connects
        def assign_channels(vna):
            for ch in self.channels:
                vna.channel = ch
                vna.set_sparam(1, ch)
        self.channel.channel = 1
        ka=self.initialize()
        if len(self.channels) == 4:
            self.channel.set_four_channels()
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.set_sparam(1, ch)
                self.configure_channel(ka)
                self.configure_trace(ka, 1)
            for ch in self.channels:
                self.channel.channel = ch
                self._set_cal_kit()
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.set_cal_type(CalType.FULL_2PORT)
            QtGui.QMessageBox.information(self.ui.centralwidget,"Open", "Conectar open")
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.is_ready()
                self.channel.cal_measure_open(1)
                self.channel.is_ready()
                self.channel.cal_measure_open(2)
                self.channel.is_ready()
            assign_channels(self.channel)
            QtGui.QMessageBox.information(self.ui.centralwidget,"Short", "Conectar short")
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.is_ready()
                self.channel.cal_measure_short(1)
                self.channel.is_ready()
                self.channel.cal_measure_short(2)
                self.channel.is_ready()
            assign_channels(self.channel)
            QtGui.QMessageBox.information(self.ui.centralwidget,"Load", "Conectar load")
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.is_ready()
                self.channel.cal_measure_load(1)
                self.channel.is_ready()
                self.channel.cal_measure_load(2)
                self.channel.is_ready()
            assign_channels(self.channel)
            QtGui.QMessageBox.information(self.ui.centralwidget,"Thru", "Conectar thru")
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.is_ready()
                self.channel.cal_measure_thru(1, 2)
                self.channel.is_ready()
                self.channel.cal_measure_thru(2, 1)
                self.channel.is_ready()
            assign_channels(self.channel)
            isolation = QtGui.QMessageBox.question(self.ui.centralwidget,"Isolation", "Calibrar isolation? (opcional)", 
                    QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
            if isolation == QtGui.QMessageBox.Yes:
                QtGui.QMessageBox.information(self.ui.centralwidget,"Isolation", "Conectar load en 1 y 2")
                for ch in self.channels:
                    self.channel.channel = ch
                    self.channel.is_ready()
                    self.channel.cal_measure_isol(1, 2)
                    self.channel.is_ready()
                assign_channels(self.channel)
            self.channel.is_ready()
        
        else:
            self.channel.set_one_channel()                  #Displays 1 channel
            ch=1
            self.channel.channel = ch
            self.channel.activate_channel()
            self.channel.set_traces(4)
            self.configure_channel(ka)
            for s in [1, 2, 3, 4]:
                self.channel.set_sparam(s, s)
                self.configure_trace(ka, s)
            self.channel.activate_trace(1)
            self._set_cal_kit()
            self.channel.set_cal_type(CalType.FULL_2PORT)
            QtGui.QMessageBox.information(self.ui.centralwidget,"Open", "Conectar open")
            self.channel.channel = ch
            self.channel.is_ready()
            self.channel.cal_measure_open(1)
            self.channel.is_ready()
            self.channel.cal_measure_open(2)
            self.channel.is_ready()
            QtGui.QMessageBox.information(self.ui.centralwidget,"Short", "Conectar short")
            self.channel.channel = ch
            self.channel.is_ready()
            self.channel.cal_measure_short(1)
            self.channel.is_ready()
            self.channel.cal_measure_short(2)
            self.channel.is_ready()    
            QtGui.QMessageBox.information(self.ui.centralwidget,"Load", "Conectar load")
            self.channel.channel = ch
            self.channel.is_ready()
            self.channel.cal_measure_load(1)
            self.channel.is_ready()
            self.channel.cal_measure_load(2)
            self.channel.is_ready()
            QtGui.QMessageBox.information(self.ui.centralwidget,"Thru", "Conectar thru")
            self.channel.channel = ch
            self.channel.is_ready()
            self.channel.cal_measure_thru(1, 2)
            self.channel.is_ready()
            self.channel.cal_measure_thru(2, 1)
            self.channel.is_ready()
            self.channel.is_ready()
            '''
            isolation = QtGui.QMessageBox.question(self.ui.centralwidget,"Isolation", "Calibrar isolation? (opcional)", 
                    QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
            if isolation == QtGui.QMessageBox.Yes:
                QtGui.QMessageBox.information(self.ui.centralwidget,"Isolation", "Conectar load en 1 y 2")
                for ch in self.channels:
                    self.channel.channel = ch
                    self.channel.is_ready()
                    self.channel.cal_measure_isol(1, 2)
                    self.channel.is_ready()
                assign_channels(self.channel)
            self.channel.is_ready()
            '''
        #Set Full 2 port for each channel
        
        should_save = QtGui.QMessageBox.question(self.ui.centralwidget, "Guardar?", "Guardar calibracion?",
                QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        if should_save == QtGui.QMessageBox.Yes:
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.save_cal()
        
        #self.impedance_recovery()
            
        
    def trl_2port_cal(self):
        self._connect()
        for ch in self.channels:
            self.channel.channel = ch
            self.channel.set_cal_kit(1) # Calkit 85033E
            self.channel.set_cal_type(CalType.TRL_2PORT)
        QtGui.QMessageBox.information(self.ui.centralwidget,"Thru", "Conectar THRU")
        for ch in self.channels:
            self.channel.channel = ch
            self.channel.trl_thru_line(1, 2)
            self.channel.is_ready()
            self.channel.trl_thru_line(2, 1)
            self.channel.is_ready()
        QtGui.QMessageBox.information(self.ui.centralwidget,"Reflect", "Conectar REFLECT")
        
        for ch in self.channels:
            self.channel.channel = ch
            self.channel.trl_reflect(1)
            self.channel.is_ready()
            self.channel.trl_reflect(2)
            self.channel.is_ready()

        QtGui.QMessageBox.information(self.ui.centralwidget,"Line/Match", "Conectar Line Match")
        
        for ch in self.channels:
            self.channel.channel = ch
            self.channel.trl_line_match(1,2)
            self.channel.is_ready()
            self.channel.trl_line_match(2,1)
            self.channel.is_ready()

        should_save = QtGui.QMessageBox.question(self.ui.centralwidget, "Guardar?", "Guardar calibracion?",
                QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)

        if should_save == QtGui.QMessageBox.Yes:
            for ch in self.channels:
                self.channel.channel = ch
                self.channel.save_cal()
 

