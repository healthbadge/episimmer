import random
import copy
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

class Agent():
	def __init__(self,state,index):
		self.state=state
		self.index=index
		self.neighbours=[]
		self.next_state=None
		self.quarantined=False
		self.HLA_type=None
