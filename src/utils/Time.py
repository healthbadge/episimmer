class Time():
    current_world = None
    current_time_step = None

    @staticmethod
    def get_current_world():
        return Time.current_world

    @staticmethod
    def get_current_time_step():
        return Time.current_time_step

    @staticmethod
    def reset():
        Time.current_world = None
        Time.current_time_step = None

    @staticmethod
    def new_world():
        if Time.current_world is None:
            Time.current_world = 0
        else:
            Time.current_world += 1

        Time.current_time_step = 0

    @staticmethod
    def increment_current_time_step():
        Time.current_time_step += 1
