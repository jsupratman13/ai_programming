from ccl import Task, WorldState

class Idling:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return []

	def effects(self):
		return []

class LandmarkToLocalize:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return [(WorldState.K_KNOW_SELF_POS, False)]

	def effects(self):
	        return [(WorldState.K_KNOW_SELF_POS, True)]

class TrackBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

	def effects(self):
	        return [(WorldState.K_TRACKING_BALL, True)]

class SearchBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return [(WorldState.K_KNOW_BALL_POS, False)]

	def effects(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

class TurnToSearchBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
	        return []

	def effects(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

class ApproachBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
	        return [(WorldState.K_KNOW_BALL_POS, True), (WorldState.K_KNOW_SELF_POS, True)]

	def effects(self):
	        return [(WorldState.K_HAVE_BALL, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, False)]

class RotateAroundBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, False), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

class AdjustToKick:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
	        return [(WorldState.K_HAVE_BALL, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, True)]

class DribbleBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True),(WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, False)]

class KickBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]

class HighKickBall:
	def __init__(self):
		self.task_type = 'Primative'

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]

if __name__ == '__main__':
	print 'ok'
