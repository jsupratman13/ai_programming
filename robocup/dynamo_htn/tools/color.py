# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
from pyenv import Robot

def OppositeColor(col):
    """Returns opposite color of specified color
    Usage: opp_col = OppositeColor(robot.HLCOLOR_BLUE)
    written by kaminaga"""
    if(col==Robot.HLCOLOR_YELLOW):
        return Robot.HLCOLOR_BLUE
    elif(col==Robot.HLCOLOR_BLUE):
        return Robot.HLCOLOR_YELLOW
    elif(col==Robot.HLCOLOR_CYAN):
        return Robot.HLCOLOR_MAGENTA
    elif(col==Robot.HLCOLOR_MAGENTA):
        return Robot.HLCOLOR_CYAN
    else:
        return Robot.HLCOLOR_BLACK
