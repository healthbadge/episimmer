import Lockdown_Policy
import Testing_Policy
import pickle
import numpy as np
import random

def event_restriction_fn(agent,event_info,current_time_step):
	return False

def lockdown_fn(time_step):
	if time_step%7==5:
		return True
	return False

def fn(x):
	if x%7==3:
		return 350
	return 0

def fn0(x):
	if x%3==0:
		return 50
	return 0

def fn1(x):
	if x%3==1:
		return 50
	return 0

def fn2(x):
	if x%3==2:
		return 50
	return 0

def generate_policy():
	policy_list=[]

	Normal_Testing0 = Testing_Policy.Test_Policy(fn0) #(fn)
	Normal_Testing0.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 1)
	Normal_Testing0.set_register_agent_testtube_func(Normal_Testing0.random_agents(1,1,'hostel',['92']))
	policy_list.append(Normal_Testing0)

	Normal_Testing1 = Testing_Policy.Test_Policy(fn1) #(fn)
	Normal_Testing1.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 1)
	Normal_Testing1.set_register_agent_testtube_func(Normal_Testing1.random_agents(1,1,'hostel',['93']))
	policy_list.append(Normal_Testing1)

	Normal_Testing2 = Testing_Policy.Test_Policy(fn2) #(fn)
	Normal_Testing2.add_machine('Simple_Machine', 200, 0.0, 0.0, 0, 50, 1)
	Normal_Testing2.set_register_agent_testtube_func(Normal_Testing2.random_agents(1,1,'hostel',['94']))
	policy_list.append(Normal_Testing2)

	ATP = Lockdown_Policy.agent_policy_based_lockdown("Testing",["Positive"],lambda x:random.random()<1,14)
	policy_list.append(ATP)

	return policy_list,event_restriction_fn
