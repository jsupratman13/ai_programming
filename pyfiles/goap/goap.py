###goap for example
import math
import operator
import time

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
		return self.current_list

	def AchieveGoal(self, goal_list):
		for status in goal_list:
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
		self.cost = get_cost

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
		print ""
		print 'cost: '+ str(self.cost)

class Planner(object):
	def __init__(self, initial_model, available_actions, goal):
		self.initial_model = initial_model
		self.available_actions = available_actions
		self.goal = goal
		self.astar = AstarSearch(self.goal, self.available_actions)

	def goal_check(self):
		for goal in self.goal:
			for action in self.available_actions:
				if goal in action.add_list:
					return True
		assert False, 'goal not in available actions'

	def process(self):
		self.goal_check()
		plan = self.astar.searchtree(self.initial_model)
#		self.check()
		if not plan:
			assert False, 'plan does not exist'
		return plan

	def check(self):
		print ''
		for status in self.available_actions:
			status.PrintList()
			print ''
		for status in self.goal:
			print status
			print ''


class AstarSearch(object):
	def __init__(self, goal_list, action_list):
#		self.initial_list = current_list
#		self.current_list = self.initial_list
		self.goal_list = goal_list
		self.action_list = action_list

		self.close_list = []
		self.open_list = []

	def neighbor(self, current_list):
		neighbor_list = []
		for action in self.action_list:
			for precon in action.precondition:
				if precon not in current_list:
					break
			else:
				neighbor_list.append(action)
		return neighbor_list

	def condition_met(self, state1, state2):
		for state in state1:
			if state not in state2:
				return False
		return True
	
	def update_list(self, successor, current_list):
		new_list = list(current_list)
		for suc_add in successor.add_list:
			if suc_add not in current_list:
				new_list.append(suc_add)
		for suc_del in successor.del_list:
			if suc_del in current_list:
				new_list.remove(suc_del)
		return new_list
		
	def searchtree(self, current_list):
		self.open_list = [[0, '',current_list]]
		neighbor_list = []
		initial_time = time.time()
		while self.open_list:
			if (time.time()-initial_time) > 5:
				assert False, 'unable to calibrate plans in 5 seconds'
			self.open_list = sorted(self.open_list)
			current_state = self.open_list.pop(0)
			neighbor_list = self.neighbor(current_state[2])

			for successor in neighbor_list:
				#model = World(current_state[2])
				successor_cost = current_state[0] + successor.cost
				successor_state = [successor_cost, current_state[1]+successor.name+' ', self.update_list(successor, current_state[2])]
				#model.PrintList()
				if self.condition_met(self.goal_list, successor_state[2]):
					return successor_state 
				for status in self.open_list:
					if (successor_state[1] == status[1]) and (successor_state[0] > status[0]):
						break
				for status in self.close_list:
					if (successor_state[1] == status[1]) and (successor_state[0] > status[0]):
						break
				else: 
					self.open_list.append(successor_state)
			self.close_list.append(current_state)

if __name__ == '__main__':
	olist = [['hello'],'bear']
	llist = ['hello']
	tlist = ['hello']
	coplist = list(olist)
	coplist.append(llist)
	print coplist
	print olist
