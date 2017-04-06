#!/usr/bin/env python
##############################
#filename: citbrains_fsm.py   
#brief:                     
#author:  
#last modified: 2017年03月01日 11時10分04秒
##############################
import traceback, math, time, pyenv, tools
from pyenv import Fallerror, Robot, GameStateChanged

class Accelite(pyenv.Robot):
    def __init__(self):
        pyenv.Robot.__init__(self)
        self.state = 'SearchBall'
        self.state_list = {\
        'SearchBall':self.SearchBall,\
        'ApproachBall':self.ApproachBall,\
        'KickBall': self.KickBall\
        }

    def SearchBall(self):
        self.DebugLogln('SearchBall')
        ballarr_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
        if ballarr_lc:
            self.PanDeg(tools.geometry.direction_deg(ballarr_lc[0]))
            self.state = 'ApproachBall'

    def ApproachBall(self):
        self.DebugLogln('ApproachBall')
        while True:
            ballarr_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
            if not ballarr_lc:
                self.state = 'SearchBall'
                break
            x,y,th = ballarr_lc[0]
            deg = tools.geometry.direction_rad(ballarr_lc[0])
            if x < 100:
                self.state = 'KickBall'
                break
            if math.fabs(deg)>30:
                walk_deg = tools.algorithm.clamp(deg,10,-10)
                self.Walk(0,walk_deg,0,0,0)
            elif math.fabs(y) >100:
                walk_y = tools.algorithm.clamp(y,20,-20)
                self.Walk(0,0,0,0,walk_y)
            else:
                self.Walk(0,0,10,0,0)

    def KickBall(self):
        self.DebugLogln('KickBall')
        self.Motion(30)
        self.WaitUntilMotionFinished()
        self.state = 'SearchBall'

    def run(self):
        while True:
            try:
                self.WaitUntilStatusUpdated()
                self.state_list[self.state]()
            except GameStateChanged, changenotify:
                self.DebugLogln(str(changenotify))
                self.Cancel()
            except FallError, e:
                self.Cancel()
        

if __name__ == '__main__':
    accelite = Accelite()
    accelite.DebugLogln('start')
    try:
        accelite.run()
    except Exception, e:
        accelite.Cancel()
        accelite.DebugLogln(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        accelite.terminate()

