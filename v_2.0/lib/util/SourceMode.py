#SMU_Source_Mode_class_creator
#SMUs can work as current source and voltage source
from enum import enum

SourceMode = enum(VOLTAGE=1, CURRENT=2, COMMON=3)
