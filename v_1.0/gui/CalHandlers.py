from lib.VnaChannel import VnaChannel
from lib.util.VnaEnums import CalType
from PyQt4 import QtGui
import thread
import time

class CalHandler(object):

    def __init__(self, ui):
        #Connects the buttons to the calibration metthods
        print "U R in CalHandlers - '__init__' " #flag 4 debug        
        self.ui = ui
        self.ui.cal_ui.open_button.clicked.connect(self.calibrate_open)
        self.ui.cal_ui.short_button.clicked.connect(self.calibrate_short)
        self.ui.cal_ui.load_button.clicked.connect(self.calibrate_load)
        self.ui.cal_ui.savecal_button.clicked.connect(self.save_cal)
        self.cal_type_selected = False
        self.cal_kit_selected = False
        self.channel = None
        self.cals_done = []

    def _connect_to_vna(self):
        #Returns a VnaChannel object
        print "U R in CalHandlers - '_connect_to_vna' " #flag 4 debug        
        
        if self.channel is not None:
            return self.channel # Reuse previously opened object (and socket)
        try:
            ip_port = str(self.ui.vna_ip_field.text()).split(":")
            ip = ip_port[0]
            port = int(ip_port[1])
            self.channel = VnaChannel(ip, port, 1) # Do connection
        except IndexError:
            QtGui.QMessageBox.information(self.ui.centralwidget,
                    "IP no especificado", 
                    "Es necesario especificar un IP y puerto en el formato IP:puerto")

    def _get_cal_data(self):
        #Returns the information of the calibration type and the calibration kit
        print "U R in CalHandlers - '_get_cal_data' " #flag 4 debug        
        
        if self.ui.cal_ui.cal_type_combo.currentIndex() == 0:
            cal_type = CalType.OPEN
        elif self.ui.cal_ui.cal_type_combo.currentIndex() == 1:
            cal_type = CalType.SHORT
        elif self.ui.cal_ui.cal_type_combo.currentIndex() == 2:
            cal_type = CalType.THRU
        elif self.ui.cal_ui.cal_type_combo.currentIndex() == 3:
            cal_type = CalType.FULL_2PORT
        elif self.ui.cal_ui.cal_type_combo.currentIndex() == 4:
            cal_type = CalType.FULL_1PORT

        if self.ui.cal_ui.cal_kit_combo.currentIndex() == 0:
            cal_kit = 1 # For 85033E
        
        return {"cal_type": cal_type, "cal_kit": cal_kit} 

    def _disable_buttons(self):
        #Disable calibration buttons
        print "U R in CalHandlers - '_disable_buttons' " #flag 4 debug        
        
        self.ui.cal_ui.open_button.setEnabled(False)
        self.ui.cal_ui.short_button.setEnabled(False)
        self.ui.cal_ui.load_button.setEnabled(False)
    
    def _selected_port(self):
        print "U R in CalHandlers - '_selected_port' " #flag 4 debug        
        
        return self.ui.cal_ui.port_combo.currentIndex() + 1
       
    def save_cal(self):
        #Saves the calibration results to the VNA
        print "U R in CalHandlers - 'save_cal' " #flag 4 debug        
        #channel is a Vna Channel object
        self.channel.save_cal()

    def calibrate_open(self):
        #Realize a open calibration
        print "U R in CalHandlers - 'calibrate_open' " #flag 4 debug        
        
        ret = QtGui.QMessageBox.information(self.ui.centralwidget, 
                "Conectar", "Conectar Open", buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Cancel:
            return
                
        def measure():
            print "U R in CalHandlers - 'calibrate_open' - measure " #flag 4 debug        
            
            self._connect_to_vna()
            self._disable_buttons()
            buttons = [self.ui.cal_ui.open_button, self.ui.cal_ui.short_button, self.ui.cal_ui.load_button]
            self.cals_done.append("open")
            thread.start_new_thread(enable_when_ready, (buttons, self.channel, self.cals_done))
            cal_data = self._get_cal_data()
            if not self.cal_kit_selected:
                self.channel.set_cal_kit(cal_data["cal_kit"])
                self.cal_kit_selected = True
            if not self.cal_type_selected:
                self.channel.set_cal_type(cal_data["cal_type"], self._selected_port())
                self.cal_type_selected = True
            self.channel.cal_measure_open(self._selected_port())

        thread.start_new_thread(measure, ())
        print "Calibrate open"

    def calibrate_short(self):
        #Realizes a short calibration
        print "U R in CalHandlers - 'calibrate_short' " #flag 4 debug        
        
        ret = QtGui.QMessageBox.information(self.ui.centralwidget, 
                "Conectar", "Conectar Short", buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Cancel:
            return
        
        def measure():
            print "U R in CalHandlers - 'calibrate_short' - measure " #flag 4 debug        
            
            self._connect_to_vna()
            self._disable_buttons()
            buttons = [self.ui.cal_ui.open_button, self.ui.cal_ui.short_button, self.ui.cal_ui.load_button]
            self.cals_done.append("short")
            thread.start_new_thread(enable_when_ready, (buttons, self.channel, self.cals_done))
            cal_data = self._get_cal_data()

            if not self.cal_kit_selected:
                self.channel.set_cal_kit(cal_data["cal_kit"])
                self.cal_kit_selected = True
            if not self.cal_type_selected:
                self.channel.set_cal_type(cal_data["cal_type"], self._selected_port())
                self.cal_type_selected = True

            self.channel.cal_measure_short(self._selected_port())

        thread.start_new_thread(measure, ())
        print "Calibrate short"

    def calibrate_load(self):
        #Realizes a load calibration
        print "U R in CalHandlers - 'calibrate_load' " #flag 4 debug        
        
        ret = QtGui.QMessageBox.information(self.ui.centralwidget, 
                "Conectar", "Conectar Load", buttons=QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Cancel:
            return
        
        def measure():
            print "U R in CalHandlers - 'calibrate_load' - measure " #flag 4 debug        
            
            self._connect_to_vna()
            self._disable_buttons()
            buttons = [self.ui.cal_ui.open_button, self.ui.cal_ui.short_button, self.ui.cal_ui.load_button]
            self.cals_done.append("load")
            thread.start_new_thread(enable_when_ready, (buttons, self.channel, self.cals_done))
            cal_data = self._get_cal_data()

            if not self.cal_kit_selected:
                self.channel.set_cal_kit(cal_data["cal_kit"])
                self.cal_kit_selected = True
            if not self.cal_type_selected:
                self.channel.set_cal_type(cal_data["cal_type"], self._selected_port())
                self.cal_type_selected = True
   
            self.channel.cal_measure_load(self._selected_port())
        
        thread.start_new_thread(measure, ())

        print "Calibrate load"

def enable_when_ready(buttons, channel, cals_done):
    print "U R in CalHandlers - 'enable_when_ready' " #flag 4 debug        
    
    while not channel.is_ready():
        time.sleep(1) # 1 Second

    for button in buttons:
        button.setEnabled(True)

    # Save when all calibrations have finished 
    if all(["open" in cals_done, "short" in cals_done, "load" in cals_done]):
        pass
