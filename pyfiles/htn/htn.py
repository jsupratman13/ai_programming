import copy, time, itertools

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

class CompoundTask(object):
	def __init__(self):
		pass

	def method(self, **kwargs):
		pass

	def subtask(self, *args):
		pass

class PrimativeTask(object):
	def __init__(self):
		pass

	def precondition(self, **kwargs):
		pass

	def operators(self):
		pass

	def effects(self, **kwargs):
		pass

class Plannner(object):
	def __init__(self):
		pass

	def process(self):
		pass

class DepthFirstSearch(object):
	def __init__(self):
		pass

	def formulate(self):
		pass

if __name__ == '__main__':
	print 'ok'
