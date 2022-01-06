class Agent():
    def __init__(self, state, info_dict):
        self.state = state
        self.next_state = None
        self.contact_list = []
        self.location_list = []
        self.info = info_dict
        self.index = info_dict['Agent Index']
        self.event_probabilities = []

        self.schedule_time_left = None
        self.can_recieve_infection = 1.0
        self.can_contribute_infection = 1.0

        self.policy_dict = {}  #Store all policy related status of agent
        self.initialize_policy_dict()

    def initialize_state(self, state, schedule_time_left=None):
        self.state = state
        self.schedule_time_left = schedule_time_left

    def initialize_policy_dict(self):
        for policy_type in ['Restrict', 'Testing', 'Vaccination']:
            temp = {'History': [], 'State': None}
            self.policy_dict[policy_type] = temp

    def get_policy_state(self, policy_type):
        return self.policy_dict[policy_type]['State']

    def get_policy_history(self, policy_type):
        return self.policy_dict[policy_type]['History']

    def add_contact(self, contact_dict):
        self.contact_list.append(contact_dict)

    def add_event_result(self, p):
        self.event_probabilities.append(p)

    def new_time_step(self):
        self.can_recieve_infection = 1.0
        self.can_contribute_infection = 1.0
        self.next_state = None
        self.contact_list = []
        self.event_probabilities = []
        if self.schedule_time_left != None:
            self.schedule_time_left -= 1
            if self.schedule_time_left <= 0:
                self.schedule_time_left = None

    def update_state(self):
        if self.next_state == None:
            return
        self.state = self.next_state
        self.next_state = None

    def set_next_state(self, state_info):
        next_state, schedule_time = state_info
        self.next_state = next_state
        self.schedule_time_left = schedule_time

    def update_recieve_infection(self, p):
        self.can_recieve_infection = p

    def update_contribute_infection(self, p):
        self.can_contribute_infection = p
