################################
# @file main.py                #
# @brief HTN Planner example   #
# @author Joshua Supratman     #
# @date 2017/09/07             #
################################

from htn import WorldState, Planner, CompoundTask, PrimitiveTask

if __name__ == '__main__':
##############################################
# KNOWLEDGE REPRESENTATION                   # 
##############################################
    world = WorldState('have_bullet', 'near_enemy', 'enemy_found', 'enemy_dead')
    world.set_initialstate(have_bullet=False, near_enemy=False, enemy_found=True, enemy_dead=False)
##############################################

##############################################
# PRIMITIVE TASK                            #
##############################################
    patrol = PrimitiveTask('Patrol')
    patrol.set_precondition()
    patrol.set_effects(enemy_found=True)

    reload = PrimitiveTask('Reload')
    reload.set_precondition(near_enemy=False)
    reload.set_effects(have_bullet=True)

    approach = PrimitiveTask('Approach')
    approach.set_precondition(enemy_found=True)
    approach.set_effects(near_enemy=True)

    shoot = PrimitiveTask('Shoot')
    shoot.set_precondition(near_enemy=True, enemy_found=True, have_bullet=True)
    shoot.set_effects(enemy_dead=True)
###############################################

###############################################
# COMPOUND TASK                              #
###############################################    
    prepare = CompoundTask('Prepare')
    m0 = prepare.Method('method_0')
    m0.set_precondition(have_bullet=False)
    m0.set_subtask(reload, approach)
    m1 = prepare.Method('method_1')
    m1.set_precondition()
    m1.set_subtask(approach)
    prepare.set_method_list(m0, m1)

    root = CompoundTask('Root')
    m0 = root.Method('method_0')
    m0.set_precondition()
    m0.set_subtask(patrol, prepare, shoot)
    root.set_method_list(m0)
###############################################

    planner = Planner()
    plans = planner.process(world, root)
    for plan in plans:
        print plan.name
