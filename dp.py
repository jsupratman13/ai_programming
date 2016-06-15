import numpy as np
import math, sys,copy,time

class FileSystem(object):
	def __init__(self):
		self.name = None
		self.word = None
		self.data = None
		self.frame_length=None
	def read_para(self,folder, num):
		num = '%003d' % num
		filename = str(folder)+'/'+str(folder)+'_'+str(num)+'.txt'
		try:
			with open(filename, 'r') as f:
				f.seek(0)
				self.name = f.readline().rstrip()
				self.word = f.readline().rstrip()
				self.frame_length = int(f.readline())
				for line in f:	
					rect = []
					rect.append([float(x) for x in line.split()])
					if self.data is None:
						self.data = np.array(rect)
					else:
						self.data = np.append(self.data, rect, axis=0)

		except IOError:
			print >> sys.stderr, 'cannot open "%s"' %filename
			sys.exit(1)

	def np_read(self, folder, num):
		num = '%003d' % num
		filename = str(folder)+'/'+str(folder)+'_'+str(num)+'.txt'	
		try:
			with open(filename, 'r') as f:
				f.seek(0)
				self.name = f.readline().rstrip()
				self.word = f.readline().rstrip()
				self.frame_length = int(f.readline())
				f.close()
			self.data = np.loadtxt(filename, skiprows=3, usecols=range(15))
		except IOError:
			print >> sys.stderr, 'cannot open "%S"' %filename
			sys.exit(1)

class DPMatching(object):
	def __init__(self, template, unknown):
		self.template = copy.deepcopy(template)
		self.unknown = copy.deepcopy(unknown)
		self.i = self.template.frame_length
		self.j = self.unknown.frame_length
		self.d = np.zeros([self.i, self.j], dtype=np.float64)
		self.g = np.zeros([self.i, self.j], dtype=np.float64)

	def get_weight(self):
		self.local_dist()
		self.algorithm()
		cost = self.g[self.i-1,self.j-1]
		return (cost/(self.i+self.j))
	
	def local_dist(self):
		t = self.template.data
		u = self.unknown.data
		for i in range(self.i):
			for j in range(self.j):
				for k in range(15):
					self.d[i,j] += math.pow(t[i,k]-u[j,k],2)
				self.d[i,j] = math.sqrt(math.fabs(self.d[i,j]))
	
	def algorithm(self):
		for i in range(self.i):
			for j in range(self.j):
				if i==0 and j==0:
					self.g[0,0] = self.d[0,0]
					#self.g[0,0] = 0
				elif i == 0:
					self.g[i,j] = self.g[i,j-1] + self.d[i,j]
				elif j == 0:
					self.g[i,j] = self.g[i-1,j] + self.d[i,j]
				else:
					hori = self.g[i,  j-1]+   self.d[i,j]
					diag = self.g[i-1,j-1]+(2*self.d[i,j])
					vert = self.g[i-1,j  ]+   self.d[i,j]
					self.g[i,j] = min(hori, diag, vert)

def dp_match(template, unknown):
	t = template.data
	u = unknown.data
	J = template.frame_length
	I = unknown.frame_length
	d = np.zeros([140,140])
	g = np.zeros([140,140])
	for i in range(I):
		for j in range(J):
			for k in range(15):
				d[i,j] += math.pow(u[i,k]-t[j,k],2)
			d[i,j] = math.sqrt(d[i,j])
			#d[i,j] = (d[i,j])**0.5
			if i==0 and j==0:
				g[0,0] = d[0,0]
			elif i == 0:
				g[i,j] = g[i,j-1] + d[i,j]
			elif j == 0:
				g[i,j] = g[i-1,j] + d[i,j]
			else:
				hori = g[i,  j-1]+   d[i,j]
				diag = g[i-1,j-1]+(2*d[i,j])
				vert = g[i-1,j  ]+   d[i,j]
				g[i,j] = min(hori, diag, vert)
	return g[I-1, J-1]/(I+J)

if __name__ == '__main__':
	TEMPLATE = sys.argv[1]
	UNKNOWN  = sys.argv[2]
	template = FileSystem()
	unknown = FileSystem()
	minimum_cost = 0
	count=0
	initial_time = time.time()
	for i in range(100):
#		unknown.read_para(UNKNOWN,i+1)
		unknown.np_read(UNKNOWN, i+1)
		for j in range(100):
#			template.read_para(TEMPLATE, j+1)
			template.np_read(TEMPLATE, i+1)
			dp = DPMatching(template, unknown)
			cost = dp.get_weight()
#			cost = dp_match(template, unknown)
			if j==0 or minimum_cost > cost:
				minimum_cost = cost
				print 'template: '+str(template.name)+ ' ' + str(cost)
				ctemplate = copy.deepcopy(template)
		if unknown.word == ctemplate.word:
			evaluate = 'o'
			count+=1
		else: evaluate = 'x'
		print str(unknown.word) + ' --> ' + str(ctemplate.word) + ' ' + evaluate
		minimum_cost = 0

	print 'total time: '+str(time.time()-initial_time)
	print 'accuracy: '+str(count)+'%'
