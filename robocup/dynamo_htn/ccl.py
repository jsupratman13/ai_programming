import abc
import time

class Task(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def operators(self): pass

	@abc.abstractmethod
	def preconditions(self): pass

	@abc.abstractmethod
	def effects(self): pass

	def get_state(self):
		pass

class WorldState(object):
	def __init__(self):
		self._world_rep = {
			WorldState.K_KNOW_BALL_POS : self._ball_pos,
			WorldState.K_KNOW_SELF_POS : self._self_pos,
			WorldState.K_KNOW_ENEMY_POS: self._enemy_pos,
			WorldState.K_KNOW_ALLY_POS: self._ally_pos,
			WorldState.K_KNOW_ALLY_STAT: self._ally_stat,
			WorldState.K_ON_TARGET_POS: self._target_pos,
			WorldState.K_HAVE_BALL: self._have_ball,
			WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE: self._ball_and_target_on_straight_line,
			WorldState.K_BALL_IN_KICK_AREA : self._ball_in_kick_area,
			WorldState.K_BALL_IN_GOAL_AREA : self._ball_in_goal_area,
			WorldState.K_BALL_IN_TARGET : self._ball_in_target,
			WorldState.K_IDLE : self._idle,
		}
		self._world_status = {key: False for key, state in self._world_rep.items()}

	def _update(self):
		for state, key in self._world_status.items():
			new_key = self._world_rep[state]()
			self._world_status[state] = new_key

	def print_state(self):
		print 'current state: ',
		for state in self._world_status.items():
			print state,
		print '\n'

	def _ball_pos(self):
		return True

	def _self_pos(self):
		return False

	def _enemy_pos(self):
		return True

	def _ally_pos(self):
		return True
	
	def _ally_stat(self):
		return True

	def _target_pos(self):
		return True

	def _have_ball(self):
		return False

	def _ball_and_target_on_straight_line(self):
		return False

	def _ball_in_kick_area(self):
		return True

	def _ball_in_goal_area(self):
		return True

	def _ball_in_target(self):
		return False

	def _idle(self):
		return False

	K_KNOW_BALL_POS = "K_KNOW_BALL_POS"
	K_KNOW_SELF_POS = "K_KNOW_SELF_POS"
	K_KNOW_ENEMY_POS ="K_KNOW_ENEMY_POS"
	K_KNOW_ALLY_POS = "K_KNOW_ALLY_POS"
	K_KNOW_ALLY_STAT ="K_KNOW_ALLY_STAT"
	K_ON_TARGET_POS = "K_ON_TARGET_POS"
	K_HAVE_BALL = "K_HAVE_BALL"
	K_BALL_AND_TARGET_ON_STRAIGHT_LINE = "K_BALL_AND_TARGET_ON_STRAIGHT_LINE"
	K_BALL_IN_KICK_AREA = "K_BALL_IN_KICK_AREA"
	K_IDLE = "K_IDLE"
	K_BALL_IN_GOAL_AREA = "K_BALL_IN_GOAL_AREA"
	K_BALL_IN_TARGET = "K_BALL_IN_TARGET"

class SoccerStrategy(object):
	def __init__(self):
		self.state = WorldState()

	def run(self, initial_time):
		for state, key in self.state._world_status.iteritems():
			print state, key

		while time.time() - initial_time < 5:
			self.state._update()
			print 'update'

			self.state.print_state()

			time.sleep(2)
