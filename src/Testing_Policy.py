import random
from Policy import Agent_Policy
import copy
from functools import partial
from collections import deque
import json

class Result():

	def __init__(self, result, agents, machine_name, time_step):
		self.result = result
		self.agents = agents
		self.machine_name = machine_name
		self.time_step = time_step

	def get_machine_name(self):
		return self.machine_name

	def get_result(self):
		return self.result

	def get_num_agents(self):
		return len(self.agents)


class Machine():

	def __init__(self, machine_name, cost, false_positive_rate, false_negative_rate, turnaround_time, capacity):
		self.machine_name = machine_name
		self.cost = cost
		self.false_positive_rate = false_positive_rate
		self.false_negative_rate = false_negative_rate
		self.true_positive_rate = 1 - self.false_negative_rate
		self.true_negative_rate = 1 - self.false_positive_rate
		self.turnaround_time = turnaround_time
		self.capacity = capacity
		self.testtubes = []
		self.results = []
		self.available = True
		self.start_step = None


	def is_running(self):
		if(not self.available):
			return True

		return False

	def is_full(self):
		if(len(self.testtubes)>=self.capacity):
			return True

		return False

	def is_empty(self):
		if(len(self.testtubes)==0):
			return True

		return False

	def has_empty_results(self):
		if(len(self.results)==0):
			return True

		return False

	def reset_machine(self):
		self.testtubes = []
		self.results = []
		self.available = True

	def register_testtube(self,testtube):
		testtube.set_in_machine(True)
		self.testtubes.append(testtube)

	def run_tests(self, infected_states, time_step):
		self.available = False
		self.start_step = time_step

		for testtube in self.testtubes:
		    self.run_single_test(testtube,infected_states)

	def run_single_test(self, testtube, infected_states):
		result = "Negative"

		for agent in testtube.agents_test:
			if(agent.state in infected_states):
				result="Positive"
				break

		if(result=="Negative"):
			if(random.random()>self.true_negative_rate):
				result = "Positive"
		else:
			if(random.random()>self.true_positive_rate):
				result = "Negative"

		testtube.set_result(result)

	def populate_machine_results(self,time_step):
		if(time_step - self.start_step>=self.turnaround_time):
			for testtube_with_result in self.testtubes:
				result_obj = Result(testtube_with_result.testtube_result, testtube_with_result.agents_test, self.machine_name, time_step)
				testtube_with_result.set_in_machine(False)
				self.results.append(result_obj)

	def get_results(self):
		return self.results

	def get_machine_name(self):
		return self.machine_name



class Testtube():

	def __init__(self):
		self.agents_test = []
		self.testtube_result = None
		self.in_machine = False

	def register_agent(self,agent):
		self.agents_test.append(agent)

	def get_num_agents(self):
		return len(self.agents_test)

	def set_result(self, result):
		self.testtube_result = result

	def set_in_machine(self, bool_val):
		if(bool_val):
			self.in_machine = bool_val
		else:
			self.in_machine = bool_val
			self.agents_test = []
			self.testtube_result = None

	def is_empty(self):
		if(len(self.agents_test)==0):
			return True

		return False

	def is_in_machine(self):
		return self.in_machine


class Test_Policy(Agent_Policy):

	def __init__(self, agents_per_step_fn=None):
		super().__init__()
		self.policy_type = 'Testing'
		self.register_agent_testtube_func = None
		self.cur_testtubes = None
		self.ready_queue = deque()
		self.machine_list = []
		self.statistics = {}
		self.current_machines = {}

		assert callable(agents_per_step_fn)
		self.agents_per_step_fn = agents_per_step_fn

	def enact_policy(self,time_step,agents,locations,model):
		self.new_time_step(time_step)
		if(len(self.cur_testtubes)<1):
			self.register_agent_testtube_func(agents, time_step)
			self.add_partial_to_ready_queue()
		self.register_testtubes_to_machines(time_step)
		self.run_tests(model,time_step)
		self.populate_results_in_machine(time_step)
		self.release_results(time_step)
		self.end_time_step(time_step)


	def initialize_statistics_logs(self,time_step):
		self.statistics[time_step] = {'Total Tests':0, 'Total Positive Results':0,\
		 								'Total Negative Results':0, 'Total Agents Tested':0}

		for machine_name in self.current_machines.keys():
			self.statistics[time_step][machine_name] = {'Number of Tests':0, 'Number of Positive Results':0,\
														'Number of Negative Results':0, 'Number of Agents Tested':0}

	def new_time_step(self,time_step):
		self.initialize_statistics_logs(time_step)
		self.initialize_process_logs(time_step)
		self.cur_testtubes = []
		self.num_agents_to_test = self.agents_per_step_fn(time_step)

	def add_machine(self, machine_name, cost, false_positive_rate, false_negative_rate, turnaround_time, capacity, num=1):
		if(machine_name in self.current_machines.keys()):
			if([cost, false_positive_rate, false_negative_rate, turnaround_time, capacity]==self.current_machines[machine_name]['parameters']):
				self.current_machines[machine_name]['number']+=num

				for i in range(num):
					self.machine_list.append(Machine(machine_name, cost, false_positive_rate, false_negative_rate, turnaround_time, capacity))

			else:
				print("Error! Machine name with different parameters already exists")
		else:
			self.current_machines[machine_name] = {'parameters':[cost, false_positive_rate, false_negative_rate, turnaround_time, capacity],\
													'number':num}

			for i in range(num):
				self.machine_list.append(Machine(machine_name, cost, false_positive_rate, false_negative_rate, turnaround_time, capacity))


	def set_register_agent_testtube_func(self,fn):
		self.register_agent_testtube_func = fn


	def random_agents(self, num_agents_testtube=1, num_testtubes_per_agent=1, attribute=None, value_list=[]):
		assert isinstance(value_list,list)
		return partial(self.full_random_agents, num_agents_testtube, num_testtubes_per_agent, attribute, value_list)


	def full_random_agents(self, num_agents_testtube, num_testtubes_per_agent, attribute, value_list, agents, time_step):
		agents_copy = copy.copy(list(agents))
		random.shuffle(agents_copy)

		# Get agents for test
		agents_to_test = []
		for agent in agents_copy:

			if(len(agents_to_test)==self.num_agents_to_test):
				break

			elif(attribute is None or agent.info[attribute] in value_list):
				agents_to_test.append(agent)

		# Create testtubes based on formula - int((ntpa x no. of agents + napt -1)/napt)
		num_testtubes = int((num_testtubes_per_agent*self.num_agents_to_test + num_agents_testtube -1)/num_agents_testtube)
		for _ in range(num_testtubes):
			testtube = Testtube()
			self.cur_testtubes.append(testtube)

		# Assign agents to testtubes
		for agent in agents_to_test:
			if(len(self.cur_testtubes)>0):
				cur_list = random.sample(self.cur_testtubes, min(num_testtubes_per_agent,len(self.cur_testtubes)))

				for testtube in cur_list:
					testtube.register_agent(agent)

					if(len(testtube.agents_test)>=num_agents_testtube):
						self.ready_queue.append(testtube)
						self.cur_testtubes.remove(testtube)
			else:
				break


	def add_partial_to_ready_queue(self):
		copy_testtubes = copy.deepcopy(self.cur_testtubes)
		for testtube in self.cur_testtubes:
			if(not testtube.is_empty()):
				self.ready_queue.append(testtube)
				copy_testtubes.remove(testtube)

		self.cur_testtubes = copy_testtubes

	def register_testtubes_to_machines(self,time_step):
		for machine in self.machine_list:
			while(self.ready_queue):
				if(machine.is_running() or machine.is_full()):
					break

				else:
					testtube = self.ready_queue.popleft()
					machine.register_testtube(testtube)

	def run_tests(self,model,time_step):
		for machine in self.machine_list:
			if(not machine.is_empty() and not machine.is_running()):
				machine.run_tests(model.infected_states,time_step)



	def populate_results_in_machine(self, time_step):
		for machine in self.machine_list:
			if(machine.is_running()):
				machine.populate_machine_results(time_step)

	def release_results_to_agents(self,results):
		for result_obj in results:
			for agent in result_obj.agents:
				self.update_agent_policy_history(agent,result_obj)

	def release_results_to_policy(self,results,time_step):
		for result_obj in results:
			machine_name = result_obj.get_machine_name()
			self.statistics[time_step][machine_name]['Number of Tests'] += 1
			self.statistics[time_step]['Total Tests'] +=1

			if(result_obj.get_result()=='Positive'):
				self.statistics[time_step][machine_name]['Number of Positive Results'] +=1
				self.statistics[time_step]['Total Positive Results'] += 1

			elif(result_obj.get_result()=='Negative'):
				self.statistics[time_step][machine_name]['Number of Negative Results'] +=1
				self.statistics[time_step]['Total Negative Results'] += 1

			self.statistics[time_step][machine_name]['Number of Agents Tested'] += result_obj.get_num_agents()
			self.statistics[time_step]['Total Agents Tested'] += result_obj.get_num_agents()


	def release_results(self,time_step):
		results = []
		for machine in self.machine_list:
			if(not machine.has_empty_results()):
				results += machine.get_results()
				machine.reset_machine()

		self.release_results_to_agents(results)
		self.release_results_to_policy(results, time_step)


	def initialize_process_logs(self,time_step):
		self.statistics[time_step]["Process"] = {}
		for machine_name in self.current_machines.keys():
			self.statistics[time_step]["Process"][machine_name] = {}

		for machine in self.machine_list:
			machine_name = machine.get_machine_name()
			self.statistics[time_step]["Process"][machine_name][machine.__str__()] = {'Running Status':'On Standby', 'Filled Status':'Empty'}

		self.statistics[time_step]["Process"]["All Testubes filled"] = 'Default'
		self.statistics[time_step]["Process"]["All Testubes in machine"] = 'Default'
		self.statistics[time_step]["Process"]["All Machines running"] = 'Default'
		self.statistics[time_step]["Process"]['Ready Queue Length'] = -1


	def update_process_logs(self, time_step):
		for machine in self.machine_list:
			machine_name = machine.get_machine_name()

			if(machine.is_running()):
				self.statistics[time_step]["Process"][machine_name][machine.__str__()]['Running Status'] = 'Running'
			else:
				self.statistics[time_step]["Process"][machine_name][machine.__str__()]['Running Status'] = 'On Standby'

			if(machine.is_empty()):
				self.statistics[time_step]["Process"][machine_name][machine.__str__()]['Filled Status'] = 'Empty'
			elif(machine.is_full()):
				self.statistics[time_step]["Process"][machine_name][machine.__str__()]['Filled Status'] = 'Completely Filled'
			else:
				self.statistics[time_step]["Process"][machine_name][machine.__str__()]['Filled Status'] = 'Partly filled'

		all_testtubes_filled = True
		all_testtubes_in_machines = True
		all_machines_running = True

		if(len(self.cur_testtubes)!=0):
			all_testtubes_filled = False

		if(self.ready_queue):
			all_testtubes_in_machines = False

		for machine in self.machine_list:
			if(not machine.is_running()):
				all_machines_running = False
				break

		self.statistics[time_step]["Process"]['All Testubes filled'] = all_testtubes_filled
		self.statistics[time_step]["Process"]['All Machines running'] = all_machines_running
		self.statistics[time_step]["Process"]['All Testubes in machine'] = all_testtubes_in_machines
		self.statistics[time_step]["Process"]['Ready Queue Length'] = len(self.ready_queue)

	def end_time_step(self, time_step):
		self.update_process_logs(time_step)
		with open("testing_stats.json", "w") as outfile:
			json.dump(self.statistics, outfile,indent=4)
