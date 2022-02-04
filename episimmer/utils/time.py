from typing import Union


class Time():
    """
    Class that handles the time step and world of simulation.
    """
    current_world: Union[int, None] = None
    current_time_step: Union[int, None] = None

    @staticmethod
    def get_current_world() -> int:
        """
        Returns the current world of simulation.

        Returns:
            Index of current world
        """
        return Time.current_world

    @staticmethod
    def get_current_time_step() -> int:
        """
        Returns the current time step of simulation.

        Returns:
            Index of current time step
        """
        return Time.current_time_step

    @staticmethod
    def reset() -> None:
        """
        Resets the world and time step at the beginning of a new simulation.
        """
        Time.current_world = None
        Time.current_time_step = None

    @staticmethod
    def new_world() -> None:
        """
        Sets the value of current_world and current time step at the onset of a world.
        """
        if Time.current_world is None:
            Time.current_world = 0
        else:
            Time.current_world += 1

        Time.current_time_step = 0

    @staticmethod
    def increment_current_time_step() -> None:
        """
        increments the current time step during simulation.
        """
        Time.current_time_step += 1
