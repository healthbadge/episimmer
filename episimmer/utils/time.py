from typing import Callable, Dict, List, Union, ValuesView,Tuple
from xmlrpc.client import Boolean

class Time():
    """
    Class that handles the timestep and world of simulation.
    """
    current_world:Union[int,None] = None
    current_time_step:Union[int,None] = None

    @staticmethod
    def get_current_world()->int:
        """
        Returns the index of the current world of simulation.
        """
        return Time.current_world

    @staticmethod
    def get_current_time_step()->int:
        """
        Returns the current time step of present world of simulation.
        """
        return Time.current_time_step

    @staticmethod
    def reset()->None:
        """
        Resets the world and time step at the beginning of a new simulation.
        """
        Time.current_world = None
        Time.current_time_step = None

    @staticmethod
    def new_world()->None:
        """
        Sets the value of current_world of simulation at the onset of simulation.If on going simulation, then this is called when the subsequent worlds are run along with setting time step for new world.
        """
        if Time.current_world is None:
            Time.current_world = 0
        else:
            Time.current_world += 1

        Time.current_time_step = 0

    @staticmethod
    def increment_current_time_step()->None:
        """
        Called to increment current time step for ongoing world simulation.
        """
        Time.current_time_step += 1
