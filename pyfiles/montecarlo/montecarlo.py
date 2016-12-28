#Monte Carlo Example
#Finds the Area of Circle with radius 1

import random
import math

total = 1000000.0 #higher means more accuracy but also more time to compute
n = 0;

for i in range(int(total)):
    x = random.uniform(0,1.0)
    y = random.uniform(0,1.0)
    if((x*x+y*y) <= 1.0):
        n+=1;

estimate_pi = (n/total)*4.0
print 'actual: '+str(math.pi) + ' estimate: ' + str(estimate_pi)
