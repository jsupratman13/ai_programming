################################
# @file main.py                #
# @brief GOAP example          #
# @author Joshua Supratman     #
# @date 2017/09/07             #
################################

from goap import WorldState, Action, Planner

if __name__=='__main__':

#####################################################
# KNOWLEDGE REPRESENTATION                         #
#####################################################
    world = WorldState('have_bullet', 'near_enemy', 'enemy_found', 'enemy_dead')
    world.set_initialstate(have_bullet=False, near_enemy=False, enemy_found=False, enemy_dead=False)
    world.set_goalstate(enemy_dead=True)
####################################################

####################################################
# ACTIONS                                         # 
####################################################
    patrol = Action('Patrol', 7)
    patrol.set_precondition()
    patrol.set_effects(enemy_found=True)

    reload = Action('Reload', 3)
    reload.set_precondition(near_enemy=False)
    reload.set_effects(have_bullet=True)

    approach = Action('Approach', 3)
    approach.set_precondition(enemy_found=True)
    approach.set_effects(near_enemy=True)

    shoot = Action('Shoot', 1)
    shoot.set_precondition(near_enemy=True, enemy_found=True, have_bullet=True)
    shoot.set_effects(enemy_dead=True)
####################################################

    action_list = []
    action_list.append(patrol)
    action_list.append(reload)
    action_list.append(approach)
    action_list.append(shoot)

    planner = Planner()
    plans = planner.process(world, action_list)
    for plan in plans:
        print plan.name

