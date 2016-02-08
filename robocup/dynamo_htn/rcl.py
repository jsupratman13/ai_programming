# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 encoding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:

##########################################################################
 # Copyright (c) 2013 Daiki Maekawa and CIT Brains All Rights Reserved. #
 #                                                                      #
 # @file rcl.py                                                         #
 # @brief Robot Core Library(RCL)                                       #
 # @author Daiki Maekawa                                                #
 # @date 2013-10-21                                                     #
##########################################################################

import SocketServer
import socket
import sys
import time
import copy
import pygame
import platform
import abc
import threading
import tools.geometry
import math
import actionbase.approachfunc

if platform.system() == 'Linux':
    from espeak import espeak

import sys
sys.path.append(".")
import os
os.chdir(".")
import env

_HLCOLOR_BALL, _HLCOLOR_YELLOW, _HLCOLOR_BLUE, _HLCOLOR_BLACK, _HLCOLOR_CYAN, _HLCOLOR_MAGENTA, _HLCOLOR_ANY = range(7)
_HLOBJECT_BALL, _HLOBJECT_GOAL, _HLOBJECT_GOAL_POLE, _HLOBJECT_ROBOT, _HLOBJECT_MYSELF, _HLOBJECT_LAST_VISIBLE_BALL = range(6)

def convert_pos_to_dlist(pos2dlist):
    ret = []
    for i in range(pos2dlist.size()):
        ret.append((pos2dlist[i].x, pos2dlist[i].y, pos2dlist[i].th))
    return ret

def convert_pos_to_dcflist(pos2dcflist):
    ret = []
    for i in range(pos2dcflist.size()):
        ret.append((pos2dcflist[i].pos.x, pos2dcflist[i].pos.y, pos2dcflist[i].pos.th, pos2dcflist[i].cf))
    return ret

def convert_to_pos2d(pos):
    x, y, th = pos
    ret = env.Pos2D(x, y, th)
    return ret;

def convert_to_hltype(type, affi, hlour_color):
    if type is SoccerAgent.Brain.BALL:
        assert(affi is SoccerAgent.Brain.AF_ANY)
        hlcolor = _HLCOLOR_BALL
        hlobject = _HLOBJECT_BALL
    elif type is SoccerAgent.Brain.LAST_VISIBLE_BALL:
        assert(affi is SoccerAgent.Brain.AF_ANY)
        hlcolor = _HLCOLOR_BALL
        hlobject = _HLOBJECT_LAST_VISIBLE_BALL
    elif type is SoccerAgent.Brain.GOAL_POLE:
        assert(affi is SoccerAgent.Brain.AF_ANY)
        hlcolor = _HLCOLOR_YELLOW
        hlobject = _HLOBJECT_GOAL_POLE
    elif type is SoccerAgent.Brain.ROBOT:
        if affi is SoccerAgent.Brain.AF_ENEMY:
            hlcolor = _HLCOLOR_CYAN if hlour_color is _HLCOLOR_MAGENTA else _HLCOLOR_MAGENTA
        elif affi is SoccerAgent.Brain.AF_OUR:
            hlcolor = _HLCOLOR_MAGENTA if hlour_color is _HLCOLOR_MAGENTA else _HLCOLOR_CYAN
        elif affi is SoccerAgent.Brain.AF_ANY:
            hlcolor = _HLCOLOR_BLACK
        else:
            assert(False)
        hlobject = _HLOBJECT_ROBOT
    else:
        assert(False)

    return hlobject, hlcolor

class TerminateHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        global ghajime
        print >> sys.stderr, "request terminate"
        ghajime.hajime_set_suspended(True)
        ghajime.hajime_cancel()
        os.system("kill -9 " + str(os.getpid()))

class TerminateServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Terminate Server listening\n"
        self.server = SocketServer.TCPServer(('0.0.0.0', 20122), TerminateHandler)
        self.server.serve_forever()

    def terminate(self):
        self.server.shutdown()
        self.join()
 
class CommandQueue(threading.Thread):
    def __init__(self, hajime, interval = 0.1):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.set_command_interval(interval)
        self.__walkargs = None
        self.__panargs = None
        self.__tiltargs = None
        self.__walklock = threading.Lock()
        self.__panlock = threading.Lock()
        self.__tiltlock = threading.Lock()
        self.request_terminate = False
        self.hajime = hajime
    
    def set_command_interval(self, interval):
        self.__cmd_interval = interval
    
    def clear_queue(self):
        self.put_walk(None)
    
    def put_walk(self, args):
        self.__walklock.acquire()
        self.__walkargs = args
        self.__walklock.release()

    def put_pan(self, args):
        self.__panlock.acquire()
        self.__panargs = args
        self.__panlock.release()

    def put_tilt(self, args):
        self.__tiltlock.acquire()
        self.__tiltargs = args
        self.__tiltlock.release()

    def terminate(self):
        self.request_terminate = True
        self.join()

    def run(self):
        while not self.request_terminate:
            env.sleepSec(0.05)
            # post walk command
            self.__walklock.acquire()
            walkargs = self.__walkargs
            self.__walkargs = None
            self.__walklock.release()
            if walkargs != None:
                self.hajime.hajime_walk(*walkargs)
                env.sleepSec(self.__cmd_interval)

            # post pan command
            self.__panlock.acquire()
            panargs = self.__panargs
            self.__panargs = None
            self.__panlock.release()
            if panargs != None:
                self.hajime.hajime_pan(*panargs)
                env.sleepSec(self.__cmd_interval)

            # post tilt command
            self.__tiltlock.acquire()
            tiltargs = self.__tiltargs
            self.__tiltargs = None
            self.__tiltlock.release()
            if tiltargs != None:
                self.hajime.hajime_tilt(*tiltargs)
                env.sleepSec(self.__cmd_interval)
        
        print "cmdqueue terminated\n"

class FallError(Exception):
    def __str__(self):
        return self.__class__.__name__

class GameStateChanged(Exception):
    def __init__(self, state):
        self.state = state
    def __str__(self):
        return self.__class__.__name__ + ": " + self.ToStr(self.state)
    def ToStr(self, state):
        if state == SoccerAgent.Brain.GAME_STATE_INITIAL:
            return 'STATE_INITIAL'
        elif state == SoccerAgent.Brain.GAME_STATE_READY:
            return 'STATE_READY'
        elif state == SoccerAgent.Brain.GAME_STATE_SET:
            return 'STATE_SET'
        elif state == SoccerAgent.Brain.GAME_STATE_PLAYING:
            return 'STATE_PLAYING'
        elif state == SoccerAgent.Brain.GAME_STATE_FINISHED:
            return 'STATE_FINISHED'
        elif state == SoccerAgent.Brain.GAME_STATE_EXT_SWITCH_PAUSED:
            return 'STATE_EXT_SWITCH_PAUSED'
        return ''

class ActionCancelSignal(Exception):
    def __str__(self):
        return self.__class__.__name__

class FormationParam(object):
    def __init__(self):
        self.role = None
        self.x_pos = None
        self.y_pos = None
        self.x_attr = None
        self.y_attr = None
        self.behind_ball = None
        self.x_min = None
        self.x_max = None

class Formation(object):
    def __init__(self, file_system, conf_file):
        role_l  = file_system.read_para("role", "", conf_file, 'r')
        x_pos_l = file_system.read_para("x_pos", "", conf_file, 'r')
        y_pos_l = file_system.read_para("y_pos", "", conf_file, 'r')
        x_attr_l = file_system.read_para("x_attr", "", conf_file, 'r')
        y_attr_l = file_system.read_para("y_attr", "", conf_file, 'r')
        behind_ball_l = file_system.read_para("behind_ball", "", conf_file, 'r')
        x_min_l = file_system.read_para("x_min", "", conf_file, 'r')
        x_max_l = file_system.read_para("x_max", "", conf_file, 'r')
        
        assert(len(role_l) == len(x_pos_l) == len(y_pos_l) == len(x_attr_l) == 
                len(y_attr_l) == len(behind_ball_l) == len(x_min_l) == len(x_max_l))
        
        self.__player_list = []
        for role, x_pos, y_pos, x_attr, y_attr, behind_ball, x_min, x_max in zip(role_l, x_pos_l, y_pos_l, 
                                                                                  x_attr_l, y_attr_l, behind_ball_l, x_min_l, x_max_l):
            params = FormationParam()
            params.role  = role
            params.x_pos = float(x_pos)
            params.y_pos = float(y_pos)
            params.x_attr = float(x_attr)
            params.y_attr = float(y_attr)
            params.behind_ball = bool(behind_ball)
            params.x_min = float(x_min)
            params.x_max = float(x_max)
            self.__player_list.append(params)
    
    def get_home_pos_gl(self, role, ballarr_gl): #TODO: Implemented
        role_name = role.__class__.__name__
        for params in self.__player_list:
            if role_name == params.role:
                player_pos_x = params.x_pos
                player_pos_y = params.y_pos
                if len(ballarr_gl) > 0:
                    player_pos_x += ballarr_gl[0][0] * params.x_attr
                    player_pos_y += ballarr_gl[0][1] * params.y_attr

                return player_pos_x, player_pos_y, 0
            
        assert False, "[%s] not exist" % role_name

class BehaviorGenerator(object):
    def __init__(self):
        self.__action_list = None
        self.__active_action = None

    def __plan(self, world_state, init_symbol_dict, goal_state_list):
        diff_set = set(goal_state_list) - set(init_symbol_dict.items())
        
        if len(diff_set) == 0:
            return []

        subgoal = diff_set.pop()
        plan_list = []
        for realize in [act for act in self.__action_list if subgoal in act.get_deletion_list() + act.get_additional_list()]:
            plan = self.__plan(world_state, init_symbol_dict, realize.get_precondition())
            if plan is None: 
                continue
            else: 
                plan += [realize]
            
            intermediate_symbol_dict = copy.deepcopy(init_symbol_dict)
            for act in plan: 
                for key, value in act.get_deletion_list() + act.get_additional_list():
                    intermediate_symbol_dict[key] = value
                #intermediate_state = act.apply_behavior(intermediate_state) #TODO Implemented

            assert(intermediate_symbol_dict is not None)
            sub_plan = self.__plan(world_state, intermediate_symbol_dict, goal_state_list)
            if sub_plan is None: 
                continue
            else: 
                plan_list += [plan + sub_plan]
        
        opt_plan = None
        if len(plan_list) >= 2:
            min_cost = 1000
            for plan in plan_list:
                cost = 0
                #world_symbol_dict = copy.deepcopy(init_symbol_dict)
                for act in plan:
                    #world_state = act.apply_behavior(world_state) #TODO: Implemented
                    #assert(world_symbol_dict is not None)
                    cost += act.get_cost(world_state)
                if cost <= min_cost:
                    min_cost = cost
                    opt_plan = plan
        
        elif len(plan_list) == 1: 
            opt_plan = plan_list[0]

        return opt_plan

    def process(self, player, goal_state_list, action_list):
        self.__action_list = action_list
        player.debug_log_ln("action_list = " + str(self.__action_list))
        player.debug_log_ln("goal_state_list = " + str(goal_state_list))
        symbol_dict = player.symbol_dict
        plan = self.__plan(player.world, symbol_dict, goal_state_list)

        if plan is None:
            assert False, "plan does not exist"

        player.debug_log_ln("/*----------------- plan -----------------*/")
        for p in plan: player.debug_log_ln(" * " + str(p.__class__.__name__))
        player.debug_log_ln("/*----------------------------------------*/")

        for act in plan:
            self.__active_action = act
            player.debug_log_ln("%s.process()" % self.__active_action.__class__.__name__)
            try:
                process_gen = act.do_process(player)
                status = act.get_state(symbol_dict)
                while status == Action.ACTIVE:
                    try:
                        process_gen.next() 
                        player.wait_until_status_updated()
                        symbol_dict = player.symbol_dict
                        status = act.get_state(symbol_dict)
                    except StopIteration: 
                        status = Action.FAILED
                else:
                    if status == Action.FAILED:
                        player.debug_log_ln("replanning")
                        break

            except ActionCancelSignal, e:
                player.debug_log_ln(str(e))
                break
            finally:
                self.__active_action = None

        else:
            player.debug_log_ln("goal success")
            return
    
    """
    def should_cancel_action(self, world_state):
        if self.__active_action is None:
            return False
        
        return self.__active_action.get_state(world_state) == Action.FAILED
    """

class StandardMoveConfig(object):
    class KickArea(object):
        def __init__(self, conf_file):
            file_system = FileSystem()
            params = file_system.read_para("kick_front", "120,220", conf_file)
            self.__kick_near = int(params[0])
            self.__kick_forward = int(params[1])

            params = file_system.read_para("kick_left", "30,100", conf_file)
            self.__kick_left_close = int(params[0])
            self.__kick_left_far = int(params[1])

            params = file_system.read_para("kick_right","-30,-100", conf_file)
            self.__kick_right_close = int(params[0])
            self.__kick_right_far = int(params[1])
        
        @property
        def kick_near(self):
            return self.__kick_near

        @property
        def kick_forward(self):
            return self.__kick_forward

        @property
        def kick_left_close(self):
            return self.__kick_left_close

        @property
        def kick_left_far(self):
            return self.__kick_left_far

        @property
        def kick_right_close(self):
            return self.__kick_right_close

        @property
        def kick_right_far(self):
            return self.__kick_right_far

    def __init__(self, conf_file):
        file_system = FileSystem()
        
        self.__kick_area = StandardMoveConfig.KickArea(conf_file)
        self.__max_stride_x = int(file_system.read_para("max_stride_x", "20", conf_file))
        self.__max_stride_y = int(file_system.read_para("max_stride_y", "26", conf_file))
        self.__mid_stride_x = int(file_system.read_para("mid_stride_x", "18", conf_file))
        self.__mid_stride_y = int(file_system.read_para("mid_stride_y", "20", conf_file))
        self.__kick_wait = float(file_system.read_para("kick_wait", "0.5", conf_file))
        self.__period = int(file_system.read_para("period", "12", conf_file))
    
    @property
    def kick_area(self):
        return self.__kick_area

    @property
    def max_stride_x(self):
        return self.__max_stride_x

    @property
    def max_stride_y(self):
        return self.__max_stride_y

    @property
    def mid_stride_x(self):
        return self.__mid_stride_x

    @property
    def mid_stride_y(self):
        return self.__mid_stride_y
    
    @property
    def kick_wait(self):
        return self.__kick_wait

    @property
    def period(self):
        return self.__period

class Motion(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self, effector):
        pass
    
    @abc.abstractmethod
    def move(self, num, x, y, th):
        pass
    
    #TODO:Delete
    def accurate_walk(self, num, x, y, th):
        pass

    @abc.abstractmethod
    def cancel(self):
        pass

    @abc.abstractmethod
    def right_kick(self):
        pass
    
    @abc.abstractmethod
    def left_kick(self):
        pass

    @abc.abstractmethod
    def high_right_kick(self):
        pass

    @abc.abstractmethod
    def high_left_kick(self):
        pass

    @abc.abstractmethod
    def turn_neck(self, angle_deg):
        pass

    @abc.abstractmethod
    def play_sound(self, str):
        pass

class SoccerRole(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, id_, file_name):
        self.__id = id_

        self.__update_func_dict = {
            WorldState.K_BEHIND_BALL_DEFENSIVE_LINE: self._behind_ball_defensive_line,
            WorldState.K_KNOW_BALL_POS: self._know_ball_pos,
            WorldState.K_KNOW_SELF_POS: self._know_self_pos,
            WorldState.K_COME_BALL: self._come_ball,
            WorldState.K_TARGET_IN_SHOT_RANGE: self._target_in_shot_range,
            WorldState.K_ON_TARGET_POS: self._on_target_pos,
            WorldState.K_BALL_AND_TARGET_ON_STRAIGHT_LINE: self._ball_and_target_on_straight_line,
            WorldState.K_HAVE_BALL: self._have_ball,
            WorldState.K_BALL_IN_TARGET: self._ball_in_target,
            WorldState.K_BALL_IN_KICK_AREA: self._ball_in_kick_area,
            WorldState.K_ENEMY_WITHIN_RANGE: self._enemy_within_range,
            WorldState.K_IDLE: lambda ws : False,
            WorldState.K_TRACKING_BALL: lambda ws : False
        }

        self.__update_func_dict.update(self._add_symbols())
        self.__symbol_dict = {key: False for key, func in self.__update_func_dict.items()} 
        self._move_conf = StandardMoveConfig(file_name)
        self.__home_pos_gl = None

    @property
    def id(self):
        return self.__id
    
    def update(self, world_state):
        self.__home_pos_gl = self._get_updated_home_pos_gl(world_state)
        
        for key, value in self.__symbol_dict.items():
            new_value = self.__update_func_dict[key](world_state)
            assert type(new_value) is bool, "unknown type: %s, %s" % (key, self.__class__.__name__)
            self.__symbol_dict[key] = new_value
        
        self.__goal = self._get_updated_goal(world_state)
        #self.__action_list = self._get_updated_action_list(self.__goal) #TODO: Implemented update function
    
    @abc.abstractmethod
    def _get_updated_home_pos_gl(self, world_state):
        pass

    @abc.abstractmethod
    def _get_updated_goal(self, world_state):
        pass

    @abc.abstractmethod
    def _get_updated_action_list(self, goal):
        pass
    
    @property
    def home_pos_gl(self):
        return self.__home_pos_gl

    @property
    def goal(self):
        return self.__goal

    @property
    def action_list(self):
        return self.__action_list[:]
    
    @property
    def symbol_dict(self):
        return self.__symbol_dict
    
    def _add_symbols(self):
        return {}

    def _know_ball_pos(self, world_state):
        ballarr_lc = world_state.get_estimated_object_pos_lc(SoccerAgent.Brain.BALL)
        return bool(ballarr_lc)

    def _know_self_pos(self, world_state):
        return world_state.self_state.pos_confidence > 5
    
    def _behind_ball_defensive_line(self, world_state):
        return False

    def _come_ball(self, world_state):
        return False

    def _target_in_shot_range(self, world_state):
        if world_state.switch_state.state(SoccerAgent.Brain.SWITCH_2):
            return True
        
        ballarr_gl = world_state.get_estimated_object_pos_gl(SoccerAgent.Brain.BALL)
        if ballarr_gl:
            #TODO: Decide goal position
            distance = tools.geometry.distance2points((5000, 0, 0), ballarr_gl[0])
            if distance < 4000:
                return True

        return False
    
    def _on_target_pos(self, world_state):
        if self.home_pos_gl:
            diff = tools.geometry.distance2points(world_state.self_state.pos, self.home_pos_gl)
            target_pos_lc = tools.geometry.coord_trans_global_to_local(world_state.self_state.pos, self.home_pos_gl)
            if diff < 700 and -20 < math.degrees(target_pos_lc[2]) < 20:
                return True

        return False
    
    def _ball_and_target_on_straight_line(self, world_state):
        ballarr_gl = world_state.get_estimated_object_pos_gl(SoccerAgent.Brain.BALL)
        #TODO: Implemented: set position
        target_arrpos_gl = [(5000, 0, 0)]
        if ballarr_gl and target_arrpos_gl:
            approachpos_gl = actionbase.approachfunc.calc_approach_pos(ballarr_gl[0], target_arrpos_gl[0], 300)
            approachpos_lc = tools.geometry.coord_trans_global_to_local(world_state.self_state.pos, approachpos_gl)
            target_deg = math.degrees(approachpos_lc[2])
            return -30 < target_deg < 30
        else:
            return False
    
    def _have_ball(self, world_state):
        ballarr_lc = world_state.get_estimated_object_pos_lc(SoccerAgent.Brain.BALL)
        
        if len(ballarr_lc) == 0:
            return False
        
        ball_dist_lc = tools.geometry.distance(ballarr_lc[0])
        ball_direction_deg = tools.geometry.direction_deg(ballarr_lc[0])
        direction_deg_threshold = 30 if self.__symbol_dict[WorldState.K_HAVE_BALL] else 20
        dist_threshold = 550 if self.__symbol_dict[WorldState.K_HAVE_BALL] else 450
        
        #return ball_dist_lc <= dist_threshold and -direction_deg_threshold < ball_direction_deg < direction_deg_threshold and math.fabs(ballarr_lc[0][1]) < 50
        return ball_dist_lc <= dist_threshold and -direction_deg_threshold < ball_direction_deg < direction_deg_threshold

    def _ball_in_target(self, world_state):
        #TODO: Implemented
        return False
    
    def _ball_in_kick_area(self, world_state):
        ballarr_lc = world_state.get_estimated_object_pos_lc(SoccerAgent.Brain.BALL)
        if len(ballarr_lc) == 0:
            return False

        return actionbase.bodymotionfunc.in_kickarea(self._move_conf.kick_area, ballarr_lc[0])

    def _enemy_within_range(self, world_state):
        enemyarr_lc = world_state.get_estimated_object_pos_lc(SoccerAgent.Brain.ROBOT, SoccerAgent.Brain.AF_ANY)
        for pos in enemyarr_lc:
            if 10 < tools.geometry.distance(pos) < 850:
                return True
        else:
            return False
    
    def _get_opt_plan(self, init_symbol_dict, goal_state_list):
        diff_set = set(goal_state_list) - set(init_symbol_dict.items())
        
        if len(diff_set) == 0:
            return []

        subgoal = diff_set.pop()
        plan_list = []
        for realize in [act for act in self.__action_list if subgoal in act.get_deletion_list() + act.get_additional_list()]:
            plan = self.plan(init_symbol_dict, realize.get_precondition())
            if plan is None: 
                continue
            else: 
                plan += [realize]
            
            intermediate_symbol_dict = copy.deepcopy(init_symbol_dict)
            for act in plan: 
                for key, value in act.get_deletion_list() + act.get_additional_list():
                    intermediate_symbol_dict[key] = value
                #intermediate_state = act.apply_behavior(intermediate_state) #TODO Implemented

            assert(intermediate_symbol_dict is not None)
            sub_plan = self.plan(intermediate_symbol_dict, goal_state_list)
            if sub_plan is None: 
                continue
            else: 
                plan_list += [plan + sub_plan]
        
        opt_plan = None
        if len(plan_list) >= 2:
            min_cost = 1000
            for plan in plan_list:
                cost = 0
                world_symbol = copy.deepcopy(init_symbol_dict)
                for act in plan:
                    #world_state = act.apply_behavior(world_state) #TODO: Implemented
                    assert(world_symbol_dict is not None)
                    cost += act.get_cost(world_symbol_dict)

                if cost <= min_cost:
                    min_cost = cost
                    opt_plan = plan
        
        elif len(plan_list) == 1: 
            opt_plan = plan_list[0]

        return opt_plan

class ActionGoal(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, id_):
        self.__id = id_
    
    @property
    def id(self):
        return self.__id

    @abc.abstractmethod
    def get_goal_state(self):
        pass

class Action(object):
    __metaclass__ = abc.ABCMeta
    
    COMPLETED = 0
    FAILED    = -1
    ACTIVE    = -2
    
    @abc.abstractmethod
    def do_process(self, player): pass

    @abc.abstractmethod
    def get_precondition(self): pass
    
    @abc.abstractmethod
    def get_deletion_list(self): pass
    
    @abc.abstractmethod
    def get_additional_list(self): pass
    
    @abc.abstractmethod
    def apply_behavior(self, world_state): pass
    
    @abc.abstractmethod
    def get_cost(self, world_state): pass
    
    def get_state(self, world_symbol_dict):
        symbol_list = world_symbol_dict.items()
        add_list = self.get_additional_list()
        precondition_list = self.get_precondition()
        if len(precondition_list) > 0:
            for precondition in precondition_list:
                if not precondition in symbol_list:
                    return Action.FAILED

        for add in add_list:
            if not add in symbol_list:
                return Action.ACTIVE
        else:
            return Action.COMPLETED

class Tactics(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_action_list(self):
        pass
    
class FileSystem(object):
    def read_para(self, name, init_value, file_name, mode = 'a+'):
        try:
            with open(file_name, mode) as f:
                for line in f:
                    rect = line.split(' ')
                    if len(rect) == 2:
                        read_name, read_value = rect
                        if read_name == name:
                            read_value = read_value.rstrip()
                            params = read_value.split(',')
                            break
                else:
                    f.write(name + ' ' + init_value + '\n')
                    params = init_value.split(',')
            
            return params[0] if len(params) == 1 else params
        except IOError:
            print >> sys.stderr, 'cannot open "%s"' % file_name
            sys.exit(1)

class SoccerAgent(object):
    __metaclass__ = abc.ABCMeta

    class Effector(object):
        def __init__(self, hajime):
            self.hajime = hajime
            self.cmdqueue = CommandQueue(self.hajime)
            self.cmdqueue.start()
        
        def terminate(self):
            self.cancel()
            self.cmdqueue.terminate()

        def walk(self, num, angle, width, period, side):
            self.cmdqueue.put_walk((int(num), int(angle), int(width), int(period), int(side)))

        def accurate_walk(self, num, x, y, th):
            self.hajime.hajime_accurate_walk(int(num), float(x), float(y), float(th))
        
        def accurate_one_step(self, x, y, th):
            self.hajime.hajime_accurate_one_step(float(x), float(y), float(th))
            
        def play_motion(self, no, num = 1):
            self.cmdqueue.clear_queue()
            self.hajime.hajime_motion(no, num)
        
        def play_variable_motion(self, no, shift):
            self.hajime.hajime_variable_motion(int(no), int(round(shift)))
        
        def set_pan_deg(self, angle, period = 1, force = True):
            if force:
                self.hajime.hajime_pan(int(angle), period)
            else:
                self.cmdqueue.put_pan((int(angle), period))

        def cancel(self):
            self.cmdqueue.clear_queue()
            self.hajime.hajime_cancel()
        
        def set_servo_power(self,num):
            self.hajime.hajime_power(num)
    
        def play_sound(self, str):
            return pygame.mixer.Sound(str).play()
        
        def speak(self, str):
            if platform.system() == 'Linux':
                return espeak.synth(str)
        
        DIVE_CENTER = 5
        DIVE_RIGHT = 10
        DIVE_LEFT = 11
        KICK_R = 30 
        KICK_L = 31 
    
    class Brain(object):
        def __init__(self, hpl):
            self.hpl = hpl
            self.__game_state = self.GAME_STATE_FINISHED
            self.__use_gamecontroller = False
            self.__autolocalizationmode = 0
            self.__prev_posture = self.get_robot_posture()
            self.__last_visible_ball_time = None
        
        def get_time(self):
            return env.getTime()

        def detect_fall_error(self):
            posture = self.get_robot_posture()
            if self.hpl.getAutoWakeup() == 1 and posture != SoccerAgent.Brain.POSTURE_STAND and self.__prev_posture != posture:
                self.__prev_posture = posture
                raise FallError()
            self.__prev_posture = posture  
        
        def get_ball_velo(self):
            v = self.hpl.getballvelo()
            return (v[0], v[1])
        
        def get_estimated_object_pos_lc(self, type, affi):
            if type is self.BALL:
                assert(affi is self.AF_ANY)
                ballarr_lc = convert_pos_to_dlist(self.hpl.getaveragedballpos(2))
                if ballarr_lc:
                    return ballarr_lc
                
                ballarr_cf_gl = convert_pos_to_dcflist(self.hpl.getestimatedballpos(0.00005, 4))
                selfpos = self.get_selfpos()
        #        if ballarr_cf_gl[0][3] > 0.01 and tools.geometry.distance2points(ballarr_cf_gl[0][:3], selfpos) >= 720:
        #           ballpos_lc = tools.geometry.coord_trans_global_to_local(selfpos, ballarr_cf_gl[0][:3])
        #            return [ballpos_lc]
                
                return []

            hlobject, hlcolor = convert_to_hltype(type, affi, self.hpl.envConfig.OurColor)
            return convert_pos_to_dlist(self.hpl.getlocalpos(hlobject, hlcolor))

        def get_estimated_object_pos_gl(self, type, affi):
            objectarr_lc = self.get_estimated_object_pos_lc(type, affi)
            objectarr_gl = []
            if len(objectarr_lc) > 0:
                objectarr_gl.append(tools.geometry.coord_trans_local_to_global(self.get_selfpos(), objectarr_lc[0]))
        
            return objectarr_gl
 
        def forget_ball_memory(self):
            return self.hpl.forgetballmemory()

        def get_robot_posture(self):
            return self.hpl.getrobotposture()

        def get_pan_deg(self):
            return self.hpl.getpanangle()

        def get_tilt_deg(self):
            return self.hpl.gettiltangle()
        
        def get_switch_state(self, switchno , switchid = 0):
            return self.hpl.getswitch(switchno , switchid)
        
        def get_selfpos(self):
            return convert_pos_to_dlist(self.hpl.getglobalpos(_HLOBJECT_MYSELF, _HLCOLOR_ANY))[0]

        def get_selfpos_confidence(self):
            return self.hpl.getselfposconfidence_entropy()

        def get_common_pos_gl(self, id, type, affi):
            hlobject, hlcolor = convert_to_hltype(type, affi, self.hpl.envConfig.OurColor)
            return convert_pos_to_dcflist(self.hpl.getcommonglobalpos(id, hlobject, hlcolor))

        def get_kickoff_state(self):
            return self.hpl.getkickoffstate()

        def detect_game_state_change(self):
            state = self.get_game_state()
            if self.__use_gamecontroller and self.__game_state != state:
                self.__game_state = state
                raise GameStateChanged(state)
        
        def set_common_string(self, common_string):
            global SELF_ID
            return self.hpl.setcommonstring(SELF_ID, common_string)
        
        def get_common_string(self, id):
            return self.hpl.getcommonstring(id)

        def set_send_common_info(self, enable):
            if enable:
                self.hpl.setsendcommoninfo(1)
            else:
                self.hpl.setsendcommoninfo(0)
        
        def set_use_gamecontroller(self, use):
            self.__use_gamecontroller = use
            if use:
                self.hpl.setusegamecontroller(1)
            else:
                self.hpl.setusegamecontroller(0)

        def get_game_state(self):
            return self.hpl.getgamestate()
        
        def overwrite_game_state(self, state):
            self.__state = state
            return self.hpl.overwriteGameState(state)
    
        def set_selfpos(self, pos):
            x, y, theta = pos
            return self.hpl.setselfpos(x, y, theta)
        
        def get_auto_localization_mode(self):
            return self.__autolocalizationmode
        
        def set_auto_localization_mode(self, autolocalization):
            self.__autolocalizationmode = autolocalization
            return self.hpl.setautolocalizationmode(autolocalization)
        
        def set_use_white_lines(self, use_wl):
            return self.hpl.SetUseWhiteLines(use_wl)
        
        def start_memorize_observation(self):
            return self.hpl.startmemorizeobservation()
        
        def memorize_visible_observation(self):
            return self.hpl.memorizevisibleobservation()
        
        def use_memorized_observation_ntimes(self, count, diffusion_mm = 500, diffusion_deg = 20, confidence_thre = 100):
            return self.hpl.usememorizedobservationntimes(count, diffusion_mm, diffusion_deg, confidence_thre)
        
        def dispose_global_position(self, own_half_only = False):
            return self.hpl.disposeglobalposition(own_half_only)
        
        def plan_path(self, start_gl, dest_gl, obs = []):
            oblist = env.PosVector()
            for o in obs:
                oblist.push_back(convert_to_pos2d(o))
            path = self.hpl.pathplan(convert_to_pos2d(start_gl), convert_to_pos2d(dest_gl), oblist)
            rpath = []
            for i in range(path.size()):
                param = [path[i].steps, path[i].angle, path[i].stridex, path[i].period, path[i].stridey]
                rpath.append(param)
            return rpath

        def clear_path(self):
            return self.hpl.clearPath()
            
        def plan_path2lc(self, dest_lc, obs_lc = []):
            oblist = env.PosVector()
            for o in obs_lc:
                oblist.push_back(convert_to_pos2d(o))
            path = self.hpl.pathplan2LC(convert_to_pos2d(dest_lc), oblist)
            rpath = []
            for i in range(path.size()):
                pos = (path[i].x, path[i].y, path[i].th)
                rpath.append(pos)
            return rpath
        
        def terminate(self):
            self.hpl.terminate()
        
        def wait_until_status_updated(self):
            return self.hpl.waituntilstatusupdated()
        
        def is_motion_finished(self):
            return self.hpl.waituntilmotionfinished()

        def wait_until_motion_finished(self):
            return self.hpl.waituntilmotionfinished()

        def wait_until_robot_stop(self):
            return self.hpl.waituntilrobotstop()

        def wait_until_robot_standup(self):
            return self.hpl.waituntilrobotstandup()
        
        def enable_auto_wakeup(self, enable):
            self.hpl.setAutoWakeup(enable)
        
        def debug_log(self, str):
            self.hpl.debugoutput(str)

        def debug_log_ln(self, str):
            self.debug_log(str + "\n")

        def sleep(self, slptime):
            env.sleepSec(slptime)

        def time(self):
            return env.getTime()

        def set_kidnap_threshold(self, pole_thre, whiteline_thre):
            self.hpl.setKidnapThreshold(pole_thre, whiteline_thre)

        def set_kidnap_detector_smoothing_factor(self, alpha):
            self.hpl.setKidnapDetectorSmoothingFactor(alpha)

        GAME_STATE_INITIAL, GAME_STATE_READY, GAME_STATE_SET, GAME_STATE_PLAYING, GAME_STATE_FINISHED = range(5)
        POSTURE_STAND, POSTURE_DOWN, POSTURE_UP, POSTURE_LEFT, POSTURE_RIGHT, POSTURE_ERROR = range(6)
        SWITCH_1 = env.ACCELITE_SWITCH_1
        SWITCH_2 = env.ACCELITE_SWITCH_2
        SWITCH_3 = env.ACCELITE_SWITCH_3
        SWITCH_4 = env.ACCELITE_SWITCH_4
        SWITCH_5 = env.ACCELITE_SWITCH_5
        
        BALL, GOAL_POLE, ROBOT, LAST_VISIBLE_BALL = range(4)
        AF_OUR, AF_ENEMY, AF_ANY = range(3)
        GAME_STATE_EXT_SWITCH_PAUSED = 10
        COMMON_INFO_NUM = 2
    
    class SwitchState(object):
        def __init__(self):
            self.__state_dict = {id_ : False for id_ in range(1,6)}

        def state(self, id_):
            return self.__state_dict[id_]

        def update(self, brain):
            for id_, state in self.__state_dict.items():
                self.__state_dict[id_] = brain.get_switch_state(id_)

    class SelfState(object):
        def __init__(self):
            global SELF_ID
            self.__id = SELF_ID
            self.__kickoff_state = None
            self.__pos = None
            self.__pos_confidence = None
            self.__pan_deg = None
            self.__tilt_deg = None
        
        @property
        def id(self):
            return self.__id
        
        @property
        def kickoff_state(self):
            return self.__kickoff_state
        
        @property
        def pos(self):
            return self.__pos

        @property
        def pos_confidence(self):
            return self.__pos_confidence

        @property
        def pan_deg(self):
            return self.__pan_deg
        
        @property
        def tilt_deg(self):
            return self.__tilt_deg

        def update(self, brain):
            HLKICKOFF_OURS, HLKICKOFF_THEIRS, HLKICKOFF_DROPBALL, HLKICKOFF_NONE = range(4)
            hlkickoff_state = brain.get_kickoff_state()
            
            if hlkickoff_state == HLKICKOFF_OURS:
                self.__kickoff_state = SoccerAgent.Brain.AF_OUR
            elif hlkickoff_state == HLKICKOFF_THEIRS:
                self.__kickoff_state = SoccerAgent.Brain.AF_ENEMY
            else:
                self.__kickoff_state = SoccerAgent.Brain.AF_ANY
            
            self.__pos = brain.get_selfpos()
            self.__pos_confidence = brain.get_selfpos_confidence()
            self.__pan_deg = brain.get_pan_deg()
            self.__tilt_deg = brain.get_tilt_deg()
    
    class TeammateState(object):
        def __init__(self, id):
            global SELF_ID
            assert(id != SELF_ID)

            self.__id = id
            self.__arrpos_gl = []
            self.__ball_arrpos_gl = []
            self.__common_string = ""
        
        @property
        def id(self):
            return self.__id

        @property
        def arrpos_gl(self):
            return self.__arrpos_gl
        
        @property
        def ball_arrpos_gl(self):
            return self.__ball_arrpos_gl
        
        @property
        def common_string(self):
            return self.__common_string

        def update(self, brain):
            arrpos_cf_gl = brain.get_common_pos_gl(self.id, SoccerAgent.Brain.ROBOT, SoccerAgent.Brain.AF_OUR)
            if arrpos_cf_gl:
                pos_cf = arrpos_cf_gl[0]
                self.__arrpos_gl = [pos_cf[:3]]
            else:
                self.__arrpos_gl = []

            ball_arrpos_cf_gl = brain.get_common_pos_gl(self.id, SoccerAgent.Brain.BALL, SoccerAgent.Brain.AF_ANY)
            if ball_arrpos_cf_gl:
                pos_cf = ball_arrpos_cf_gl[0]
                self.__ball_arrpos_gl = [pos_cf[:3]]
            else:
                self.__ball_arrpos_gl = []
            
            self.__common_string = brain.get_common_string(self.id)

    class ObservationObject(object):
        def __init__(self, type, affi):
            self.__type = type
            self.__affi = affi
            self.__arrpos_lc = []
        
        @property
        def type(self):
            return self.__type
        
        @property
        def affi(self):
            return self.__affi

        @property
        def arrpos_lc(self):
            return self.__arrpos_lc

        def update(self, brain):
            self.__arrpos_lc = brain.get_estimated_object_pos_lc(self.type, self.affi)

    def __init__(self, create_field_properties):
        global SELF_ID
        
        pygame.init()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', 20122))
            sock.sendall("stop\n")
            time.sleep(1)
        except:
            pass
        
        argid = 0
        self.__arg = ""
        for arg in sys.argv:
            print arg
            if arg.startswith("ID="):
                idstr = arg[3:]
                argid = int(idstr)
            elif not ".py" in arg:
                self.__arg = arg

        global ghajime
        self.__hpl = env.HPL(argid)
        ghajime = self.__hpl.hajime #TODO: Delete

        SELF_ID = self.__hpl.envConfig.RobotID 

        self.__field_properties = create_field_properties()
        self.__effector = SoccerAgent.Effector(self.__hpl.hajime)
        self.__brain = SoccerAgent.Brain(self.__hpl)
        self.__terminate_server = TerminateServer()
        self.__terminate_server.start()
        self.__world_state = WorldState(self.__field_properties)
        
    def __del__(self): 
        self.terminate()
    
    @property
    def field_properties(self):
        return self.__field_properties

    @property
    def world(self):
        self.__world_state.update(self.brain)
        return self.__world_state

    @property
    def effector(self): 
        return self.__effector
    
    @property
    def brain(self):
        return self.__brain
    
    def get_arg(self):
        return self.__arg

    def terminate(self):
        self.__terminate_server.terminate()
        self.brain.terminate()
        self.effector.terminate()

    def wait_until_status_updated(self):
        self.brain.wait_until_status_updated()
        self.brain.detect_fall_error()
        self.brain.detect_game_state_change()

class StaticFieldProperties(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def ENEMY_GOAL_POLE_GL(cls):
        pass
    
    @abc.abstractproperty
    def OUR_GOAL_POLE_GL(cls):
        pass
    
    @abc.abstractproperty
    def ENEMY_GOAL_GL(cls):
        pass

    @abc.abstractproperty
    def OUR_GOAL_GL(cls):
        pass

    @abc.abstractproperty
    def NUM_PLAYERS(cls):
        pass

class WorldState(object):
    def __init__(self, field_prop):
        global SELF_ID
        
        self.time_sec = None
        self.permitted_intrusion_circle = False
        self.__game_state = None
        self.__switch_state = None
        self._estimated_obj_list = [ 
            SoccerAgent.ObservationObject(SoccerAgent.Brain.BALL, SoccerAgent.Brain.AF_ANY),
            SoccerAgent.ObservationObject(SoccerAgent.Brain.GOAL_POLE, SoccerAgent.Brain.AF_ANY),
            SoccerAgent.ObservationObject(SoccerAgent.Brain.ROBOT, SoccerAgent.Brain.AF_ENEMY),
            SoccerAgent.ObservationObject(SoccerAgent.Brain.ROBOT, SoccerAgent.Brain.AF_OUR),
            SoccerAgent.ObservationObject(SoccerAgent.Brain.ROBOT, SoccerAgent.Brain.AF_ANY),
            SoccerAgent.ObservationObject(SoccerAgent.Brain.LAST_VISIBLE_BALL, SoccerAgent.Brain.AF_ANY) 
        ]
        
        self.__self_state = SoccerAgent.SelfState()
        self.__switch_state = SoccerAgent.SwitchState()
        self.__teammates = [SoccerAgent.TeammateState(i) for i in range(1, field_prop.NUM_PLAYERS + 1) if i != SELF_ID]

    def update(self, brain):
        for obj in self._estimated_obj_list:
            obj.update(brain)

        self.__self_state.update(brain)
        self.__switch_state.update(brain)
        
        for ap in self.__teammates:
            ap.update(brain)

        self.time_sec = brain.time()
        self.__game_state = brain.get_game_state()
        
        if self.self_state.kickoff_state != SoccerAgent.Brain.AF_ENEMY:
            self.permitted_intrusion_circle = True
        elif self.game_state != SoccerAgent.Brain.GAME_STATE_PLAYING:
            self.permitted_intrusion_circle = False
    
    @property
    def game_state(self):
        return self.__game_state

    @property
    def switch_state(self):
        return self.__switch_state

    @property
    def self_state(self):
        return self.__self_state

    @property
    def teammates(self):
        return self.__teammates

    """
    def set_estimated_object_pos_lc(self, type, affi, arrpos):
        for obj in self._estimated_obj_list:
            if obj.type == type and obj.affi == affi:
                obj.arrpos_lc = arrpos
                return
        assert(False)
    """

    def get_estimated_object_pos_lc(self, type, affi = SoccerAgent.Brain.AF_ANY):
        obj = self._get_estimated_object(type, affi)
        return obj.arrpos_lc
    
    def get_estimated_object_pos_gl(self, type, affi = SoccerAgent.Brain.AF_ANY):
        objectarr_lc = self.get_estimated_object_pos_lc(type, affi)
        objectarr_gl = []
        if len(objectarr_lc) > 0:
            objectarr_gl.append(tools.geometry.coord_trans_local_to_global(self.__self_state.pos, objectarr_lc[0]))
        
        return objectarr_gl
    
    def get_estimated_object_velo(self, type, affi = SoccerAgent.Brain.AF_ANY):
        return self._get_estimated_object(type, affi).velo

    def _get_estimated_object(self, type, affi):
        for obj in self._estimated_obj_list:
            if obj.type == type and obj.affi == affi:
                return obj
        assert(False)

    K_BEHIND_BALL_DEFENSIVE_LINE = "K_BEHIND_BALL_DEFENSIVE_LINE"
    K_KNOW_BALL_POS = "K_KNOW_BALL_POS"
    K_KNOW_SELF_POS = "K_KNOW_SELF_POS"
    K_COME_BALL = "K_COME_BALL"
    K_TARGET_IN_SHOT_RANGE = 'K_TARGET_IN_SHOT_RANGE'
    K_ON_TARGET_POS = 'K_ON_TARGET_POS'
    K_BALL_AND_TARGET_ON_STRAIGHT_LINE = 'K_BALL_AND_TARGET_ON_STRAIGHT_LINE'
    K_HAVE_BALL = 'K_HAVE_BALL'
    K_BALL_IN_TARGET = 'K_BALL_IN_TARGET'
    K_BALL_IN_KICK_AREA = 'K_BALL_IN_KICK_AREA'
    K_ENEMY_WITHIN_RANGE = 'K_ENEMY_WITHIN_RANGE'
    K_IDLE = 'K_IDLE'
    K_TRACKING_BALL = 'K_TRACKING_BALL'

class SoccerPlayer(object):
    def __init__(self, create_strategy):
        self.__strategy = create_strategy()
        self.__agent = SoccerAgent(self.__strategy.create_field_properties)
        self.__motion = self.__strategy.create_motion(self.__agent.effector)
        self.__behavior_gen = BehaviorGenerator()
    
    @property
    def world(self):
        return self.__agent.world
    
    @property
    def symbol_dict(self):
        return self.__strategy.symbol_dict
    
    @property
    def motion(self):
        return self.__motion

    def plan_path(self, start_gl, dest_gl, obs = []):
        return self.__agent.brain.plan_path(start_gl, dest_gl, obs)

    def plan_path2lc(self, dest_lc, obs_lc = []):
        return self.__agent.brain.plan_path2lc(dest_lc, obs_lc)

    def wait_until_status_updated(self):
        self.__agent.wait_until_status_updated()
        if self.__strategy.update(self.world):
            raise ActionCancelSignal()

    def is_motion_finished(self):
        return self.__agent.brain.is_motion_finished()

    def wait_until_motion_finished(self):
        return self.__agent.brain.wait_until_motion_finished()

    def wait_until_robot_stop(self):
        return self.__agent.brain.wait_until_robot_stop()

    def wait_until_robot_standup(self):
        return self.__agent.brain.wait_until_robot_standup()

    def debug_log(self, str):
        self.__agent.brain.debug_log(str)

    def debug_log_ln(self, str):
        self.__agent.brain.debug_log_ln(str)
    
    def sleep(self, slptime):
        self.__agent.brain.sleep(slptime)
        self.wait_until_status_updated()
    
    def time(self):
        return self.__agent.brain.time()

    def get_target_arrpos_gl(self): #TODO: Implemented
        #return self.__strategy.get_target_arrpos_gl()
        return [(5000, 0, 0)]
    
    def set_selfpos(self, pos):
        return self.__agent.brain.set_selfpos(pos)

    def get_auto_localization_mode(self):
        return self.__agent.brain.get_auto_localization_mode()

    def set_auto_localization_mode(self, mode):
        return self.__agent.brain.set_auto_localization_mode(mode)

    def dispose_global_position(self, own_half_only = False):
        return self.__agent.brain.dispose_global_position(own_half_only)

    def start_memorize_observation(self):
        return self.__agent.brain.start_memorize_observation()
    
    def memorize_visible_observation(self):
        return self.__agent.brain.memorize_visible_observation()

    def use_memorized_observation_ntimes(self, count, diffusion_mm = 500, diffusion_deg = 20, confidence_thre = 100):
        return self.__agent.brain.use_memorized_observation_ntimes(count, diffusion_mm, diffusion_deg, confidence_thre)
    
    def set_kidnap_threshold(self, pole_thre, whiteline_thre):
        return self.__agent.brain.set_kidnap_threshold(pole_thre, whiteline_thre)

    def set_kidnap_detector_smoothing_factor(self, alpha):
        return self.__agent.brain.set_kidnap_detector_smoothing_factor(alpha)

    def __process(self):
        self.__strategy.update(self.__agent.world)
        pcs = self.__strategy.common_string.split(' ')
        if len(pcs) == 2:
            role, goal = pcs
            if role == "Attacker":
                self.set_kidnap_threshold(0, 0)
            else:
                self.set_kidnap_threshold(0.1, 0.1)

        self.__agent.brain.set_common_string(self.__strategy.common_string)
        self.__behavior_gen.process(self, self.__strategy.goal_symbol_list, self.__strategy.action_list)

    def terminate(self):
        self.__agent.terminate()
    
    def run(self):
        self.__agent.brain.set_auto_localization_mode(1)
        self.__agent.brain.set_use_white_lines(1)
        self.__agent.brain.enable_auto_wakeup(1)
        self.__agent.effector.set_pan_deg(0)
        
        arg = self.__agent.get_arg()
        if arg == 'GC' or arg == 'WAIT_START_SIGNAL':
            self.__agent.brain.set_use_gamecontroller(True)
            self.__agent.brain.set_send_common_info(True)
        elif arg == '' or arg == 'START' or arg == 'RESTART':
            pass
        else:
            assert False, "unknown args: " + arg

        self.__agent.brain.debug_log_ln("player start: " + arg)
        self.__agent.brain.dispose_global_position(own_half_only = False)
        time.sleep(3)
        while True:
            try:
                self.__process()
            except GameStateChanged, changenotify:
                self.__agent.brain.debug_log_ln(str(changenotify))
            except FallError, e:
                self.__agent.brain.debug_log_ln(str(e))
                self.__agent.effector.cancel()
                time.sleep(3)
                self.__agent.brain.wait_until_robot_standup()
                self.__agent.brain.wait_until_motion_finished()
                time.sleep(1)

class Strategy(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def common_string(self):
        pass

    @abc.abstractproperty
    def goal_symbol_list(self):
        pass
    
    @abc.abstractproperty
    def symbol_dict(self):
        pass
    
    @abc.abstractproperty
    def action_list(self):
        pass

    @abc.abstractmethod
    def update(self, world_state):
        pass
    
    @abc.abstractmethod
    def create_field_properties(self):
        pass
    
    @abc.abstractmethod
    def create_motion(self, effector):
        pass


