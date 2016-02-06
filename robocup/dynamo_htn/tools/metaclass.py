# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

""" Emulates the super functionality of the python3.x
written by Daiki Maekawa"""
class SuperMeta(type):
    def __new__(cls, name, bases, dct):
        obj = type.__new__(cls, name, bases, dct)
        setattr(obj, '_%s__super' % name, super(obj))
        return obj

