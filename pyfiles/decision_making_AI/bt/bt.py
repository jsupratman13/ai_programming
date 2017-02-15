#www.indiedb.com/groups/indievault/tutorials/game-ai-behavior-tree
#Game AI - Behavior Tree

import math
import time

class WorldStatus(object):
    def __init__(self):
        self.open_door = False  #door status
        self.step = 3       #distance from door

class Node(object):
    def __init__(self):
        self._children = []
    
    def run(self):
        pass

    def add_child(self, c):
        self._children.append(c)

class Selector(Node):
    def __init__(self):
        super(Selector, self).__init__()

    def run(self):
        for c in self._children:
            if c.run():
                return True
        return False

class Sequence(Node):
    def __init__(self):
        super(Sequence, self).__init__()

    def run(self):
        for c in self._children:
            if not c.run():
                return False
        return True

class IsDoorOpen(Node):
    def __init__(self, status):
        super(IsDoorOpen, self).__init__()
        self._status = status

    def run(self):
        if self._status.open_door:
            print 'door is open'
        else:
            print 'door is close'
        return self._status.open_door

class ApproachDoor(Node):
    def __init__(self, status):
        super(ApproachDoor, self).__init__()
        self._status = status

    def run(self):
        if self._status.step > 0:
            print str(self._status.step) +' m away from door'
            self._status.step -= 1
            return True
        return False

class OpenDoor(Node):
    def __init__(self, status):
        super(OpenDoor, self).__init__()
        self._status = status

    def run(self):
        if self._status.step != 0:
            print 'still too far'
            return False
        print 'open door'
        self._status.open_door = True
        return True

if __name__ == '__main__':
    #Define Functional Node
    root = Sequence()
    seq = Sequence()
    sel = Selector()

    #create world status
    status = WorldStatus()

    #create action
    is_door_open = IsDoorOpen(status)
    approach_door = ApproachDoor(status)
    open_door = OpenDoor(status)

    #assemble tree
    root.add_child(sel)

    sel.add_child(is_door_open)
    sel.add_child(seq)

    seq.add_child(approach_door)
    seq.add_child(open_door)

    #run root until value is true
    while not root.run():
        print("-----------")

    print 'finished action'
