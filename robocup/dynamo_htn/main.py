import ccl
import ptask, ctask
import time

class AcceliteStrategy(object):
	def __init__(self):
		self.task_type = 'Compound'
		self.method_list = [AcceliteStrategy.NormalStrategy, AcceliteStrategy.Localize]
	
	class NormalStrategy:
		def preconditions(self):
			return [(ccl.WorldState.K_KNOW_SELF_POS, True)]

		def subtask(self):
			return [ptask.SearchBall, ptask.ApproachBall, ptask.RotateAroundBall, ptask.AdjustToKick, ctask.KickMode]

	class Localize:
		def preconditions(self):
			return [(ccl.WorldState.K_KNOW_SELF_POS, False)]

		def subtask(self):
			return [ptask.LandmarkToLocalize, ptask.SearchBall]

class Hello:
	def __init__(self):
		self.task_type = 'compound'

if __name__ == '__main__':
	soccer = ccl.SoccerStrategy()
	root = AcceliteStrategy()

	soccer.run(AcceliteStrategy)
	
