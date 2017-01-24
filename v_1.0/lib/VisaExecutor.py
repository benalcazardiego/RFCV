#VISA_connector_and_executor
#Description: VISA TCP/IP Resources to the stablish the control.
from CommandExecutor import CommandExecutor
import visa

rm = visa.ResourceManager()
class VisaExecutor(CommandExecutor):
    def __init__(self, ip, port=1225):
        self.ip = ip
        self.device = rm.open_resource("TCPIP::{ip}::{port}::SOCKET".format(ip=ip, port=port))

    def execute_command(self, command):
        self.device.write(command)
