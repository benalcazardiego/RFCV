# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/conalt.ui'
#
# Created: Sat May 10 18:59:04 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

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

class Ui_conalt_dialog(object):
    def setupUi(self, conalt_dialog):
        conalt_dialog.setObjectName(_fromUtf8("conalt_dialog"))
        conalt_dialog.resize(277, 159)
        self.sweep_delay_label = QtGui.QLabel(conalt_dialog)
        self.sweep_delay_label.setGeometry(QtCore.QRect(10, 60, 91, 16))
        self.sweep_delay_label.setObjectName(_fromUtf8("sweep_delay_label"))
        self.smu_combo = QtGui.QComboBox(conalt_dialog)
        self.smu_combo.setGeometry(QtCore.QRect(110, 12, 161, 31))
        self.smu_combo.setObjectName(_fromUtf8("smu_combo"))
        self.smu_combo.addItem(_fromUtf8(""))
        self.smu_combo.setItemText(0, _fromUtf8(""))
        self.smu_combo.addItem(_fromUtf8(""))
        self.smu_combo.addItem(_fromUtf8(""))
        self.smu_combo.addItem(_fromUtf8(""))
        self.smu_combo.addItem(_fromUtf8(""))
        self.smu_label = QtGui.QLabel(conalt_dialog)
        self.smu_label.setGeometry(QtCore.QRect(10, 20, 61, 14))
        self.smu_label.setObjectName(_fromUtf8("smu_label"))
        self.sweep_delay_field = QtGui.QLineEdit(conalt_dialog)
        self.sweep_delay_field.setGeometry(QtCore.QRect(110, 50, 141, 31))
        self.sweep_delay_field.setObjectName(_fromUtf8("sweep_delay_field"))
        self.label = QtGui.QLabel(conalt_dialog)
        self.label.setGeometry(QtCore.QRect(260, 60, 16, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.conalt_measure = QtGui.QPushButton(conalt_dialog)
        self.conalt_measure.setGeometry(QtCore.QRect(10, 100, 251, 41))
        self.conalt_measure.setObjectName(_fromUtf8("conalt_measure"))

        self.retranslateUi(conalt_dialog)
        QtCore.QMetaObject.connectSlotsByName(conalt_dialog)

    def retranslateUi(self, conalt_dialog):
        conalt_dialog.setWindowTitle(_translate("conalt_dialog", "Continuo-Analogo", None))
        self.sweep_delay_label.setText(_translate("conalt_dialog", "Sweep Delay:", None))
        self.smu_combo.setItemText(1, _translate("conalt_dialog", "SMU1", None))
        self.smu_combo.setItemText(2, _translate("conalt_dialog", "SMU2", None))
        self.smu_combo.setItemText(3, _translate("conalt_dialog", "SMU3", None))
        self.smu_combo.setItemText(4, _translate("conalt_dialog", "SMU4", None))
        self.smu_label.setText(_translate("conalt_dialog", "SMU:", None))
        self.label.setText(_translate("conalt_dialog", "s", None))
        self.conalt_measure.setText(_translate("conalt_dialog", "Measure", None))

