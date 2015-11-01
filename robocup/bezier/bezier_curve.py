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

if __name__ == '__main__':
	plt.xlim(0,100)
	plt.ylim(0,100)
	plt.grid(True)

	ps = (10,10)
	pt = (90, 50)
	pc = (50,90)
	pc2 = (70,30)
	cx, cy = passthroughpoint(ps, pt, pc)

#	x3, y3 = quadraticBezier(ps, pt ,(cx,cy))
	x4, y4 = BezierCurve(ps,pt,pc, pc2)
	x, y = BezierCurve(ps, pt, (30,70), (50, 30),(70,90))

	plt.plot(x,y ,'b-')
#	plt.plot(x3, y3, 'ko')
	plt.plot(x4, y4, 'r-')
	print x
	plt.plot(10,10, 'ro')
	plt.plot(90,50, 'ro')
	plt.plot(70,90, 'ro')
	plt.plot(50,30, 'ro')
	plt.plot(30,70, 'ro')
	plt.show()
	
