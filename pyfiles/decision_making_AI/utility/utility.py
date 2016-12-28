import math

class WorldState(object):
    def __init__(self, *args):
        self.define_status = args
        self.current_state = None

    def set_initialstate(self, **kwargs):
        if len(kwargs) != len (self.define_status) : assert False, 'number of initial state does not match with WorldState'
        for state in kwargs:
            if state not in self.define_status:
                assert False, 'initial state not found in WorldState'
        self.current_state = kwargs
    
    def update_status(self, worldstate):
        pass

class Action(object):
    def __init__(self, name):
        self.name = name
        self.u_type = 0
        self.status_name = None
        self.utility_list = []

    def set_utility(self, status_name, u_func):
        utility = self.Utility(status_name, u_func)
        self.utility_list.append(utility)

    class Utility:
        def __init__(self, name, func_type=0):
            self.name = name
            self.func_type = func_type

        def get_utility(self, status):
            if self.func_type == 1:
                return (-10*status) +100
            elif self.func_type == 2:
                return 100/(1+math.exp(0.1*(status-49)))
            elif self.func_type == 3:
                return 200/(1+math.exp(0.1*status))
            else:
                assert False, 'no utility function set'

