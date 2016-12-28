################################
# @file main.py                #
# @brief utility based system  #
# @author Joshua Supratman     #
# @date 2016/01/07             #
################################

from utility import WorldState,Action
import time

if __name__ == '__main__':
    initial_time = time.time()

    #Initialize: set world status and action
    world = WorldState('enemy_HP', 'HP', 'bullets')
    world.set_initialstate(enemy_HP=6, HP=70, bullets=10)

    attacking = Action('attacking')
    attacking.set_utility('enemy_HP',1)

    healing = Action('healing')
    healing.set_utility('HP',2)

    reloading = Action('reload')
    reloading.set_utility('bullets', 3)

    action_list = [attacking,healing,reloading]
    action_to_execute = {}

    #get utility for each actions
    print world.current_state  
    for action in action_list:
        weight = 0
        for utility_status in action.utility_list:
            for status in world.current_state:
                if status == utility_status.name:
                    weight += utility_status.get_utility(world.current_state[status])
        action_to_execute[action.name] = weight
    
    #choose which action to execute
    print action_to_execute
    action_to_execute = sorted(action_to_execute, key=action_to_execute.get, reverse=True)
    action = action_to_execute.pop(0)
    print 'execute: ' + action
