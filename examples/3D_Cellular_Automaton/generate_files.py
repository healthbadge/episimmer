import sys

def write_agents(filename,n):
	header='Agent Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(1, n + 1):
		f.write(str(i)+'\n')

def write_interactions(filename, n):
	header = 'Agent Index:Interacting Agent Index'

	f = open(filename, 'w')
	f.write(str(8*n*(n - 1) + 2*n*n)+'\n')
	f.write(header+'\n')

	for i in range(1, n*n + 1):
		f.write(str(2*i) + ':' + str(2*i - 1) + '\n')
		f.write(str(2*i - 1) + ':' + str(2*i) + '\n')

		if i%n != 1:
			f.write(str(2*i) + ':' + str(2*i - 2) + '\n')
			f.write(str(2*i - 1) + ':' + str(2*i - 3) + '\n')

		if i%n != 0:
			f.write(str(2*i) + ':' + str(2*i + 2) + '\n')
			f.write(str(2*i - 1) + ':' + str(2*i + 1) + '\n')

		if 1 <= 2*i - 2*n <= 2*n*n:
			f.write(str(2*i) + ':' + str(2*i - 2*n) + '\n')
		if 1 <= 2*i + 2*n <= 2*n*n:
			f.write(str(2*i) + ':' + str(2*i + 2*n) + '\n')
		if 1 <= 2*i - 1 - 2*n <= 2*n*n:
			f.write(str(2*i-1) + ':' + str(2*i - 1 - 2*n) + '\n')
		if 1 <= 2*i - 1 + 2*n <= 2*n*n:
			f.write(str(2*i - 1) + ':' + str(2*i - 1 + 2*n) + '\n')

	f.close()

n = int(sys.argv[1])
no_of_agents = 2*n*n
write_agents('agents.txt', no_of_agents)
write_interactions('interactions.txt', n)
