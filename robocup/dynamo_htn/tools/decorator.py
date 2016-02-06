# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

##########################################################################
 # Copyright (c) 2013 Daiki Maekawa and CIT Brains All Rights Reserved. #
 #                                                                      #
 # @file decorator.py                                                   #
 # @brief Hodgepodge of useful functions                                #
 # @author Daiki Maekawa                                                #
 # @date 2013-10-21                                                     #
##########################################################################

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

