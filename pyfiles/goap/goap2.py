class WorldState(object):
	def __init__(self, *args):
		self.define_status = args
		self.initial_state = None
		self.goal_state = None

	def set_initialstate(self, **kwargs):
		if len(kwargs) != len(self.define_status): assert False, "number of initial state does not match with WorldState"
		for state in kwargs:
			if state not in self.define_status:
				assert False, "initial state does not match with WorldState"
		self.initial_state = kwargs
	
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
			self.pathplan = DepthFirstSearch(self.world, self,actionlist)
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
		for status in self.world.initial_state.iteritems():
			print status,

	def process(self):
		print 'searching plan'
		return self.pathplan.formulate()

class AstarSearch(object):
	def __init__(self, world, actionlist):
		self.world = world
		self.actionlist = actionlist
	
	def neighbor(self):
		pass

	def formulate(self):
		pass

class DepthFirstSearch(object):
	def __init__(self, world, actionlist):
		self.world = world
		self.actionlist = actionlist
	
	def formulate(self):
		pass
