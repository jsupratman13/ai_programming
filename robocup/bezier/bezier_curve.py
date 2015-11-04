import math
import numpy as np
import matplotlib.pyplot as plt

def quadraticBezier(ps, pt, pc):
	x0 ,y0 = ps #start point
	x1, y1 = pc #control point
	x2, y2 = pt #target point
	
	xf = []
	yf = []

	for t in np.linspace(0,1): #0<t<1
		xf.append(math.pow(1-t,2)*x0+(1-t)*2*t*x1+t*t*x2)
		yf.append(math.pow(1-t,2)*y0+(1-t)*2*t*y1+t*t*y2)

	return xf, yf

def cubicBezier(ps, pt, pc1, pc2):
	x0 ,y0 = ps  #start point
	x1, y1 = pc1 #control point 1
	x2, y2 = pc2 #control point 2
	x3, y3 = pt  #target point

	xf = []
	yf = []
	for t in np.linspace(0,1):
		xf.append(math.pow(1-t,3)*x0+math.pow(1-t,2)*3*t*x1+(1-t)*3*t*t*x2+t*t*t*x3)
		yf.append(math.pow(1-t,3)*y0+math.pow(1-t,2)*3*t*y1+(1-t)*3*t*t*y2+t*t*t*y3)

	return xf, yf

def BezierCurve(ps, pt, *args):
	if len(args) == 1:
		pc = args[0]
		return quadraticBezier(ps,pt,pc)
	if len(args) == 2:
		pc1 = args[0]
		pc2 = args[1]
		return cubicBezier(ps, pt, pc1, pc2)
	xf = []
	yf = []
	n = len(args)
	for i in range(0,n-1):
		p0 = args[i]
		p1 = args[i+1]
		x,y = quadraticBezier(ps, midpoint(p0, p1), p0)
		for xi in x:
			xf.append(xi)
		for yi in y:
			yf.append(yi)
		ps = midpoint(p0, p1)
	x,y = quadraticBezier(ps, pt, args[n-1])
	for xi in x:
		xf.append(xi)
	for yi in y:
		yf.append(yi)
	return xf, yf

def midpoint(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	midx = (x1 + x2) / 2
	midy = (y1 + y2) / 2
	return midx, midy

def passthroughpoint(ps, pt, pc): #new control point necessary to pass through point pc
	x0 ,y0 = ps	#start point
	x1, y1 = pc #pass through point
	x2, y2 = pt #target point
	
	cpx = x1 * 2 - (x0 + x2) / 2
	cpy = y1 * 2 - (y0 + y2) / 2
	return cpx,cpy

def controlpoint2(ps, pt):
	x0, y0, th0 = ps
	x1, y1, th1 = pt
	
	d1 = 1000	#Parameter polygon
	d2 = 1000

	xf1 = x0 + d1*math.cos(th0)
	yf1 = y0 + d1*math.sin(th0)

	xf2 = x1 + d2*math.cos(math.pi+th1)
	yf2 = y1 + d2*math.sin(math.pi+th1)

	pc1 = (xf1, yf1)
	pc2 = (xf2, yf2)

	return pc1, pc2

if __name__ == '__main__':
	plt.xlim(-5000,5000)
	plt.ylim(-3200,3200)
	plt.grid(True)

	pt = (0,0)
	ps = (-3000, 0)
	pc1, pc2 = controlpoint2((-3000,0,math.pi/2),(0,0,0))

	x, y = BezierCurve(ps, pt, pc1, pc2)

	plt.plot(x,y ,'b-')
	plt.plot(ps[0], ps[1], 'ro', pt[0], pt[1], 'ro', pc1[0], pc1[1], 'go', pc2[0], pc2[1], 'go')
	plt.show()
	
