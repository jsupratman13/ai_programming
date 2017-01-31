#!/usr/bin/env python
import traceback, math, time, pyenv, tools
from pyenv import Fallerror, Robot, GameStateChanged

class Accelite(pyenv.Robot):
    def __init__(self):
        pyenv.Robot.__init__(self)
        self.state = 'SearchBall'
        self.state_list = {\
        'SearchBall':self.SearchBall,\
        'KickBall': self.KickBall\
        }

    def SearchBall(self):
        self.DebugLogln('SearchBall')
        ballarr_lc = self.GetEstimatedLocalPos(self.HLOBJECT_BALL, self.HLCOLOR_BALL)
        if ballarr_lc:
            self.PanDeg(tools.geometry.direction_deg(ballarr_lc[0]))
            #self.state = 'ApproachBall'

    def KickBall(self):
        self.DebugLogln('KickBall')
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

