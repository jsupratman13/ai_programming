import csp
import task.root
import time,sys
import rcl
from tools.decorator import classproperty

class DummyFieldProperties(rcl.StaticFieldProperties):
	@classproperty
	def ENEMY_GOAL_POLE_GL(cls):
		return [(4500, 750, 0), (4500, -750, 0)]

	@classproperty
	def OUR_GOAL_POLE_GL(cls):
		return[(-4500, -750, 0), (-4500, 750, 0)]

	@classproperty
	def ENEMY_GOAL_GL(cls):
		return (5000, 0, 0)

	@classproperty
	def OUR_GOAL_GL(cls):
		return (-5000,0,0)

	@classproperty
	def NUM_PLAYERS(cls):
		return 6

if __name__ == '__main__':
	agent = rcl.SoccerAgent(lambda: DummyFieldProperties())
	root = task.root.Root
	soccer = csp.SoccerStrategy(agent)	

	try:
		agent.brain.set_selfpos((1000,0,0))
		soccer.execute(root)

#	except Exception, e:
#		agent.brain.debug_log_ln('Exception: '+str(e))
#		time.sleep(1)
#		agent.effector.cancel()
#		agent.terminate()
#		time.sleep(1)

	except (KeyboardInterrupt, SystemExit):
		agent.terminate()
	
