## GOAP improvement

from goap2 import WorldState, Action, Planner

if __name__=='__main__':
	world = WorldState('hungry', 'has_food', 'in_kitchen', 'tired', 'in_bed')
	world.set_initialstate(hungry=True, has_food=False, in_kitchen=False, in_bed=False, tired=True)
	world.set_goalstate(tired=False)

	actionlist = []
	
	action = Action('eat',1)
	action.set_precondition(hungry=True, has_food=True, in_kitchen=False)
	action.set_effects(hungry=False, has_food=False)
	actionlist.append(action)

	action = Action('cook',1)
	action.set_precondition(hungry=True, has_food=False, in_kitchen=True)
	action.set_effects(has_food=True)
	actionlist.append(action)

	action = Action('sleep',1)
	action.set_precondition(tired=True, in_bed=True)
	action.set_effects(tired=False)
	actionlist.append(action)

	action = Action('go_to_bed',1)
	action.set_precondition(in_bed=False, hungry=False)
	action.set_effects(in_bed=True)
	actionlist.append(action)
	
	action = Action('go_to_kitchen',10)
	action.set_precondition(in_kitchen=False)
	action.set_effects(in_kitchen=True)
	actionlist.append(action)
	
	action = Action('leave_kitchen',1)
	action.set_precondition(in_kitchen=True)
	action.set_effects(in_kitchen=False)
	actionlist.append(action)
	
	action = Action('order_pizza',1)
	action.set_precondition(has_food=False, hungry=True)
	action.set_effects(has_food=True)
	actionlist.append(action)

	task = Planner(world, actionlist)
	plans = task.process()
	for plan in plans.actionlist:
		print plan.name
	print '\ncurrent status: '
	for state in plans.world.current_state.iteritems():
		print state,

