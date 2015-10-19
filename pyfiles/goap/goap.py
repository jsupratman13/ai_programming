###goap for example
import math
import operator


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
		self.astar = AstarSearch(self.initial_model, self.goal, self.available_actions)

	def Goal(self, goals):
		self.goal = goals
		for goal in self.goals:
			if goal not in self.available_actions:
				assert False, 'goal not in available actions'

	def process(self):
		plan = self.astar.planning()
		self.check()
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
	def __init__(self, current_list, goal_list, action_list):
		self.initial_list = current_list
		self.current_list = self.initial_list
		self.goal_list = goal_list
		self.action_list = action_list

		self.visited = []
		self.frontier = []
		self.neighbor_list = []
		self.close_list = []
		self.open_list = []

	def planning(self):
		plan_list = []
		plans = {}
		self.neighbor(self.initial_list)
#		plan_list = [self.outline(self.initial_list)]
		if len(plan_list) <= 1:
			return plan_list
		
		for plan in plan_list:
			plans[str(plan)] = cost_calc(plan)
		
		plan_list = sorted(plans.items(), key=operator.itemgetter(1))
		plan_list = plan_list[0][0]
		return plan_list

	def neighbor(self, current_list):
		neighbor_exist = False
		for action in self.action_list:
			if action.precondition in current_list:
				self.neighbor_list.append(action)
				neighbor_exist = True
#		if not neighbor_exist:
#			assert False, "neighbor doesn't exist"

	def cost_calc(self, plan):
#TODO		implement heuristic calculation
		total_cost = 0
		for action in plan:
			total_cost += action.cost
		return int(total_cost)

	def condition_met(self, state1, state2):
		for state in state2:
			if state not in state1:
				print 'Missing: ' + str(state) + 'from initial list'
				return False
		for state in state1:
			if state not in state2:
				print 'Missing: ' + str(state) + 'from current list'
				return False
		return True
		
	def outline(self, current_list):
	#TODO:how to take care of world list?
		world = World(current_list)
		self.open_list = [[0, 'start']]
		self.clost_list = []
		while self.open_list:
			self.open_list = sorted(self.open_list)
			current_state = self.open_list[0] #self.open_list.pop()
			neigbor_list = self.neighbor(current_list)
			for successor in neighbor_list:
				#successor_list = UPDATE List
				if self.condition_met(self.goal_list, successor_list):
					return path #
				successor_cost = current_state[0] + successor.cost
				# if succesor in self.open_list:
				#	self._openlist pop
				#	if succcessor_cost > self list cost: continues
				# if successor in self.close_list:
				#	self. close list pop
				# i	if successor _cost > self list cost: continue

				self.open_list.append{[successor_cost, successor)
			self.close_list.append(curren_state)

#initialize open and close list
#leave f=0, put start in ol
#while ol is not empty
#	find node with least f on ol and call it "q"   q is current node
#	pop off q from ol
#	generate successor and set their parents to q
#	for each succesor
#		if successor is goal, stop
#		successor.g = q.g + path
#		successor.h = distance from goal to successor
#		successor.f = g + h
#
#		if same_node in open list is same as succssor but better, skip successor
#		if same_node in close list is same as succssor but better, skip succsor
#		else add successor to open list
#	push q to close list

if __name__ == '__main__':
	tec = [[9, 'big']]
	so = [7, 'tec']
	pi = [9, 'arg']
	tec.append(so)
	tec.append(pi)
	print sorted(tec)	
