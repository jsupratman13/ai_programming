import sys, time, math
from simplegoap import List, Action, BehaviorGenerator, PlanningTask

def action_list():
	actions = []
	
	#Action: Pickup Spear
	actions.append(Action('pickup_spear',
				['at_armory', 'empty_hands'], 
				['hold_spear'], 
				['empty_hands']))

	#Action: Store Spear
	actions.append(Action('store_spear',
				['at_armory','hold_spear'],
				['empty_hands'],
				['hold_spear']))

	#Action: Hunt Deer
	actions.append(Action('hunt_deer',
				['at_forest', 'hold_spear','empty_backpack'],
				['carry_rawmeat'],
				['empty_backpack']))

	#Action: Cook Food REEDIT
	actions.append(Action('cook_food',
				['at_kitchen','carry_rawmeat'],
				['carry_food'],
				['carry_rawmeat']))

	#Action: Eat Dinner
	actions.append(Action('eat_dinner',
				['at_dinning_room', 'empty_hands', 'carry_food'],
				['have_dinner'],
				['carry_food']))

	#Action: Move to Armory REEDIT
	actions.append(Action('moveto_armory',
				['ready_to_move'],
				['at_armory'],
				['ready_to_move']))
	
	#Action: Move to Kitchen REEDIT
	actions.append(Action('moveto_kitchen',
				['ready_to_move'],
				['at_kitchen'],
				['ready_to_move']))

	#Action: Move to Forest REEDIT
	actions.append(Action('moveto_forest',
				['ready_to_move'],
				['at_forest'],
				['ready_to_move']))

	#Action: Move to Dinning room
	actions.append(Action('moveto_dinning_room',
				['empty_hands', 'carry_food'],
				['at_dinning_room'],
				[]))

	#Action: Ready to Move
	actions.append(Action('new_destination',
				[],
				['ready_to_move'],
				['at_forest', 'at_gates', 'at_armory',
				'at_kitchen','at_farmhouse']))

	return actions

def main():
	initial_model = List(['at_armory', 'empty_backpack', 'empty_hands'])
	goal = [] #carry_food
	actions = action_list()
	
#	print 'initial model: ' + str(initial_model)
#	print 'action list: ' + str(actions)
#	print 'goal: ' + str(goal)

	behavior_generator = BehaviorGenerator(initial_model, actions, goal)
	plan = behavior_generator.process()
	print 'Plan: ',
	print plan

#	for action in plan:
#		initial_model.UpdateList(action)
#	print 'updated model',
#	initial_model.PrintList()

def main2():
	initial_model = List(['ready_to_move', 'empty_backpack','empty_hands'])
	goal = ['carry_food']
	actions = action_list()
	task = PlanningTask(initial_model, actions, goal)
	print 'Solving the present planning problem'
	plan = task.depth_first_search(8)
	print 'Plan: ',
	print plan


if __name__ == '__main__':
	try:
		main2()
	
	except (KeyboardInterrupt,SystemExit):
		sys.exit()

	except Exception, e:
		print 'Exception: ' + str(e)
