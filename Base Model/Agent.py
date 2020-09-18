import random
import copy
import numpy as np

class Agent():
	def __init__(self,state,info_dict):
		self.state=state
		self.next_state=None
		self.contact_list=[]
		self.info=info_dict
		self.index=info_dict['Agent Index']
		self.schedule_time_left=None

	def add_contact(self,contact_dict):
		self.contact_list.append(contact_dict)

	def new_day(self):
		self.next_state=None
		self.contact_list=[]
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
