from ccl import Task, WorldState
import time

class Idling(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		pass

	def preconditions(self):
		return []

	def effects(self):
		return []

class LandmarkToLocalize(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'localize!'
			yield

	def preconditions(self):
#		return [(WorldState.K_KNOW_SELF_POS, False)]
		return []

	def effects(self):
	        return [(WorldState.K_KNOW_SELF_POS, True)]

class TrackBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		pass

	def preconditions(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

	def effects(self):
	        return [(WorldState.K_TRACKING_BALL, True)]

class SearchBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'ball search!'
			yield

	def preconditions(self):
#		return [(WorldState.K_KNOW_BALL_POS, False)]
		return []

	def effects(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

class TurnToSearchBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		pass

	def preconditions(self):
	        return []

	def effects(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

class ApproachBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'approaching ball!'
			yield

	def preconditions(self):
	        return [(WorldState.K_KNOW_BALL_POS, True), (WorldState.K_KNOW_SELF_POS, True)]

	def effects(self):
	        return [(WorldState.K_HAVE_BALL, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, False)]

class RotateAroundBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'rotating ball!'
			yield

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, False), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

class AdjustToKick(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'adjusting to kick!'
			yield

	def preconditions(self):
	        return [(WorldState.K_HAVE_BALL, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, True)]

class DribbleBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		pass

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True),(WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, False)]

class KickBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'kicking ball!'
			yield

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]

class HighKickBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		while True:
			time.sleep(1)
			print 'high kicking ball!'
			yield

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]

if __name__ == '__main__':
	print 'ok'
