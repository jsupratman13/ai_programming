from csp import WorldState
import offense


class KickMode:
	def __init__(self):
		self.task_type = 'Compound'	
		self.method_list = [KickMode.HighKickMode,KickMode.NormalKickMode,KickMode.DribbleMode]

	class HighKickMode:
		def preconditions(self):
			return [(WorldState.K_BALL_IN_GOAL_AREA, True)]

		def subtask(self):
			return [offense.HighKickBall]

	class NormalKickMode:
		def preconditions(self):
			return []

		def subtask(self):
			return [offense.KickBall]

	class DribbleMode:
		def preconditions(self):
			return []

		def subtask(self):
			return [offense.DribbleBall]
			
if __name__ == '__main__':
	print 'ok'
