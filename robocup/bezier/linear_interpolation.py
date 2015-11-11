import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as itp

def test():
	coord = [(0,0),(10,11),(20,25),(30,40),(31,41),(50,50)]

	x = []
	y = []
	for point in coord:
		plt.plot(point[0],point[1], 'ro')
		x.append(point[0])
		y.append(point[1])
		print point	
	
	#baycentric langrange
	interpo1 = itp.BarycentricInterpolator(x,y) 
	#Krogh
	#interpo2 = itp.KroghInterpolator(x,y)
	xnew = np.arange(-10,60, 0.1)
	ynew = interpo1(xnew)

	plt.plot(xnew, ynew, 'b-')
	
	coefficient1 = np.polyfit(x,y,3)
	coefficient2 = np.polyfit(x,y,4)

	func1 = np.poly1d(coefficient1)
	func2 = np.poly1d(coefficient2)
	
	ynew1 = func1(xnew)
	ynew2 = func2(xnew)

	plt.plot(xnew, ynew1, 'r-',xnew, ynew2, 'g-')


def random_coordinate(coordinate):
	datax = []
	datay = []
	for n in range(0,coordinate):
		datax.append(np.random.random_integers(1,10))
		datay.append(np.random.random_integers(1,10))
	return datax, datay

def plotfunc():
	plt.xlim(-10,60)
	plt.ylim(-10,60)
	plt.grid(True)

	x = np.linspace(0.0, 10.0)
	y = x**2

	plt.plot(x,y, 'ro')

if __name__ == '__main__':
	plt.xlim(-10,60)
	plt.ylim(-10,60)
	plt.grid(True)
	test()
	plt.show()
