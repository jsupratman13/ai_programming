import math
import time

class WorldStatus(object):
    def __init__(self):
        self.open_door = False
        self.step = 3

class State(object):
    def __init__(self):
        self._states = {}
        self.transition = 'OpenDoor'
    
    def run(self):
        pass

    def add_states(self, state):
        self._states[str(state.__class__.__name__)]=state

    def execute(self):
        self.transition = self._states[self.transition].run()
    
class ApproachDoor(State):
    def __init__(self, status):
        super(ApproachDoor, self).__init__()
        self._status = status

    def run(self):
        if self._status.step > 0:
            print str(self._status.step) + ' m away from door'
            self._status.step -= 1
        else:
            print '0 m away from door'
            self.transition = 'OpenDoor'
        return self.transition

class OpenDoor(State):
    def __init__(self, status):
        super(OpenDoor, self).__init__()
        self._status = status

    def run(self):
        if self._status.step != 0:
            print 'too far'
            self.transition = 'ApproachDoor'
        else:
            print 'opening door'
            self._status.open_door = True
        return self.transition

if __name__ == '__main__':
    #create world status
    status = WorldStatus()

    #create states
    approach_door = ApproachDoor(status)
    open_door = OpenDoor(status)

    #assemble states
    fsm = State()
    fsm.add_states(approach_door)
    fsm.add_states(open_door)
    
    while not status.open_door:
        fsm.execute()
        print '------------------------'
