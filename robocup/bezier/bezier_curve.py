import math
import numpy as np
import matplotlib.pyplot as plt


def quadraticBezier(ps, pc, pt):
	x0 ,y0 = ps #start point
	x1, y1 = pc #control point
	x2, y2 = pt #target point
	
	xf = []
	yf = []

	for t in np.linspace(0,1): #0<t<1
		xf.append(math.pow(1-t,2)*x0+(1-t)*2*t*x1+t*t*x2)
		yf.append(math.pow(1-t,2)*y0+(1-t)*2*t*y1+t*t*y2)

	return xf, yf


def cubicBezier(ps, pc1, pc2, pt):
	x0 ,y0 = ps	 #start point
	x1, y1 = pc1 #control point 1
	x2, y2 = pc2 #control point 2
	x3, y3 = pt  #target point

	xf = []
	yf = []
	for t in np.linspace(0,1):
		xf.append(math.pow(1-t,3)*x0+math.pow(1-t,2)*3*t*x1+(1-t)*3*t*t*x2+t*t*t*x3)
		yf.append(math.pow(1-t,3)*y0+math.pow(1-t,2)*3*t*y1+(1-t)*3*t*t*y2+t*t*t*y3)

	return xf, yf

def passthroughpoint(p0, p1, p2): #Return control point necessary to pass through point p
	x0 ,y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	
	cpx = x1 * 2 - (x0 + x2) / 2
	cpy = y1 * 2 - (y0 + y2) / 2

if __name__ == '__main__':
	plt.xlim(0,100)
	plt.ylim(0,100)
	plt.grid(True)

	ps = (10,10)
	pt = (90, 50)
	pc = (50,90)
	
	x,y = quadraticBezier(ps, pc, pt)
	x2, y2 = cubicBezier(ps,pc, (70,30), pt)

	plt.plot(x,y, 'bo')
	plt.plot(x2, y2, 'go')

	plt.plot(10,10, 'ro')
	plt.plot(90,50, 'ro')
	plt.plot(50,90, 'ro')
	plt.plot(70,30, 'ro')
	plt.show()
	
