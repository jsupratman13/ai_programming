######################################
# @file csp.py 						 #
# @brief central strategy processor  #
######################################

import abc
import time,copy
from htn import Planner
import tools.geometry, tools.motionfuncagent
import math
from rcl import StandardMoveConfig

class Task(object):
	__metaclass__ = abc.ABCMeta	
	
	COMPLETE = 'COMPLETE'
	ACTIVE = 'ACTIVE'
	FAILED = 'FAILED'

	def __init__(self):
		filename = 'kid/actionconf/kid-strategy.cnf'
		self._move_conf = StandardMoveConfig(filename)

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
		
class TaskEnaction(object):
	def __init__(self):
		pass

	def _execute(self, agent, world_state, root_task):
		self._state = world_state
		self._state._update()
		self._planner = Planner(self._state.world_status, root_task)
		
		plans = self._planner.process()

		print "*-----------------------*"
		for task in plans: print str(task.__class__.__name__)
		print "*-----------------------*"
		print ''
		print 'operating task right now'
		for task in plans:
			print 'executing: %s' % str(task.__class__.__name__)
			try:
				process_task = task.operators(agent)
				status = task.status(self._state.world_status)
				while status == Task.ACTIVE:
					try:
						process_task.next()
						self._state._update()
						self._state.print_state()
						status = task.status(self._state.world_status)
					except StopIteration:
						status = Task.FAILED
				else:
					if status == Task.FAILED:
						print ''
						print 'replanning'
						print ''
						break
			finally:
				pass
		else:
			print ''
			print 'task successful'
			print ''
			return

class WorldState(object):
	def __init__(self, agent, filename):
		self._move_conf = StandardMoveConfig(filename)
		self.agent = agent
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
		self.old_status = copy.deepcopy(self.world_status)

	def _update(self):
		for state, key in self.world_status.items():
			new_key = self._world_rep[state]()
			self.world_status[state] = new_key

	def print_state(self):
		for state,key in self.world_status.items():
			if key != self.old_status[state]:
				break
		else:
			return None
		self.agent.brain.debug_log_ln("")
		self.agent.brain.debug_log_ln('current state: ')
		for state,key in self.world_status.items():
			self.old_status = copy.deepcopy(self.world_status)
			self.agent.brain.debug_log_ln(str(state)+" "+str(key))
		self.agent.brain.debug_log_ln("")

	def _ball_pos(self):
		ballarr_lc = self.agent.brain.get_estimated_object_pos_lc(self.agent.brain.BALL, self.agent.brain.AF_ANY)
		return bool(ballarr_lc)

	def _self_pos(self):
		return self.agent.brain.get_selfpos_confidence> 5

	def _enemy_pos(self):
		return False

	def _ally_pos(self):
		return False
	
	def _ally_stat(self):
		return False

	def _target_pos(self):
		return False

	def _have_ball(self):
		ballarr_lc = self.agent.brain.get_estimated_object_pos_lc(self.agent.brain.BALL, self.agent.brain.AF_ANY)
		if len(ballarr_lc) == 0:
			return False

		ball_dist_lc = tools.geometry.distance(ballarr_lc[0])
		ball_direction_deg = tools.geometry.direction_deg(ballarr_lc[0])
		direction_deg_threshold = 30 if self.world_status[WorldState.K_HAVE_BALL] else 20
		dist_threshold = 550 if self.world_status[WorldState.K_HAVE_BALL] else 450
		
		return ball_dist_lc <= dist_threshold and -direction_deg_threshold < ball_direction_deg < direction_deg_threshold

	def _ball_and_target_on_straight_line(self):
		ballarr_gl = self.agent.brain.get_estimated_object_pos_gl(self.agent.brain.BALL, self.agent.brain.AF_ANY)
		target_arrpos_gl = [(5000,0,0)]
		if ballarr_gl and target_arrpos_gl:
			approachpos_gl = tools.motionfuncagent.calc_approach_pos(ballarr_gl[0], target_arrpos_gl[0], 300)
			approachpos_lc = tools.geometry.coord_trans_global_to_local(self.agent.brain.get_selfpos(), approachpos_gl)
			target_deg = math.degrees(approachpos_lc[2])
			return -30 < target_deg < 30
		else:
			return False

	def _ball_in_kick_area(self):
		ballarr_lc = self.agent.brain.get_estimated_object_pos_lc(self.agent.brain.BALL, self.agent.brain.AF_ANY)
		if len(ballarr_lc) == 0:
			return False
		return tools.motionfuncagent.in_kickarea(self._move_conf.kick_area, ballarr_lc[0])

	def _ball_in_goal_area(self):
		return False

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
	def __init__(self, agent):
		filename = "kid/actionconf/kid-strategy.cnf"
		self._state = WorldState(agent, filename)
		self._task_enaction = TaskEnaction()
		self.agent = agent

	def execute(self, root):
		self.agent.brain.set_auto_localization_mode(1)
		self.agent.brain.set_use_white_lines(1)
		self.agent.brain.enable_auto_wakeup(1)
		self.agent.effector.set_pan_deg(0)

		self.agent.brain.debug_log_ln('Execute Accelite Strategy')
		while True:
#			try:
				self._state.print_state()
				self._task_enaction._execute(self.agent, self._state, root)

#			except FallError, e:
#				self.agent.brain.debug_log_ln(str(e))
#				self.agent.effector.cancel()
#				time.sleep(3)
#				self.agent.brain.wait_until_robot_standup()
#				self.agent.brain.wait_until_motion_finished()
#				time.sleep(1)

