# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

##########################################################################
 # Copyright (c) 2013 Daiki Maekawa and CIT Brains All Rights Reserved. #
 #                                                                      #
 # @file algorithm.py                                                   #
 # @brief Hodgepodge of useful functions                                #
 # @author Daiki Maekawa                                                #
 # @date 2013-10-21                                                     #
##########################################################################

def clamp(value, high, low):
    if value > high:
        return high
    else:
        if value < low:
            return low
        else:
            return value

