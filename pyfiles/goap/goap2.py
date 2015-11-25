class WorldState(object):
	def __init__(self, *args):
		self.define_status = args
		self.initial_state = None
		self.goal_state = None

	def set_state(self, **kwargs):
		for state in kwargs:
			if state not in self.define_status:
				assert False, "initial state does not match with WorldState"
		self.initial_state = kwargs
	
	def set_goalstate(self, **kwargs):
		for state in kwargs:
			if state not in self.defnie_status:
				assert False, "goal state does not correspond with WorldState"	
		self.goal_state = kwargs

class Action(object):
	def __init__(self,name):
		self.name = name
		self.precondition = None
		self.effects = None
	
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

if __name__ == '__main__':
	world = WorldState('candy','pink')
	world.set_state(candy=True, pink=True)

	actionlist = []

	action = Action('eating')
	action.set_precondition(pink=True)
	action.set_effects(candy=False)
	actionlist.append(action)

	plan = Planner(world,actionlist)
	plan.process()
