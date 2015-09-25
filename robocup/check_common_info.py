import socket, sys, time
from pyenv import FallError, Robot, GameStateChanged, env

robot = Robot()
robot.SetSendCommonInfo(1)
robot.SetCommonString('Test')
initial_time = time.time()
current_time = time.time()
initial_string = robot.GetCommonString(robot.id)
robot.DebugLogln('\n String sent is: '+ initial_string + '\n')
while True:
    try:
        robot.WaitUntilStatusUpdated()
        if initial_string != robot.GetCommonString(robot.id):
            initial_string = robot.GetCommonString(robot.id)
            past_time = current_time
            current_time = time.time()
            time_from_inital = current_time - initial_time
            time_from_last = current_time - past_time
            robot.DebugLogln('String cut ocured')
            robot.DebugLogln('Time from inital: '+str(time_from_initial))
            robot.DebugLogln('Time from last cut: ' + str(time_from_last))

    except FallError, fall:
        robot.DebugLogln(str(fall))
    except (KeyboardInterrupt, SystemExit):
        robot.terminate()
        sys.exit()

