import math
import tools.geometry

def plan_path_with_obstacle_avoidance_lc(agent, destlc):
    """ plan_path_with_obstacle_avoidance_lc
    input
        destlc: destination in robot local coordinates
    return
        array of sub-goals
    """

    obs  = []
    rpos = agent.brain.get_estimated_object_pos_lc(agent.brain.ROBOT, agent.brain.AF_ANY)
    rpos += agent.brain.get_estimated_object_pos_lc(agent.brain.ROBOT, agent.brain.AF_ENEMY)
    rpos += agent.brain.get_estimated_object_pos_lc(agent.brain.ROBOT, agent.brain.AF_OUR)
    
    for pos in rpos:
        if tools.geometry.distance(pos) > 10:
            obs.append(pos)
    path = agent.brain.plan_path2lc(destlc, obs)
    return path

"""
def follow_path_accurate_walk(motion, path, step_width):
        follow path to destination by accurate walk
    input
        path: array of sub-goals in robot local coordinates
        step_width: step width[mm]
    
    if len(path) >= 2:
        accurate_walk_to_dest_lc(motion, path[0], step_width, False)
    else:
        accurate_walk_to_dest_lc(motion, path[0], step_width, True)
"""

def follow_path_normal_walk(agent, path, step_width, period):
    """ follow path to destination by normal walk
    input
        path: array of sub-goals in robot local coordinates
        step_width: step width[mm]
    """
    if len(path) >= 2:
        normal_walk_to_dest_lc(agent, path[0], step_width, period,False)
    else:
        normal_walk_to_dest_lc(agent, path[0], step_width, period,True)

"""
def accurate_walk_to_dest_lc(motion, destlc, step_width, use_theta = False):
     accurate_walk_to_dest_lc
    input
        destlc: destination in robot local coordinates
        step_width: step width[mm]
    
    onestep_dist = step_width
    dist = tools.geometry.distance(destlc)
    dir_deg = tools.geometry.direction_deg(destlc)
    dx, dy, dt = destlc
    theta_ratio = min(math.fabs(dir_deg) / 30.0, 1.0)
    stride_ratio = 1 - theta_ratio
    sign_dir = 1 if dir_deg > 0 else -1
    
    if dist < 500 and math.fabs(dir_deg) < 80: #thre
        x = int(dx / dist * onestep_dist)
        y = int(dy / dist * onestep_dist)
        th = (dt / 2) if use_theta else 0
    
    else:
        if math.fabs(dir_deg) > 45:
            x = 0
            y = 0
            th = int(sign_dir * 10)
        else: 
            x = int(min(dx, onestep_dist * stride_ratio))
            y = 0
            th = int(min(math.fabs(dir_deg / 2), 15) * sign_dir)
    
    effector.accurate_walk(0, x, y, th)
"""

def normal_walk_to_dest_lc(agent, destlc, step_width, period,use_theta = False):
    """ normal_walk_to_dest_lc
    input
        destlc: destination in robot local coordinates
        step_width: step width[mm]
    """
    onestep_dist = step_width
    dist = tools.geometry.distance(destlc)
    dir_deg = tools.geometry.direction_deg(destlc)
    dx, dy, dt = destlc
    theta_ratio = min(math.fabs(dir_deg) / 30.0, 1.0)
    stride_ratio = 1 - theta_ratio
    sign_dir = 1 if dir_deg > 0 else -1
    
    if dist < 500 and math.fabs(dir_deg) < 80: #thre
        x = int(dx / dist * onestep_dist)
        y = int(dy / dist * onestep_dist)
        th = (dt / 3) if use_theta else 0
    else:
        if math.fabs(dir_deg) > 45:
            x = 0
            y = 0
            th = int(min(math.fabs(dir_deg / 2), 20) * sign_dir)
        else: 
            x = int(min(dx, onestep_dist * stride_ratio))
            y = 0
            th = int(min(math.fabs(dir_deg / 2), 6) * sign_dir)

    wx = int(x / 5)
    wy = int(y / 4)
    wt = th
    agent.effector.walk(0,wt,wx,period,wy)



def track_ball(agent, use_estimate = False):
    """ track ball
    Usage: track_ball(player, use_estimate = False):
    """

    ballarr = agent.brain.get_estimated_object_pos_lc(agent.brain.BALL, agent.brain.AF_ANY)
    selfpos = agent.brain.get_selfpos()

    if len(ballarr) == 0:
        return
    else:
        ballarr[0] = tools.geometry.coord_trans_local_to_global(selfpos, ballarr[0])
    
    ball_lc = tools.geometry.coord_trans_global_to_local(selfpos, ballarr[0])

    current_pan = agent.brain.get_pan_deg()
    distance = tools.geometry.distance(ball_lc)
    if (distance < 400):
        distance = 400
    ratio = 1
    bx, by, bt = ball_lc[0], ball_lc[1], ball_lc[2]
    if ((distance < 600) and (bx > 0)):
        ratio = (distance - 400) / (600 - 400) 
    angle_error = tools.geometry.direction_rad(ball_lc) - math.radians(current_pan) # angle error (rad)
    if math.fabs(angle_error) > math.radians(20):                                   #rad
        dist_angle = (math.radians(current_pan) + angle_error) * ratio              #rad
        if (math.degrees(dist_angle) != current_pan):
            agent.effector.set_pan_deg(math.degrees(dist_angle))
   
def in_kickarea_x(kick_conf, ballpos):
    bx, by, bt = ballpos
    return 0 < bx < kick_conf.kick_forward

def in_kickarea_y(kick_conf, ballpos):
    bx, by, bt = ballpos

    right_far   = kick_conf.kick_right_far - 30
    right_close = kick_conf.kick_right_close + 30
    left_far    = kick_conf.kick_left_far + 30
    left_close  = kick_conf.kick_left_close - 30

    return (right_far < by < right_close) or (left_close < by < left_far)

def in_kickarea(kick_conf, ballpos):
    return in_kickarea_x(kick_conf, ballpos) and in_kickarea_y(kick_conf, ballpos)

def calc_approach_pos(ballpos, goalpos, dist):
    """ calculate the position to approach the ball
    Usage: calc_approach_pos(ballpos, goalpos, dist)
    input
        ballpos: global position of ball (x, y, the)
        goalpos: global position of goal (x, y, the)
        dist: distance from the ball
    output
        global position to approach (x, y, the)
    """
    
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

    return (dx, dy, dt)                                                         # return global position to approach (x, y, the)


