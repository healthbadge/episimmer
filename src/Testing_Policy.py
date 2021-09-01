import random
from Policy import Agent_Policy
import copy
from functools import partial
from collections import deque
import json

class Result():

	def __init__(self, result, agent, machine_name, time_step, machine_start_step, time_step_done):
		self.result = result
		self.agent = agent
		self.machine_name = machine_name
		self.time_step = time_step
		self.machine_start_step = machine_start_step
		self.time_step_done = time_step_done

	def get_machine_name(self):
		return self.machine_name

	def get_result(self):
		return self.result



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
		# In a time_step, a machine can run only once. EDGE CASE : If turnaround_time = 0 and the number of agents to test
		# is greater than capacity, then the machine runs only once in that time step.
		self.testtubes = []
		self.results = []
		self.available = True
		self.start_step = None
		self.machine_cost = 0


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
		self.machine_cost+=self.cost

	def run_tests(self, infected_states, time_step):
		self.available = False
		self.start_step = time_step

		for testtube in self.testtubes:
			self.run_single_test(testtube,infected_states)

	def run_single_test(self, testtube, infected_states):
		result = "Negative"

		for agent in testtube.testtube_agent_dict.keys():
			if(testtube.testtube_agent_dict[agent]["state"] in infected_states):
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
		if(self.run_completed(time_step)):
			for testtube_with_result in self.testtubes:
				self.save_results(testtube_with_result,time_step)
				testtube_with_result.set_in_machine(False)

	def run_completed(self,time_step):
		return time_step - self.start_step>=self.turnaround_time

	def save_results(self, testtube,time_step):
		for agent in testtube.testtube_agent_dict.keys():
			time_step_entered = testtube.testtube_agent_dict[agent]["time_step"]
			result_obj = Result(testtube.testtube_result, agent, self.machine_name, time_step_entered, self.start_step, time_step)
			self.results.append(result_obj)

	def get_results(self):
		return self.results

	def get_machine_name(self):
		return self.machine_name



class Testtube():

	def __init__(self):
		self.testtube_agent_dict = {}
		self.testtube_result = None
		self.in_machine = False

	def register_agent(self,agent,time_step):
		self.testtube_agent_dict[agent] = {"state":agent.state, "time_step":time_step}

	def get_num_agents(self):
		return len(self.testtube_agent_dict)

	def set_result(self, result):
		self.testtube_result = result

	def set_in_machine(self, bool_val):
		if(bool_val):
			self.in_machine = bool_val
		else:
			self.in_machine = bool_val
			self.testtube_agent_dict = {}
			self.testtube_result = None

	def is_empty(self):
		if(len(self.testtube_agent_dict)==0):
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
		self.total_cost=0

		assert callable(agents_per_step_fn)
		self.agents_per_step_fn = agents_per_step_fn

	def reset(self):
		self.statistics = {}
		self.ready_queue = deque()
		for machine in self.machine_list:
			machine.machine_cost = 0
			machine.testtubes = []
			machine.results = []
			machine.available = True
			machine.start_step = None

	def enact_policy(self,time_step,agents,locations,model):

		self.new_time_step(time_step)
		self.populate_results_in_machine(time_step)
		self.release_results(time_step)
		self.register_agent_testtube_func(agents, time_step)
		self.add_partial_to_ready_queue()
		self.register_testtubes_to_machines(time_step)
		self.run_tests(model,time_step)
		self.run_edge_case(time_step)
		self.end_time_step(time_step)

	def run_edge_case(self,time_step):
		# For the case when turnaround_time = 0
		for machine in self.machine_list:
			if not machine.is_empty() and machine.run_completed(time_step):
				self.populate_results_in_machine(time_step)
				self.release_results(time_step)
				break

	def set_register_agent_testtube_func(self,fn):
		self.register_agent_testtube_func = fn


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


	def initialize_statistics_logs(self,time_step):
		self.statistics[time_step] = {'Total Tests':0, 'Total Positive Results':0,\
										'Total Negative Results':0, 'Total Agents Tested':0}

		for machine_name in self.current_machines.keys():
			self.statistics[time_step][machine_name] = {'Number of Tests':0, 'Number of Positive Results':0,\
														'Number of Negative Results':0, 'Number of Agents Tested':0}

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

	def new_time_step(self,time_step):
		self.initialize_statistics_logs(time_step)
		self.initialize_process_logs(time_step)
		self.cur_testtubes = []
		self.num_agents_to_test = self.agents_per_step_fn(time_step)



	def full_random_agents(self, num_agents_per_testtube, num_testtubes_per_agent, attribute, value_list, agents, time_step):
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
		num_testtubes = int((num_testtubes_per_agent*self.num_agents_to_test + num_agents_per_testtube -1)/num_agents_per_testtube)
		for _ in range(num_testtubes):
			testtube = Testtube()
			self.cur_testtubes.append(testtube)

		# Assign agents to testtubes
		for agent in agents_to_test:
			if(len(self.cur_testtubes)>0):
				cur_list = random.sample(self.cur_testtubes, min(num_testtubes_per_agent,len(self.cur_testtubes)))

				for testtube in cur_list:
					testtube.register_agent(agent,time_step)

					if(testtube.get_num_agents()>=num_agents_per_testtube):
						self.ready_queue.append(testtube)
						self.cur_testtubes.remove(testtube)
			else:
				break

	def random_agents(self, num_agents_per_testtube=1, num_testtubes_per_agent=1, attribute=None, value_list=[]):
		assert isinstance(value_list,list)
		return partial(self.full_random_agents, num_agents_per_testtube, num_testtubes_per_agent, attribute, value_list)

	def full_random_agents_CR(self, num_agents_per_testtube, num_testtubes_per_agent, attribute, value_list, agents, time_step):
		agents_copy = copy.copy(list(agents))
		random.shuffle(agents_copy)

		# Get agents for test
		agents_to_test = []
		for agent in agents_copy:
			# print(time_step, self.num_agents_to_test)

			if(len(agents_to_test)==self.num_agents_to_test):
				break

			elif(attribute is None or agent.info[attribute] in value_list):
				if(agent.can_contribute_infection and agent.can_recieve_infection):
					agents_to_test.append(agent)

		# Create testtubes based on formula - int((ntpa x no. of agents + napt -1)/napt)
		num_testtubes = int((num_testtubes_per_agent*self.num_agents_to_test + num_agents_per_testtube -1)/num_agents_per_testtube)
		for _ in range(num_testtubes):
			testtube = Testtube()
			self.cur_testtubes.append(testtube)

		# Assign agents to testtubes
		for agent in agents_to_test:
			if(len(self.cur_testtubes)>0):
				cur_list = random.sample(self.cur_testtubes, min(num_testtubes_per_agent,len(self.cur_testtubes)))

				for testtube in cur_list:
					testtube.register_agent(agent,time_step)

					if(testtube.get_num_agents()>=num_agents_per_testtube):
						self.ready_queue.append(testtube)
						self.cur_testtubes.remove(testtube)
			else:
				break

	def random_agents_CR(self, num_agents_per_testtube=1, num_testtubes_per_agent=1, attribute=None, value_list=[]):
		assert isinstance(value_list,list)
		return partial(self.full_random_agents_CR, num_agents_per_testtube, num_testtubes_per_agent, attribute, value_list)

	def full_random_agents_CR2(self, num_agents_per_testtube, num_testtubes_per_agent, state_list, agents, time_step):
		agents_copy = copy.copy(list(agents))
		random.shuffle(agents_copy)

		# Get agents for test
		agents_to_test = []

		from itertools import cycle

		for agent in cycle(agents_copy):
			# print(time_step, self.num_agents_to_test)

			if(len(agents_to_test)==self.num_agents_to_test):
				break

			else:
				if(time_step<=19 and agent.index in ['201525177', '2019701001', '2019702008', 'I-100757', '66O', '39O', '83F', '129F', '43F', '160O', '201456113', '92F', '2018102003', '20171405', '62F', '201356193', '175O', '20171172', '2018122007', '2018111027', '202020100', '202012014', '211O', '130O', '229O', '200999003', '21F', '119O', '95O', '133O', '73O', '23O', '2018101101', '115O', 'I-100763', '58F', '147F', '153F', '191O', '93F', '201502183', '128F', '86O', '2019702005', '18S', '3O', '11S', '166O', '158O', '201256067', '138O', '20171185', '31O', '201202022', '125O', '2018112005', '217O', '55O', '51F', '46O', '2020701024', '85F', '19F', '123F', '20172147', '20171136', '96F', '64O', '27O', '1O', '2018101069', '20171144', '201516045', '155F', '20161028', '9F', '87O', '124O', '60F', '29O', '2019702014', '20161224', '79F', '2018101085', '178O', '32F', '111F', '2018112001', '68F', '20171042', '194O', '2019201011', '2019701003', '141F', '2019701015', '2019210016', '38O', 'I-100764', '172O', '94O', '20171048', '20171116', '2018102048', '2020102012', '2019710004', '219O', '2018702010', '59O', '52O', '210O', '123O', '151O', '2020702009', '195O', '20F', '154F', '2020702013', '148O', '213O', '20172067', '127O', '145O', '2020101107', '20161020', '36F', '2018111007', '2018701024', '12F', '63F', '34F', '215O', '225O', '2018114009', '33F', '79O', '2018900050', '26O', '68O', '2018111024', '70F', '105F', 'I-100769', '61F', '149O', '46F', '65F', '2019112011', '181O', '20161211', '11O', '18O', '20171132', '88O', '119F', '6O', '143F', '201556143', '20171311', '72F', '76O', '155O', '2020201048', '2018702005', '2018102032', '2019201007', '2019102052', '143O', '56F', '131O', '89O', '71F', '214O', '5O', '201531085', '6S', '20171194', '12S', '82O', '137O', '192O', '63O', '228O', '125F', '2019701025', '107F', '2018702004', '20171135', '102F', '2020201038', '2020702020', '2018111006', '173O', '159O', '221O', '157O', '131F', '66F', '110O', '113O', '201502168', '150F', '49O', '135O', '204O', '216O', '226O', '2019101102', '95F', '49F', '103O', '156F', '227O', '2018101073', '2018101100', '101O', '80F', '80O', '156O', '198O', '2019111035', '2018111018', '32O', '2020102058', '2020201063', '7O', '153O', '2019201060', '78F', '14S', '201402182', '67O', '137F', '43O', '65O', '2020701005', '167O', '2018122002', '20161237', '2018121004', '89F', '208O', '2018113004', '2018701010', '78O', '20171151', '2019102038', '222O', '11F', 'I-100748', '100O', '33O', '20161160', '2020702010', '2020702012', '20171125', '2019201036', '9O', '20171095', '20171182', '2020801007', '2019122001', '2018111001', '106O', '20172153', '81O', 'I-100759', '139O', '2019201014', '20161081', '142O', '171O', '105O', '70O', '20172088', '2020101098', '87F', '7F', '148F', '13F', '129O', '44F', '206O', '2019701005', '45F', '4S', '42O', '101F', '20172157', '85O', '28F', '104O', '2018702006', '20171038', '45O', '2020701025', '201O', '103F', '126F', '2020111022', '57O', '30F', '182O', '122F', '2020701019', '2019201049', '56O', '2020702021', '136O', '2019701006', '135F', '2O', '2019201067', '168O', '2019802001', '20171213', '40F', 'I-100760', '99F', '2019121011', '48O', '2018701012', '190O', '19O', '3S', '2019101100', '112O', '69O', '20171035', '127F', '117O', '2018101115', '37O', '2018101093', '130F', '97O', '20161088', '201516174', '86F', '107O', '20171205', '17S', '124F', '201422649', '154O', '47F', '2019801003', '75F', '34O', '93O', '200O', '201302029', '2018102047', '2019702018', '20171175', '20161063', '144F', '2019702002', '27F', '209O', '20171137', '201507602', '13S', '158F', '2018111017', '20171067', '97F', '203O', '200902041', '40O', '183O', '152O', '2020701013', '174O', '94F', '20171148', '54F', '2020101101', '117F', '113F', '2019112025', '14F', '100F', '22O', '42F', '20161004', '13O', '53O', '2019702016', '67F', '2019102033', '2020702005', '6F', '177O', '20171402', '2020702007', '2020900010', '2S', '0S', '2018102029', '161O', '179O', '2020900015', '2018701002', '20161231', '140F', '20171006', '20161167', '2018114008', '20171160', '77O', '2018701023', '201921029', '133F', '102O', '196O', '12O', '201403009', '108O', '205O', '90O', '201432634', '2018101099', '2018122001', '2020702023', '201502059', '37F', '20171111', '111O', '22F', '121O', '20171130', '147O', '2018701020', '2018114005', '53F', '92O', '96O', '74F', '139F', '20171027', '126O', '2019121004', '2018701015', '84O', '10F', '2020702004', '142F', '112F', '20161122', '2020702001', '20171052', '132F', '2020702011', '118O', '212O', '2018101078', '36O', '59F', '17F', '185O', '74O', '50F', '152F', '0O', '165O', '20171060', '72O', '20171084', '2018802005', '8F', '39F', '108F', '10O', '2018101116', '157F', '88F', '31F', '201125172', '116F', '8S', '2020812001', '20162049', '2018802008', '90F', '10S', '128O', '144O', '20171129', '2020701035', '20161031', '224O', '2018701008', '5S', '2018701019', '2018101075', '2019701011', '20171165', '23F', '2020101058', '25O', '201814026', '199O', '20171103', 'I-100690', '9S', '2019102053', '19S', '2018101077', '50O', '2019701008', '164O', '2018101108', '170O', '2018101112', '2019701014', '223O', '15F', '17O', '2018701007', '35F', '2018101050', '187O', '2019811001', '38F', '2018113007', '1S', '51O', '24F', '180O', '55F', '146O', '2020101103', '2018101090', '48F', '114F', '2019701007', '2019702007', '207O', '24O', '2019102026', '35O', '2020101104', '0F', '2020202001', '20171087', '2020701006', '71O', '2020701022', '2018102034', '44O', '2019102039', '201431202', '2020102025', '61O', '2171157', '2019702004', '2020701010', '2020710001', '2020810001', '2018122010', '20172148', '2019801006', '28O', '20162311', '20171105', '145F', '20171211', '20171039', '4F', '121F', '104F', '2019101104', '138F', '20161220', '20171178', '76F', '202O', '2018111025', '83O', '134F', '2020102063', '146F', '41O', '2018114014', '99O', '2019900018', '1F', '106F', '8O', '62O', '140O', '201402078', '91O', '60O', '2019701020', '110F', '141O', '2019900003', '5F', '4O', '84F', '20161202', '7S', '163O', '201564223', '2019201089', '2018101025', '25F', '2020701027', '2020102061', '91F', '150O', '188O', '162O', '2018101088', '220O', '2020702017', '169O', '176O', '201556206', '2019810001', '115F', '69F', '136F', '2F', '20171013', '2020102062', '20171049', '75O', '159F', '122O', '201402222', '109F', '26F', '197O', '2018900069', '186O', '16F', '2018114017', '57F', '2020101106', '109O', '64F', '2018114012', '2019201080', '2018702008', '201256138', '82F', '20171138', '41F', '134O', '2019113006', '20171110', '73F', '184O', '29F', '2019900052', '114O', '81F', '2020701001', '2018711001', '2018111028', '2019101055', '201912020', '77F', '54O', '189O', '2019702017', '15S', '2020702018', '58O', '20172145', '120O', '2019702001', '2018102001', '120F', '20161163', '2018111008', '116O', '2020701017', '2019702006', '2018111003', '218O', '2020702015', '2019710005', '98F', '98O', '2019701010', '20O', '3F', '2018111011', '30O', '20171020', '16O', '201556003', '20161192', '2019701024', '20171007', '2018102022', '14O', '16S', '2020702006', '2019102037', '52F', '151F', '132O', '2018802001', '15O', '20171177', '193O', '118F', '2020201056', '20161048', '149F', '20172078', '18F', '21O', '47O', '2019101098', 'I-100768', '2018101118']):
					if(agent.state in state_list):
						agents_to_test.append(agent)

					elif(agent.info["VolTest"] == "True"):
						agents_to_test.append(agent)

				if(time_step>19 and agent.index in ['66O', '39O', '83F', '129F', '43F', '160O', '92F', '62F', '201356193', '175O', '211O', '130O', '229O', '21F', '119O', '95O', '133O', '73O', '23O', '115O', 'I-100763', '58F', '147F', '153F', '191O', '93F', '128F', '86O', '2019702005', '18S', '3O', '11S', '166O', '158O', '138O', '31O', '201202022', '125O', '217O', '55O', '51F', '46O', '85F', '19F', '123F', '20172147', '96F', '64O', '27O', '1O', '155F', '201516045', '87O', '9F', '124O', '60F', '29O', '2019702014', '79F', '178O', '32F', '111F', '68F', '194O', '141F', '2019701015', '38O', 'I-100764', '172O', '94O', '20171116', '219O', '2018702010', '59O', '52O', '210O', '123O', '151O', '2020702009', '195O', '20F', '154F', '148O', '213O', '20172067', '127O', '145O', '36F', '2018701024', '12F', '63F', '34F', '215O', '225O', '33F', '79O', '2018900050', '26O', '68O', '70F', '105F', 'I-100769', '61F', '149O', '46F', '65F', '181O', '11O', '18O', '88O', '119F', '6O', '143F', '201556143', '72F', '76O', '155O', '2018702005', '143O', '56F', '131O', '89O', '71F', '214O', '5O', '6S', '12S', '82O', '137O', '192O', '228O', '63O', '125F', '2019701025', '107F', '2018702004', '102F', '173O', '159O', '221O', '157O', '131F', '66F', '110O', '113O', '49O', '150F', '135O', '226O', '204O', '216O', '95F', '49F', '103O', '156F', '227O', '101O', '80F', '80O', '156O', '198O', '2018111018', '32O', '7O', '2020201063', '153O', '78F', '14S', '67O', '137F', '43O', '65O', '167O', '89F', '208O', '78O', '222O', '11F', 'I-100748', '100O', '33O', '2020702012', '9O', '106O', '2020801007', '20172153', '81O', '139O', '142O', '171O', '105O', '70O', '20172088', '87F', '7F', '148F', '13F', '129O', '44F', '206O', '2019701005', '45F', '4S', '42O', '101F', '20172157', '85O', '28F', '104O', '2018702006', '45O', '2020701025', '201O', '103F', '126F', '2020111022', '57O', '30F', '182O', '122F', '2020701019', '56O', '136O', '2020801008', '2019701006', '135F', '2O', '168O', '2019802001', '40F', 'I-100760', '99F', '48O', '2018701012', '190O', '19O', '3S', '112O', '69O', '127F', '117O', '37O', '130F', '97O', '86F', '107O', '17S', '124F', '154O', '47F', '2019801003', '75F', '34O', '93O', '200O', '144F', '27F', '209O', '201507602', '13S', '158F', '97F', '203O', '200902041', '40O', '183O', '152O', '2020701013', '174O', '94F', '54F', '117F', '113F', '22O', '14F', '100F', '53O', '42F', '13O', '2019702016', '67F', '177O', '6F', '2S', '0S', '161O', '179O', '2018701002', '140F', '20161167', '77O', '2018701023', '133F', '102O', '196O', '12O', '201403009', '108O', '205O', '90O', '201432634', '37F', '111O', '22F', '121O', '147O', '2018701020', '53F', '92O', '96O', '2019202009', '74F', '139F', '126O', '2018701015', '84O', '10F', '142F', '112F', '2020702001', '132F', '2020702011', '2019702013', '118O', '212O', '36O', '59F', '17F', '185O', '74O', '50F', '152F', '0O', '165O', '72O', '8F', '39F', '108F', '10O', '2018101116', '157F', '88F', '31F', '116F', '8S', '2018802008', '90F', '10S', '128O', '144O', '20161031', '224O', '5S', '2018701019', '2019701011', '23F', '2020101058', '25O', '199O', 'I-100690', '9S', '19S', '50O', '164O', '170O', '2019701014', '223O', '15F', '17O', '2018701007', '35F', '187O', '2019811001', '38F', '1S', '51O', '24F', '180O', '55F', '146O', '48F', '114F', '2019701007', '2019702007', '207O', '24O', '35O', '2020101104', '0F', '20171087', '2020701006', '71O', '2020701022', '44O', '61O', '2019702004', '2019801006', '20172148', '28O', '145F', '4F', '121F', '104F', '138F', '76F', '202O', '83O', '134F', '2020102063', '146F', '41O', '99O', '2019900018', '1F', '106F', '8O', '62O', '140O', '91O', '60O', '110F', '141O', '2019900003', '5F', '4O', '84F', '7S', '163O', '2019201089', '25F', '2020102061', '91F', '150O', '188O', '162O', '220O', '169O', '176O', '201556206', '115F', '69F', '136F', '2F', '2020102062', '75O', '159F', '122O', '201402222', '109F', '26F', '197O', '2018900069', '186O', '16F', '57F', '2020101106', '109O', '64F', '82F', '201256138', '41F', '134O', '73F', '184O', '29F', '2019900052', '114O', '81F', '77F', '54O', '189O', '2019702017', '15S', '2020702018', '58O', '20172145', '120O', '2019702001', '120F', '116O', '2019702006', '218O', '2020702015', '98F', '98O', '20O', '3F', '30O', '16O', '201556003', '2019701024', '14O', '16S', '2020702006', '52F', '151F', '132O', '15O', '193O', '118F', '20161048', '149F', '20172078', '18F', '21O', '47O', 'I-100768']):
					if(agent.state in state_list):
						agents_to_test.append(agent)

					elif(agent.info["VolTest"] == "True"):
						agents_to_test.append(agent)

		# Create testtubes based on formula - int((ntpa x no. of agents + napt -1)/napt)
		num_testtubes = int((num_testtubes_per_agent*self.num_agents_to_test + num_agents_per_testtube -1)/num_agents_per_testtube)
		for _ in range(num_testtubes):
			testtube = Testtube()
			self.cur_testtubes.append(testtube)

		# Assign agents to testtubes
		for agent in agents_to_test:
			if(len(self.cur_testtubes)>0):
				cur_list = random.sample(self.cur_testtubes, min(num_testtubes_per_agent,len(self.cur_testtubes)))

				for testtube in cur_list:
					testtube.register_agent(agent,time_step)

					if(testtube.get_num_agents()>=num_agents_per_testtube):
						self.ready_queue.append(testtube)
						self.cur_testtubes.remove(testtube)
			else:
				break

	def random_agents_CR2(self, num_agents_per_testtube=1, num_testtubes_per_agent=1, state_list=[]):
		assert isinstance(state_list,list)
		return partial(self.full_random_agents_CR2, num_agents_per_testtube, num_testtubes_per_agent, state_list)


	def full_random_agents_CR3(self, num_agents_per_testtube, num_testtubes_per_agent, state_list, type, agents, time_step):
		agents_copy = copy.copy(list(agents))
		random.shuffle(agents_copy)

		# Get agents for test
		agents_to_test = []

		from itertools import cycle

		for agent in cycle(agents_copy):
			# print(time_step, self.num_agents_to_test)

			if(len(agents_to_test)==self.num_agents_to_test):
				break

			else:
				if((type == "Other" and agent.info["Type"] == "Others") or (type == "Rest" and agent.info["Type"] != "Others")):
					if(time_step<=19 and agent.index in ['201525177', '2019701001', '2019702008', 'I-100757', '66O', '39O', '83F', '129F', '43F', '160O', '201456113', '92F', '2018102003', '20171405', '62F', '201356193', '175O', '20171172', '2018122007', '2018111027', '202020100', '202012014', '211O', '130O', '229O', '200999003', '21F', '119O', '95O', '133O', '73O', '23O', '2018101101', '115O', 'I-100763', '58F', '147F', '153F', '191O', '93F', '201502183', '128F', '86O', '2019702005', '18S', '3O', '11S', '166O', '158O', '201256067', '138O', '20171185', '31O', '201202022', '125O', '2018112005', '217O', '55O', '51F', '46O', '2020701024', '85F', '19F', '123F', '20172147', '20171136', '96F', '64O', '27O', '1O', '2018101069', '20171144', '201516045', '155F', '20161028', '9F', '87O', '124O', '60F', '29O', '2019702014', '20161224', '79F', '2018101085', '178O', '32F', '111F', '2018112001', '68F', '20171042', '194O', '2019201011', '2019701003', '141F', '2019701015', '2019210016', '38O', 'I-100764', '172O', '94O', '20171048', '20171116', '2018102048', '2020102012', '2019710004', '219O', '2018702010', '59O', '52O', '210O', '123O', '151O', '2020702009', '195O', '20F', '154F', '2020702013', '148O', '213O', '20172067', '127O', '145O', '2020101107', '20161020', '36F', '2018111007', '2018701024', '12F', '63F', '34F', '215O', '225O', '2018114009', '33F', '79O', '2018900050', '26O', '68O', '2018111024', '70F', '105F', 'I-100769', '61F', '149O', '46F', '65F', '2019112011', '181O', '20161211', '11O', '18O', '20171132', '88O', '119F', '6O', '143F', '201556143', '20171311', '72F', '76O', '155O', '2020201048', '2018702005', '2018102032', '2019201007', '2019102052', '143O', '56F', '131O', '89O', '71F', '214O', '5O', '201531085', '6S', '20171194', '12S', '82O', '137O', '192O', '63O', '228O', '125F', '2019701025', '107F', '2018702004', '20171135', '102F', '2020201038', '2020702020', '2018111006', '173O', '159O', '221O', '157O', '131F', '66F', '110O', '113O', '201502168', '150F', '49O', '135O', '204O', '216O', '226O', '2019101102', '95F', '49F', '103O', '156F', '227O', '2018101073', '2018101100', '101O', '80F', '80O', '156O', '198O', '2019111035', '2018111018', '32O', '2020102058', '2020201063', '7O', '153O', '2019201060', '78F', '14S', '201402182', '67O', '137F', '43O', '65O', '2020701005', '167O', '2018122002', '20161237', '2018121004', '89F', '208O', '2018113004', '2018701010', '78O', '20171151', '2019102038', '222O', '11F', 'I-100748', '100O', '33O', '20161160', '2020702010', '2020702012', '20171125', '2019201036', '9O', '20171095', '20171182', '2020801007', '2019122001', '2018111001', '106O', '20172153', '81O', 'I-100759', '139O', '2019201014', '20161081', '142O', '171O', '105O', '70O', '20172088', '2020101098', '87F', '7F', '148F', '13F', '129O', '44F', '206O', '2019701005', '45F', '4S', '42O', '101F', '20172157', '85O', '28F', '104O', '2018702006', '20171038', '45O', '2020701025', '201O', '103F', '126F', '2020111022', '57O', '30F', '182O', '122F', '2020701019', '2019201049', '56O', '2020702021', '136O', '2019701006', '135F', '2O', '2019201067', '168O', '2019802001', '20171213', '40F', 'I-100760', '99F', '2019121011', '48O', '2018701012', '190O', '19O', '3S', '2019101100', '112O', '69O', '20171035', '127F', '117O', '2018101115', '37O', '2018101093', '130F', '97O', '20161088', '201516174', '86F', '107O', '20171205', '17S', '124F', '201422649', '154O', '47F', '2019801003', '75F', '34O', '93O', '200O', '201302029', '2018102047', '2019702018', '20171175', '20161063', '144F', '2019702002', '27F', '209O', '20171137', '201507602', '13S', '158F', '2018111017', '20171067', '97F', '203O', '200902041', '40O', '183O', '152O', '2020701013', '174O', '94F', '20171148', '54F', '2020101101', '117F', '113F', '2019112025', '14F', '100F', '22O', '42F', '20161004', '13O', '53O', '2019702016', '67F', '2019102033', '2020702005', '6F', '177O', '20171402', '2020702007', '2020900010', '2S', '0S', '2018102029', '161O', '179O', '2020900015', '2018701002', '20161231', '140F', '20171006', '20161167', '2018114008', '20171160', '77O', '2018701023', '201921029', '133F', '102O', '196O', '12O', '201403009', '108O', '205O', '90O', '201432634', '2018101099', '2018122001', '2020702023', '201502059', '37F', '20171111', '111O', '22F', '121O', '20171130', '147O', '2018701020', '2018114005', '53F', '92O', '96O', '74F', '139F', '20171027', '126O', '2019121004', '2018701015', '84O', '10F', '2020702004', '142F', '112F', '20161122', '2020702001', '20171052', '132F', '2020702011', '118O', '212O', '2018101078', '36O', '59F', '17F', '185O', '74O', '50F', '152F', '0O', '165O', '20171060', '72O', '20171084', '2018802005', '8F', '39F', '108F', '10O', '2018101116', '157F', '88F', '31F', '201125172', '116F', '8S', '2020812001', '20162049', '2018802008', '90F', '10S', '128O', '144O', '20171129', '2020701035', '20161031', '224O', '2018701008', '5S', '2018701019', '2018101075', '2019701011', '20171165', '23F', '2020101058', '25O', '201814026', '199O', '20171103', 'I-100690', '9S', '2019102053', '19S', '2018101077', '50O', '2019701008', '164O', '2018101108', '170O', '2018101112', '2019701014', '223O', '15F', '17O', '2018701007', '35F', '2018101050', '187O', '2019811001', '38F', '2018113007', '1S', '51O', '24F', '180O', '55F', '146O', '2020101103', '2018101090', '48F', '114F', '2019701007', '2019702007', '207O', '24O', '2019102026', '35O', '2020101104', '0F', '2020202001', '20171087', '2020701006', '71O', '2020701022', '2018102034', '44O', '2019102039', '201431202', '2020102025', '61O', '2171157', '2019702004', '2020701010', '2020710001', '2020810001', '2018122010', '20172148', '2019801006', '28O', '20162311', '20171105', '145F', '20171211', '20171039', '4F', '121F', '104F', '2019101104', '138F', '20161220', '20171178', '76F', '202O', '2018111025', '83O', '134F', '2020102063', '146F', '41O', '2018114014', '99O', '2019900018', '1F', '106F', '8O', '62O', '140O', '201402078', '91O', '60O', '2019701020', '110F', '141O', '2019900003', '5F', '4O', '84F', '20161202', '7S', '163O', '201564223', '2019201089', '2018101025', '25F', '2020701027', '2020102061', '91F', '150O', '188O', '162O', '2018101088', '220O', '2020702017', '169O', '176O', '201556206', '2019810001', '115F', '69F', '136F', '2F', '20171013', '2020102062', '20171049', '75O', '159F', '122O', '201402222', '109F', '26F', '197O', '2018900069', '186O', '16F', '2018114017', '57F', '2020101106', '109O', '64F', '2018114012', '2019201080', '2018702008', '201256138', '82F', '20171138', '41F', '134O', '2019113006', '20171110', '73F', '184O', '29F', '2019900052', '114O', '81F', '2020701001', '2018711001', '2018111028', '2019101055', '201912020', '77F', '54O', '189O', '2019702017', '15S', '2020702018', '58O', '20172145', '120O', '2019702001', '2018102001', '120F', '20161163', '2018111008', '116O', '2020701017', '2019702006', '2018111003', '218O', '2020702015', '2019710005', '98F', '98O', '2019701010', '20O', '3F', '2018111011', '30O', '20171020', '16O', '201556003', '20161192', '2019701024', '20171007', '2018102022', '14O', '16S', '2020702006', '2019102037', '52F', '151F', '132O', '2018802001', '15O', '20171177', '193O', '118F', '2020201056', '20161048', '149F', '20172078', '18F', '21O', '47O', '2019101098', 'I-100768', '2018101118']):
						if(agent.state in state_list):
							agents_to_test.append(agent)

						elif(agent.info["VolTest"] == "True"):
							agents_to_test.append(agent)

					if(time_step>19 and agent.index in ['66O', '39O', '83F', '129F', '43F', '160O', '92F', '62F', '201356193', '175O', '211O', '130O', '229O', '21F', '119O', '95O', '133O', '73O', '23O', '115O', 'I-100763', '58F', '147F', '153F', '191O', '93F', '128F', '86O', '2019702005', '18S', '3O', '11S', '166O', '158O', '138O', '31O', '201202022', '125O', '217O', '55O', '51F', '46O', '85F', '19F', '123F', '20172147', '96F', '64O', '27O', '1O', '155F', '201516045', '87O', '9F', '124O', '60F', '29O', '2019702014', '79F', '178O', '32F', '111F', '68F', '194O', '141F', '2019701015', '38O', 'I-100764', '172O', '94O', '20171116', '219O', '2018702010', '59O', '52O', '210O', '123O', '151O', '2020702009', '195O', '20F', '154F', '148O', '213O', '20172067', '127O', '145O', '36F', '2018701024', '12F', '63F', '34F', '215O', '225O', '33F', '79O', '2018900050', '26O', '68O', '70F', '105F', 'I-100769', '61F', '149O', '46F', '65F', '181O', '11O', '18O', '88O', '119F', '6O', '143F', '201556143', '72F', '76O', '155O', '2018702005', '143O', '56F', '131O', '89O', '71F', '214O', '5O', '6S', '12S', '82O', '137O', '192O', '228O', '63O', '125F', '2019701025', '107F', '2018702004', '102F', '173O', '159O', '221O', '157O', '131F', '66F', '110O', '113O', '49O', '150F', '135O', '226O', '204O', '216O', '95F', '49F', '103O', '156F', '227O', '101O', '80F', '80O', '156O', '198O', '2018111018', '32O', '7O', '2020201063', '153O', '78F', '14S', '67O', '137F', '43O', '65O', '167O', '89F', '208O', '78O', '222O', '11F', 'I-100748', '100O', '33O', '2020702012', '9O', '106O', '2020801007', '20172153', '81O', '139O', '142O', '171O', '105O', '70O', '20172088', '87F', '7F', '148F', '13F', '129O', '44F', '206O', '2019701005', '45F', '4S', '42O', '101F', '20172157', '85O', '28F', '104O', '2018702006', '45O', '2020701025', '201O', '103F', '126F', '2020111022', '57O', '30F', '182O', '122F', '2020701019', '56O', '136O', '2020801008', '2019701006', '135F', '2O', '168O', '2019802001', '40F', 'I-100760', '99F', '48O', '2018701012', '190O', '19O', '3S', '112O', '69O', '127F', '117O', '37O', '130F', '97O', '86F', '107O', '17S', '124F', '154O', '47F', '2019801003', '75F', '34O', '93O', '200O', '144F', '27F', '209O', '201507602', '13S', '158F', '97F', '203O', '200902041', '40O', '183O', '152O', '2020701013', '174O', '94F', '54F', '117F', '113F', '22O', '14F', '100F', '53O', '42F', '13O', '2019702016', '67F', '177O', '6F', '2S', '0S', '161O', '179O', '2018701002', '140F', '20161167', '77O', '2018701023', '133F', '102O', '196O', '12O', '201403009', '108O', '205O', '90O', '201432634', '37F', '111O', '22F', '121O', '147O', '2018701020', '53F', '92O', '96O', '2019202009', '74F', '139F', '126O', '2018701015', '84O', '10F', '142F', '112F', '2020702001', '132F', '2020702011', '2019702013', '118O', '212O', '36O', '59F', '17F', '185O', '74O', '50F', '152F', '0O', '165O', '72O', '8F', '39F', '108F', '10O', '2018101116', '157F', '88F', '31F', '116F', '8S', '2018802008', '90F', '10S', '128O', '144O', '20161031', '224O', '5S', '2018701019', '2019701011', '23F', '2020101058', '25O', '199O', 'I-100690', '9S', '19S', '50O', '164O', '170O', '2019701014', '223O', '15F', '17O', '2018701007', '35F', '187O', '2019811001', '38F', '1S', '51O', '24F', '180O', '55F', '146O', '48F', '114F', '2019701007', '2019702007', '207O', '24O', '35O', '2020101104', '0F', '20171087', '2020701006', '71O', '2020701022', '44O', '61O', '2019702004', '2019801006', '20172148', '28O', '145F', '4F', '121F', '104F', '138F', '76F', '202O', '83O', '134F', '2020102063', '146F', '41O', '99O', '2019900018', '1F', '106F', '8O', '62O', '140O', '91O', '60O', '110F', '141O', '2019900003', '5F', '4O', '84F', '7S', '163O', '2019201089', '25F', '2020102061', '91F', '150O', '188O', '162O', '220O', '169O', '176O', '201556206', '115F', '69F', '136F', '2F', '2020102062', '75O', '159F', '122O', '201402222', '109F', '26F', '197O', '2018900069', '186O', '16F', '57F', '2020101106', '109O', '64F', '82F', '201256138', '41F', '134O', '73F', '184O', '29F', '2019900052', '114O', '81F', '77F', '54O', '189O', '2019702017', '15S', '2020702018', '58O', '20172145', '120O', '2019702001', '120F', '116O', '2019702006', '218O', '2020702015', '98F', '98O', '20O', '3F', '30O', '16O', '201556003', '2019701024', '14O', '16S', '2020702006', '52F', '151F', '132O', '15O', '193O', '118F', '20161048', '149F', '20172078', '18F', '21O', '47O', 'I-100768']):
						if(agent.state in state_list):
							agents_to_test.append(agent)

						elif(agent.info["VolTest"] == "True"):
							agents_to_test.append(agent)

		# Create testtubes based on formula - int((ntpa x no. of agents + napt -1)/napt)
		num_testtubes = int((num_testtubes_per_agent*self.num_agents_to_test + num_agents_per_testtube -1)/num_agents_per_testtube)
		for _ in range(num_testtubes):
			testtube = Testtube()
			self.cur_testtubes.append(testtube)

		# Assign agents to testtubes
		for agent in agents_to_test:
			if(len(self.cur_testtubes)>0):
				cur_list = random.sample(self.cur_testtubes, min(num_testtubes_per_agent,len(self.cur_testtubes)))

				for testtube in cur_list:
					testtube.register_agent(agent,time_step)

					if(testtube.get_num_agents()>=num_agents_per_testtube):
						self.ready_queue.append(testtube)
						self.cur_testtubes.remove(testtube)
			else:
				break

	def random_agents_CR3(self, num_agents_per_testtube=1, num_testtubes_per_agent=1, state_list=[], type = "Other"):
		assert isinstance(state_list,list)
		return partial(self.full_random_agents_CR3, num_agents_per_testtube, num_testtubes_per_agent, state_list, type)

	def add_partial_to_ready_queue(self):
		for testtube in self.cur_testtubes:
			if(not testtube.is_empty()):
				self.ready_queue.append(testtube)

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
			self.update_agent_policy_history(result_obj.agent,result_obj)

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

			self.statistics[time_step][machine_name]['Number of Agents Tested'] += 1
			self.statistics[time_step]['Total Agents Tested'] += 1


	def release_results(self,time_step):
		results = []
		for machine in self.machine_list:
			if(not machine.has_empty_results()):
				results += machine.get_results()
				machine.reset_machine()

		self.release_results_to_agents(results)
		self.release_results_to_policy(results, time_step)



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


		for testtube in self.cur_testtubes:
			if(testtube.is_empty()):
				all_testtubes_filled = False
				break

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
