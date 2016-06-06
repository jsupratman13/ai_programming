import csp
import offense as ptask
import compound as ctask
import initialize
import time

class Root(object):
	def __init__(self):
		self.task_type = 'Compound'
		self.method_list = [Root.NormalStrategy, Root.Localize]

	class Idling:
		def preconditions(self):
			pass

		def subtask(self):
			return [initialize.Idling]
	
	class NormalStrategy:
		def preconditions(self):
			return [(csp.WorldState.K_KNOW_SELF_POS, True)]

		def subtask(self):
			return [ptask.SearchBall, ptask.ApproachBall, ptask.TurnAroundBallToTarget, ptask.AdjustToKick, ctask.KickMode]

	class Localize:
		def preconditions(self):
			return [(csp.WorldState.K_KNOW_SELF_POS, False)]

		def subtask(self):
			return [initialize.LandmarkToLocalize]

if __name__ == '__main__':
	print 'ok'
