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

	def process(self):
		print 'searching plan'
		return self.pathplan.formulate()

class PartialPlan(object):
	def __init__(self,world, actionlist, calc_cost):
		self.world = world
		self.actionlist = actionlist
		self.cost = calc_cost
	
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
	
	def neighbor(self, parent): #TODO: remove repeatitive action
		neighbor_list = []
		for action in self.actionlist:
			for precondition in action.precondition.iteritems():
				print precondition[0]
				if precondition not in parent.current_state.iteritems():
					print 'precon not match'
					break
			else:
				neighbor_list.append(action)
				print 'precon match new neighbor'
		return neighbor_list

	def update_status(self, action, parent): #TODO: copy classes to prevent change simultaneously
		successor = parent
		successor.world.current_state.update(action.effects)
		for suc in successor.world.current_state.iteritems():
			print suc,
		successor.cost = successor.cost + action.cost #TODO; heuristic calculation and cost adjustment

		return successor

	def condition_met(self, successor):
		for goal in self.world.goal_state.iteritems():
			if goal not in successor.world.current_state.iteritems():
				return False
		return True

	def formulate(self):
		successor = PartialPlan(self.world, [],0)
		self.ol.append(successor)
		parent = self.ol.pop(0)
		successor_list = self.neighbor(parent.world)
		for action in successor_list:
			successor = self.update_status(action, parent)
#		while self.ol:
			#TODO: sort ollist in order of least successor cost to greatest
#			parent = self.ol.pop(0)
#			successor_list = self.neigbor(parent.world)
#			for action in successor_list:
#				successor = upadate_status(action, parent)
#				if self.condition_met(successor):
#					return successor.actionlist
					
			
			
			
		

if __name__ == '__main__':
	world = WorldState('eat','sleep')
	world.set_initialstate(eat=False,sleep=False)
	world.set_goalstate(sleep=True)
	
	alist = []

	action = Action('get_food', 1)
	action.set_precondition(eat=False,sleep=False)
	action.set_effects(eat=True)
	alist.append(action)

	task = Planner(world,alist)
	task.process()
