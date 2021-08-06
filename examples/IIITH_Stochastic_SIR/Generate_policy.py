import Lockdown_Policy
import Testing_Policy
import pickle
import numpy as np

def event_restriction_fn(agent,event_info,current_time_step):
	return False

def lockdown_fn(time_step):
	return True

def generate_policy():
	policy_list=[]

	return policy_list,event_restriction_fn
