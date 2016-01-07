################################
# @file main.py                #
# @brief GOAP example          #
# @author Joshua Supratman     #
# @date 2016/01/07             #
################################

from goap import WorldState, Action, Planner
import time

if __name__=='__main__':
	initial_time = time.time()

	world = WorldState('enemy_dead', 'tired', 'enemy_found', 'near_enemy', 'fear')
	world.set_initialstate(enemy_dead=False, enemy_found=True, tired=False, near_enemy=False, fear=False)
	world.set_goalstate(enemy_dead=True)

	actionlist = []
	
	charge = Action('Charge', 3)
	charge.set_precondition(enemy_found=True, near_enemy=False, fear=False)
	charge.set_effects(near_enemy=True)
	actionlist.append(charge)

	movein = Action('MoveIn', 5)
	movein.set_precondition(enemy_found=True, near_enemy=False, fear=True)
	movein.set_effects(near_enemy=True)
	actionlist.append(movein)

	shoot = Action('Shoot',1)
	shoot.set_precondition(enemy_dead=False, near_enemy=True, enemy_found=True)
	shoot.set_effects(enemy_dead=True, near_enemy=False, enemy_found=False)
	actionlist.append(shoot)

	idle = Action('Idle',3)
	idle.set_precondition(enemy_found=False, tired=True)
	idle.set_effects(tired=False)
	actionlist.append(idle)

	walk = Action('Walk', 5)
	walk.set_precondition(enemy_found=False, tired=False)
	walk.set_effects(tired=True)
	actionlist.append(walk)

	task = Planner(world, actionlist)
	plans = task.process()
	for plan in plans.actionlist:
		print plan.name
	print '\ncurrent status: '
	for state in plans.world.current_state.iteritems():
		print state,
	
	print '\ntotal time: ' + str(time.time()-initial_time)

