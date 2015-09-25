import sys, time, math, traceback
from simplegoap import World, Action_List, PlanningTask

def hunting_motion_ex():
	actions = []
	
	#Action: Pickup Spear
	actions.append(Action_List('pickup_spear',
				['at_armory', 'empty_hands'], 
				['hold_spear'], 
				['empty_hands']))

	#Action: Store Spear
	actions.append(Action_List('store_spear',
				['at_armory','hold_spear'],
				['empty_hands'],
				['hold_spear']))

	#Action: Hunt Deer
	actions.append(Action_List('hunt_deer',
				['at_forest', 'hold_spear','empty_backpack'],
				['carry_rawmeat'],
				['empty_backpack']))

	#Action: Cook Food REEDIT
	actions.append(Action_List('cook_food',
				['at_kitchen','carry_rawmeat'],
				['carry_food'],
				['carry_rawmeat']))

	#Action: Eat Dinner
	actions.append(Action_List('eat_dinner',
				['at_dinning_room', 'empty_hands', 'carry_food'],
				['have_dinner'],
				['carry_food']))

	#Action: Move to Armory REEDIT
	actions.append(Action_List('moveto_armory',
				['ready_to_move'],
				['at_armory'],
				['ready_to_move']))
	
	#Action: Move to Kitchen REEDIT
	actions.append(Action_List('moveto_kitchen',
				['ready_to_move'],
				['at_kitchen'],
				['ready_to_move']))

	#Action: Move to Forest REEDIT
	actions.append(Action_List('moveto_forest',
				['ready_to_move'],
				['at_forest'],
				['ready_to_move']))

	#Action: Move to Dinning room
	actions.append(Action_List('moveto_dinning_room',
				['empty_hands', 'carry_food'],
				['at_dinning_room'],
				[]))

	#Action: Ready to Move
	actions.append(Action_List('new_destination',
				[],
				['ready_to_move'],
				['at_forest', 'at_gates', 'at_armory',
				'at_kitchen','at_farmhouse']))

	return actions

def main():
	model = World(['at_armory', 'empty_backpack', 'empty_hands'])
	goal = ['carry_food']
	actions = hunting_motion_ex()
	
	task = PlanningTask(model, actions, goal)
	plan = task.depth_first_search(8)
	print 'Plan: ',
	print plan

if __name__ == '__main__':
	try:
		main()
	
	except (KeyboardInterrupt,SystemExit):
		sys.exit()

	except Exception, e:
		print traceback.format_exc()
		print 'Exception: ' + str(e)
