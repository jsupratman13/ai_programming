from csp import WorldState, Task

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

