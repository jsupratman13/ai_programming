################################
# @file htn.py                 #
# @brief HTN Planner core      #
# @author Joshua Supratman     #
# @date 2017/09/07             #
################################

import copy

class WorldState(object):
    def __init__(self, *args):
        self.define_status = args
        self.current_state = None

    def set_initialstate(self, **kwargs):
        if len(kwargs) != len(self.define_status): assert False, "number of initial state does not match with WorldState"
        for state in kwargs:
            if state not in self.define_status:
                assert False, "initial state does not match with WorldState"
        self.current_state = kwargs 

class CompoundTask(object):
    def __init__(self, name):
        self.name = name
        self.method_list = []
    
    def set_method_list(self, *args):
        self.method_list = args

    class Method(list):
        def __init__(self, name):
            self.name = name
            self.preconditions = None
            self.subtask = []

        def set_precondition(self, **kwargs):
            self.preconditions = kwargs

        def set_subtask(self, *args):
            self.subtask = args

class PrimitiveTask(list):
    def __init__(self, name):
        self.name = name
        self.preconditions = None
        self.effects = None

    def set_precondition(self, **kwargs):
        self.preconditions = kwargs
    
    def set_effects(self, **kwargs):
        self.effects = kwargs

class DecompHistory(list):
    def __init__(self):
        self.history_list = []

    class RecordHistory(list):
        def __init__(self, current_task, other_methods, task_list, working_state, plans, mtr):
            current_task.method_list = other_methods
            self.last_recorded_task_list = [current_task]
            self.last_recorded_task_list.extend(task_list)
            self.last_recorded_working_state = copy.deepcopy(working_state)
            self.last_recorded_plans = plans
            self.last_mtr = mtr

    def RestoreHistory(self):
        return self.history_list

class Planner(object):
    def __init__(self):
        self.__working_state = None
        self.decomphistory = DecompHistory()

    def process(self, world, root_task):
        print '\ninitial status: ', 
        for status in world.current_state.iteritems():
            print status,   
        
        print '\n\ngenerating plan:'
        plan, mtr = self._plan(world, root_task)
        
        print 'method to reconsider: ' + str(mtr)

        if plan is None:
            assert False, "no plan could be generated"
        
        return plan
    
    def condition_met(self, method):
        for precondition in method.preconditions.iteritems():
            if precondition not in self.__working_state.current_state.iteritems():
                return False
        return True

    def _plan(self, world, root_task):
        method_list = []
        opt_plan = []
        task_list = [root_task]
        self.__working_state = copy.deepcopy(world)
        mtr = 0

        while task_list:
            current_task = task_list.pop(0)
            if str(current_task.__class__.__name__) == 'CompoundTask':
                method_list = [method for method in current_task.method_list if self.condition_met(method)]
                
                if method_list:
                    m = method_list.pop(0)
                    mtr = next(i for i, method in enumerate(current_task.method_list) if method.name == m.name) 
                    history = self.decomphistory.RecordHistory(current_task, method_list, task_list, self.__working_state, opt_plan, mtr)
                    task_list[0:0] = m.subtask
                    self.decomphistory.history_list.append(history)

                else:
                    history_list = self.decomphistory.RestoreHistory()
                    if history_list:
                        history = history_list.pop()
                        task_list = history.last_recorded_task_list
                        self.__working_state= history.last_recorded_working_state
                        opt_plan = history.last_recorded_plans
                        mtr = history.last_mtr
                    else:
                        return None
                
            elif str(current_task.__class__.__name__) == 'PrimitiveTask':
                if self.condition_met(current_task):
                    self.__working_state.current_state.update(current_task.effects)
                    opt_plan.append(current_task)
                
                else:
                    history_list= self.decomphistory.RestoreHistory()
                    history = history_list.pop()
                    task_list = history.last_recorded_task_list
                    self.__working_state = history.last_recorded_working_state
                    opt_plan = history.last_recorded_plans
                    mtr = history.last_mtr
            else:
                assert False, 'Unknown Task Type'
        
        return opt_plan, mtr
