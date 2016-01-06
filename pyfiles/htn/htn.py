import copy, time, itertools

class WorldState(object):
	def __init__(self, *args):
		self.define_status = args
		self.current_state = None

	def set_initialstate(self, **kwargs):
		if len(kwargs) != len(self.define_status): assert False, "number of initial state does not match with WorldState"
		for state in kwargs:
			if state not in self.define_status:
				assert False, "initial state does not match with WorldState"
		self.current_state = kwargs	

class CompoundTask(object):
	def __init__(self, name):
		self.name = name
		self.method_list = []
	
	def set_method_list(self, *args):
		self.method_list = args

	class Method(object):
		def __init__(self, name):
			self.name = name
			self.preconditions = None
			self.subtask = []

		def set_precondition(self, **kwargs):
			self.preconditions = kwargs

		def set_subtask(self, *args):
			self.subtask = args

class PrimativeTask(object):
	def __init__(self, name):
		self.name = name
		self.preconditions = None
		self.effects = None

	def set_precondition(self, **kwargs):
		self.preconditions = kwargs
	
	def set_effects(self, **kwargs):
		self.effects = kwargs

class DecompHistory(object):
	def __init__(self):
		self.last_known_state = None
		self.last_method_list = []

	def record(self,method):
		self.last_method_list = method

	def restore(self):
		return None

class Planner(object):
	def __init__(self, world, root_task):
		self.world = world
		self.pathplan = DepthFirstSearch(world, root_task)

	def print_world(self):
		for status in self.world.current_state.iteritems():
			print status,	

	def process(self):
		print '\ninitial status: ', 
		self.print_world()
		print '\n\ngenerating plan:'
		plans = self.pathplan.formulate()
		if plans is None:
			assert False, "no plan could be generated"
		return plans

class DepthFirstSearch(object):
	def __init__(self, world, root_task):
		self.plans = []
		self.current_world = world
		self.working_world = copy.deepcopy(self.current_world)
		self.processing_task = [root_task]
		self.method_list = []

	def condition_met(self, task):
		for precondition in task.preconditions.iteritems():
			if precondition not in self.working_world.current_state.iteritems():
				return False
		return True

	def find_method(self, task):
		return False

	def formulate(self):
		while self.processing_task:
#			print self.working_world.current_state
			current_task = self.processing_task.pop(0)
			if str(current_task.__class__.__name__) == 'CompoundTask':
				for method in current_task.method_list:
					if self.condition_met(method):
						self.method_list.append(method)
				if self.method_list:
					m = self.method_list.pop(0)
					self.processing_task.append(m.subtask) #find way to append in order
					#record rest of list
				else:
					pass
					#restore last session
				
			elif str(current_task.__class__.__name__) == 'PrimativeTask':
				if self.condition_met(current_task):
					self.working_world.current_state.update(current_task.effects)
					self.plans.append(current_task)
				
				else:
					pass
					#restore to last task
			else:
				print current_task.name
				print str(current_task.__class__.__name__)
				assert False, 'Unknown Task Type'
		return self.plans

if __name__ == '__main__':
	print 'ok'
