import math
import numpy as np


#TODO: save control point
def quadraticBezier(p0, p1, p2, p3, t):
	x0 ,y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	x3, y3, z3 = p3

	xf = math.pow(1-t,2)*x0+(1-t)*2*t*x1+t*t*x2
	yf = math.pow(1-t,2)*y0+(1-t)*2*t*y1+t*t*y2
	zf = 0

	return (xf, yf, zf) 

#TODO: save control point
def cubicBezier(p0, p1, p2, p3, t):
	x0 ,y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	x3, y3, z3 = p3
	
	xf = math.pow(1-t,3)*x0+math.pow(1-t,2)*3*t*x1+(1-t)*3*t*t*x2+t*t*t*x3
	yf = math.pow(1-t,3)*y0+math.pow(1-t,2)*3*t*y1+(1-t)*3*t*t*y2+t*t*t*y3
	zf = 0

	return(xf, yf, zf)

def passthroughpoint(p0, p1, p2): #Return control point necessary to pass through point p
	x0 ,y0, z0 = p0
	x1, y1, z1 = p1
	x2, y2, z2 = p2
	
	cpx = x1 * 2 - (x0 + x2) / 2
	cpy = y1 * 2 - (y0 + y2) / 2
