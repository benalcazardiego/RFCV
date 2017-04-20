#RI_SubGUI_handlers_for_apparition_connection_and_execution
from lib.SocketExecutor import SocketExecutor
from PyQt4 import QtGui

class RiHandler(object):

    def __init__(self, ui):
        self.ui = ui
        #The SubGUI appears when when the RI button is clicked
        self.ui.ri_ui.measure_ri_button.clicked.connect(self.measure_ri)
        self.executor = None

    def _connect(self):
        if self.executor is not None:
            return self.executor # Reuse previously opened object (and socket)
        try:
            ip_port = str(self.ui.ipField.text()).split(":")
            ip = ip_port[0]
            port = int(ip_port[1])
            self.executor = SocketExecutor(ip, port) # Connect to the server socket
        except IndexError:
            QtGui.QMessageBox.information(self.ui.centralwidget,
                    "IP no especificado",
                    "Es necesario especificar un IP y puerto en el formato IP:puerto")

    def measure_ri(self):
        #Get measured data
        self._connect()
        smu = int(self.ui.ri_ui.smu_lineedit.text())
        current = float(self.ui.ri_ui.current_ri_lineedit.text())
        current_compliance = float(self.ui.ri_ui.compliance_ri_lineedit.text())
        self.executor.execute_command("RI {smu}, {current}, {current_compliance}".format(smu=smu, current=current, 
                    current_compliance=current_compliance))
