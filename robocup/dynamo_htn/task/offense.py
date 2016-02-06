from csp import WorldState, Task
import time, math
import tools.geometry, tools.motionfuncagent, tools.algorithm
from rcl import StandardMoveConfig

class SearchBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self, agent):
		agent.effector.cancel()
		agent.brain.wait_until_status_updated()
		
		ballarr_lc = agent.brain.get_estimated_object_pos_lc(agent.brain.BALL, agent.brain.AF_ANY)
		if len(ballarr_lc) > 0:
			ballpos_lc = ballarr_lc[0]
			agent.effector.set_pan_deg(tools.geometry.direction_deg(ballpos_lc))

		prev_autolocalization = agent.brain.get_auto_localization_mode()
		agent.brain.set_auto_localization_mode(0)
		agent.brain.start_memorize_observation()
		num_found_landmarks = 0
		search_pan_angles = [135, 45, -45, 135]

		try:
			for pan in search_pan_angles:
				agent.brain.wait_until_status_updated()
				agent.effector.set_pan_deg(pan)
				if math.fabs(agent.brain.get_pan_deg() - pan > 60):
					agent.brain.sleep(1.0)
				else:
					agent.brain.sleep(0.8)
				num_found_landmarks += agent.brain.memorize_visible_observation()
				yield
		finally:
			if agent.brain.get_selfpos_confidence < 80 and num_found_landmarks > 1:
				agent.brain.use_memorized_observation_ntimes(5)
			agent.brain.set_auto_localization_mode(prev_autolocalization)

	def preconditions(self):
#		return [(WorldState.K_KNOW_SELF_POS, True)]
		return []

	def effects(self):
		return [(WorldState.K_KNOW_BALL_POS, True)]

class ApproachBall(Task):
	def __init__(self):
		Task.__init__(self)
		self.task_type = 'Primative'
		self.mid_stride_x = self._move_conf.mid_stride_x #18
		self.max_stride_y = self._move_conf.max_stride_y #26
		self.mid_stride_y = self._move_conf.mid_stride_y #20
		self.period = self._move_conf.period

	def operators(self, agent):
		while True:
			mid_x = self.mid_stride_x
			max_y = self.max_stride_y
			mid_y = self.mid_stride_y
			period = self.period

			tools.motionfuncagent.track_ball(agent, use_estimate = True)
			targetarr_gl = agent.brain.get_estimated_object_pos_gl(agent.brain.BALL, agent.brain.AF_ANY)
			if targetarr_gl:
				targetpos_lc = tools.geometry.coord_trans_global_to_local(agent.brain.get_selfpos(), targetarr_gl[0])
				target_dist_lc = tools.geometry.distance(targetpos_lc)
				target_direction_deg = tools.geometry.direction_deg(targetpos_lc)
	
				if target_dist_lc >= 700:
					plan_lc = tools.motionfuncagent.plan_path_with_obstacle_avoidance_lc(agent, targetpos_lc)
					tools.motionfuncagent.follow_path_normal_walk(agent, plan_lc, mid_x*5,period)
			
				else:
					target_x_lc, target_y_lc, target_th_lc = targetpos_lc
					if math.fabs(target_direction_deg) > 30:
						walk_th = tools.algorithm.clamp(target_direction_deg, 10,-10)
						agent.effector.walk(0,walk_th,0,period,0)
#						agent.effector.move(0,0,0,walk_th)

					elif math.fabs(target_y_lc) > 50:
						walk_y = tools.algorithm.clamp(target_y_lc*0.1, max_y, -max_y)
						walk_y = (walk_y/math.fabs(walk_y)) * max(math.fabs(walk_y), 4)
						agent.effector.walk(0,0,0,period,walk_y)
#						agent.effector.move(0,0,walk_y,0)

					else:
						walk_y = tools.algorithm.clamp(target_y_lc*0.1,mid_y, -mid_y)
						agent.effector.walk(0,0,mid_x,period,walk_y)
#						agent.effector.move(0,mid_x, walk_y, 0)
			yield

	def preconditions(self):
	        return [(WorldState.K_KNOW_BALL_POS, True), (WorldState.K_KNOW_SELF_POS, True)]

	def effects(self):
	        return [(WorldState.K_HAVE_BALL, True)]

class TurnAroundBallToTarget(Task):
	def __init__(self):
		Task.__init__(self)
		self.task_type = 'Primative'
		self.max_stride_y = self._move_conf.max_stride_y #26
		self.period = self._move_conf.period
		self.turn_dist = 450

	def operators(self, agent):
		period = self.period
		first = True
		base_ang = 10
		ang_comp = 0
		ka = 0.02
		kb = 0.05
		agent.effector.walk(2,0,0,period,0)
		while True:
			tools.motionfuncagent.track_ball(agent, use_estimate = True)
			x,y,t = agent.brain.get_selfpos()
			ballarr_gl = agent.brain.get_estimated_object_pos_gl(agent.Brain.BALL, agent.Brain.AF_ANY)
			target_arrpos_gl = [(5000,0,0)]
			if ballarr_gl and target_arrpos_gl:
				shootpos = tools.motionfuncagent.calc_approach_pos(ballarr_gl[0], target_arrpos_gl[0], self.turn_dist)
				dx, dy, dt = shootpos
				ball_lc_x, ball_lc_y, ball_lc_th = tools.geometry.coord_trans_global_to_local(agent.brain.get_selfpos(), ballarr_gl[0])
				
				if first:
					ccw = tools.geometry.normalize_rad(dt-t) > 0
					first = False
				dist = ball_lc_x

				if ccw: ang_comp_d = ((dist-self.turn_dist) * ka + ball_lc_y*kb)
				else: ang_comp_d = ((dist-self.turn_dist)*ka - ball_lc_y*kb)

				ang_comp = ang_comp*0.9 + ang_comp_d*0.1
				ang_comp = tools.algorithm.clamp(ang_comp, 4, -base_ang)
				if ang_comp > 0: stridey_abs = self.max_stride_y - ang_comp
				else: stridey_abs = self.max_stride_y + ang_comp

				if ccw:
					agent.effector.walk(0,base_ang+int(ang_comp), 0, period, -stridey_abs)
#					agent.effector.move(0,0,-stridey_abs, base_ang+int(ang_comp))
				else:
					agent.effector.walk(0,-(base_ang+int(ang_comp)), 0, period, stridey_abs)
#					agent.effector.move(0,0, stridey_abs, -(base_ang+int(ang_comp)))
			yield

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True)]

	def effects(self):
		return [(WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

class AdjustToKick(Task):
	def __init__(self):
		Task.__init__(self)
		self.task_type = 'Primative'
		self.kick_conf = self._move_conf.kick_area
		self.period = self._move_conf.period

	def operators(self, agent):
		period = self.period
		agent.effector.walk(2,0,0,period,0)
		agent.brain.sleep(0.2)

		ballarr_lc = agent.brain.get_estimated_object_pos_lc(agent.brain.BALL, agent.brain.AF_ANY)
		should_left_kick = ballarr_lc[0][1] > (self.kick_conf.kick_left_close + self.kick_conf.kick_right_close) / 2

		while True:
			tools.motionfuncagent.track_ball(agent, use_estimate = True)
			ballarr_gl = agent.brain.get_estimated_object_pos_gl(agent.brain.BALL, agent.brain.AF_ANY)
			if ballarr_gl:
				selfpos = agent.brain.get_selfpos()
				ballx_lc, bally_lc, ballth_lc = tools.geometry.coord_trans_global_to_local(selfpos, ballarr_gl[0])
				target_x = ballx_lc - (self.kick_conf.kick_forward + self.kick_conf.kick_near) / 2.0

				if bally_lc > self.kick_conf.kick_left_far:
					should_left_kick = True
				if bally_lc < self.kick_conf.kick_right_far:
					should_left_kick = False

				if should_left_kick:
					target_y = bally_lc - (self.kick_conf.kick_left_far + self.kick_conf.kick_left_close) / 2.0
				else:
					target_y = bally_lc - (self.kick_conf.kick_right_far + self.kick_conf.kick_right_clse) / 2.0

				target_x = tools.algorithm.clamp(target_x, 40, -40)
				target_y = tools.algorithm.clamp(target_y, 40, -40)
				targetarr_gl = [(5000,0,0)]
				target_deg = 0
				if targetarr_gl:
					approachpos_gl = tools.motionfuncagent.calc_approach_pos(ballarr_gl[0], targetarr_gl[0], 300)
					approachpos_lc = tools.geometry.coord_trans_global_to_local(selfpos, approachpos_gl)
					target_th = approachpos_lc[2]
					target_deg = tools.algorithm.clamp(math.degrees(target_th), 5, -5)
		
					target_x = (target_x / math.fabs(target_x) * max(math.fabs(target_x), 20))
					target_y = (target_y / math.fabs(target_y) * max(math.fabs(target_y), 20))
					
					if math.fabs(target_y) > 100: target_deg = 0
					
					agent.effector.accurate_walk(0, target_x, target_y, target_deg)
					agent.brain.sleep(0.3)

			yield

	def preconditions(self):
	        return [(WorldState.K_HAVE_BALL, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, True)]

class DribbleBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self, agent):
		pass

	def preconditions(self):
		return [(WorldState.K_HAVE_BALL, True),(WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
		return [(WorldState.K_BALL_IN_KICK_AREA, False)]

class KickBall(Task):
	def __init__(self):
		Task.__init__(self)
		self.task_type = 'Primative'
		self.kick_conf = self._move_conf.kick_area
		self.kick_wait = self._move_conf.kick_wait

	def operators(self, agent):
		while True:
			print 'low shot!'
#			agent.effector.play_sound("sound/shoot.wav")
			agent.effector.cancel()
			agent.brain.wait_until_status_updated()
			agent.brain.sleep(self.kick_wait)

			ballarr_lc = agent.brain.get_estimated_object_pos_lc(agent.brain.BALL, agent.brain.AF_ANY)
			if ballarr_lc:
				if tools.motionfuncagent.in_kickarea(self.kick_conf, ballarr_lc[0]):
					if ballarr_lc[0][1] > (self.kick_conf.kick_left_close + self.kick_conf.kick_right_close) / 2:
						agent.effector.play_motion(31)
					else:
						agent.effector.play_motion(30)

					agent.effector.cancel()
					agent.brain.wait_until_motion_finished()			
			yield

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]

class HighKickBall(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self, agent):
		while True:
			time.sleep(1)
			print 'high kicking ball!'
			yield

	def preconditions(self):
	        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True)]

	def effects(self):
	        return [(WorldState.K_BALL_IN_TARGET, True)]


