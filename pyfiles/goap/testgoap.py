import math, sys, traceback, time
from goap import World, ActionList, Planner

def accelitesoccer():
	model = World([])
	goals = model.GoalList(['ball_in_target'])
	initial_list = ['unknown_self_pos', 'unknown_ball_pos','ball_not_in_target', 'dont_have_ball', 'ball_not_straight', 'ball_not_in_kickarea']

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


	task = Planner(initial_list, actions, goals)	
	plans = task.process()

	print '\nFormulated Plan: '+ str(plans[1])
	print '\nCurrent State: ' + str(plans[2])
	print '\nTotal Cost: ' + str(plans[0])

def hunting():
	model = World([])
	goals = model.GoalList(['cook_food'])


if __name__ == '__main__':
	try:
		initial_time = time.time()
		accelitesoccer()
		print 'time: ' + str(time.time() - initial_time)

	except Exception, e:
		print traceback.format_exc()
		print 'Exception: '+str(e)

	except KeyboardInterrupt:
		sys.exit()
