import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as itp

def test():
	x,y = random_coordinate(3)

	plt.plot(x,y, 'ro')
	print x,y	
	
	#baycentric langrange
	interpo1 = itp.BarycentricInterpolator(x,y) 
	#Krogh
	#interpo2 = itp.KroghInterpolator(x,y)
	xnew = np.arange(-20,20, 0.1)
	ynew = interpo1(xnew)

	plt.plot(xnew, ynew, 'b-')

def random_coordinate(coordinate):
	datax = []
	datay = []
	for n in range(0,coordinate):
		datax.append(np.random.random_integers(1,10))
		datay.append(np.random.random_integers(1,10))
	return datax, datay

def plotfunc():
	plt.xlim(0,10)
	plt.ylim(0,100)
	plt.grid(True)

	x = np.linspace(0.0, 10.0)
	y = x**2

	plt.plot(x,y, 'ro')

if __name__ == '__main__':
	plt.xlim(-20,20)
	plt.ylim(-20,20)
	plt.grid(True)
	test()
	plt.show()
