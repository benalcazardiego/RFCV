# Socket_connector_and_executor

from CommandExecutor import CommandExecutor
import socket

class SocketExecutor(CommandExecutor):
    def __init__(self, ip, port=1225, expect_reply=True, endline="\0"):
        #Creates the socket and connect it to the server address
        print "U R in SocketExecutor - __init__" #flag 4 debug
        self.port = port
        self.ip = ip
        self.endline = endline #Character needed at the ende of the command
        self.data = None #Data excepted to be received
        self.expect_reply = expect_reply
        print "Port: %s" % self.port
        print "IP: %s" % self.ip
        
        # Create a TCP/IP socket s
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address=(ip,port)
        self.s.connect(server_address)
        
    def execute_command(self, command):
        #Send a command and receive data if expect_reply is true
        print "U R in SocketExecutor - execute_command" #flag 4 debug
        print "Executed: %s" % command
        self.s.send(command + self.endline)
        if self.expect_reply:
            Buffer_size=8192
            data = self.s.recv(Buffer_size)
            self.data = ''
            self.data = data

    def ask(self, command):
        #Send a command and receive a bigger amount of data
        print "U R in SocketExecutor - ask" #flag 4 debug
        
        print "Asked: %s" % command
        self.s.send(command + self.endline)
        self.data = ""
        data = ""
        pdata = ""
        while True:
            Buffer_size=8192
            pdata = self.s.recv(Buffer_size)
            if len(pdata) > 0 and (pdata[len(pdata)-1] == "\n" or pdata[len(pdata)-1] == "\0"): # Check if the pdata is the last piece of data
                data += pdata
                break
            data += pdata
        data = data[:-1] # For some reason there's a comma at the end of the transmission. Delete it
        self.data = data
        return self.data


    # Should be called after command execution
    def get_data(self):
        print "U R in SocketExecutor - get_data" #flag 4 debug
        
        return self.data

    def close(self):
        print "U R in SocketExecutor - close" #flag 4 debug
        
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
