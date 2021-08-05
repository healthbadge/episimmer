
def write_agents(filename,n):
	header='Agent Index'

	f=open(filename,'w')
	f.write(str(n)+'\n')
	f.write(header+'\n')

	for i in range(n):
		f.write(str(i)+'\n')

number_of_agents=1344
write_agents('agents.txt',number_of_agents)
