#############################
# @file fsm.py               #
# @brief FSM example         #
# @author Joshua Supratman   #
# @date 2017/09/07           #
##############################

import math

#####################################################
# KNOWLEDGE REPRESENTATION                         # 
#####################################################
class WorldStatus(object):
    def __init__(self):
        self.bullet = 50
        self.target_dist = 100
        self.enemy_found = False
        self.enemy_dead = False
#####################################################

class FSM(object):
    def __init__(self,world_status):
        self.world = world_status
        self.states_list = {\
                       'Patrol':self.Patrol,
                       'Reload': self.Reload,
                       'Approach': self.Approach,
                       'Shoot' : self.Shoot,
                       }
        self.state = 'Patrol'

    def run(self):
        print self.state
        self.states_list[self.state]()

######################################################
# STATES                                            #
######################################################
    def Patrol(self):
        #Process
        self.world.enemy_found = True

        #Transition
        if self.world.bullet < 50:
            self.state = 'Reload'
        elif self.world.enemy_found:
            if self.world.target_dist > 50:
                self.state = 'Approach'
            else:
                self.state = 'Shoot'

    def Reload(self):
        #Process
        self.world.bullet = 50

        #Transition
        if self.world.enemy_found:
            self.state = 'Approach'
        else:
            self.state = 'Patrol'

    def Approach(self):
        #Process
        self.world.target_dist -= 20
        print 'distance to target: ' + str(self.world.target_dist)

        #Transition
        if self.world.target_dist < 50:
            self.state = 'Shoot'
        elif not self.world.enemy_found:
            self.state = 'Patrol'

    def Shoot(self):
        #Process
        self.world.enemy_dead = True
        self.world.enemy_found = False
        self.world.bullet -= 3

        #Transition
        self.state = 'Patrol'
#####################################################

if __name__ == '__main__':
    world_status = WorldStatus()
    fsm = FSM(world_status)
    while not world_status.enemy_dead:
        fsm.run()
        print '----------------------------'
