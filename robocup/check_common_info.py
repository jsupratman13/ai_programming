import socket, sys, time
from pyenv import FallError, Robot, GameStateChanged, env


def self_communication(robot):
    robot.WaitUntilStatusUpdated()
    if initial_string != robot.GetCommonString(robot.id):
        initial_string = robot.GetCommonString(robot.id)
        past_time = current_time
        current_time = time.time()
        time_from_initial = current_time - initial_time
        time_from_last_cut = current_time - past_time
        robot.DebugLogln('String cut occured')
        robot.DebugLogln('Time from initial: ' + str(time_from_initial)
        robot.DebugLogln('Time from last cut: ' + str(time_from_last_cut))


def team_communication(robot, other_id):
    robot.WaitUntilStatusUpdated()
    if initial_string != robot.GetCommonString(other_id):
        initial_string = robot.GetCommonString(other_id)
        past_time = current_time
        current_time = time.time()
        time_from_initial = current_time - initial_time
        time_from_last_cut = current_time - past_time
        robot.DebugLogln('String cut occured')
        robot.DebugLogln('Time from initial: ' + str(time_from_initial)
        robot.DebugLogln('Time from last cut: ' + str(time_from_last_cut))

robot = Robot()
robot.SetSendCommonInfo(1)
robot.SetCommonString('Test')
initial_time = time.time()
current_time = time.time()
robot.WaitUntilStatusUpdated()
initial_string = robot.GetCommonString(robot.id)
robot.DebugLogln('\n String sent is: '+ initial_string + '\n')
while True:
    try:
     
        self_communication(robot)
#        team_communication(robot, ) # add robot id

    except FallError, fall:
        robot.DebugLogln(str(fall))
    except (KeyboardInterrupt, SystemExit):
        robot.terminate()
        sys.exit()

