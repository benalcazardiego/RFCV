#SMU_Sweep_Type_class_creator
#SMUs can work IN linear, LOG10, LOG25 and LOG50 types when the SMU is in sweep configuration 
from enum import enum

SweepType = enum(LINEAR=1, LOG10=2, LOG25=3, LOG50=4)
