#Description: Wrapper for Vna class that specifies a fixed channel

from Vna import Vna


class VnaChannel(Vna):
    def __init__(self, ip, port, channel):
        print "U R in VnaChannel - __init__" #FLAG FOR DEBUGGING
        #super(VnaChannel, self) creates an object that pairs the self instance with access to the calling class's 
        #location on the MRO of self's class
        super(VnaChannel, self).__init__(ip, port)
        self.channel = channel

    def set_continuous(self, cont):
        print "U R in VnaChannel - set_continuous" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_continuous(self.channel, cont)

    def is_ready(self):
        print "U R in VnaChannel - is_ready" #FLAG FOR DEBUGGING
        
        return super(VnaChannel, self).is_ready()

    def set_sweep_type(self, sweep_type):
        print "U R in VnaChannel - set_sweep_type" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_sweep_type(self.channel, sweep_type)

    def set_center_span(self, center, span):
        print "U R in VnaChannel - set_center_span" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_center_span(self.channel, center, span)

    def set_start_stop(self, start, stop):
        print "U R in VnaChannel - set_start_stop" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_start_stop(self.channel, start, stop)

    def activate_channel(self):
        print "U R in VnaChannel - activate_channel" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).activate_channel(self.channel)

    def activate_trace(self, trace):
        print "U R in VnaChannel - activate_trace" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).activate_trace(self.channel, trace)
       
    def set_traces(self, trace):
        print "U R in VnaChannel - set_traces" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_traces(self.channel, trace)

    def add_marker(self, marker, trace=1):
        print "U R in VnaChannel - add_marker" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).add_marker(self.channel, trace, marker)

    def set_x(self, new_x, mark=1):
        print "U R in VnaChannel - set_x" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_x(self.channel, new_x, mark)

    def get_start_x(self):
        print "U R in VnaChannel - get_start_x" #FLAG FOR DEBUGGING
        
        return super(VnaChannel, self).get_start_x(self.channel)

    def get_stop_x(self):
        print "U R in VnaChannel - get_stop_x" #FLAG FOR DEBUGGING
        
        return super(VnaChannel, self).get_stop_x(self.channel)

    def get_x(self, mark=1):
        print "U R in VnaChannel - get_x" #FLAG FOR DEBUGGING
        
        return super(VnaChannel, self).get_x(self.channel, mark)

    def get_y(self, mark=1):
        print "U R in VnaChannel - get_y" #FLAG FOR DEBUGGING
        
        return super(VnaChannel, self).get_y(self.channel, mark)

    def set_sparam(self, trace, sparam):
        print "U R in VnaChannel - set_sparam" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_sparam(self.channel, trace, sparam)

    def set_points(self, points):
        print "U R in VnaChannel - set_points" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_points(self.channel, points)

    def auto_scale(self):
        print "U R in VnaChannel - auto_scale" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).auto_scale(self.channel)

    def set_format(self, fmt):
        print "U R in VnaChannel - set_format" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_format(self.channel, fmt)

    def set_cal_kit(self, kit):
        print "U R in VnaChannel - set_cal_kit" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_cal_kit(self.channel, kit)

    def set_cal_type(self, cal_type, port=None):
        print "U R in VnaChannel - set_cal_type" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_cal_type(self.channel, cal_type, port)

    def cal_measure_open(self, port):
        print "U R in VnaChannel - cal_measure_open" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).cal_measure_open(self.channel, port)

    def cal_measure_short(self, port):
        print "U R in VnaChannel - cal_measure_short" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).cal_measure_short(self.channel, port)

    def cal_measure_load(self, port):
        print "U R in VnaChannel - cal_measure_load" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).cal_measure_load(self.channel, port)

    def cal_measure_thru(self, port_x, port_y):
        print "U R in VnaChannel - cal_measure_thru" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).cal_measure_thru(self.channel, port_x, port_y)

    def cal_measure_isol(self, port_x, port_y):
        print "U R in VnaChannel - cal_measure_isol" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).cal_measure_isol(self.channel, port_x, port_y)

    def trl_thru_line(self, port_x, port_y):
        print "U R in VnaChannel - trl_thru_line" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).trl_thru_line(self.channel, port_x, port_y)

    def trl_reflect(self, port):
        print "U R in VnaChannel - trl_reflect" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).trl_reflect(self.channel, port)

    def trl_line_match(self, port_x, port_y):
        print "U R in VnaChannel - trl_line_match" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).trl_line_match(self.channel, port_x, port_y)
    
    def save_cal(self):
        print "U R in VnaChannel - save_cal" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).save_cal(self.channel)

    def set_cs5(self):
        print "U R in VnaChannel - set_cs5" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_cs5(self.channel)

    def set_immediate(self):
        print "U R in VnaChannel - set_immediate" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_immediate(self.channel)
    
    def set_sweep_time(self, time):
        print "U R in VnaChannel - set_sweep_time" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_sweep_time(self.channel, time)

    def set_sweep_delay(self, delay):
        print "U R in VnaChannel - set_sweep_delay" #FLAG FOR DEBUGGING
        
        super(VnaChannel, self).set_sweep_delay(self.channel, delay)
