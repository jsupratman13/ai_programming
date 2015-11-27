import copy, itertools

class WorldState(object):
	def __init__(self, *args):
		self.define_status = args
		self.goal_state = None
		self.current_state = None

	def set_initialstate(self, **kwargs):
		if len(kwargs) != len(self.define_status): assert False, "number of initial state does not match with WorldState"
		for state in kwargs:
			if state not in self.define_status:
				assert False, "initial state does not match with WorldState"
		self.current_state = kwargs
	
	def set_goalstate(self, **kwargs):
		for state in kwargs:
			if state not in self.define_status:
				assert False, "goal state does not correspond with WorldState"	
		self.goal_state = kwargs

class Action(object):
	def __init__(self,name, cost):
		self.name = name
		self.precondition = None
		self.effects = None
		self.cost = cost
	
	def set_precondition(self, **kwargs):
		self.precondition = kwargs
	
	def set_effects(self, **kwargs):
		self.effects = kwargs

class Planner(object):
	def __init__(self, world, actionlist, planstyle='astar'):
		self.world = world
		self.actionlist = actionlist
		self.check()
		if planstyle == 'dfs':
			assert False, "DepthFirstSearch not created yet"
		else:
			self.pathplan = AstarSearch(self.world, self.actionlist)
		
	def check(self):
		for action in self.actionlist:
			for precondition in action.precondition:
				if precondition not in self.world.define_status:
					assert False, "%s precondition does not match world state" %action.name
			for effect in action.effects:
				if effect not in self.world.define_status:
					assert False, "%s effect does not match world state" %action.name

	def print_actionlist(self):
		for action in self.actionlist:
			print action.name
	
	def print_world(self):
		for status in self.world.current_state.iteritems():
			print status,
	
	def print_goal(self):
		for goal in self.world.goal_state.iteritems():
			print goal,

	def process(self):
		print '\ninitial status: ', 
		self.print_world()
		print '\ngoal: ', 
		self.print_goal()
		print '\n\ngenerating plan:'
		plans = self.pathplan.formulate()
		if plans is None:
			assert False, "no plan could be generated"
		return plans

class PartialPlan(object):
	def __init__(self,world, actionlist, calc_cost):
		self.world = world
		self.actionlist = actionlist
		self.cost = calc_cost

	def __repr__(self):
		return '{}'.format(self.cost)
	
	def __cmp__(self, other):
		if hasattr(other, 'cost'):
			return self.cost.__cmp__(other.cost)
	
	def print_plan(self):
		for state in self.world.current_state.iteritems():
			print state,
		print ""
		for action in self.actionlist:
			print action.name,
		print ""
		print self.cost

class AstarSearch(object):
	def __init__(self, world, actionlist):
		self.world = world
		self.actionlist = actionlist
		self.ol = []
		self.cl = []
	
	def neighbor(self, parent): #brief: neighbor is determine from list of action if precon match and it is not already visited
		neighbor_list = []
		for action in self.actionlist:
			if action in parent.actionlist:
				continue
			for precondition in action.precondition.iteritems():
				if precondition not in parent.world.current_state.iteritems():
					break
			else:
				neighbor_list.append(action)
		return neighbor_list

	def update_status(self, action, parent):
		successor = copy.deepcopy(parent)
		successor.world.current_state.update(action.effects)
		successor.actionlist.append(action)
		successor.cost = successor.cost + action.cost #TODO; heuristic calculation and cost adjustment

#		successor.print_plan()
		return successor

	def condition_met(self, successor):
		for goal in self.world.goal_state.iteritems():
			if goal not in successor.world.current_state.iteritems():
				return False
		return True

	def formulate(self):
		successor = PartialPlan(self.world, [],0)
		self.ol.append(successor)
		while self.ol:
			self.ol.sort()
			parent = self.ol.pop(0)
			successor_list = self.neighbor(parent)
			for action in successor_list:
				successor = self.update_status(action, parent)
				if self.condition_met(successor):
					return successor
				for other_ol, other_cl in itertools.izip_longest(self.ol,self.cl):
					if other_ol and successor.actionlist == other_ol.actionlist and successor.cost > other_ol.cost:
						break
					if other_cl and successor.actionlist == other_cl.actionlist and successor.cost > other_cl.cost:
						break
				else:
					self.ol.append(successor)
			self.cl.append(parent)	
			
		
