from SMU import SMUBase
from SMU import SMUConfigError
from util.SweepType import SweepType
from util.SourceType import SourceType

class SMUSweep(SMUBase):
    # Source mode is for channel definition, Source type for VAR1 definition
    def __init__(self, ch_number, source_mode, source_type, start, stop, step, compliance, sweep_type=SweepType.LINEAR,
                 voltage_name=None, current_name=None):
        print "U R in SMUSweep -> __init__"#flag 4 debug
        super(SMUSweep, self).__init__(voltage_name, current_name, ch_number, source_mode)
        
        if source_type not in [SourceType.VOLTAGE, SourceType.CURRENT]:
            raise SMUConfigError("source_type must be defined from SourceType enum")

        if sweep_type not in [SweepType.LINEAR, SweepType.LOG10, SweepType.LOG25, SweepType.LOG50]:
            raise SMUConfigError("sweep_type must be defined from SweepType enum")

        self.source_type = source_type
        
        if self.source_type == SourceType.VOLTAGE:
            self._validate_voltage(start)
            self._validate_voltage(stop)
            self._validate_voltage(step)
            self._validate_current(compliance)


        if self.source_type == SourceType.CURRENT:
            self._validate_current(start)
            self._validate_current(stop)
            self._validate_current(step)
            self._validate_voltage(compliance)

        # Validation passed! Create the object:
        self.start = start
        self.stop = stop
        self.step = step
        self.compliance = compliance
        self.sweep_type = sweep_type
        #-------------------------------------

    def _is_log(self, sweep_type):
        #Checks if the sweep type is logarithmic as if it is the command is different
        print "U R in SMUSweep -> _is_log"#flag 4 debug
        
        return sweep_type in [SweepType.LOG10, SweepType.LOG25, SweepType.LOG50]

    def _get_var1_cmd(self):
        print "U R in SMUSweep -> _get_var1_cmd"#flag 4 debug
        
        # We ignore the step parameter when doing LOG* sweeps    
        if self.source_type == SourceType.VOLTAGE and not self._is_log(self.sweep_type):
            template = "VR{sweep_type},{start},{stop},{step},{compliance}"
        elif self.source_type == SourceType.CURRENT and not self._is_log(self.sweep_type):
            template = "IR{sweep_type},{start},{stop},{step},{compliance}"
        elif self.source_type == SourceType.VOLTAGE and self._is_log(self.sweep_type):
            template = "VR{sweep_type},{start},{stop},{compliance}"
        elif self.source_type == SourceType.CURRENT and self._is_log(self.sweep_type):
            template = "IR{sweep_type},{start},{stop},{compliance}"
        if self._is_log(self.sweep_type):
            command = template.format(sweep_type=self.sweep_type, start=self.start, stop=self.stop, 
                                 compliance=self.compliance)
        elif not self._is_log(self.sweep_type):
            command = template.format(sweep_type=self.sweep_type, start=self.start, stop=self.stop, 
                                 step=self.step, compliance=self.compliance)
        return command


    def _get_chan_cmd(self):
        print "U R in SMUSweep -> _get_chan_cmd"#flag 4 debug
        
        command = "DE CH{ch_number}, '{voltage_name}','{current_name}',{source_mode},1".format(ch_number=self.ch_number,
                                    voltage_name=self.voltage_name, current_name=self.current_name, source_mode=self.source_mode)
        return command

    def get_commands(self):
        print "U R in SMUSweep -> get_commands"#flag 4 debug
        
        return [self._get_chan_cmd(), "SS " + self._get_var1_cmd()] 

