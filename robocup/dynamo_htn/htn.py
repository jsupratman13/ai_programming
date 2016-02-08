################################
# @file htn.py                 #
# @brief HTN Planner core      #
# @author Joshua Supratman     #
# @date 2016/01/07             #
################################

import copy, time, itertools

class DecompHistory(list):
	def __init__(self):
		self.history_list = []

	class RecordHistory(list):
		def __init__(self, current_task, other_methods, task_list, working_state, plans):
			current_task.method_list = other_methods
			self.last_recorded_task_list = [current_task]
			self.last_recorded_task_list.extend(task_list)
			self.last_recorded_working_state = copy.deepcopy(working_state)
			self.last_recorded_plans = plans

	def RestoreHistory(self):
		return self.history_list

class Planner(object):
	def __init__(self, world, root_task):
		self.pathplan = DepthFirstSearch(world, root_task)	

	def process(self):
		print '\ngenerating plan'
		plans = self.pathplan.formulate()
		print ''
		if plans is None:
			assert False, "no plan could be generated"
		return plans

class DepthFirstSearch(object):
	def __init__(self, world, root_task):
		self.plans = []
		self.working_state = copy.deepcopy(world)
		self.task_list = [root_task]
		self.method_list = []
		self.decomphistory = DecompHistory()

	def condition_met_method(self, methods):
		method = methods()
		for precondition in method.preconditions():
			if precondition not in self.working_state.iteritems():
				return False
		return True

	def condition_met(self, task):
		for precondition in task.preconditions():
			if precondition not in self.working_state.iteritems():
				return False
		return True

	def print_method(self, method_list):
		for Method in method_list:
			method = Method()
			print str(method.__class__.__name__) + ' subtask: ',
			for Task in method.subtask():
				task = Task()
				print str(task.__class__.__name__),
			print ''

	def find_method(self, task):
		method_list = []
		for method in task.method_list:
			if self.condition_met_method(method):
				method_list.append(method)
		return method_list

	def formulate(self):
		while self.task_list:
			Task = self.task_list.pop(0)
			current_task = Task()
			if current_task.task_type == 'Compound':
#				print '\ncompound: ' + str(current_task.__class__.__name__)
				self.method_list = self.find_method(current_task)
#				self.print_method(self.method_list)
				
				if self.method_list:
#					print '**decomposing task**'
					Method = self.method_list.pop(0)
					m = Method()
					history = self.decomphistory.RecordHistory(current_task, self.method_list, self.task_list, self.working_state, self.plans)
					self.task_list[0:0] = m.subtask() #extend and insert in beginning of list
					self.decomphistory.history_list.append(history)

				else:
#					print '**no available method, returning to last decomposed task**'
					history_list = self.decomphistory.RestoreHistory()
					if history_list:
						history = history_list.pop()
						self.task_list = history.last_recorded_task_list
						self.working_state= history.last_recorded_working_state
						self.plans = history.last_recorded_plans
					else:
						return None
				
			elif current_task.task_type == 'Primative':
#				print '\nprimative: ' + str(current_task.__class__.__name__)
				if self.condition_met(current_task):
#					print '**add task to plans**'
					self.working_state.update(current_task.effects())
					self.plans.append(current_task)
				
				else:
#					print '**condition not met, reset plans and returning to last decomposed task**'
					history_list= self.decomphistory.RestoreHistory()
					history = history_list.pop()
					self.task_list = history.last_recorded_task_list
					self.working_state = history.last_recorded_working_state
					self.plans = history.last_recorded_plans
			else:
				assert False, 'Unknown Task Type'

		return self.plans

if __name__ == '__main__':
	print 'ok'
