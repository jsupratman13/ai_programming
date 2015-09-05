###goap for example

class List(object):
	def __init__(self, current_list):
		self.current_list = current_list

	def PrintList(self):
		pass

	def UpdateList(self, action):
		pass

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
		for del in self.del_list:
			print del,
			print""

class BehaviorGenerator(object):
	pass
