import sys
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4 import QtCore                            #To add buttons
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut
from gui.Keithley import Ui_mainWindow
from gui.Handlers import SlotContainer              #Contains all the files of communication and measures
from gui.utils import restore_ui
#import trace


#def Aplicacion():
if __name__ == "__main__":

    app = QApplication(sys.argv)        #Generate loop
    window = QMainWindow()              #Create window
    ui = Ui_mainWindow()                #Create interface
    ui.setupUi(window)                  #Link interface to window
    combo_boxes = [ui.smu1_combo, ui.smu2_combo, ui.smu3_combo, ui.smu4_combo]  #Create comboboxes to choose the configurations of the 4 SMUs
    combo_groupboxes = [ui.smu1_groupbox, ui.smu2_groupbox, ui.smu3_groupbox, ui.smu4_groupbox] #Create groupboxes to define the different parameters for the 4 SMUs
    combo_elements = ["Open","Current Constant","Current Sweep",        #Create the list of the possible SMUs configurations to choose from in the comboboxes
                      "Current List Sweep", "Current Step",
                      "Voltage Constant", "Voltage Sweep",
                      "Voltage List Sweep", "Voltage Step",]
    container = SlotContainer(ui)       #Create container to save state between callbacks
    for box in combo_boxes:             #Links the SMUs possible configurations to each combobox
        for element in combo_elements:
            box.addItem(element)
        box.currentIndexChanged.connect(container.on_measure_select) #Connect SMUs comboboxes to callbacks

    ui.start_stop_radio.toggled.connect(container.selected_start_stop)      #Create and connect the button to choose the "Star-Stop" kind of medition for the VNA
    ui.center_span_radio.toggled.connect(container.selected_center_span)    #Create and connect the button to choose the "Center-Span" kind of medition for the VNA
    ui.measure_button.clicked.connect(container.on_measure)                 #Create and link button to start the measure with the SMUs
    ui.measure_vna.clicked.connect(container.on_vna_measure)                #Create and link button to start the measure with the VNA
    ui.browse_button.clicked.connect(container.browse)                      #Create button to access the directory where the SMU data is saved
    ui.vna_browse_button.clicked.connect(container.browse)                  #Create button to access the directory where the VNA data is saved

    #Adding a button to graph
    #ui.Graf_button.clicked.connect(container.Graficar)

    ui.actionAbrir.triggered.connect(container.open_file)                   #Create options in the file menu
    ui.actionGuardar.triggered.connect(container.save_file)
    ui.actionGuardar_como.triggered.connect(container.save_as_file)
    ui.actionSalir.triggered.connect(container.close)
    ui.actionCalibration.triggered.connect(container.launch_calibration)
    ui.actionCalibration_Presets.triggered.connect(container.launch_preset_calibration)
    ui.actionRI.triggered.connect(container.launch_ri)
    ui.actionContinuo_Alterno.triggered.connect(container.launch_conalt)

    ui.left_button.clicked.connect(container.move_left)                     #Create and link left button
    left_shortcut = QShortcut(QKeySequence(QtCore.Qt.ControlModifier + QtCore.Qt.Key_Left),
            ui.centralwidget)
    left_shortcut.setContext(QtCore.Qt.ApplicationShortcut)
    left_shortcut.activated.connect(container.move_left)

    ui.right_button.clicked.connect(container.move_right)                   #Create and link right button
    right_shortcut = QShortcut(QKeySequence(QtCore.Qt.ControlModifier + QtCore.Qt.Key_Right),
            ui.centralwidget)
    right_shortcut.setContext(QtCore.Qt.ApplicationShortcut)
    right_shortcut.activated.connect(container.move_right)

    ui.all_checkbox.stateChanged.connect(container.checked_all)             #Create and link the box to choose all the S parameters

    app.aboutToQuit.connect(container.save_ui)                              #Save the states before exiting
    restore_ui(ui)
    window.show()
    sys.exit(app.exec_())
        
#a=trace.Trace(timing=True)
#a.runfunc(Aplicacion)

