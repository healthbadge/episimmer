class Location():
    def __init__(self, info_dict):
        self.info = info_dict
        self.index = info_dict['Location Index']
        self.events = []
        self.lock_down_state = False

    def new_time_step(self):
        self.lock_down_state = False
        self.events = []

    def add_event(self, event_info):
        if not self.lock_down_state:
            self.events.append(event_info)
