'''
Created on 12 nov. 2016

@author: Diego
'''
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

class Ui_Medicionescontinuoalterno(object):
    def setupUi(self, Medicionescontinuoalterno, Slot1, Slot2, Slot3, Slot4, Slot5):
        Medicionescontinuoalterno.setObjectName(_fromUtf8("Medicionescontinuoalterno"))
        Medicionescontinuoalterno.resize(400, 300)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        Medicionescontinuoalterno.setFont(font)
        self.gridLayout = QtGui.QGridLayout(Medicionescontinuoalterno)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.OpenDevice = QtGui.QPushButton(Medicionescontinuoalterno)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OpenDevice.sizePolicy().hasHeightForWidth())
        self.OpenDevice.setSizePolicy(sizePolicy)
        self.OpenDevice.setObjectName(_fromUtf8("OpenDevice"))
        self.verticalLayout.addWidget(self.OpenDevice)
        self.OpenPad = QtGui.QPushButton(Medicionescontinuoalterno)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OpenPad.sizePolicy().hasHeightForWidth())
        self.OpenPad.setSizePolicy(sizePolicy)
        self.OpenPad.setObjectName(_fromUtf8("OpenPad"))
        self.verticalLayout.addWidget(self.OpenPad)
        self.Short = QtGui.QPushButton(Medicionescontinuoalterno)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Short.sizePolicy().hasHeightForWidth())
        self.Short.setSizePolicy(sizePolicy)
        self.Short.setObjectName(_fromUtf8("Short"))
        self.verticalLayout.addWidget(self.Short)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.Devicewithdeembedding = QtGui.QPushButton(Medicionescontinuoalterno)
        self.Devicewithdeembedding.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Devicewithdeembedding.sizePolicy().hasHeightForWidth())
        self.Devicewithdeembedding.setSizePolicy(sizePolicy)
        self.Devicewithdeembedding.setObjectName(_fromUtf8("Devicewithdeembedding"))
        self.verticalLayout_2.addWidget(self.Devicewithdeembedding)
        self.Devicewithoutdeembedding = QtGui.QPushButton(Medicionescontinuoalterno)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Devicewithoutdeembedding.sizePolicy().hasHeightForWidth())
        self.Devicewithoutdeembedding.setSizePolicy(sizePolicy)
        self.Devicewithoutdeembedding.setObjectName(_fromUtf8("Devicewithoutdeembedding"))
        self.verticalLayout_2.addWidget(self.Devicewithoutdeembedding)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        global a1
        global a2
        a1=0
        a2=0
        self.retranslateUi(Medicionescontinuoalterno)
        QtCore.QObject.connect(self.OpenDevice, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Enableembeddingopen)
        QtCore.QObject.connect(self.Short, QtCore.SIGNAL(_fromUtf8("clicked()")), self.Enableembeddingshort)
        QtCore.QObject.connect(self.OpenDevice, QtCore.SIGNAL(_fromUtf8("clicked()")), Slot1)
        QtCore.QObject.connect(self.OpenPad, QtCore.SIGNAL(_fromUtf8("clicked()")), Slot2)
        QtCore.QObject.connect(self.Short, QtCore.SIGNAL(_fromUtf8("clicked()")), Slot3)
        QtCore.QObject.connect(self.Devicewithdeembedding, QtCore.SIGNAL(_fromUtf8("clicked()")), Slot4)
        QtCore.QObject.connect(self.Devicewithoutdeembedding, QtCore.SIGNAL(_fromUtf8("clicked()")), Slot5)
        QtCore.QMetaObject.connectSlotsByName(Medicionescontinuoalterno)
    
    def Enableembeddingopen(self):
        global a1
        global a2
        if a2=='1':
            self.Devicewithdeembedding.setEnabled(True)
        a1='1'
    def Enableembeddingshort(self):
        global a1
        global a2
        if a1=='1':
            self.Devicewithdeembedding.setEnabled(True)
        a2='1'
    
    
    def retranslateUi(self, Medicionescontinuoalterno):
        Medicionescontinuoalterno.setWindowTitle(_translate("Medicionescontinuoalterno", "Mediciones Continuo-Alterno", None))
        self.OpenDevice.setText(_translate("Medicionescontinuoalterno", "Open Device", None))
        self.OpenPad.setText(_translate("Medicionescontinuoalterno", "Open Pad", None))
        self.Short.setText(_translate("Medicionescontinuoalterno", "Short", None))
        self.Devicewithdeembedding.setText(_translate("Medicionescontinuoalterno", "Device with De-embedding", None))
        self.Devicewithoutdeembedding.setText(_translate("Medicionescontinuoalterno", "Device without De-embedding", None))

'''
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Medicionescontinuoalterno = QtGui.QWidget()
    ui = Ui_Medicionescontinuoalterno()
    ui.setupUi(Medicionescontinuoalterno)
    Medicionescontinuoalterno.show()
    sys.exit(app.exec_())
'''