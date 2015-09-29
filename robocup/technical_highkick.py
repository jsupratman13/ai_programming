import rcl, math
import tools.geometry
import kid.motion, kid.goal, kid.role
import actionbase.search, kid.action.approach, actionbase.bodymotion, actionbase.bodymotionfunc
from tools.decorator import classproperty
from rcl import SoccerAgent, Action, WorldState

class SetSelfPos(Action):
    def do_process(self, player):
        player.set_auto_localization_mode(0)
        while True:
            player.set_selfpos((2000,0,0)) 
            yield
 
    def get_precondition(self):
        return []
    
    def get_deletion_list(self):
        return []
    
    def get_additional_list(self):
        return [(WorldState.K_KNOW_SELF_POS, True)]
    
    def apply_behavior(self, world_state):
        return world_state
        
    def get_cost(self, world_state):
        return 5

class Idling(Action):
    def do_process(self, player):
        player.motion.cancel()
        has_switch_paused = player.world.switch_state.state(SoccerAgent.Brain.SWITCH_3)
        try:
            while True:
                player.sleep(1)
                yield

        finally:
            player.set_selfpos((2000,0,0))
            if has_switch_paused and not player.world.switch_state.state(SoccerAgent.Brain.SWITCH_3) and player.world.game_state == SoccerAgent.Brain.GAME_STATE_PLAYING:
                player.set_selfpos((2000,0,0))
    def get_precondition(self):
        return []

    def get_deletion_list(self):
        return []

    def get_additional_list(self):
        return [(WorldState.K_IDLE, True)]

    def apply_behavior(self, world_state):
        return world_state

    def get_cost(self, world_state):
        return 0

class KickBallToTarget(Action):
    def __init__(self, kick_conf, kick_wait):
        Action.__init__(self)
        self.kick_conf = kick_conf
        self.kick_wait = kick_wait

    def do_process(self, player):
        while True:
            print "shoot!"
            player.motion.play_sound("sound/shoot.wav")
            player.motion.cancel()
            player.wait_until_status_updated()
            player.sleep(2.0 if player.world.switch_state.state(SoccerAgent.Brain.SWITCH_1) and self.kick_wait < 2.0 else self.kick_wait)
            x,y,th = player.get_selfpos()
            ballarr_lc = player.world.get_estimated_object_pos_lc(SoccerAgent.Brain.BALL, SoccerAgent.Brain.AF_ANY)
            if ballarr_lc:
                if actionbase.bodymotionfunc.in_kickarea(self.kick_conf, ballarr_lc[0]):
                    if ballarr_lc[0][1] > (self.kick_conf.kick_left_close + self.kick_conf.kick_right_close) / 2:
                        if x > 3000:
                            player.motion.high_left_kick()
                        else:
                            player.motion.left_kick()
                    else:
                        if x > 3000:
                            player.motion.high_right_kick()
                        else:
                            player.motion.right_kick()

                    player.motion.cancel()
                    player.wait_until_motion_finished()
            yield

    def apply_behavior(self, world_state):
        """
        target_arrpos_gl = self.get_target_arrpos_gl(world_state)
        if len(target_arrpos_gl) > 0:
            target_pos_lc = tools.geometry.coord_trans_global_to_local(world_state.self.pos, target_arrpos_gl[0])
            world_state.set_estimated_object_pos_lc(SoccerAgent.Brain.BALL, SoccerAgent.Brain.AF_ANY, target_pos_lc)
        """
        return world_state

    def get_cost(self, world_state):
        return 5

    def get_precondition(self):
        return [(WorldState.K_BALL_IN_KICK_AREA, True), (WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE, True), (WorldState.K_TARGET_IN_SHOT_RANGE, True)]

    def get_deletion_list(self):
        return []

    #TODO: delete symbol: K_BEHIND_BALL_DEFENSIVE_LINE
    def get_additional_list(self):
        return [(WorldState.K_BALL_IN_TARGET, True), (WorldState.K_BEHIND_BALL_DEFENSIVE_LINE, False)]

class Initial(rcl.SoccerRole):
    def __init__(self):
        conf_file = 'kid/actionconf/highkick-strategy.cnf'
        rcl.SoccerRole.__init__(self, 1, conf_file)
    
    def _get_updated_home_pos_gl(self, world_state):
        return None

    def _get_updated_action_list(self, goal):
        return []

    def _get_updated_goal(self, world_state):
        return kid.goal.ball_in_goal
     
class TC_Strategy(rcl.Strategy):
    def __init__(self):
        rcl.Strategy.__init__(self)

        #default strategic property
        self.__goal_cls = kid.goal.ball_in_goal
        self.__role_cls = Initial()
        self.__common_string = ""

        #TODO: Delete action_list
        move_conf = self.__role_cls._move_conf #TODO: Delete param
        
        self.__action_list = [
            KickBallToTarget(move_conf.kick_area, move_conf.kick_wait),
            kid.action.approach.AdjustToKickpos(move_conf.kick_area),
            kid.action.approach.TurnAroundBallToTarget(move_conf.max_stride_y),
            kid.action.approach.ApproachBall(move_conf.mid_stride_x, move_conf.max_stride_y, move_conf.mid_stride_y),
            kid.action.approach.ApproachTargetPos((0, 0, 0), move_conf.mid_stride_x, move_conf.mid_stride_y),
            SetSelfPos(),
            actionbase.search.SearchCloseBall(),
            actionbase.search.TurnToSearchBall(),
            actionbase.search.TrackBall(),
            Idling(),
        ]

    def __decide_role(self, world_state): #TODO: Implemented
        if world_state.game_state != rcl.SoccerAgent.Brain.GAME_STATE_PLAYING or not self.symbol_dict[rcl.WorldState.K_KNOW_SELF_POS]:
            return kid.role.neutral
        
        ballarr_gl = world_state.get_estimated_object_pos_gl(rcl.SoccerAgent.Brain.BALL)
        another_players = [ap for ap in world_state.teammates if ap.arrpos_gl]
        
        keeper_clear_state = False
        contains_attacker = False
        for ap in another_players:
            pcs = self.__parse_common_string(ap.common_string)
            if len(pcs) != 2:
                continue

            role_name, goal_name = pcs
            if role_name == "Keeper" and goal_name == "CLEAR":
                keeper_clear_state = True

            if role_name == "Attacker":
                contains_attacker = True

            if keeper_clear_state and contains_attacker:
                break
        
        if keeper_clear_state:
            return kid.role.defender

        if ballarr_gl:
            ball_dist = tools.geometry.distance2points(world_state.self_state.pos, ballarr_gl[0])

            if self.__role_cls == kid.role.attacker and ball_dist < 1000:
                role_cls = kid.role.attacker
            else:
                bx_gl, by_gl, bt_gl = ballarr_gl[0]
                ball_dist += 0 if world_state.self_state.pos[0] < bx_gl else world_state.self_state.pos[0] - bx_gl
                
                for ap in another_players:
                    pcs = self.__parse_common_string(ap.common_string)
                    if len(pcs) != 2:
                        continue

                    role_name, goal_name = pcs

                    if role_name == "Neutral":
                        continue
                    
                    offset_threshold_dist = 0
                    if role_name == "Attacker" and self.__role_cls != kid.role.attacker:
                        offset_threshold_dist = 1000

                    if ap.ball_arrpos_gl and tools.geometry.distance2points(ap.ball_arrpos_gl[0], ap.arrpos_gl[0]) < ball_dist + offset_threshold_dist:
                        role_cls = kid.role.defender
                        break

                else:
                    role_cls = kid.role.attacker

        else:
            role_cls = kid.role.defender if contains_attacker else kid.role.neutral

        return role_cls

    @property
    def goal_symbol_list(self):
        return self.__goal_symbol_list
    
    @property
    def symbol_dict(self):
        return self.__role_cls.symbol_dict

    @property
    def action_list(self):
        #return self.__role_cls.action_list
        return self.__action_list #DEBUG CODE!
    
    @property
    def common_string(self):
        return self.__common_string

    def update(self, world_state):
        old_goal_cls = self.__goal_cls
        old_role_cls = self.__role_cls
        assert not None in (self.__goal_cls, self.__role_cls), "Not Assigned strategic property"
        
        self.__role_cls = self.__decide_role(world_state)
        self.__role_cls.update(world_state)

        #[DANGER]: Set target_pos_gl
        l = [act for act in self.__action_list if act.__class__ == kid.action.approach.ApproachTargetPos]
        l[0]._ApproachTargetPos__target_pos_gl = self.__role_cls.home_pos_gl
        
        self.__goal_cls = self.__role_cls.goal
        self.__goal_symbol_list = self.__goal_cls.get_goal_state()
        self.__common_string = self.__role_cls.__class__.__name__ + " " + self.__goal_cls.__class__.__name__
            
        changed = False
        if old_goal_cls is not self.__goal_cls:
            print "goal changed: %s -> %s" % (old_goal_cls.__class__.__name__, self.__goal_cls.__class__.__name__)
            changed = True

        if old_role_cls is not self.__role_cls:
            print "role changed: %s -> %s" % (old_role_cls.__class__.__name__, self.__role_cls.__class__.__name__)
            changed = True

        return changed
    
    def create_field_properties(self):
        class HLKidFieldProperties(rcl.StaticFieldProperties):
            @classproperty
            def ENEMY_GOAL_POLE_GL(cls):
                return [(4500, 750, 0), (4500, -750, 0)]
            
            @classproperty
            def OUR_GOAL_POLE_GL(cls):
                return [(-4500, -750, 0), (-4500, 750, 0)]
            
            @classproperty
            def ENEMY_GOAL_GL(cls):
                return (5000, 0, 0)
            
            @classproperty
            def OUR_GOAL_GL(cls):
                return (-5000, 0, 0)
            
            @classproperty
            def NUM_PLAYERS(cls):
                return 6

        return HLKidFieldProperties()
    
    def create_motion(self, effector):
        return kid.motion.HR46Motion(effector)

    def __parse_common_string(self, common_string):
        if common_string:
            tokens = common_string.split(' ')
        else:
            tokens = []
        
        if len(tokens) == 3 and tokens[0] == "Keeper":
            tokens = tokens[1:]
        elif len(tokens) != 2:
            tokens = []

        return tokens


if __name__ == '__main__':
	agent = rcl.SoccerPlayer(lambda: TC_Strategy())
	
	try:
		agent.run()
	
	except (KeyboardInterrupt,SystemExit):
		agent.terminate()

	except Exception, e:
		agent.debug_log_ln("Exception: " + str(e))
		agent.sleep(1)
		agent.terminate()
		agent.brain.sleep(1)
