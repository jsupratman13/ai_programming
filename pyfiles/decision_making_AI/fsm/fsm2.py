#!/usr/bin/env python
import math
import time

class WorldStatus(object):
    def __init__(self):
        self.open_door = False
        self.step = 3

class FSM(object):
    def __init__(self,world_status):
        self.status = world_status
        self.states_list = {\
                       'ApproachDoor':self.ApproachDoor,\
                       'OpenDoor': self.OpenDoor\
                       }
        self.state = 'OpenDoor'

    def ApproachDoor(self):
        if self.status.step > 0:
            print str(self.status.step) + ' m away from door'
            self.status.step -= 1
        else:
            print '0 m away from door'
            self.state = 'OpenDoor'
    
    def OpenDoor(self):
        if self.status.step != 0:
            print 'too far'
            self.state = 'ApproachDoor'
        else:
            print 'opening door'
            self.status.open_door = True

    def run(self):
        self.states_list[self.state]()

if __name__ == '__main__':
    world_status = WorldStatus()
    fsm = FSM(world_status)
    while not world_status.open_door:
        fsm.run()
        print '----------------------------'
