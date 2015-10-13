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

	'''
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
	'''
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
			if state in state1:
				return True
		return False
		
	def outline(self, current_list):
		path = []
		if self.condition_met(self.initial_list, self.current_list):
			return path

		self.neighbor(current_list)
		for states in self.neighbor_list:
			if states not in self.frontier:
				self.frontier.append(states)
				frontier_continue = True

		for option in self.frontier:
			if option not in self.visited:
				self.visited.append(option)
#TODO				update LIST
				path = self.outline(current_list)
				return path	

if __name__ == '__main__':
	tec = {}
	tec['big'] = 8;
	ex = 9
	ex2 = ['low', 'high']
	tec[str(9)] = 10;
	tec[str(ex2)] = 11;
	sort_tec = sorted(tec.items(), key=operator.itemgetter(1))
	print sort_tec
	print sort_tec[0]
	print sort_tec[0][0]	
