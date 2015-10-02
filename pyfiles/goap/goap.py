###goap for example

class World(object):
	def __init__(self, current_list):
		self.current_list = current_list
		self.goal_list = []

	def GoalList(self, goal):
		self.goal_list = goal
		return self.goal_list

	def PrintList(self):
		for status in self.current_list:
			print status,
		print ''

	def UpdateList(self, action):
		for status in action.add_list:
			if status not in self.current_list:
				self.current_list.append(status)
		for status in action.del_list:
			if status in self.current_list:
				self.current_list.remove(status)

	def AchieveGoal(self):
		for status in self.goal_list:
			if status not in self.current_list:
				return False
		return True

	def IsExecutable(self, action_list):
		for status in action_list.precondition:
			if status not in self.current_list:
				return False
		return True

class ActionList(object):
	def __init__(self, name, precondition, add_list, del_list, get_cost):
		self.name = name
		self.precondition = precondition
		self.add_list = add_list
		self.del_list = del_list
		self.get_cost = get_cost

	def PrintList(self):
		print 'action: ' + self.name
		print 'precondition: ',
		for precon in self.precondition:
			print precon,
		print ""
		print 'add list: ',
		for add in self.add_list:
			print add,
		print ""
		print 'del_list: ',
		for remove in self.del_list:
			print remove,
		print""
		print 'cost: '+ str(self.get_cost)

class Planner(object):
	def __init__(self, initial_model, available_actions, goal):
		self.initial_model = initial_model
		self.available_actions = available_actions
		self.goal = goal
		self.astar = AstarSearch(self.initial_model, self.goal,3,2,4)

	def Goal(self, goals):
		self.goal = goals
		for goal in self.goals:
			if goal not in self.available_actions:
				assert False, 'goal not in available actions'

	def planning(self, action_list, goal_list):
		plan_list = []
		self.check()
		pass

	def process(self):
		plan = self.planning(self.available_actions, self.goal)
		if plan is None:
			assert False, 'plan does not exist'
		pass

	def check(self):
		for status in self.available_actions:
			print status
		print ''


class AstarSearch(object):
	def __init__(self,initial_list, goal_list, add_list, del_list, weight):
		_path = {'nodes': {},
			'node_id': 0,
			'goal': goal_list,
			'append': add_list,
			'remove': del_list,
			'cost': weight,
			'action_node': {},
			'olist':{},
			'clist':{}
			}
		open_list = []
		close_list = []


	def distance_to_state(state1, state2):
		score = 0
	
		for state in state2:
			if state not in state1:
				score += 1

		for state in state1:
			if state not in state2:
				score += 1
	
		return score

	def condition_met(state1, state2):
		for state in state2:
			if state in state1:
				return True
		return False

	def frontier(self):
		pass


if __name__ == '__main__':
	pass
	
