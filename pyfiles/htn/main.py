from htn import WorldState, Planner, CompoundTask, PrimativeTask

if __name__ == '__main__':
	world = WorldState('enemy_dead', 'tired', 'enemy_found', 'near_enemy', 'fear')
	world.set_initialstate(enemy_dead=False, enemy_found=True, tired=False, near_enemy=False, fear=True)

	charge = PrimativeTask('Charge')
	charge.set_precondition(enemy_found=True, near_enemy=False, fear=False)
	charge.set_effects(near_enemy=True)

	movein = PrimativeTask('MoveIn')
	movein.set_precondition(enemy_found=True, near_enemy=False, fear=True)
	movein.set_effects(near_enemy=True)

	shoot = PrimativeTask('Shoot')
	shoot.set_precondition(enemy_dead=False, near_enemy=True, enemy_found=True)
	shoot.set_effects(enemy_dead=True, near_enemy=False, enemy_found=False)

	idle = PrimativeTask('Idle')
	idle.set_precondition(enemy_found=False, tired=True)
	idle.set_effects(tired=False)

	walk = PrimativeTask('Walk')
	walk.set_precondition(enemy_found=False, tired=False)
	walk.set_effects(tired=True)

	approach = CompoundTask('Approach')
	m0 = approach.Method('m0')
	m0.set_precondition(fear=True)
	m0.set_subtask(movein)
	m1 = approach.Method('m1')
	m1.set_precondition(fear=False)
	m1.set_subtask(charge)
	approach.set_method_list(m0, m1)

	attack = CompoundTask('Attack')
	m0 = attack.Method('m0')
	m0.set_precondition(near_enemy=True)
	m0.set_subtask(shoot)
	m1 = attack.Method('m1')
	m1.set_precondition(near_enemy=False)
	m1.set_subtask(approach, shoot)
	attack.set_method_list(m0, m1)

	root = CompoundTask('Root')
	m0 = root.Method('m0')
	m0.set_precondition(enemy_found=True)
	m0.set_subtask(attack)
	m1 = root.Method('m1')
	m1.set_precondition(enemy_found=False)
	m1.set_subtask(walk, idle)
	root.set_method_list(m0, m1)

	planning = Planner(world, root)
	plans = planning.process()
	for plan in plans:
		print str(plan.__class__.__name__)
