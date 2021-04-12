
import random
import copy
import numpy as np

class Agent():
	def __init__(self,state,info_dict):
		self.state=state
		self.next_state=None
		self.contact_list=[]
		self.location_list=[]
		self.info=info_dict
		self.index=info_dict['Agent Index']
		self.event_probabilities=[]
		
		self.schedule_time_left=None
		self.testing_history=[] #tuple of (<testing time(Time tested)>, <testing type(Pool, Antigen,...)>, <test machine id(unique machine)>, <result(Positive, Negative, Viral Load...)>)
		self.compliance = None #Can be a dictionary of Guideline compliance, Restriction compliancce, Governemnt Policy compliance
		self.lock_down_state=False

	def add_contact(self,contact_dict):
		if not self.lock_down_state:
			self.contact_list.append(contact_dict)

	def add_event_result(self,p):
		if not self.lock_down_state:
			self.event_probabilities.append(p)

	def new_time_step(self):
		self.lock_down_state=False
		self.next_state=None
		self.contact_list=[]
		self.event_probabilities=[]
		if self.schedule_time_left!=None:
			self.schedule_time_left-=1
			if self.schedule_time_left <=0:
				self.schedule_time_left=None

	def update_state(self):

		if self.next_state==None:
			return
		self.state=self.next_state
		self.next_state=None

	def set_next_state(self,state_info):
		next_state,schedule_time=state_info
		self.next_state=next_state
		self.schedule_time_left=schedule_time
