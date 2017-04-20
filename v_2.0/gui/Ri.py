# -*- coding: utf-8 -*-
#RI_SubGUI_handlers_for_apparition_connection_and_execution
# RI_GUI_creation
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

class Ui_RI_dialog(object):
    def setupUi(self, RI_dialog):
        RI_dialog.setObjectName(_fromUtf8("RI_dialog"))
        RI_dialog.resize(276, 193)
        self.current_ri_lineedit = QtGui.QLineEdit(RI_dialog)
        self.current_ri_lineedit.setGeometry(QtCore.QRect(90, 60, 171, 22))
        self.current_ri_lineedit.setObjectName(_fromUtf8("current_ri_lineedit"))
        self.compliance_ri_lineedit = QtGui.QLineEdit(RI_dialog)
        self.compliance_ri_lineedit.setGeometry(QtCore.QRect(90, 100, 171, 22))
        self.compliance_ri_lineedit.setObjectName(_fromUtf8("compliance_ri_lineedit"))
        self.current_ri_label = QtGui.QLabel(RI_dialog)
        self.current_ri_label.setGeometry(QtCore.QRect(20, 60, 61, 14))
        self.current_ri_label.setObjectName(_fromUtf8("current_ri_label"))
        self.compliance_ri_label = QtGui.QLabel(RI_dialog)
        self.compliance_ri_label.setGeometry(QtCore.QRect(10, 100, 81, 31))
        self.compliance_ri_label.setObjectName(_fromUtf8("compliance_ri_label"))
        self.measure_ri_button = QtGui.QPushButton(RI_dialog)
        self.measure_ri_button.setGeometry(QtCore.QRect(80, 150, 111, 23))
        self.measure_ri_button.setObjectName(_fromUtf8("measure_ri_button"))
        self.smu_label = QtGui.QLabel(RI_dialog)
        self.smu_label.setGeometry(QtCore.QRect(20, 20, 61, 14))
        self.smu_label.setObjectName(_fromUtf8("smu_label"))
        self.smu_lineedit = QtGui.QLineEdit(RI_dialog)
        self.smu_lineedit.setGeometry(QtCore.QRect(90, 20, 171, 22))
        self.smu_lineedit.setObjectName(_fromUtf8("smu_lineedit"))

        self.retranslateUi(RI_dialog)
        QtCore.QMetaObject.connectSlotsByName(RI_dialog)

    def retranslateUi(self, RI_dialog):
        RI_dialog.setWindowTitle(_translate("RI_dialog", "RI", None))
        self.current_ri_label.setText(_translate("RI_dialog", "Current:", None))
        self.compliance_ri_label.setText(_translate("RI_dialog", "Compliance:\n"
"(current)", None))
        self.measure_ri_button.setText(_translate("RI_dialog", "Medir", None))
        self.smu_label.setText(_translate("RI_dialog", "SMU #:", None))

