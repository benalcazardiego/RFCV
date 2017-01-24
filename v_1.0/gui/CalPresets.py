# -*- coding: utf-8 -*-
#Calibration_parameters_GUI_creation


from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_cal_presets(object):
    def setupUi(self, cal_presets):
        cal_presets.setObjectName(_fromUtf8("cal_presets"))
        cal_presets.resize(294, 157)
        self.cal_kit_combo = QtGui.QComboBox(cal_presets)
        self.cal_kit_combo.setGeometry(QtCore.QRect(130, 20, 151, 31))
        self.cal_kit_combo.setObjectName(_fromUtf8("cal_kit_combo"))
        self.cal_kit_combo.addItem(_fromUtf8(""))
        self.cal_kit_combo.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(cal_presets)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.full_2port_button = QtGui.QPushButton(cal_presets)
        self.full_2port_button.setGeometry(QtCore.QRect(20, 100, 131, 31))
        self.full_2port_button.setObjectName(_fromUtf8("full_2port_button"))
        self.trl_2port_button = QtGui.QPushButton(cal_presets)
        self.trl_2port_button.setGeometry(QtCore.QRect(160, 100, 121, 31))
        self.trl_2port_button.setObjectName(_fromUtf8("trl_2port_button"))
        self.channel_label = QtGui.QLabel(cal_presets)
        self.channel_label.setGeometry(QtCore.QRect(20, 60, 131, 16))
        self.channel_label.setObjectName(_fromUtf8("channel_label"))
        self.channel_combo = QtGui.QComboBox(cal_presets)
        self.channel_combo.setGeometry(QtCore.QRect(160, 52, 121, 31))
        self.channel_combo.setObjectName(_fromUtf8("channel_combo"))
        self.channel_combo.addItem(_fromUtf8(""))
        self.channel_combo.addItem(_fromUtf8(""))

        self.retranslateUi(cal_presets)
        QtCore.QMetaObject.connectSlotsByName(cal_presets)

    def retranslateUi(self, cal_presets):
        cal_presets.setWindowTitle(_translate("cal_presets", "Calibration presets", None))
        self.cal_kit_combo.setItemText(0, _translate("cal_presets", "85033E", None))
        self.cal_kit_combo.setItemText(1, _translate("cal_presets", "CS5", None))
        self.label.setText(_translate("cal_presets", "Calibration kit:", None))
        self.full_2port_button.setText(_translate("cal_presets", "Full 2-Port", None))
        self.trl_2port_button.setText(_translate("cal_presets", "2-Port TRL", None))
        self.channel_label.setText(_translate("cal_presets", "Number of channels:", None))
        self.channel_combo.setItemText(0, _translate("cal_presets", "1", None))
        self.channel_combo.setItemText(1, _translate("cal_presets", "4", None))

