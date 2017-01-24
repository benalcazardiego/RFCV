# VNA_characteristics_classes_creators
from enum import enum

print "U R in VnaEnums" # Flag 4 debug

SweepType = enum(LINEAR=1, LOG=2, SEGM=3, POW=4)
SParameters= enum(S11=1, S12=2, S21=3, S22=4)
CalType = enum(OPEN=1, SHORT=2, THRU=3, FULL_2PORT=4, FULL_1PORT=5, TRL_2PORT=6)
DataFormat = enum(LOG=1, LIN=2, LIN_PHASE=3, PHASE=4, GDELAY=5, 
        SMITH_LIN_PHASE=6, SMITH_LOG_PHASE=7, SMITH_RE_IM=8, SMITH_R_JX=9, SMITH_G_JB=10)
Direction = enum(LEFT=1, RIGHT=2)
