#Groupbox_definition
from PyQt4 import QtGui, QtCore 

def get_step_groupbox():
# function get_step_groupbox() from module SubUi.py
# #Returns the groupbox GUI element conformed by the fields:
# "Start, Step, Steps, Compliance" used when "Voltage Step" or "Current Step" are selected for a SMU

    step_groupbox = QtGui.QGroupBox()                                                                                                                      
    step_groupbox.setGeometry(QtCore.QRect(20, 20, 301, 171))
    step_groupbox.setTitle("")
    step_groupbox.setObjectName("step_groupbox")

    start_lineedit = QtGui.QLineEdit(step_groupbox)
    start_lineedit.setGeometry(QtCore.QRect(100, 30, 171, 25))
    start_lineedit.setObjectName("start_lineedit")

    step_lineedit = QtGui.QLineEdit(step_groupbox)
    step_lineedit.setGeometry(QtCore.QRect(100, 60, 171, 25))
    step_lineedit.setObjectName("step_lineedit")

    steps_lineedit = QtGui.QLineEdit(step_groupbox)
    steps_lineedit.setGeometry(QtCore.QRect(100, 90, 171, 25))
    steps_lineedit.setObjectName("steps_lineedit")

    compliance_lineedit = QtGui.QLineEdit(step_groupbox)
    compliance_lineedit.setGeometry(QtCore.QRect(100, 120, 171, 25))
    compliance_lineedit.setObjectName("compliance_lineedit")

    start_label = QtGui.QLabel(step_groupbox)
    start_label.setGeometry(QtCore.QRect(20, 30, 53, 14))
    start_label.setObjectName("start_label")

    step_label = QtGui.QLabel(step_groupbox)
    step_label.setGeometry(QtCore.QRect(20, 60, 53, 14))
    step_label.setObjectName("step_label")
    steps_label = QtGui.QLabel(step_groupbox)
    steps_label.setGeometry(QtCore.QRect(20, 90, 53, 14))
    steps_label.setObjectName("steps_label")

    compliance_label = QtGui.QLabel(step_groupbox)
    compliance_label.setGeometry(QtCore.QRect(20, 120, 71, 16))
    compliance_label.setObjectName("compliance_label")

    start_label.setText("Start:")
    step_label.setText("Step:")
    steps_label.setText("Steps:")
    compliance_label.setText("Compliance:")


    return step_groupbox
 
def get_sweep_groupbox():
# function get_sweep_groupbox() from module SubUi.py
# #Returns the groupbox GUI element conformed by the fields: "Initial value, Final value, Compliance, Step" 
# and the combobox with the options "Linear, Log10, Log25, Log50" used when "Voltage Sweep" 
# or "Current Sweep" are selected for a SMU

    sweep_groupbox = QtGui.QGroupBox()
    sweep_groupbox.setGeometry(QtCore.QRect(30, 20, 271, 140))
    sweep_groupbox.setTitle("")
    sweep_groupbox.setObjectName("sweep_groupbox")

    
    sweep_type_label = QtGui.QLabel(sweep_groupbox)
    sweep_type_label.setGeometry(QtCore.QRect(6, 10, 81, 20))
    sweep_type_label.setObjectName("sweep_type_label")

    combobox = QtGui.QComboBox(sweep_groupbox)
    combobox.setGeometry(QtCore.QRect(100, 10, 161, 25))
    combobox.setObjectName("sweep_type_combobox")
    combobox.addItem("Linear")
    combobox.addItem("Log10")
    combobox.addItem("Log25")
    combobox.addItem("Log50")

    value_stop = QtGui.QLabel(sweep_groupbox)
    value_stop.setGeometry(QtCore.QRect(10, 90, 71, 16))
    value_stop.setObjectName("value_stop")
    value_stop.setText("Valor final: ")

    value_init = QtGui.QLabel(sweep_groupbox)
    value_init.setGeometry(QtCore.QRect(10, 50, 71, 16))
    value_init.setObjectName("value_init")
    value_init.setText("Valor inicio: ")

    val_inicio_field = QtGui.QLineEdit(sweep_groupbox)
    val_inicio_field.setGeometry(QtCore.QRect(100, 50, 161, 25))
    val_inicio_field.setObjectName("val_inicio_field")

    val_stop_field = QtGui.QLineEdit(sweep_groupbox)
    val_stop_field.setGeometry(QtCore.QRect(100, 80, 161, 25))
    val_stop_field.setObjectName("val_stop_field")
 

    compliance_label = QtGui.QLabel(sweep_groupbox)
    compliance_label.setGeometry(QtCore.QRect(10, 120, 80, 16))
    compliance_label.setObjectName("compliance_label")
    compliance_label.setText("Compliance: ")

    compliance_field = QtGui.QLineEdit(sweep_groupbox)
    compliance_field.setObjectName("compliance_field")
    compliance_field.setGeometry(QtCore.QRect(100, 110, 161, 25))

    step_label = QtGui.QLabel(sweep_groupbox)
    step_label.setGeometry(QtCore.QRect(10, 150, 80, 16))
    step_label.setObjectName("step_label")
    step_label.setText("Step: ")

    step_field = QtGui.QLineEdit(sweep_groupbox)
    step_field.setObjectName("step_field")
    step_field.setGeometry(QtCore.QRect(100, 140, 161, 25))

    return sweep_groupbox

def get_constant_groupbox():
# function get_constant_groupbox() from module SubUi.py
# #Returns the groupbox GUI element conformed by the fields: "Value, Compliance" used when "Voltage Constant"
# or "Current Constant" are selected for a SMU

    constant_groupbox = QtGui.QGroupBox()
    constant_groupbox.setGeometry(QtCore.QRect(10, 10, 181, 140))
    constant_groupbox.setTitle("")
    constant_groupbox.setObjectName("constant_groupbox")
    constant_label = QtGui.QLabel(constant_groupbox)
    constant_label.setGeometry(QtCore.QRect(10, 30, 61, 14))
    constant_label.setObjectName("constant_label")
    constant_textbox = QtGui.QLineEdit(constant_groupbox)
    constant_textbox.setGeometry(QtCore.QRect(100, 25, 113, 22))
    constant_textbox.setObjectName("constant_textbox") 
    constant_label.setText("Valor: ") 
    compliance_label = QtGui.QLabel(constant_groupbox)
    compliance_label.setGeometry(QtCore.QRect(10, 70, 90, 14))
    compliance_label.setText("Compliance: ")
    compliance_label.setObjectName("compliance_label")
    compliance_textbox = QtGui.QLineEdit(constant_groupbox)
    compliance_textbox.setGeometry(QtCore.QRect(100, 70, 113, 22))
    compliance_textbox.setObjectName("compliance_textbox")
    return constant_groupbox

def get_list_groupbox():
# function get_list_groupbox() from module SubUi.py
# #Returns the groupbox GUI element conformed by the text-edition box and its corresponding label 
# used when "Voltage List Sweep" or "Current List Sweep" are selected for a SMU

    list_groupbox = QtGui.QGroupBox()
    textEdit = QtGui.QTextEdit(list_groupbox)
    textEdit.setGeometry(QtCore.QRect(20, 30, 250, 140))
    textEdit.setObjectName("list_textedit")
    label = QtGui.QLabel(list_groupbox)
    label.setGeometry(QtCore.QRect(20, 5, 250, 19))
    label.setObjectName("label_description")
    label.setText("Lista de valores separados por comas")
    return list_groupbox

def get_start_stop_ui():
# function get_start_stop_ui() from module SubUi.py
# #Returns the groupbox GUI element conformed by the fields "Initial frecuency, Final frecuency, Range" 
# and the label "Frecuency" used when the "Start-Stop"type of medition is selected

    freq_groupbox = QtGui.QGroupBox()
    freq_groupbox.setGeometry(QtCore.QRect(20, 20, 250, 140))
    freq_groupbox.setObjectName("freq_groupbox")
    verticalLayoutWidget = QtGui.QWidget(freq_groupbox)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 250, 107))
    verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    verticalLayout = QtGui.QVBoxLayout(verticalLayoutWidget)
    verticalLayout.setMargin(0)
    verticalLayout.setObjectName("verticalLayout")
    horizontalLayout_6 = QtGui.QHBoxLayout()
    horizontalLayout_6.setObjectName("horizontalLayout_6")
    freqstart_label = QtGui.QLabel(verticalLayoutWidget)
    freqstart_label.setObjectName("freqstart_label")
    horizontalLayout_6.addWidget(freqstart_label)
    freqstart_field = QtGui.QLineEdit(verticalLayoutWidget)
    freqstart_field.setObjectName("freqstart_field")
    horizontalLayout_6.addWidget(freqstart_field)
    verticalLayout.addLayout(horizontalLayout_6)
    horizontalLayout_4 = QtGui.QHBoxLayout()
    horizontalLayout_4.setObjectName("horizontalLayout_4")
    freqstop_label = QtGui.QLabel(verticalLayoutWidget)
    freqstop_label.setObjectName("freqstop_label")
    horizontalLayout_4.addWidget(freqstop_label)
    freqstop_field = QtGui.QLineEdit(verticalLayoutWidget)
    freqstop_field.setObjectName("freqstop_field")
    horizontalLayout_4.addWidget(freqstop_field)
    verticalLayout.addLayout(horizontalLayout_4)
    horizontalLayout_5 = QtGui.QHBoxLayout()
    horizontalLayout_5.setObjectName("horizontalLayout_5")
    range_label = QtGui.QLabel(verticalLayoutWidget)
    range_label.setObjectName("range_label")
    horizontalLayout_5.addWidget(range_label)
    range_field = QtGui.QLineEdit(verticalLayoutWidget)
    range_field.setObjectName("range_field")
    horizontalLayout_5.addWidget(range_field)
    verticalLayout.addLayout(horizontalLayout_5)
    freq_groupbox.setTitle("Frecuencia")
    freqstart_label.setText("Frecuencia inicial")
    freqstop_label.setText("Frecuencia final")
    range_label.setText("Rango")
    return freq_groupbox

def get_center_span_ui():
# function get_center_span_ui() from module SubUi.py
# #Returns the groupbox GUI element conformed by the fields "Center, Span" and the label "Frecuency" 
# used when the "Center-Span" type of medition is selected

    freq_groupbox = QtGui.QGroupBox()
    freq_groupbox.setGeometry(QtCore.QRect(20, 20, 250, 148))
    freq_groupbox.setObjectName("freq_groupbox")
    verticalLayoutWidget = QtGui.QWidget(freq_groupbox)
    verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 250, 107))
    verticalLayoutWidget.setObjectName("verticalLayoutWidget")
    verticalLayout = QtGui.QVBoxLayout(verticalLayoutWidget)
    verticalLayout.setMargin(0)
    verticalLayout.setObjectName("verticalLayout")
    horizontalLayout_6 = QtGui.QHBoxLayout()
    horizontalLayout_6.setObjectName("horizontalLayout_6")
    center_label = QtGui.QLabel(verticalLayoutWidget)
    center_label.setObjectName("center_label")
    horizontalLayout_6.addWidget(center_label)
    center_field = QtGui.QLineEdit(verticalLayoutWidget)
    center_field.setObjectName("center_field")
    horizontalLayout_6.addWidget(center_field)
    verticalLayout.addLayout(horizontalLayout_6)
    horizontalLayout_4 = QtGui.QHBoxLayout()
    horizontalLayout_4.setObjectName("horizontalLayout_4")
    span_label = QtGui.QLabel(verticalLayoutWidget)
    span_label.setObjectName("span_label")
    horizontalLayout_4.addWidget(span_label)
    span_field = QtGui.QLineEdit(verticalLayoutWidget)
    span_field.setObjectName("span_field")
    horizontalLayout_4.addWidget(span_field)
    verticalLayout.addLayout(horizontalLayout_4)
    freq_groupbox.setTitle("Frecuencia")
    center_label.setText("Centro")
    span_label.setText("Span")
    return freq_groupbox