# Layout_groupbox_management_for_the_SMUs
from PyQt4 import QtGui
import SubUi


def layout_update(sender, ui):
# function layout_update(sender, ui) from module LayoutUtil.py
# Arguments: sender, ui
## Deletes the corresponding groupbox when a option is chosen for the SMU operation mode for sender SMU in the GUI object ui
## and attaches the new one corresponding to the new configuration chosen.
        sender_name = str(sender.objectName())
        # The SMU is the sender
        # sender.objectName() is the SMU name which start with 'smu#'
        # Map sender name to layout
        mapping = {
            "smu1": ui.smu1_layout,
            "smu2": ui.smu2_layout,
            "smu3": ui.smu3_layout,
            "smu4": ui.smu4_layout
        }
        caller_layout = mapping[sender_name[0:4]]
        # The smu#_layout correspnding to the smu# changing is taken as caller_layout.
        # A new groupbox is created corresponding to the configurtion chosen, For open it is an empty one
        # The old groupbox corresponding to the previous configuration is deleted
        # The new groupbox is added to the SMU layout
        if "open" in sender.currentText().toLower():
            caller_layout.itemAt(2).widget().setParent(None) # Delete widget
            new_groupbox = QtGui.QGroupBox()
            caller_layout.addWidget(new_groupbox)
        if "list" in sender.currentText().toLower():
            new_groupbox = get_list_groupbox()
            caller_layout.itemAt(2).widget().setParent(None) # Delete widget
            caller_layout.addWidget(new_groupbox)
        elif "sweep" in sender.currentText().toLower():
            new_groupbox = get_sweep_groupbox()
            caller_layout.itemAt(2).widget().setParent(None) # Delete widget
            caller_layout.addWidget(new_groupbox)
        elif "step" in sender.currentText().toLower():
            new_groupbox = get_step_groupbox()
            caller_layout.itemAt(2).widget().setParent(None) # Delete widget
            caller_layout.addWidget(new_groupbox)
        elif "constant" in sender.currentText().toLower():
            new_groupbox = get_constant_groupbox()
            caller_layout.itemAt(2).widget().setParent(None) # Delete widget
            caller_layout.addWidget(new_groupbox)

# These functions only return the corresponding groupbox for each configuration. 
def get_constant_groupbox():
    return SubUi.get_constant_groupbox()

def get_sweep_groupbox():
    return SubUi.get_sweep_groupbox()

def get_step_groupbox():
    return SubUi.get_step_groupbox()

def get_list_groupbox():
    return SubUi.get_list_groupbox()
    
def get_center_span_groupbox():
    return SubUi.get_center_span_ui()

def get_start_stop_groupbox():
    return SubUi.get_start_stop_ui()
