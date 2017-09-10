################################
# @file goap.py                #
# @brief GOAP core             #
# @author Joshua Supratman     #
# @date 2017/09/07             #
################################

import copy

class WorldState(object):
    def __init__(self, *args):
        self.define_status = args
        self.goal_state = None
        self.current_state = None

    def set_initialstate(self, **kwargs):
        if len(kwargs) != len(self.define_status): assert False, "number of initial state does not match with WorldState"
        for state in kwargs:
            if state not in self.define_status:
                assert False, "initial state does not match with WorldState"
        self.current_state = kwargs
    
    def set_goalstate(self, **kwargs):
        for state in kwargs:
            if state not in self.define_status:
                assert False, "goal state does not correspond with WorldState"  
        self.goal_state = kwargs

class Action(object):
    def __init__(self,name, cost):
        self.name = name
        self.precondition = None
        self.effects = None
        self.cost = cost
    
    def set_precondition(self, **kwargs):
        self.precondition = kwargs
    
    def set_effects(self, **kwargs):
        self.effects = kwargs

class Planner(object):
    def __init__(self):
        self.action_list = None
        
    def process(self, world, action_list):
        print '\ninitial status: ', 
        for status in world.current_state.iteritems():
            print status,
        
        print '\ngoal: ', 
        for goal in world.goal_state.iteritems():
            print goal,
        
        print '\n\ngenerating plan:'
        self.action_list = action_list
        plan = self._plan(world.current_state, world.goal_state)
        
        if plan is None:
            assert False, "no plan could be generated"
    
        return plan

    def _plan(self, working_state, goal_state):
        diff_set = list(set(goal_state) - set(working_state.items()))
        subgoal = [key for key in diff_set if goal_state[key] != working_state[key]]

        if len(subgoal) == 0:
            return []

        plan_list = []
        action = []
        for act in self.action_list:
            for goal in subgoal:
                if goal in act.effects and goal_state[goal] == act.effects[goal]:
                    action.append(act)
        
        for realize in action:
            plan = self._plan(working_state, realize.precondition)
            if plan is None:
                continue
            else:
                plan += [realize]

            intermediate_working_state = copy.deepcopy(working_state)
            for act in plan:
                intermediate_working_state.update(act.effects)
            
            assert(intermediate_working_state is not None)
            sub_plan = self._plan(intermediate_working_state, goal_state)

            if sub_plan is None:
                continue
            else:
                plan_list += [plan + sub_plan]

        opt_plan = None
        if len(plan_list) >= 2:
            min_cost = 1000
            for plan in plan_list:
                cost = 0
                for act in plan:
                    cost += act.cost + 1 
                if cost <= min_cost:
                    min_cost = cost
                    opt_plan = plan
        
        elif len(plan_list) == 1:
            opt_plan = plan_list[0]
        
        return opt_plan
    
