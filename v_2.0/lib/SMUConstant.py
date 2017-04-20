from SMU import SMUBase
from SMU import SMUConfigError
from util.SourceType import SourceType


class SMUConstant(SMUBase):

    def __init__(self, ch_number, source_mode, source_type, output, compliance, voltage_name=None, current_name=None):
        print "U R in SMUConstant __init__" #Flag  4 debug
        super(SMUConstant, self).__init__(voltage_name, current_name, ch_number, source_mode)
        if source_type not in [SourceType.VOLTAGE, SourceType.CURRENT]:
            raise SMUConfigError("source_type must be defined from SourceType enum")
        
        self.source_type = source_type
        
        # TODO figure out how to move validation to superclass or at least elsewhere:
        if self.source_type == SourceType.VOLTAGE: #Constant -> Voltaje Mode
            self._validate_voltage(output) # Output is the value of voltaje that we enter in the interface
            self._validate_voltage(compliance) # Compliance is the value that we enter in the interface
        if self.source_type == SourceType.CURRENT:
            self._validate_current(output)
            self._validate_voltage(compliance)
        #----------------------------------------------------------------------------
        
        # Create object now that validation has finished:
        self.output = output
        self.compliance = compliance
        #-----------------------------------------------
      
    def _get_chan_cmd(self):
        #Change the system mode to enable the sent of commands
        print "U R in SMUConstant - _get_chan_cmd" #Flag  4 debug
        
        command = "DE CH{ch_number},'{voltage_name}','{current_name}',{source_mode},3".format(ch_number=self.ch_number,
                          voltage_name=self.voltage_name, current_name=self.current_name, source_mode=self.source_mode)
        return command

    def _get_const_cmd(self):
        
        print "U R in SMUConstant - _get_const_cmd" #Flag  4 debug
        
        if self.source_type == SourceType.VOLTAGE:
            template = "SS VC{ch},{output},{compliance}" #Instruction to Keithley. Means:force 'output' volt with 'compliance' current limit
        elif self.source_type == SourceType.CURRENT:
            template = "SS IC{ch},{output},{compliance}"

        command=template.format(ch=self.ch_number, output=self.output, compliance=self.compliance)
        
        return command

    def get_commands(self):
        #Return both commands in a list
        Command1=self._get_chan_cmd()
        Command2=self._get_const_cmd()
        return [Command1, Command2]



''' #Descomentar esto una vez acabada la test.. Tomar en cuenta que esto tiene q estar para hacer la prueba
    def configure(self, executor, ui):#funcion anadida 29/01/2016 
        for cmd in self.get_commands():
            executor.execute_command(cmd)
            VnaMeasureThreaded(ui)
        #data = VnaMeasure(ui)
        # Add V to data
        '''
