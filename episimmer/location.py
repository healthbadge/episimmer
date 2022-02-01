from typing import Callable, Dict, List, Union, ValuesView


class Location():
    """
    Class used for storing any information related to the location such as events and lockdown state of location.

    Args:
        info_dict: Information of each location obtained from locations.txt .
    """
    def __init__(self, info_dict: Dict[str, str]):
        self.info: Dict[str, str] = info_dict
        self.index: str = info_dict['Location Index']
        self.events: List[str] = []
        self.lock_down_state: bool = False

    def new_time_step(self) -> None:
        """
        Resets the lockdown state of the location as it is the first time of the new world in the simulation.
        """
        self.lock_down_state = False
        self.events = []

    def add_event(self, event_info: Dict[str, List[str]]) -> None:
        """
        Storing all the events that take place in the location under the events list.
        """
        if not self.lock_down_state:
            self.events.append(event_info)
