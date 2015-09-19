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
	def __init__(self, name, precondition, add_list, del_list):
		self.name = name
		self.precondition = precondition
		self.add_list = add_list
		self.del_list = del_list

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

class PartialPlan:
	def __init__(self, actions, model):
		self.actions = actions
		self.model = model
	
	def nice_print(self):
		print 'Partial actions: ',
		print self.actions
		print 'Partial world model: ',
		self.model.nice_print()

class PlanningTask:
	def __init__(self, initial_model, available_actions, goal):
		self.initial_model = initial_model
		self.available_actions = available_actions
		self.goal = goal

	def depth_first_search(self, bound):
		node = PartialPlan([], self.initial_model)
		open_nodes = [node]

		while open_nodes:
			node = open_nodes.pop()
			if node.model.AchieveGoal(self.goal):
				return node.actions
			if len(node.actions) == bound:
				continue
			for action in self.available_actions:
				if node.model.IsExecutable(action):
					successor = node.model.create_successor(action)
					actions = list(node.actions)
					actions.append(action.name)
					open_nodes.append(PartialPlan(actions, successor))
		return False


