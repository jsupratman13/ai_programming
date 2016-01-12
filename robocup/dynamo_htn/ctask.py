from ccl import Task, WorldState

class KickMode:
	def __init__(self):
		self.task_type = 'Compound'	
		self.method_list = [HighKickMode(),NormalKickMode(),DribbleMode()]

	class HighKickMode:
		def precondition(self):
			pass

		def subtask(self):
			pass

	class NormalKickMode:
		def precondition(self):
			pass

		def subtask(self):
			pass

	class DribbleMode:
		def precondition(self):
			pass

		def subtas(self):
			pass
			
if __name__ == '__main__':
	print 'ok'
