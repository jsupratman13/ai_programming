###goap for example

class World(object):
	def __init__(self, current_list):
		self.current_list = current_list
		self.goal_list = []

	def GoalList(self, goal):
		self.goal_list = goal

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

	def AchieveGoal(self, goal):
		for status in goal:
			if status not in self.current_list:
				return False
		return True

	def IsExecutable(self, action_list):
		for status in action_list.precondition:
			if status not in self.current_list:
				return False
		return True
	
	def create_successor(self, action):
		successor_model = List(list(self.current_list))
		successor_model.UpdateList(action)
		return successor_model

class Action_List(object):
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
	
	def planning(self, action_list, goal_list):
		plan_list = []
		pass

	def process(self):
		plan = self.planning(available_actions, goal)
		if plan is None:
			assert False, 'plan does not exist'
		pass

class AstarSearch(object):
	def __init__(self):
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

if __name__ == '__main__':
	state1 = ['yuck', 'wonder', 'weird']
	state2 = ['wonder']

	score = distance_to_state(state1, state2)
	print score
	
