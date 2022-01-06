import sys

def write_agents(filename,n):
	header='Agent Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(1, n + 1):
		f.write(str(i-1)+'\n')

def write_interactions(filename, n, k):
	header = 'Agent Index:Interacting Agent Index'

	f = open(filename, 'w')
	# k*n*(n - 1)
	f.write(str(2*(k*2*n*(n - 1) + n*n*(k-1)))+'\n')
	f.write(header+'\n')

	for l in range(k):
		for i in range(n*n):
			if l != k-1:
				f.write(str(i+l*n*n) + ':' + str(i +(l+1)*n*n) + '\n')
				f.write(str(i+(l+1)*n*n) + ':' + str(i +l*n*n) + '\n')

			if i<n*n-n:
				f.write(str(i+l*n*n) + ':' + str(i+l*n*n+n) + '\n')
				f.write(str(i+l*n*n+n) + ':' + str(i+l*n*n) + '\n')

			if (i+1) % n != 0:
				f.write(str(i+l*n*n) + ':' + str(i+l*n*n+1) + '\n')
				f.write(str(i+l*n*n+1) + ':' + str(i+l*n*n) + '\n')

	f.close()

# n x n x k agents
n = int(sys.argv[1])
k = int(sys.argv[2])

no_of_agents = k*n*n
write_agents('agents.txt', no_of_agents)
write_interactions('interactions.txt', n, k)
