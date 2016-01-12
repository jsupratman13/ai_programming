import ccl
import time

if __name__ == '__main__':
	soccer = ccl.SoccerStrategy()

	initial_time = time.time()

	#while time.time() - initial_time < 3:
	soccer.run(initial_time)
	
