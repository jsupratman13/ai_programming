################################
# @file htn.py                 #
# @brief HTN Planner core      #
# @author Joshua Supratman     #
# @date 2016/01/07             #
################################

import copy, time, itertools
from operator import itemgetter
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

class CompoundTask:
	def __init__(self, name):
		self.name = name
		self.method_list = []
	
	def set_method_list(self, *args):
		self.method_list = args

	class Method(list):
		def __init__(self, name):
			self.name = name
			self.preconditions = None
			self.subtask = []

		def set_precondition(self, **kwargs):
			self.preconditions = kwargs

		def set_subtask(self, *args):
			self.subtask = args

class PrimativeTask(list):
	def __init__(self, name):
		self.name = name
		self.preconditions = None
		self.effects = None

	def set_precondition(self, **kwargs):
		self.preconditions = kwargs
	
	def set_effects(self, **kwargs):
		self.effects = kwargs

class DecompHistory(list):
	def __init__(self):
		self.history_list = []

	class RecordHistory(list):
		def __init__(self, current_task, other_methods, task_list, working_state, plans, mtr):
			current_task.method_list = other_methods
			self.last_recorded_task_list = [current_task]
			self.last_recorded_task_list.extend(task_list)
			self.last_recorded_working_state = copy.deepcopy(working_state)
			self.last_recorded_plans = plans
			self.last_mtr = mtr

	def RestoreHistory(self):
		return self.history_list

class Planner(object):
	def __init__(self, world, root_task):
		self.world = world
		self.pathplan = DepthFirstSearch(world, root_task)
		self.mtr = 0

	def print_world(self):
		for status in self.world.current_state.iteritems():
			print status,	

	def process(self):
		print '\ninitial status: ', 
		self.print_world()
		print '\n\ngenerating plan:'
		plans, mtr = self.pathplan.formulate()
		if plans is None:
			assert False, "no plan could be generated"
		self.mtr = mtr
		return plans

class DepthFirstSearch(object):
	def __init__(self, world, root_task):
		self.plans = []
		self.working_state = world
		self.task_list = [root_task]
		self.method_list = []
		self.decomphistory = DecompHistory()
		self.mtr = 0

	def find_mtr(self, task, pop_method):
		print [x for x in task.method_list].index(pop_method)

	def condition_met(self, method):
		for precondition in method.preconditions.iteritems():
			if precondition not in self.working_state.current_state.iteritems():
				return False
		return True

	def print_method(self, method_list):
		for method in method_list:
			print str(method.name) + ' subtask: ',
			for task in method.subtask:
				print str(task.name),
			print ''

	def find_method(self, task):
		method_list = []
		for method in task.method_list:
			if self.condition_met(method):
				method_list.append(method)
		return method_list

	def formulate(self):
		while self.task_list:
			current_task = self.task_list.pop(0)
			if str(current_task.__class__.__name__) == 'CompoundTask':
				print '\ncompound: ' + str(current_task.name)
				self.method_list = self.find_method(current_task)
				self.print_method(self.method_list)
				
				if self.method_list:
					print '**decomposing task**'
					m = self.method_list.pop(0)
					history = self.decomphistory.RecordHistory(current_task, self.method_list, self.task_list, self.working_state, self.plans, self.mtr)
					self.task_list[0:0] = m.subtask #extend and insert in beginning of list
					self.decomphistory.history_list.append(history)

				else:
					print '**no available method, returning to last decomposed task**'
					history_list = self.decomphistory.RestoreHistory()
					if history_list:
						history = history_list.pop()
						self.task_list = history.last_recorded_task_list
						self.working_state= history.last_recorded_working_state
						self.plans = history.last_recorded_plans
						self.mtr = history.last_mtr
					else:
						return None
				
			elif str(current_task.__class__.__name__) == 'PrimativeTask':
				print '\nprimative: ' + str(current_task.name)
				if self.condition_met(current_task):
					print '**add task to plans**'
					self.working_state.current_state.update(current_task.effects)
					self.plans.append(current_task)
				
				else:
					print '**condition not met, reset plans and returning to last decomposed task**'
					history_list= self.decomphistory.RestoreHistory()
					history = history_list.pop()
					self.task_list = history.last_recorded_task_list
					self.working_state = history.last_recorded_working_state
					self.plans = history.last_recorded_plans
					self.mtr = history.last_mtr
			else:
				assert False, 'Unknown Task Type'

		return self.plans, self.mtr
