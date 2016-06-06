from csp import WorldState, Task
import math

class Idling(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self,agent):
		agent.effector.cancel()
		has_switch_paused = agent.brain.get_switch_state(agent.brain.SWITCH_3)
		agent.brain.dispose_global_position(own_half_only = True)
		try:
			while True:
				if has_switch_paused:
					agent.brain.forget_ball_memory()
				agent.brain.sleep(1)
				yield

		finally:
			if has_switch_paused and not agent.brain.get_switch_state(agent.brain.SWITCH_3) and agent.brain.get_game_state() == agent.brain.GAME_STATE_PLAYING:
				x,y,th = agent.brain.get_selfpos()
				if th > math.radians(50) and th < math.radians(130):
					print 'under side'
					agent.brain.set_selfpos((0, -3200, math.pi/2))
				elif th < math.radians(-50) and th < math.radians(-130):
					print 'top side'
					agent.brain.set_selfpos((0, 3200, -math.pi/2))
				else:
					print 'reset global position'
					agent.brain.set_selfpos(own_half_only = True)

	def preconditions(self):
		return []

	def effects(self):
		return [(WorldState.K_IDLE, True)]

class LandmarkToLocalize(Task):
	def __init__(self):
		self.task_type = 'Primative'

	def operators(self):
		init_pan_deg = agent.brain.get_pan_deg()
		agent.effector.cancel()
		agent.brain.wait_until_status_updated()

		prev_autolocalization = agent.brain.get_auto_localization_mode()
		if agent.brain.get_game_state() == agent.brain.GAME_STATE_SET or agent.brain.get_game_state() == agent.brain.GAME_STATE_READY:
			agent.brain.dispose_global_position(own_half_only = True)
		else:
			agent.brain.dispose_global_position(own_half_only = False)

		agent.brain.start_memorize_observation()
		search_pan_angles = [-135, -70, 0, 70, 135]
		num_found_landmarks = 0

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
			agent.brain.use_memorized_observation_ntimes(10,500,20,95)
			agent.brain.set_auto_localization_mode(prev_autolocalization)
			agent.effector.set_pan_deg(init_pan_deg)
			agent.brain.forget_ball_memory()
			agent.brain.wait_until_status_updated()
			agent.brain.sleep(3)

	def preconditions(self):
#		return [(WorldState.K_KNOW_SELF_POS, False)]
		return []

	def effects(self):
	        return [(WorldState.K_KNOW_SELF_POS, True)]

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


