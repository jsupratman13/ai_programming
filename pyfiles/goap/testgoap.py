import math, sys, traceback
from goap import World, ActionList, Planner

def main():
	pass

if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print traceback.format_exc()
		print 'Exception: '+str(e)
	except KeyboardInterrupt:
		sys.exit()
