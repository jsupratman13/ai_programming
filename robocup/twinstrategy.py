# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
#import env, sys, pyenv, time, math, traceback
import sys, pyenv, time, math, traceback
import tactics.approach, tactics.search_object, tactics.shoot, tactics.geometry, tactics.move, tactics.localization, tactics.common_info, tactics.approach_Move
from pyenv import FallError, Robot, GameStateChanged, env

PAN_DEG_MAX = 135
TURN_DIST_THRE = 400
DEG_MARGEN = 10
STATE_CHANGE_TIME = 0.5

def in_kickareaX(self, ballpos):
    bx, by, bth = ballpos
    return 0 < bx < (self.conf_kick_forward+30)
def in_kickareaY(self, ballpos):
    bx, by, bth = ballpos
    right_far   = self.conf_kick_right_far - 30
    right_close = self.conf_kick_right_close + 30
    left_far    = self.conf_kick_left_far + 30
    left_close  = self.conf_kick_left_close - 30
    return (right_far < by < right_close) or (left_close < by < left_far)
def in_kickarea(self, ballpos):
    return in_kickareaX(self, ballpos) and in_kickareaY(self, ballpos)

def switch(robot):
    while robot.GetSwitch(3):
        robot.Cancel()
        robot.sleep(3)
    self.status = 'INIT'
    return self.status        

def normal_walk_to_destLC(robot, destlc, step_width, use_theta = False):
    onestep_dist = step_width
    dist = tactics.geometry.Distance(destlc)
    dir_deg = tactics.geometry.DirectionDeg(destlc)
    dx, dy, dt = destlc
    theta_ratio = min(math.fabs(dir_deg) / 30.0, 1.0)
    stride_ratio = 1 - theta_ratio
    if dir_deg > 0: sign_dir = 1
    else: sign_dir = -1
    if dist < 500 and math.fabs(dir_deg) < 80: #thre
        x = int(dx / dist * onestep_dist)
        y = int(dy / dist * onestep_dist)
        th = 0
        if use_theta:
            th = dt / 3
    else:
        if math.fabs(dir_deg) > 45:
            x = 0
            y = 0
            th = int(min(math.fabs(dir_deg/2),20) * sign_dir)
        else:
            x = int(min(dx, onestep_dist * stride_ratio))
            y = 0
            th = int(min(math.fabs(dir_deg / 2), 6) * sign_dir)
    
    wx = int(x/5)
    wy = int(y/4)
    wt = th

#    robot.DebugLogln("Walk: 0, " + str(wt) + ", " + str(wx) + ", 0, " + str(wy))
    robot.Walk(0, wt, wx, 12, wy)

def follow_path_normal_walk(robot, path, step_width):
    if len(path) >= 2: normal_walk_to_destLC(robot, path[0], step_width, False)
    else: normal_walk_to_destLC(robot, path[0], step_width, True)

def plan_path_with_obstacle_avoidanceLC(robot, destlc):
    obs = []
    rpos  = robot.GetLocalPos(robot.HLOBJECT_POLE, robot.HLCOLOR_BLACK)
#    rpos += robot.GetLocalPos(robot.HLOBJECT_POLE, robot.HLCOLOR_CYAN)
#    rpos += robot.GetLocalPos(robot.HLOBJECT_POLE, robot.HLCOLOR_MAGENTA)
    for pos in rpos:
        if tactics.geometry.Distance(pos) > 10:
            obs.append(pos)
    path = robot.PlanPath2LC(destlc, obs)
    return path

def FwTrackingBall(robot):
    ball_lc = robot.GetEstimatedLocalPos(robot.HLOBJECT_BALL, robot.HLCOLOR_BALL)
    if( len(ball_lc) <= 0):
        robot.status = 'SEARCH_BALL'
        robot.Cancel()
        return 'E_FAILURE'

    current_pan = robot.GetPanAngleDeg()
    distance = tactics.geometry.Distance(ball_lc[0])

    angle_difference = tactics.geometry.DirectionDeg(ball_lc[0]) - current_pan
    if(math.fabs(angle_difference) > 10):
        robot.PanDeg(current_pan + angle_difference)
    return 'E_SUCCESS'

def FwCheckBallposGL(robot, ball_lc):
    ball_x_lc, ball_y_lc, ball_th_lc = ball_lc[0]
    ball_gl = tactics.geometry.CoordTransLocalToGlobal(robot.GetSelfPos(), ball_lc[0])
    ball_x_gl, ball_y_gl, ball_th_gl = ball_gl
    if(ball_x_gl < -1000):
        return ((1000, 0, 0))
    else:
        return ((5000, 0, 0))

def FwCalcArrivePos(robot, ballpos, goalpos, dist):
    bx, by, bt = ballpos                                                        # ball position
    gx, gy, gt = goalpos                                                        # goal position
    if gx > 0:
        #fightside yellow
        theta = math.atan2(by - gy, bx - gx)                                    # direction to the ball from the opposite goal
        dx = bx + dist * math.cos(theta)                                        # position to approach
        dy = by + dist * math.sin(theta)
        dt = math.atan2(gy - dy, gx - dx)                                       # the direction to the goal from the approach position
    else:
        #fightside blue
        theta = math.atan2(gy - by, gx - bx)                                    # direction to the ball from the opposite goal
        dx = bx - dist * math.cos(theta)                                        # position to approach
        dy = by - dist * math.sin(theta)
        dt = math.atan2(gy - dy, gx - dx)                                       # the direction to the goal from the approach position

    return (dx, dy, dt)

def ConvertOldarg(arg):                                                                # Old Argument -> New Argument
    if arg == 'start':                                                                  # start -> KICK_OFF
        return 'KICK_OFF'
    elif arg == 'restart':                                                              # restart -> RESTART
        return 'RESTART'
    elif arg == 'start_wait':                                                           # start_wait -> KICK_OFF_DEFENCE
        return 'KICK_OFF_DEFENCE'
    return arg

def Limit(value, high, low):    #(((x)>(h))?(h):(((x)<(l))?(l):(x)))
    if value > high:
        return high
    else:
        if value < low:
            return low
        else:
            return value

def Distance(pos):
    x, y, th =pos
    return math.sqrt(x**2+y**2)

class FW(pyenv.Robot):
    def __init__(self):
        pyenv.Robot.__init__(self)

        self.statusfunc = {
        'SEARCH_BALL': self.FwSearchBall, \
        'APPROACH_BALL': self.FwApproachBall, \
        'TURN_AROUND_BALL': self.FwTurnAroundBall, \
        'ADJUST_TO_KICK': self.FwAdjustToKick, \
        'SHOOT': self.FwShoot, \
        'SUPPORT': self.FwSupport,\
        }

        # read shoot area
        conf_file = "kid/actionconf/kid-strategy.cnf"                                                   # conf_file : "fw-move.cnf"
        self.DebugLogln("")
        self.SetParaFile(conf_file)
        value = self.ReadPara("kick_front", "120,2200", conf_file)
        rect = value.split(",")
        self.conf_kick_near    = int(rect[0])
        self.conf_kick_forward = int(rect[1])

        value = self.ReadPara("kick_left", "30,100", conf_file)
        params = value.split(",")
        self.conf_kick_left_close = int(params[0])
        self.conf_kick_left_far = int(params[1])

        value = self.ReadPara("kick_right", "-30,-100", conf_file)
        params = value.split(",")
        self.conf_kick_right_close = int(params[0])
        self.conf_kick_right_far = int(params[1])

        self.kick_conf = self.conf_kick_near, self.conf_kick_forward, self.conf_kick_left_close, self.conf_kick_left_far, self.conf_kick_right_close, self.conf_kick_right_far
        self.kick_wait = float(self.ReadPara("kick_wait", "0.5", conf_file))

        self.max_stride_x = int(self.ReadPara("max_stride_x", "20", conf_file))
        self.max_stride_y = int(self.ReadPara("max_stride_y", "26", conf_file))
        self.mid_stride_x = int(self.ReadPara("mid_stride_x", "18", conf_file))
        self.mid_stride_y = int(self.ReadPara("mid_stride_y", "20", conf_file))
        self.max_walk_angle = int(self.ReadPara("max_walk_angle", "8", conf_file))
        self.mid_walk_angle = int(self.ReadPara("mid_walk_angle", "6", conf_file))

        self.turn_dist = int(self.ReadPara("turn_dist", "700", conf_file))
        self.walk_period = int(self.ReadPara("walk_period", "15", conf_file))

        self.statusparam = ''
        self.role = 'Striker'
#        self.role_switch_time = self.time()
    
    def FwSearchBall(self):
        self.DebugLogln("Search Ball")
        self.WaitUntilStatusUpdated()
        for num in [0,PAN_DEG_MAX, 45, -45 , -PAN_DEG_MAX]:
            self.WaitUntilStatusUpdated()
            self.PanDeg(num)
            self.sleep(1.0)
            ball_lc = self.GetLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if( len(ball_lc) > 0):
                ball_x_lc, ball_y_lc, ball_th_lc = ball_lc[0]
                ball_th_lc = math.degrees(math.atan2(ball_y_lc, ball_x_lc))
                self.status = 'APPROACH_BALL'
                self.Cancel()
                break

    def FwApproachBall(self):
        self.DebugLogln("Approach ball: start")
        while(True):
            self.WaitUntilStatusUpdated()
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if(len(ball_lc) < 0 or FwTrackingBall(self) == 'E_FAILURE'):
                self.status = 'SEARCH_BALL'
                self.Cancel()
                self.sleep(0.5)
                break

            ball_gl = tactics.geometry.CoordTransLocalToGlobal(self.GetSelfPos(), ball_lc[0])
            ball_x_lc, ball_y_lc, ball_th_lc = ball_lc[0]
            ball_x_gl, ball_y_gl, ball_th_gl = ball_gl
            target_dist_lc = tactics.geometry.Distance(ball_lc[0]) #=(ball_x_lc^2+ball_y_lc^2)^1/2
            target_direction_deg = tactics.geometry.DirectionDeg(ball_lc[0])#=atan2(ball_y_lc/ball_x_lc)
            self.DebugLogln(str(target_dist_lc))
            if target_dist_lc >= 500:
                plan_lc =  plan_path_with_obstacle_avoidanceLC(self, ball_lc[0])
                follow_path_normal_walk(self, plan_lc, self.mid_stride_x * 5)
            else:
                if math.fabs(target_direction_deg) > 30:
                    walk_th = Limit(target_direction_deg, 10, -10)
                    self.Walk(0,walk_th,0,12,0)
                elif math.fabs(ball_y_lc) > 50:
                    walk_y = Limit(ball_y_lc, self.max_stride_y, -self.max_stride_y)
                    walk_y = (walk_y / math.fabs(walk_y)) * max(math.fabs(walk_y), 4)
                    self.Walk(0, 0, 0, 12, walk_y)
                else:
                    self.DebugLogln("Approach ball: done")
                    self.Cancel()
                    self.status = 'TURN_AROUND_BALL'
                    self.sleep(STATE_CHANGE_TIME)
                    break;

    def FwTurnAroundBall(self):
        first = True
        base_ang = 10
        ang_comp = 0
        prev_dist = -10
        ka = 0.02
        kb = 0.05
        ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
#        target_pos = FwCheckBallposGL(self, ball_lc)
        target_pos = ((5000,0,0))
#        self.Walk(2,0,0,12,0)
        while True:
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            robot_x_gl,robot_y_gl,robot_th_gl = self.GetSelfPos()
            if(len(ball_lc) > 0 or FwTrackingBall(self) == 'E_SUCCESS'):
                ball_gl = tactics.geometry.CoordTransLocalToGlobal(self.GetSelfPos(), ball_lc[0])
                shootpos = FwCalcArrivePos(self, ball_gl, target_pos, self.turn_dist)
                dx, dy, dt = shootpos
                ball_lc_x, ball_lc_y, ball_lc_t = ball_lc[0]
#                if( tactics.geometry.Distance(ball_lc[0]) > TURN_DIST_THRE or math.fabs(tactics.geometry.DirectionDeg(ball_lc[0])) > 30):
#                    self.DebugLogln("FwTurnAroundBall:false")
#                    self.status = 'APPROACH_BALL'
#                    self.Cancel()
#                    break
            else:
                self.DebugLogln("turn_around_ball_to_goal: ball not found")
                self.status = 'SEARCH_BALL'
                self.Cancel()
                break

            if first:
                ccw = tactics.geometry.NormalizeRad(dt-robot_th_gl) > 0
                first = False
            dist = ball_lc_x

            if ccw: ang_comp_d = ((dist-self.turn_dist) * ka + ball_lc_y * kb)
            else: ang_comp_d = ((dist-self.turn_dist) * ka - ball_lc_y * kb)

            ang_comp = ang_comp * 0.9 + ang_comp_d * 0.1
            ang_comp = Limit(ang_comp, 4, -base_ang)

            if ang_comp > 0: stridey_abs = self.max_stride_y - ang_comp
            else: stridey_abs = self.max_stride_y + ang_comp

            if ccw: self.Walk(0, base_ang + int(ang_comp), 0, 12, -stridey_abs)
            else: self.Walk(0, -(base_ang + int(ang_comp)), 0, 12, stridey_abs)

            shootpos_lc = tactics.geometry.CoordTransGlobalToLocal(self.GetSelfPos(), shootpos)
            shootpos_x, shootpos_y, shootpos_th = shootpos_lc
            target_th = math.degrees(shootpos_th)

            if( -DEG_MARGEN < target_th < DEG_MARGEN):
                self.DebugLogln("turn_around_ball_to_goal: done")
                self.Cancel()
                self.status = 'ADJUST_TO_KICK'
                self.sleep(STATE_CHANGE_TIME)
                break

    def FwAdjustToKick(self):
        self.DebugLogln("Adjust To Kick")
#        self.Walk(2,0,0,12,0)
        self.sleep(0.2)

        ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
        should_kick_left = ball_lc[0][1] > (self.conf_kick_left_close + self.conf_kick_right_close)/2

        while True:
            if(FwTrackingBall(self) == 'E_FAILURE'):
                self.DebugLogln("Adjust_to_kick : failed")
                self.status = 'SEARCH_BALL'
                self.Cancel()
                self.sleep(0.5)
                break
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if ball_lc:
                self_pos = self.GetSelfPos()
                ballx_lc, bally_lc, ballth_lc = ball_lc[0]#tactics.geometry.CoordTransGlobalToLocal(self_pos, ball_gl[0])
                targetx = ballx_lc - (self.conf_kick_forward + self.conf_kick_near) / 2.0

                if bally_lc > self.conf_kick_left_far:
                    should_kick_left = True
                if bally_lc < self.conf_kick_left_far:
                    should_kick_left = False

                if should_kick_left:
                    targety = bally_lc - (self.conf_kick_left_far + self.conf_kick_left_close) / 2.0
                else:
                    targety = bally_lc - (self.conf_kick_right_far + self.conf_kick_right_close) / 2.0

                targetx = Limit(targetx, 40, -40)
                targety = Limit(targety, 40, -40)
                target_gl = [(5000, 0, 0)]
                targetdeg = 0
                if target_gl:
                    ball_gl = tactics.geometry.CoordTransGlobalToLocal(self_pos, ball_lc[0])
                    approachpos_gl = FwCalcArrivePos(self, ball_gl, target_gl[0], 300)
                    approachpos_lc = tactics.geometry.CoordTransGlobalToLocal(self_pos, approachpos_gl)
                    targetth = approachpos_lc[2]
                    targetdeg = Limit(math.degrees(targetth), 5, -5)

                    targetx = (targetx / math.fabs(targetx) * max(math.fabs(targetx), 20))
                    targety = (targety / math.fabs(targety) * max(math.fabs(targety), 20))

                    if math.fabs(targety) > 100: targetdeg = 0
                    
                    #tactics.move.Move(self, targetx, targety, 0, 7, 15,16)
                    self.AccurateWalk(0, targetx, targety, targetdeg)
                    self.sleep(0.3)
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if in_kickarea(self, ball_lc[0]):
                self.DebugLogln("adjust_to_kick : done")
                self.Cancel()
                self.status = 'SHOOT'
                self.sleep(STATE_CHANGE_TIME)
                break


    def FwShoot(self):
        ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
        self.DebugLogln("shoot")
        while(True):
            self.WaitUntilStatusUpdated()
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if(len(ball_lc) < 0 or FwTrackingBall(self) == 'E_FAILURE'):
                self.status = 'SEARCH_BALL'
                break
            ballx, bally, ballth = ball_lc[0]
            if in_kickarea(self, ball_lc[0]):
                if bally > (self.conf_kick_left_close + self.conf_kick_right_close)/2:
                    self.Motion(31,1)
                else:
                    self.Motion(30,1)
                self.WaitUntilMotionFinished()
            else:
                self.Cancel()
                self.status = 'APPROACH_BALL'
                break

    def FwSupport(self):
        self.PanDeg(0)
        striker_id = SearchStriker()
        while True:
            if striker_id:
                if self.GetCommonString(striker_id) == 'Supporter':
                    self.SetCommonString('Striker')
                    self.status = 'APPROACH_BALL'
                    break
                else:
                    striker_pos = self.GetCommonGlobalPos(striker_id, self.HLOBJECT_ROBOT, self.GetOurColor())
                    if len(striker_pos) > 0:
                        striker_pos = ((striker_pos[0][0], striker_pos[0][1], striker_pos[0][2]))
                        selfpos = self.GetSelfPos()
                        target_lc = tactics.geometry.CoordTransGlobalToLocal(selfpos, striker_pos)
                        dist_lc = tactics.geometry.Deistance(target_lc)
                        targetdir = tactics.geometry.DirectionDeg(target_lc)
                        self.DebugLogln('dist_lc: ' + str(dist_lc))
                        if dist_lc > 600:
                            plan_lc = plan_path_with_obstacle_avoidanceLC(self, target_lc)
                            follow_path_normal_walk(self, plan_lc, self.mid_stride_x * 5)
                        else:
                            if math.fabs(targetdir) > 30:
                                walkth = Limit(targetdir, 10, -10)
                                self.walk_period(0,walkth, 0, 12,0)
                            elif math.fabs(target_lc[0]) > 100:
                                walk_y = Limit(ball_y_lc, self.max_stride_y, -self.max_stride_y)
                                self.Walk(0, 0, 0, 12, walk_y)
                            else:
                                self.Cancel()
                                self.DebugLogln('Arrive')
            else:
                self.DebugLogln('striker id not found')
                striker_id = SearchStriker()

    def SearchStriker(self):
        for id in [1,2,3,4,5,6]:
            if self.GetCommonStrind(id) == 'Striker':
                return id
        return False

    def RoleCheck(self):
        role = self.GetCommonString(self.id)
        return role

    def FwMain(self, arg):
        """Forward main loop"""
        if arg == 'GC':
            arg = 'WAIT_START_SIGNAL'
            self.DebugLogln("Initialize: GameController")
            self.SetUseGameController(1)
        else:
            self.DebugLogln("initialize: ManualControl")
            arg = 'SEARCH_BALL'                                              # Set Common Info
       
        self.SetSendCommonInfo(True)
        self.SetCommonString("Striker")                                                  # Set Common String
#        self.SetCommonString("Supporter")
        self.start_time = time.time()                                               # Set Start Time
        self.should_relocalize = True
        self.status = arg                                                           # status <- arg (KICK_OFF, RESTART, KICK_DEFENCE, ...)
        self.SetSelfPos((0,0,0))
        while True:
            try:                                                                    # for catching fall error
                self.role = self.RoleCheck()
                self.DebugLogln('role: ' +self.role)
                if self.role == 'Supporter':
                    self.status = 'SUPPORT'
                self.SetHighResoMode(1)                                             # Set High Resolution Mode
                self.SetAutoLocalizationMode(1)
                self.SetUseWhiteLines(1)
                self.WaitUntilStatusUpdated()                                       # Wait Until Status Updated
                func = self.statusfunc[self.status]()                               # execute own function
            except GameStateChanged, changenotify:                                  # game status is changed by referee box
                self.DebugLogln(str(changenotify))
                if not self.NavigationFinished():
                    self.StopNavigation()
            except FallError, e:                                                    # when the robot fall down
                self.SetCommonString('Supporter')
                self.Cancel()
                self.sleep(3)
                self.WaitUntilRobotStandUp()
                self.WaitUntilMotionFinished()
                self.sleep(1)

if __name__ == '__main__':
    fw = FW()

    fw.DebugLogln("Twin Strategy Start")
    fw.DisposeGlobalPosition()
    fw.EnableAutoWakeup(1)

    try:
        fw.FwMain(fw.GetArg())
    except Exception, e:
        fw.StopNavigation()
        fw.DebugLog(traceback.format_exc())
        fw.terminate()
        raise
    except (KeyboardInterrupt, SystemExit):
        fw.terminate()
        raise
