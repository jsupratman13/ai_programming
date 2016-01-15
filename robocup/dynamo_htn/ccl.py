# @file
# @brief central command list
# 
import abc
import time
from htn import Planner

class Task(object):
	__metaclass__ = abc.ABCMeta

	COMPLETE = 'COMPLETE'
	ACTIVE = 'ACTIVE'
	FAILED = 'FAILED'

	@abc.abstractmethod
	def operators(self): pass

	@abc.abstractmethod
	def preconditions(self): pass

	@abc.abstractmethod
	def effects(self): pass

	def status(self, current_state):
		state = current_state.items()
		effect = self.effects()
		if len(self.preconditions()) > 0:
			for precondition in self.preconditions():
				if precondition not in current_state.iteritems():
					return Task.FAILED
		for effect in self.effects():
			if effect not in current_state.iteritems():
				return Task.ACTIVE
		else:
			return Task.COMPLETE
			
class WorldState(object):
	def __init__(self):
		self.it = time.time()
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
		self.world_status = {key: False for key, state in self._world_rep.items()}

	def _update(self):
		for state, key in self.world_status.items():
			new_key = self._world_rep[state]()
			self.world_status[state] = new_key

	def print_state(self):
		print 'current state: ',
		for state,key in self.world_status.items():
			print state, key
		print ''

	def _ball_pos(self):
		if time.time()-self.it > 3:
			return True
		return False

	def _self_pos(self):
		return True

	def _enemy_pos(self):
		return True

	def _ally_pos(self):
		return True
	
	def _ally_stat(self):
		return True

	def _target_pos(self):
		return True

	def _have_ball(self):
		if time.time()-self.it > 6:
			return True
		return False

	def _ball_and_target_on_straight_line(self):
		if time.time()-self.it > 9:
			return True
		return False

	def _ball_in_kick_area(self):
		if time.time()-self.it > 12:
			return True
		return False

	def _ball_in_goal_area(self):
		return False

	def _ball_in_target(self):
		if time.time()-self.it > 15:
			return True
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

	def run(self, root):
		self.state._update()
		self.state.print_state()

		planner = Planner(self.state.world_status, root)
		plans = planner.process()
		for task in plans:
			print str(task.__class__.__name__)

		print 'operating task right now'
		for task in plans:
			process_task = task.operators()
			status = task.status(self.state.world_status)
			while status == Task.ACTIVE:
				process_task.next()
				self.state._update()
				status = task.status(self.state.world_status)
			else:
				if status == Task.FAILED:
					print 'replanning'
					break
		print 'finished'

