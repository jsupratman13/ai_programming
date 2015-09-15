import sys, time, math
from simplegoap import World, Action_List, BehaviorGenerator, PlanningTask

def hunting_motion_ex():
	actions = []
	
	#Action: Pickup Spear
	actions.append(Action_List('pickup_spear',
				['at_armory', 'empty_hands'], 
				['hold_spear'], 
				['empty_hands'],1))

	#Action: Store Spear
	actions.append(Action_List('store_spear',
				['at_armory','hold_spear'],
				['empty_hands'],
				['hold_spear'],1))

	#Action: Hunt Deer
	actions.append(Action_List('hunt_deer',
				['at_forest', 'hold_spear','empty_backpack'],
				['carry_rawmeat'],
				['empty_backpack'],1))

	#Action: Cook Food REEDIT
	actions.append(Action_List('cook_food',
				['at_kitchen','carry_rawmeat'],
				['carry_food'],
				['carry_rawmeat'],1))

	#Action: Eat Dinner
	actions.append(Action_List('eat_dinner',
				['at_dinning_room', 'empty_hands', 'carry_food'],
				['have_dinner'],
				['carry_food'],1))

	#Action: Move to Armory REEDIT
	actions.append(Action_List('moveto_armory',
				['ready_to_move'],
				['at_armory'],
				['ready_to_move'],1))
	
	#Action: Move to Kitchen REEDIT
	actions.append(Action_List('moveto_kitchen',
				['ready_to_move'],
				['at_kitchen'],
				['ready_to_move'],1))

	#Action: Move to Forest REEDIT
	actions.append(Action_List('moveto_forest',
				['ready_to_move'],
				['at_forest'],
				['ready_to_move'],1))

	#Action: Move to Dinning room
	actions.append(Action_List('moveto_dinning_room',
				['empty_hands', 'carry_food'],
				['at_dinning_room'],
				[],1))

	#Action: Ready to Move
	actions.append(Action_List('new_destination',
				[],
				['ready_to_move'],
				['at_forest', 'at_gates', 'at_armory',
				'at_kitchen','at_farmhouse'],1))

	return actions

def main():
	model = List(['at_armory', 'empty_backpack', 'empty_hands'])
	model.GoalList(['carry_food'])
	actions = hunting_motion_ex()
	
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

def ex_simple():
	initial_model = List(['ready_to_move', 'empty_backpack','empty_hands'])
	goal = ['carry_food']
	actions = hunting_motion_ex()
	task = PlanningTask(initial_model, actions, goal)
	print 'Solving the present planning problem'
	plan = task.depth_first_search(8)
	print 'Plan: ',
	print plan


if __name__ == '__main__':
	try:
		ex_simple()
	
	except (KeyboardInterrupt,SystemExit):
		sys.exit()

	except Exception, e:
		print 'Exception: ' + str(e)
