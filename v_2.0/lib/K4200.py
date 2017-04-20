#SCS_class_creator_for_initialization_configuration_sate_validation_and_data_adquisition
from SocketExecutor import SocketExecutor

class K4200:
    print "U R in class K4200" #flag 4 debug
    #Relate a IP address to the SCS
    def __init__(self, ip, port=2099):
        
        print "U R in K4200 - __init__" #flag 4 debug
        
        self.ip = ip
        #For the SCS expect_reply is true
        self.executor = SocketExecutor(ip, port)
        #The class is not configured yet when it is initialized
        self.configured = False
        #The class has measured anything when it is initialized
        self.has_measured = False #Its not realizing measure
        #The K4200 has a list of SMUs
        self.smus = list()

    def attach(self, smu):
        #Add a new SMU to the SCS
        print "U R in K4200 - attach" #flag 4 debug
        
        self.smus.append(smu)

    def configure(self):
        print "U R in K4200 - configure" #flag 4 debug
        #Send the commands necessary to configure a SMU
        for smu in self.smus:
            #Each SMU has a list of commands used to configure it
            #Execute each configuration command
            for command in smu.get_commands():
                self.executor.execute_command(command)
        #Change the state of the configuration of the SMU
        self.configured = True

    def is_ready(self):
        #Check if the device is ready to send a command
        print "U R in K4200 - is_ready" #flag 4 debug
        #SP command allows the user to acquire the GPIB spoll byte to determine when not busy or data 
        #ready while in the Ethernet communication mode.
        self.executor.execute_command("SP")
        is_ready = self.executor.get_data()
        is_ready = is_ready.replace("\0","")
        #Returns 1 if there is data
        return 0b00000001 & int(is_ready)

    def measure(self):
        #Send the command to start the measure
        print "U R in K4200 - measure" #flag 4 debug
        #Sends the command and get data
        # The ME1 or ME2 command will trigger the start of the test and perform the programmed number of measurements.
        self.executor.execute_command("MD ME1") #"MD ME1" means Measurement control with trigger
        self.has_measured = True #Indicator that its measuring

    def get_data(self, ch=1): 
        #Get data from the channel 1 
        print "U R in K4200 - get_data" #flag 4 debug
        
        if self.has_measured:
            template = "DO CH{ch}T"
            cmd = template.format(ch=ch)
            self.executor.execute_command(cmd)
            return self.executor.get_data()
        else:
            raise NotMeasuredYetError("No data to retrieve")

class NotMeasuredYetError(Exception):
    pass
