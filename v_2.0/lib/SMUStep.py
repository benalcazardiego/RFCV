from SMU import SMUBase
from SMU import SMUConfigError
from util.SourceType import SourceType

class SMUStep(SMUBase):
    # Source mode is for channel definition, Source type for VAR2 definition
    def __init__(self, ch_number, source_mode, source_type, start, step, steps, compliance, voltage_name = None, current_name = None):
        super(SMUStep, self).__init__(voltage_name, current_name, ch_number, source_mode)
        
        if source_type not in [SourceType.VOLTAGE, SourceType.CURRENT]:
            raise SMUConfigError("source_type must be defined from SourceType enum")

        self.source_type = source_type
        
        # TODO move validation to superclass
         
        if self.source_type == SourceType.VOLTAGE:
            self._validate_voltage(start)
            self._validate_voltage(step)
            self._validate_current(compliance)
        if self.source_type == SourceType.CURRENT:
            self._validate_current(start)
            self._validate_current(step)
            self._validate_voltage(compliance)

        if steps > 32:
            raise SMUConfigError("The max number of steps is 32")


        # Validation passed! Create the object

        self.start = start
        self.steps = steps
        self.step = step
        self.compliance = compliance


    def _get_var2_cmd(self):
        if self.source_type == SourceType.VOLTAGE:
            template = "SS VP {start},{step},{steps},{compliance}"
        elif self.source_type == SourceType.CURRENT:
            template = "SS IP {start},{step},{steps},{compliance}"

        command = template.format(start=self.start, step=self.step, steps=self.steps, 
                                 compliance=self.compliance)
        return command

    def _get_chan_cmd(self):
        command = "DE CH{ch_number},'{voltage_name}','{current_name}',{source_mode},2".format(ch_number=self.ch_number,
                                        voltage_name=self.voltage_name, current_name=self.current_name, source_mode=self.source_mode)
        return command

    def get_commands(self):
        return [self._get_chan_cmd(), self._get_var2_cmd()] + self._get_measure_commands()


