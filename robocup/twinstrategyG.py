import rcl, math
import tools.geometry
import kid.motion, kid.goal, kid.role
import actionbase.search, kid.action.approach, actionbase.bodymotion, actionbase.bodymotionfunc
from tools.decorator import classproperty
from rcl import SoccerAgent, Action, WorldState


class Wingman(rcl.SoccerRole):
    def __init__(self, id_):
        conf_file = "kid/actionconf/kid-strategy.cnf"
        rcl.SoccerRole.__init__(self, id_, conf_file)
        self.__home_pos = None

    def _get_updated_home_pos_gl(self, world_state):
        another_players = [ap for ap in world_state.teammates if ap.arrpos_gl]
        for ap in another_players:
            pcs = self.__parse_common_string(ap.common_string)                      #TODO: UPDATE Stuff
            if len(pcs) != 2:
                continue
            role_name, goal_name = pcs
            if role_name == "Attacker":
                target_pos = ap.arrpos_gl[0]
                break

        if target_pos:
            if world_state.self_state.pos[0] > target_pos[0]:
                offset = 1000
            else:
                offset = -1000

            if tools.geometry.distance2points(world_state.self_state.pos, target_pos) > 900:
                home_pos = target_pos + offset
            else: 
                home_pos = world_state.self_state.pos

        else:
            home_pos = world_state.self_state.pos
        
        return home_pos

    def _get_updated_goal(self, world_state):
        if not world_state.permitted_intrusion_circle:
            world_state.permitted_intrusion_circle = True
        
        if not self.symbol_dict[rcl.WorldState.K_ON_TARGET_POS]:
            goal_t = goal.on_target_pos
        else:
            goal_t = goal.tracking_ball
        
        return goal_t

    def _get_updated_action_list(self, goal):
        return []


    def __parse_common_string(self, common_string):                         #TODO update stuff
        if common_string:
            tokens = common_string.split(' ')
        else:
            tokens = []
        
        if len(tokens) == 3 and tokens[0] == "Keeper":
            tokens = tokens[1:]

        elif len(tokens) != 2:
            tokens = []

        return tokens

class TwinStrategy(rcl.Strategy):
    def __init__(self):
        rcl.Strategy.__init__(self)

        #default strategic property
        self.__goal_cls = kid.goal.ball_in_goal
        self.__role_cls = kid.role.neutral
        self.__common_string = ""

        move_conf = self.__role_cls._move_conf
        
        self.__action_list = [
            actionbase.bodymotion.KickBallToTarget(move_conf.kick_area, move_conf.kick_wait),
            kid.action.approach.AdjustToKickpos(move_conf.kick_area),
            kid.action.approach.TurnAroundBallToTarget(move_conf.max_stride_y),
            kid.action.approach.ApproachBall(move_conf.mid_stride_x, move_conf.max_stride_y, move_conf.mid_stride_y),
            kid.action.approach.ApproachTargetPos((0, 0, 0), move_conf.mid_stride_x, move_conf.mid_stride_y),
            actionbase.search.FindLandmarksToLocalize(),
            actionbase.search.SearchCloseBall(),
            actionbase.search.TurnToSearchBall(),
            actionbase.search.TrackBall(),
            actionbase.bodymotion.Idling(),
        ]

    def __decide_role(self, world_state):
        if world_state.game_state != rcl.SoccerAgent.Brain.GAME_STATE_PLAYING or not self.symbol_dict[rcl.WorldState.K_KNOW_SELF_POS]:
            return kid.role.neutral
        
        ballarr_gl = world_state.get_estimated_object_pos_gl(rcl.SoccerAgent.Brain.BALL)
        another_players = [ap for ap in world_state.teammates if ap.arrpos_gl]
        
        keeper_clear_state = False
        contains_attacker = False
        for ap in another_players:
            pcs = self.__parse_common_string(ap.common_string)                      #TODO: UPDATE Stuff
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
###########Update


                    if ap.ball_arrpos_gl and tools.geometry.distance2points(ap.arrpos_gl[0], ap.ball_arrpos_gl[0]) > tools.geometry.distance2points(world_state.self_state.pos, ap.ball_arrpos_gl[0]):
                        role_cls = kid.role.attacker                   
                        break
###################
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
        self.__common_string = self.__role_cls.__class__.__name__ + " " + self.__goal_cls.__class__.__name__ ##TODO: Share Ball Position
#        self.__common_string = self.__role_cls.__class__.__name__ + " " + self.__goal_cls.__class__.__name__ + " " + str(world_state.get_estimated_object_pos_gl(rcl.SoccerAgent.Brain.BALL))

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

    def __parse_common_string(self, common_string):                         #TODO update stuff
        if common_string:
            tokens = common_string.split(' ')
        else:
            tokens = []
        
        if len(tokens) == 3 and tokens[0] == "Keeper":
            tokens = tokens[1:]

#        elif len(tokens) != 2 or len(tokens) !=3:
#	    tokens = []
        elif len(tokens) != 2:
            tokens = []

        return tokens


if __name__ == '__main__':
	player = rcl.SoccerPlayer(lambda: TwinStrategy())
	
	try:
		player.run()
	
	except (KeyboardInterrupt,SystemExit):
		player.terminate()

	except Exception, e:
		player.debug_log_ln("Exception: " + str(e))
		player.sleep(1)
		player.terminate()
		player.brain.sleep(1)
