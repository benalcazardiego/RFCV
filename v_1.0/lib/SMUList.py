from SMU import SMUBase, SMUConfigError
from util.SourceType import SourceType
from util.CurrentVoltage import CurrentVoltage
from util.SlaveMaster import SlaveMaster

class SMUList(SMUBase):
    # Source mode is for channel definition, Source type for VAR1 definition
    def __init__(self, ch_number, source_mode, source_type, sweep_values, compliance, slave_master, voltage_name=None,
                 current_name=None):
        super(SMUList, self).__init__(voltage_name, current_name, ch_number, source_mode)
        
        if source_type not in [SourceType.VOLTAGE, SourceType.CURRENT]:
            raise SMUConfigError("source_type must be defined from SourceType enum")

        self.source_type = source_type
        
        if slave_master not in [SlaveMaster.SLAVE, SlaveMaster.MASTER]:
            raise SMUConfigError("Slave or master mode must be specified from SlaveMaster enum")

        if self.source_type == SourceType.VOLTAGE:
            self._validate_current(compliance)
            self._validate_list(sweep_values, CurrentVoltage.VOLTAGE)
        if self.source_type == SourceType.CURRENT:
            self._validate_voltage(compliance)
            self._validate_list(sweep_values, CurrentVoltage.CURRENT)
                    


        # Validation passed! Create the object
        
        self.sweep_values = sweep_values
        self.compliance = compliance
        self.slave_master = slave_master

    def _get_sweep_cmd(self):
        sweep_string = ",".join(str(i) for i in self.sweep_values)
        if self.source_type == SourceType.VOLTAGE:
            template = "SS VL{ch},{slave_master},{compliance},{values}"
        elif self.source_type == SourceType.CURRENT:
            template = "SS IL{ch},{slave_master},{compliance},{values}"

        command = template.format(ch = self.ch_number, slave_master=self.slave_master, compliance=self.compliance, values=sweep_string)
        return command

    def _get_chan_cmd(self):
        command = "DE CH{ch_number}, '{voltage_name}','{current_name}',{source_mode},1".format(ch_number=self.ch_number,
                                    voltage_name=self.voltage_name, current_name=self.current_name, source_mode=self.source_mode)
        return command

    def get_commands(self):
        #Add an empty list
        return [self._get_chan_cmd(), self._get_sweep_cmd()] + self._get_measure_commands()



