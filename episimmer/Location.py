import random
import copy

class Location():
	def __init__(self,info_dict):
		self.info=info_dict
		self.index=info_dict['Location Index']
		self.events=[]

	def new_time_step(self):
		self.events=[]

	def add_event(self,event_info):
		self.events.append(event_info)

