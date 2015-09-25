import math, sys, traceback, time
from goap import World, ActionList, Planner

def main():
	model = World([])
	goals = model.GoalList(['ball_in_target'])
	initial_list = []

	actions = []
	#Name, precondition, addlist, dellist, cost
	actions.append(ActionList('Localize',[],['know_self_pos'],[],2))
	actions.append(ActionList('SearchBall',[],['know_ball_pos'],[],3))
	actions.append(ActionList('ApproachBall', ['know_ball_pos'], ['have_ball'],[], 5))
	actions.append(ActionList('TurnAroundBall', ['know_self_pos', 'have_ball'],['ball_straight'], ['ball_kickarea'], 5))
	actions.append(ActionList('AdjustToKick', ['have_ball', 'ball_straight'], ['ball_kickarea'], [], 8))
	actions.append(ActionList('Shoot', ['ball_kickarea', 'ball_straight', 'have_ball'], ['ball_in_target'], ['ball_kickarea', 'ball_straight', 'have_ball'], 5))

	task = Planner(initial_list, actions, goals)
	plans = task.process()

	for plan in plans:
		print plan,
	print ''


if __name__ == '__main__':
	try:
		initial_time = time.time()
		main()
		print 'time: ' + str(initial_time - time.time())

	except Exception, e:
		print traceback.format_exc()
		print 'Exception: '+str(e)

	except KeyboardInterrupt:
		sys.exit()
