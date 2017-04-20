from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QFileDialog, QDialog
import LayoutUtil
import os
from MeasureHandler import MeasureHandler
from VnaMeasure import VnaMeasureThreaded
from lib.VnaChannel import VnaChannel
from lib.util.VnaEnums import Direction #
from utils import restore_ui  #
from utils import save_ui  #
from gui import MenuHandlers 
from Calibration import Ui_cal_dialog 
from Ri import Ui_RI_dialog
from ConAlt import Ui_conalt_dialog
from CalPresets import Ui_cal_presets
from RiHandlers import RiHandler
from CalHandlers import CalHandler 
from PresetHandlers import PresetHandler
from ConAltHandlers import ConAltHandler

class SlotContainer(QtGui.QMainWindow):

    print "U R in Handlers - 'SlotContainer' " #flag 4 debug
    
    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)
        self.ui = ui
        self.handler = MeasureHandler()
        self.curr_x = 0
        self.channel = None

#Check the options of the 'S' parametres that is going to measure:
    def checked_all(self, event):
        print "U R in Handlers - 'checked_all' " #flag 4 debug
        sender = self.sender()
        if sender.isChecked():
            self.ui.s11_radio.setEnabled(False)
            self.ui.s12_radio.setEnabled(False)
            self.ui.s21_radio.setEnabled(False)
            self.ui.s22_radio.setEnabled(False)
        elif not sender.isChecked():
            self.ui.s11_radio.setEnabled(True)
            self.ui.s12_radio.setEnabled(True)
            self.ui.s21_radio.setEnabled(True)
            self.ui.s22_radio.setEnabled(True)

#Browser. Selecting the directory where we're going to save our data:
    def browse(self, event):

        print "U R in Handlers - 'browse' " #flag 4 debug
        
        directory = QFileDialog.getExistingDirectory(self, 
                "Donde guardar?", "~", options=QFileDialog.ShowDirsOnly)
        if self.sender().objectName() == "browse_button":
            data_file = os.path.join(str(directory), str(self.ui.fileField.text()))
            self.ui.fileField.setText(data_file)
        elif self.sender().objectName() == "vna_browse_button":
            data_file = os.path.join(str(directory), str(self.ui.vna_file_field.text()))
            self.ui.vna_file_field.setText(data_file)

    def selected_start_stop(self, event):
        if self.ui.start_stop_radio.isChecked():
            print "Selected start stop"
            self.ui.bottom_layout.itemAt(3).widget().setParent(None)
            self.ui.bottom_layout.addWidget(LayoutUtil.get_start_stop_groupbox())

    def selected_center_span(self, event):
        if self.ui.center_span_radio.isChecked():
            print "Selected center span"
            self.ui.bottom_layout.itemAt(3).widget().setParent(None)
            self.ui.bottom_layout.addWidget(LayoutUtil.get_center_span_groupbox())

    def Graficar(self, event):
    
        print "U R in Handlers - 'Graficar' " #flag 4 debug
        #Function "Graficar". Summary goes here:
        #
        # This function graph the data
        """
        x = [1,2,3]
        y = [5,7,4]

        x1 = [1,5,2]
        y1 = [8,5,2]

        plt.plot(x,y,label='Muestra 1')
        plt.plot(x1,y1,label='Muestra 2')
        plt.xlabel('Voltaje [V]')
        plt.ylabel('Capacitancia [C]')
        plt.title('Voltaje vs Capacitancia')
        plt.legend()
        plt.show()  
        """
    
    def get_port_ip(self):
        print "U R in Handlers - 'get_port_ip' " #flag 4 debug
        try:
            ip_port = str(self.ui.ipField.text()).split(":")
            ip = ip_port[0]
            port = int(ip_port[1])
            self.handler.ip = ip
            self.handler.port = port
            return (ip, port)
        except IndexError:
            QtGui.QMessageBox.information(self.ui.centralwidget, 
                    "IP no especificado", "Es necesario especificar un IP y puerto en el formato IP:puerto")

    def on_measure(self, event):
            
            print "U R in Handlers - 'on_measure' " #flag 4 debug
            # WARNING: MAGIC AHEAD
            # Handler expects ip and port as members of the self.handler object. 
            # get_port_ip() makes sure to put them there
            self.get_port_ip()
            params = self
            self.handler.handle(event, self.ui, params)

    def on_measure_select(self, event):
        # Two SMUs can't be in sweep mode or step mode at the same time! 
        # List sweep or constant is fair enough in more than one SMU

        print "U R in Handlers - 'on_measure_select' " #flag 4 debug
        
        print "ComboBox: {cbox}, Text = {ctext}".format(cbox=self.sender().objectName(), 
                                                ctext = self.sender().currentText())
        #print self.modes_activated
        # Pass the sender to the handling function
                 
        LayoutUtil.layout_update(self.sender(), self.ui)
   
    def on_vna_measure(self):
        print "U R in Handlers - 'on_vna_measure' " #flag 4 debug
        if self.channel is not None:
            self.channel.executor.close()
            self.channel = None # Makes sure move recreates its executor
        VnaMeasureThreaded(self.ui)

    def restore_ui(self):
        print "U R in Handlers - 'restore_ui' " #flag 4 debug
        
        restore_ui(self.ui)

    def save_ui(self):
        print "U R in Handlers - 'save_ui' " #flag 4 debug
        save_ui(self.ui)

    def launch_calibration(self):
        print "U R in Handlers - 'launch_calibration' " #flag 4 debug
        self.ui.cal_ui = Ui_cal_dialog() # Make the calibration dialog available app-wise
        dialog = QDialog()
        dialog.ui = self.ui.cal_ui
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        handler = CalHandler(self.ui)
        dialog.exec_()

    def launch_ri(self):
        print "U R in Handlers - 'launch_ri' " #flag 4 debug
        
        self.ui.ri_ui = Ui_RI_dialog() 
        dialog = QDialog()
        dialog.ui = self.ui.ri_ui
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        handler = RiHandler(self.ui)
        dialog.exec_()
        

    def launch_conalt(self):
        print "U R in Handlers - 'launch_conalt' " #flag 4 debug
        
        self.ui.conalt_ui = Ui_conalt_dialog() 
        dialog = QDialog()
        dialog.ui = self.ui.conalt_ui
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        handler = ConAltHandler(self.ui)
        dialog.exec_()


    def launch_preset_calibration(self):
        print "U R in Handlers - 'launch_preset_calibration' " #flag 4 debug
        
        self.ui.cal_presets_ui = Ui_cal_presets()
        dialog = QDialog()
        dialog.ui = self.ui.cal_presets_ui
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        handler = PresetHandler(self.ui)
        dialog.exec_()

    # TODO Move this elsewhere
    def move(self, direction):
        print "U R in Handlers - 'move' " #flag 4 debug
        
        ip_port = str(self.ui.vna_ip_field.text()).split(":")
        ip = ip_port[0]
        port = int(ip_port[1])
        if self.channel is None:
            self.channel = VnaChannel(ip, port, 1)
        self.channel.add_marker(1)
        start_x = self.channel.get_start_x()
        stop_x = self.channel.get_stop_x()
        bandwidth = stop_x - start_x
        gran = bandwidth/100 # By default 1/100th bandwidth granularity
        self.curr_x = self.channel.get_x()
        if direction == Direction.LEFT:
            self.curr_x = self.curr_x - gran # Save curr_x in container for future use
        elif direction == Direction.RIGHT:
            self.curr_x = self.curr_x + gran # Save curr_x in container for future use
        self.channel.set_x(self.curr_x)
        y = self.channel.get_y()

        self.ui.y_re_label.setText(str(y[0]))
        self.ui.y_im_label.setText(str(y[1]))
        self.ui.x_label.setText(str(self.curr_x))

    def move_left(self):
        print "U R in Handlers - 'move_left' " #flag 4 debug
        
        self.move(Direction.LEFT)  

    def move_right(self):
        print "U R in Handlers - 'move_right' " #flag 4 debug
        
        self.move(Direction.RIGHT)

    
    def open_file(self):
        print "U R in Handlers - 'open_file' " #flag 4 debug
        
        MenuHandlers.handle_open(self.ui)

    def save_file(self):
        print "U R in Handlers - 'save_file' " #flag 4 debug
        
        MenuHandlers.handle_save(self.ui)

    def save_as_file(self):
        print "U R in Handlers - 'save_as_file' " #flag 4 debug
        
        MenuHandlers.handle_save_as(self.ui)

    def close(self):
        print "U R in Handlers - 'close' " #flag 4 debug
        
        MenuHandlers.handle_close(self.ui)
