###goap for example

class List(object):
	def __init__(self, current_list):
		self.current_list = current_list

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

	def AchieveGoal(self, goal):
		pass

	def IsExecutable(self, action_list):
		pass

class Action(object):
	def __init__(self, name, precondition, add_list, del_list):
		self.name = name
		self.precondition = precondition
		self.add_list = add_list
		self.del_list = del_list

	def PrintList(self):
		print 'action' + name
		print 'precondition'
		for precon in self.precondition:
			print precon,
			print ""
		print 'add list'
		for add in self.add_list:
			print add,
			print ""
		print 'del_list'
		for remove in self.del_list:
			print remove,
			print""

class BehaviorGenerator(object):
	pass
