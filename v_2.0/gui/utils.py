#GUI_Configuration_state_management

import yaml
import gzip
from PyQt4 import QtGui

def ui_state(ui):
    """ Returns the current state of the GUI in an easily usable dict """
    state = dict()
    ip = str(ui.ipField.text())
    f = str(ui.fileField.text())

    ip_vna = str(ui.vna_ip_field.text())
    file_vna = str(ui.vna_file_field.text())

    state["ip"] = ip
    state["f"] = f

    state["ip_vna"] = ip_vna
    state["file_vna"] = file_vna

    state["combos"] = list()

    for index, combo in enumerate(
            [(ui.smu1_combo, ui.smu1_layout), 
             (ui.smu2_combo, ui.smu2_layout), 
             (ui.smu3_combo, ui.smu3_layout), 
             (ui.smu4_combo, ui.smu4_layout)]):
        combo_text = combo[0].currentText().toLower()
        layout = combo[1]
        groupbox = layout.itemAt(2).widget()
        if "open" in combo_text:
# Combobox empty, don't save anything
            continue
        hdict = dict()
        hdict["num"] = str(index+1)
        if "voltage" in combo_text:
            hdict["type"] = "voltage"
        if "current" in combo_text:
            hdict["type"] = "current"
        if "constant" in combo_text:
            hdict["value"] = str(groupbox.findChild(QtGui.QLineEdit, "constant_textbox").text())
            hdict["compliance"] = str(groupbox.findChild(QtGui.QLineEdit, "compliance_textbox").text())
            hdict["sfun"] = "constant"
        if "step" in combo_text:
            hdict["start"] = str(groupbox.findChild(QtGui.QLineEdit, "start_lineedit").text())
            hdict["step"] = str(groupbox.findChild(QtGui.QLineEdit, "step_lineedit").text())
            hdict["steps"] = str(groupbox.findChild(QtGui.QLineEdit, "steps_lineedit").text())
            hdict["compliance"] = str(groupbox.findChild(QtGui.QLineEdit, "compliance_lineedit").text())
            hdict["sfun"] = "step"
        if "sweep" in combo_text and "list" not in combo_text:
            hdict["stop"]  = str(groupbox.findChild(QtGui.QLineEdit, "val_stop_field").text())
            hdict["start"] = str(groupbox.findChild(QtGui.QLineEdit, "val_inicio_field").text())
            hdict["step"]  = str(groupbox.findChild(QtGui.QLineEdit, "step_field").text())
            hdict["compliance"] = str(groupbox.findChild(QtGui.QLineEdit, "compliance_field").text())
            hdict["sweep_type"] = str(groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").currentText())
            hdict["sfun"] = "sweep"
        if "list" in combo_text:
            hdict["value_list"] = str(groupbox.findChild(QtGui.QTextEdit, "list_textedit").toPlainText())
            hdict["sfun"] = "list"

        state["combos"].append(hdict)

    # VNA GUI saving from here

    a = map(lambda option_box: option_box if option_box.isChecked() else None, [ui.s11_radio, ui.s12_radio, ui.s21_radio, ui.s22_radio])
    a = filter(lambda option_box: option_box is not None,a)
    state["spar"] = str(a[0].objectName()[0:3])
    state["format_idx"] = ui.format_combobox.currentIndex()

    if ui.center_span_radio.isChecked():
        state["vna_type"] = "center_span"
        state["center"] = str(ui.centralwidget.findChild(QtGui.QLineEdit, "center_field").text())
        state["span"] = str(ui.centralwidget.findChild(QtGui.QLineEdit, "span_field").text())

    elif ui.start_stop_radio.isChecked():
        state["vna_type"] = "start_stop"
        state["start"] = str(ui.centralwidget.findChild(QtGui.QLineEdit, "freqstart_field").text())
        state["stop"] = str(ui.centralwidget.findChild(QtGui.QLineEdit, "freqstop_field").text())

    state["points"] = str(ui.points_field.text())

    state["autoscale"] = bool(ui.autoscale_checkbox.isChecked())

    state["all_checked"] = bool(ui.all_checkbox.isChecked())

    return state


def save_ui_file(ui, fname):
    # Serialize dict to disk
    fname = str(fname)
    with gzip.open(fname, "wb") as stream:
        yaml.dump(ui_state(ui), stream)

def save_ui(ui):
    save_ui_file(ui, "ui_state.config")

def restore_ui_file(ui, fname):
    fname = str(fname)
    mapping = [(ui.smu1_combo, ui.smu1_layout),
               (ui.smu2_combo, ui.smu2_layout),
               (ui.smu3_combo, ui.smu3_layout),
               (ui.smu4_combo, ui.smu4_layout)]
    try:
        with gzip.open(fname, 'rb') as stream:
            state = yaml.load(stream)
    except IOError as e:
        # Start with empty interface as there's no saved configuration
        return
    
    ui.ipField.setText(state["ip"])
    ui.fileField.setText(state["f"])
    ui.vna_ip_field.setText(state["ip_vna"])
    ui.vna_file_field.setText(state["file_vna"])


    for combo in state["combos"]:
        # Get the combo object in the Qt GUI that corresponds to the
        # combo object in the yml representation. Do the same with the layout
        wcombo = mapping[int(combo["num"])-1][0] 
        wlayout = mapping[int(combo["num"])-1][1]
        groupbox = wlayout.itemAt(2).widget()
        if combo["sfun"] == "sweep":
            if combo["type"] == "voltage":
                wcombo.setCurrentIndex(6)
            elif combo["type"] == "current":
                wcombo.setCurrentIndex(2)
            
        if combo["sfun"] == "step":
            if combo["type"] == "voltage":
                wcombo.setCurrentIndex(8) 
            if combo["type"] == "current":
                wcombo.setCurrentIndex(4) 

        if combo["sfun"] == "constant":
            if combo["type"] == "voltage":
                wcombo.setCurrentIndex(5)
            if combo["type"] == "current":
                wcombo.setCurrentIndex(1)
   
        if combo["sfun"] == "list":
            if combo["type"] == "voltage":
                wcombo.setCurrentIndex(3)
            if combo["type"] == "current":
                wcombo.setCurrentIndex(7)

    for combo in state["combos"]:
        # Get the combo object in the Qt GUI that corresponds to the
        # combo object in the yml representation. Do the same with the layout
        wcombo = mapping[int(combo["num"])-1][0] 
        wlayout = mapping[int(combo["num"])-1][1]
        groupbox = wlayout.itemAt(2).widget()
        if combo["sfun"] == "sweep":
            groupbox.findChild(QtGui.QLineEdit, "val_stop_field").setText(combo["stop"])
            groupbox.findChild(QtGui.QLineEdit, "val_inicio_field").setText(combo["start"])
            groupbox.findChild(QtGui.QLineEdit, "step_field").setText(combo["step"])
            groupbox.findChild(QtGui.QLineEdit, "compliance_field").setText(combo["compliance"])
            if combo["sweep_type"] == "Linear":
                groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").setCurrentIndex(0)
            if combo["sweep_type"] == "Log10":
                groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").setCurrentIndex(1)
            if combo["sweep_type"] == "Log25":
                groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").setCurrentIndex(2)
            if combo["sweep_type"] == "Log50":
                groupbox.findChild(QtGui.QComboBox, "sweep_type_combobox").setCurrentIndex(3)

        if combo["sfun"] == "step":
            groupbox.findChild(QtGui.QLineEdit, "start_lineedit").setText(combo["start"])
            groupbox.findChild(QtGui.QLineEdit, "step_lineedit").setText(combo["step"])
            groupbox.findChild(QtGui.QLineEdit, "steps_lineedit").setText(combo["steps"])
            groupbox.findChild(QtGui.QLineEdit, "compliance_lineedit").setText(combo["compliance"])

        if combo["sfun"] == "constant":
            groupbox.findChild(QtGui.QLineEdit, "constant_textbox").setText(combo["value"])
            groupbox.findChild(QtGui.QLineEdit, "compliance_textbox").setText(combo["compliance"])
   
        if combo["sfun"] == "list":
            groupbox.findChild(QtGui.QTextEdit, "list_textedit").setText(combo["value_list"])

    # Restore VNA GUI

    if state["spar"] == "s11":
        ui.s11_radio.setChecked(True)
    elif state["spar"] == "s21":
        ui.s21_radio.setChecked(True)
    elif state["spar"] == "s12":
        ui.s12_radio.setChecked(True)
    elif state["spar"] == "s22":
        ui.s22_radio.setChecked(True)

    # Restore data format combobox

    ui.format_combobox.setCurrentIndex(int(state["format_idx"]))

    # Set center-span or start-stop

    if state["vna_type"] == "center_span":
        ui.center_span_radio.setChecked(True)
        ui.centralwidget.findChild(QtGui.QLineEdit, "center_field").setText(state["center"])
        ui.centralwidget.findChild(QtGui.QLineEdit, "span_field").setText(state["span"])
   
    elif state["vna_type"] == "start_stop":
        ui.start_stop_radio.setChecked(True)
        ui.centralwidget.findChild(QtGui.QLineEdit, "freqstart_field").setText(state["start"])
        ui.centralwidget.findChild(QtGui.QLineEdit, "freqstop_field").setText(state["stop"])

    ui.points_field.setText(str(state["points"]))

    ui.autoscale_checkbox.setChecked(bool(state["autoscale"]))
    ui.all_checkbox.setChecked(bool(state["all_checked"]))


def restore_ui(ui):
    restore_ui_file(ui, "ui_state.config")

