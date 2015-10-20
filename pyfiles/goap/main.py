import math, sys, traceback, time
from goap import World, ActionList, Planner

def accelitesoccer():
	model = World([])
	goals = model.GoalList(['ball_in_target'])
	initial_state = ['unknown_self_pos', 'unknown_ball_pos','ball_not_in_target', 'dont_have_ball', 'ball_not_straight', 'ball_not_in_kickarea']

	actions = []
	#Name, precondition, addlist, dellist, cost
	actions.append(ActionList('Localize',['unknown_self_pos'],['know_self_pos'],['unknown_self_pos'],2)) #5
	
	actions.append(ActionList('SearchBall',['unknown_ball_pos'],['know_ball_pos'],['unknown_ball_pos'],3)) #5
	
	actions.append(ActionList('ApproachBall', ['know_ball_pos','dont_have_ball'], ['have_ball'],['dont_have_ball'], 5)) #4
	
	actions.append(ActionList('TurnAroundBall', ['know_self_pos', 'have_ball', 'ball_not_straight'],['ball_straight','ball_not_in_kickarea'], ['ball_kickarea','ball_not_straight'], 5)) #3
	
	actions.append(ActionList('AdjustToKick', ['have_ball', 'ball_straight','ball_not_in_kickarea'], ['ball_kickarea'], ['ball_not_in_kickarea'], 8)) #2
	
	actions.append(ActionList('Shoot', ['ball_kickarea', 'ball_straight', 'have_ball','ball_not_in_target'], 
					['ball_in_target', 'dont_have_ball','ball_not_straight','ball_not_in_kickarea'], 
					['ball_kickarea', 'ball_straight', 'have_ball', 'ball_not_in_target'], 5)) #1


	task = Planner(initial_state, actions, goals)	
	plans = task.process()

	print '\nFormulated Plan: '+ str(plans[1])
#	print '\nCurrent State: ' + str(plans[2])
#	print '\nTotal Cost: ' + str(plans[0])

def hunting():
	model = World([])
	goals = ['have_dinner']
	initial_state = ['at_armory', 'empty_backpack', 'empty_hands']

	actions = []
	#Name, precondition, addlist, dellist, cost
	actions.append(ActionList('pickup_spear',['at_armory', 'empty_hands'], ['hold_spear'], ['empty_hands'], 5))

	actions.append(ActionList('store_spear',['at_armory','hold_spear'],['empty_hands'],['hold_spear'], 5))

	actions.append(ActionList('hunt_deer',['at_forest', 'hold_spear','empty_backpack'],['carry_rawmeat'],['empty_backpack'], 5))

	actions.append(ActionList('cook_food',['at_kitchen','carry_rawmeat'],['carry_food'],['carry_rawmeat'], 5))

	actions.append(ActionList('eat_dinner',['at_dinning_room','carry_food','empty_hands'],['have_dinner'],['carry_food'], 5))

	actions.append(ActionList('moveto_armory',[],['at_armory'],['at_kitchen', 'at_forest', 'at_dinning_room'], 5))
	
	actions.append(ActionList('moveto_kitchen',['carry_rawmeat'],['at_kitchen'],['at_armory', 'at_forest', 'at_dinning_room'], 5))

	actions.append(ActionList('moveto_forest',['hold_spear'],['at_forest'],['at_armory', 'at_kitchen', 'at_dinning_room'], 5))

	actions.append(ActionList('moveto_dinning_room',['carry_food'],['at_dinning_room'],['at_armory', 'at_kitchen', 'at_forest'], 5))

#	actions.append(ActionList('new_destination',[],['ready_to_move'],['at_forest', 'at_gates', 'at_armory','at_kitchen','at_farmhouse', 'at_dinning_room'], 3))

	
	task = Planner(initial_state, actions, goals)
	plans = task.process()
	print '\nFomulated Plan: ' + str(plans[1])
	print '\nCurrent State: ' + str(plans[2])
#	print '\nTotal Cost: ' + str(plans[0])


def warefare():
	initial_state = ['no_ammo','engage_enemy']
	goals = ['enemy_eliminated']

	actions = []
	#Name, precondition, addlist, delist, cost
	actions.append(ActionList('move_in', ['engage_enemy', 'weapons_armed'], ['near_enemy'],['away_from_danger'],5))

	actions.append(ActionList('reload', ['has_ammo', 'in_cover'], ['weapons_loaded'], [], 5))
	
	actions.append(ActionList('take_cover', ['engage_enemy'], ['in_cover'], [], 10))
	
	actions.append(ActionList('shoot_enemy', ['weapons_armed', 'near_enemy'], ['enemy_eliminated'], ['engage_enemy','no_ammo'], 5))
	
	actions.append(ActionList('arm_weapon', ['weapons_loaded'],['weapons_armed'],[], 5))
	
	actions.append(ActionList('find_ammo', ['no_ammo','away_from_danger'],['has_ammo'], ['no_ammo'], 5))
	
	actions.append(ActionList('retreat', [], ['away_from_danger'], ['near_enemy'], 5))
	
	actions.append(ActionList('heal', ['injured', 'away_from_danger'], [], ['injured'], 5))
	
	actions.append(ActionList('patrol', [], ['patrol'],['engage_enemy'],5))

	actions.append(ActionList('found_enemy', ['patrol'], ['engage_enemy'],['patrol'], 5))

	task = Planner(initial_state, actions, goals)
	plans = task.process()
	print '\nFomulated Plan: ' + str(plans[1])
	print '\nCurrent State: ' + str(plans[2])
#	print '\nTotal Cost: ' + str(plans[0])


if __name__ == '__main__':
	try:
		initial_time = time.time()
		
		#accelitesoccer()
		#hunting()
		warefare()
		
		print '\ntime: ' + str(time.time() - initial_time)

	except Exception, e:
		print traceback.format_exc()
		print 'Exception: '+str(e)

	except KeyboardInterrupt:
		sys.exit()
