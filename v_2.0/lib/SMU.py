from util.SourceMode import SourceMode
from util.CurrentVoltage import CurrentVoltage
from util.funcs import random_id

# Abstract class that should NEVER be used by itself
# Class hierarchy needs work to increase code re-use

class SMUBase(object):

    def __init__(self, voltage_name, current_name, ch_number, source_mode=SourceMode.VOLTAGE):
        print "U R in SMUBase -> __init__"#flag 4 debug
        #Generate a random voltage name
        if voltage_name is None:
            voltage_name = random_id(CurrentVoltage.VOLTAGE)
        #Generate a random current name
        if current_name is None:
            current_name = random_id(CurrentVoltage.CURRENT)
        #Validates the SourceMode selected
        if source_mode not in [SourceMode.VOLTAGE, SourceMode.CURRENT, SourceMode.COMMON]:
            raise SMUConfigError("Source mode must be defined from SourceMode enum")
        #Validates the voltage_name length. It cannot be longer than 6 characters (Maker requirement) 
        if len(voltage_name) > 6:
            raise SMUConfigError("Voltage name too long")
        #Validates the current_name length. It cannot be longer than 6 characters (Maker requirement)
        if len(current_name) > 6:
            raise SMUConfigError("Current name too long")
        #Validates the election of a channel.
        if ch_number > 8:
            raise SMUConfigError("Channel number too high")
        
        self.ch_number = ch_number
        self.current_name = current_name
        self.voltage_name = voltage_name
        self.source_mode = source_mode

    # In base class, as we need to always set up a channel

    def _validate_voltage(self, voltage):
        print "U R in SMUBase -> _validate_voltage"#flag 4 debug
        
        if abs(voltage) > 210:
            raise SMUConfigError("Voltage must be above -210V and below 210V")

    def _validate_current(self, current):
        print "U R in SMUBase -> _validate_current"#flag 4 debug
        
        if abs(current) > 0.105:
            raise SMUConfigError("Current must be above -0.105A and below 0.105A")

    def _validate_list(self, to_validate, current_or_voltage = CurrentVoltage.CURRENT):
        print "U R in SMUBase -> _validate_list"#flag 4 debug
        
        if current_or_voltage == CurrentVoltage.CURRENT:
            for current in to_validate:
                self._validate_current(current)
        elif current_or_voltage == CurrentVoltage.VOLTAGE:
            for voltage in to_validate:
                self._validate_voltage(voltage)
        
    def _random_id(self, current_voltage):
        print "U R in SMUBase -> _random_id"#flag 4 debug
        
        return random_id(current_voltage)
        
#   def _get_measure_commands(self):
#       return ["MD ME1", "MD DO 'CH{ch}T'".format(ch=self.ch_number)]
        
    def _get_measure_commands(self):
        print "U R in SMUBase -> _get_measure_commands"#flag 4 debug
                  
        return []
        

class SMUConfigError(Exception):
    pass 
