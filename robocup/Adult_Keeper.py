import time, math, sys, traceback, pyenv
import tactics.geometry, tactics.move_keeper_teen, tactics.move
from pyenv import FallError, Robot, GameStateChanged

GOALAREAX = -4300

def Limit(value, max, min):
    if value > max:
        return max
    else:
        if value < min:
            return min
        else:
            return value
def CheckEnemy(self, enemypos_lc):
    selfpos = self.GetSelfPos()
    if len(enemypos_lc) > 2:
        for i in [0,1,2]:
            enemy_gl = tactics.geometry.CoordTransLocalToGlobal(selfpos, enemypos_lc[i])
            if (tactics.geometry.Distance2Points(enemy_gl, self.pos_gl1) > 50) and (tactics.geometry.Distance2Points(enemy_gl, self.pos_gl2) > 50):
                return enemy_gl
    return False

class GK(pyenv.Robot):
    def __init__(self):
        pyenv.Robot.__init__(self)
        self.pos_gl1 = None
        self.pos_gl2 = None

        # action block
        self.statusfunc = {\
            'IDLE': self.GkIdle,\
            'LOK_GUARD': self.GkLokGuard,\
            'SEARCH_BALL': self.GkSearchBall,\
            'DEFAULT_GUARD': self.GkDefaultGuard,\
            'MARK_OBSTACLE': self.GkMarkObstacle,\
            'LOCALIZATION': self.GkLocalization,\
            }

    def GkLocalization(self):
        init_pan_deg = self.GetPanAngleDeg()
        self.Cancel()
        self.WaitUntilStatusUpdated()
        prev_autolocalization = self.GetAutoLocalizationMode()
        self.SetAutoLocalizationMode(0)
        #self.DisposeGlobalPosition()
        self.StartMemorizeObservation()
        pan_angles = [-90, -45, 0, 45, 90]
        num_found_landmarks = 0
        for pan in pan_angles:
            self.WaitUntilStatusUpdated()
            self.PanDeg(pan)
            self.sleep(0.8)
            num_found_landmarks += self.MemorizeVisibleObservation()
        self.UseMemorizedObservationNtimes(10, 500, 20, 95)
        self.SetAutoLocalizationMode(prev_autolocalization)
        self.PanDeg(init_pan_deg)
        self.WaitUntilStatusUpdated()
        self.sleep(2)


    def GkMarkObstacle(self):
        self.DebugLogln("\n Marking Obstacle Now \n")
        initial_time = time.time()
        while time.time() - initial_time < 10:
            self.WaitUntilStatusUpdated()
            rpos = self.GetEstimatedLocalPos(self.HLOBJECT_POLE, self.HLCOLOR_BLACK)
            if len(rpos) > 1:
            	self.pos_gl1 = tactics.geometry.CoordTransLocalToGlobal((-4300,0,0), rpos[0])
            	self.pos_gl2 = tactics.geometry.CoordTransLocalToGlobal((-4300,0,0), rpos[1])
            	x,y,th = self.pos_gl1
            	x2,y2,th2 = self.pos_gl2
            	self.DebugLogln("Obs1 x: "+str(x)+" y: "+str(y))
            	self.DebugLogln("Obs2 x: "+str(x2)+" y: "+str(y2))
        while True:
            enemypos_lc = self.GetEstimatedLocalPos(self.HLOBJECT_POLE, self.HLCOLOR_BLACK)
            epos = CheckEnemy(self, enemypos_lc)
            if epos:
                ex, ey, eth = epos
                self.DebugLogln("Epos x: " +str(ex) + " y: "+str(ey))
            else:
                self.DebugLogln("Unable To Locate Enemy")
            self.sleep(1)

        #self.status = 'SEARCH_BALL'

    def GkSearchBall(self):
        self.DebugLogln("\n Searching Ball Now \n")
        for num in [-90,-45,45,90]:
            self.WaitUntilStatusUpdated()
            self.PanDeg(num)
            self.sleep(1.0)
            ball_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if len(ball_lc) > 0:
                self.status = 'LOK_GUARD'
                self.Cancel()
                break

    #Guard with respect to ball
    def GkDefaultGuard(self):
        self.DebugLogln("\n Default Defense Mode \n")
        while True:
            self.WaitUntilStatusUpdated()
            ballpos_lc = self.GetLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if len(ballpos_lc) <= 0:
                self.status = 'SEARCH_BALL'
                break
            enemypos_lc = self.GetLocalPos(self.HLOBJECT_POLE, self.HLCOLOR_BLACK)
            if len(enemypos_lc) > 0:
                self.status = 'LOK_GUARD'
                break
            selfpos = self.GetSelfPos()
            x, y, th = selfpos
            ballpos_gl = tactics.geometry.CoordTransLocalToGlobal(selfpos, ballpos_lc[0])
            bx, by, bth = ballpos_gl

            target_angle = tactics.geometry.DirectionDeg(ballpos_lc[0])
            if math.fabs(target_angle - self.GetPanAngleDeg()) > 10:
                self.PanDeg(target_angle)

            if math.fabs(by - y) > 200:
                if by > y:
                    self.Walk(0,0,0,15,10)
                elif by < y:
                    self.Walk(0,0,0,15,-10)

    #Guard with respect to enemy Line Of Kick
    def GkLokGuard(self):
        self.DebugLogln("\n Line of Kick Defense Mode \n")
 #       selfpos = self.GetSelfPos()
 #       x ,y, th = selfpos
 #       while math.fabs(th) > 20:
 #           self.DebugLogln("\n fixing orientation\n")
 #           if th >0: self.Walk(0, -10,0,0,0)
 #           else: self.Walk(0,10,0,0,0)
 #       if GOALAREAX - x < -300:
 #           self.DebugLogln("\n fixing x position \n")
 #           self.Walk(3,0,10,0,0)
 #           self.WaitUntilMotionFinished()
        init_time = time.time()
        while True: #while time.time() - init_time < 5:
            self.WaitUntilStatusUpdated()
            ballpos_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if len(ballpos_lc) <= 0:
                self.DebugLogln("Lost Ball")
                self.status = 'SEARCH_BALL'
                break
            enemypos_lc = self.GetEstimatedLocalPos(self.HLOBJECT_POLE, self.HLCOLOR_BLACK)
            selfpos = self.GetSelfPos()
            x, y, th = selfpos
            ballpos_gl = tactics.geometry.CoordTransLocalToGlobal(selfpos, ballpos_lc[0])
            bx, by, bth = ballpos_gl

            target_angle = tactics.geometry.DirectionDeg(ballpos_lc[0])
            if math.fabs(target_angle - self.GetPanAngleDeg()) > 10:
                self.PanDeg(target_angle)

            if len(enemypos_lc) > 0:
                enemypos_gl = CheckEnemy(self, enemypos_lc)
                if enemypos_gl:
                    ex, ey, eth = enemypos_gl
                    dx = ex - bx
                    dy = ey - by
                    if dx < 200: dx = 200
                    m = dy/dx
                    c = by - (m*bx)
                    dest_y = (m*x) - c
                    dest_y = Limit(int(dest_y), 800, -800)
                    rag = math.fabs(dest_y-int(y))
                    self.DebugLogln("dest_y: "+str(dest_y)+" selfposy: "+str(int(y))+" rangechek: "+str(rag))
                    destpos = (-4300, dest_y, 0)
                    if rag > 700: #unit width
                        if dest_y > int(y):
                            self.Walk(0,0,0,15,10)
                        elif dest_y < int(y):
                            self.Walk(0,0,0,15,-10)
                    else:
                        self.DebugLogln("ARRIVE")
                        self.Cancel()
 #               else:
 #                   self.status = 'DEFAULT_GUARD'
 #                   self.Cancel()
 #                   break
            else:
                #self.status = 'DEFAULT_GUARD'
                #break
                self.DebugLogln("POLE Lost")
                self.Cancel()
#        self.Cancel()
#        self.status = 'LOCALIZATION'

    def GkIdle(self):
        self.DebugLogln("\n Idiling \n")
        self.Pan(0)
        self.Cancel()
        self.SetSelfPos((-4300,0,0))
        self.DisposeGlobalPosition()
        self.sleep(1.0)

    def GkGameStatus(self,state):
        if state == Robot.HLGAME_STATE_INITIAL:
            self.status = 'IDLE'
        elif state == Robot.HLGAME_STATE_READY:
            self.status = 'IDLE'
        elif state == Robot.HLGAME_STATE_SET:
            self.status = 'IDLE'
        elif state == Robot.HLGAME_STATE_PLAYING:
            self.status = 'MARK_OBSTACLE'
        elif state == Robot.HLGAME_STATE_FINISHED:
            self.status = 'IDLE'
        elif state == Robot.HLGAME_STATE_EXT_SWITCH_PAUSED:
            self.status = 'IDLE'

    def GkMain(self, arg):
        if arg == 'WAIT_START_SIGNAL':
            self.SetUseGameController(True)
            arg = 'IDLE'
        else:
            arg = 'MARK_OBSTACLE'
            pass
        self.DebugLogln("initiate: " + arg)
        self.status = arg
        self.SetHighResoMode(1)
 #       self.SetAutoLocalizationMode(1)
 #       self.SetUseWhiteLines(1)
        self.SetSelfPos((GOALAREAX,0,0))
        while True:
            try:
                self.WaitUntilStatusUpdated()
                func = self.statusfunc[self.status]()
            except GameStateChanged, changenotify:
                self.DebugLogln(str(changenotify))
                self.Cancel()
                self.GkGameStatus(self.GetGameState())
            except FallError,e:
                self.Cancel()

if 1 == 1:
    gk = GK()
    gk.DebugLogln("GoalKeeper Xega Start")
    gk.DisposeGlobalPosition()
    gk.EnableAutoWakeup(1)

    try:
        gk.GkMain(gk.GetArg())

    except Exception, e:
        gk.StopNavigation()
        gk.DebugLogln(traceback.format_exc())
        sys.exit()
        raise

    except KeyboardInterrupt:
        gk.StopNavigation()
        gk.Cancel()
        sys.exit()
        raise
