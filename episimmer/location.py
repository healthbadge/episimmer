from typing import Dict, List, Union


class Location():
    """
    Class for a location.

    Args:
        info_dict: Information of each location taken from the locations file .
    """
    def __init__(self, info_dict: Dict[str, str]):
        self.info: Dict[str, str] = info_dict
        self.index: str = info_dict['Location Index']
        self.events: List[Dict[str, Union[str, List[str]]]] = []
        self.lock_down_state: bool = False

    def new_time_step(self) -> None:
        """
        Resets the lockdown state and events of the location at the start of each timestep
        """
        self.lock_down_state = False
        self.events = []

    def add_event(self, event_info: Dict[str, List[str]]) -> None:
        """
        Storing an event that take place in the location
        """
        if not self.lock_down_state:
            self.events.append(event_info)
