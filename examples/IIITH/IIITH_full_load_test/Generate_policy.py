import Lockdown_Policy
import Testing_Policy
import pickle
import numpy as np
import random

def event_restriction_fn(agent,event_info,current_time_step):
	return False

def lockdown_fn(time_step):
	return False

def generate_policy():
	policy_list=[]

	Normal_Testing = Testing_Policy.Test_Policy(lambda x:20)
	Normal_Testing.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 20, 1)
	Normal_Testing.set_register_agent_testtube_func(Normal_Testing.random_agents(1,1))
	policy_list.append(Normal_Testing)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:random.random()<0.95,14)
	policy_list.append(ATP)
	policy_list.append(Lockdown_Policy.full_lockdown(lockdown_fn))

	return policy_list,event_restriction_fn
