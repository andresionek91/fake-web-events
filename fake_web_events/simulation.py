from datetime import datetime, timedelta
from random import randrange, choices
from fake_web_events.event import Event
from fake_web_events.__init__ import load_config
from time import time


class Simulation:
    """
    Keep track of the simulation state
    """
    config = load_config()

    def __init__(self, user_pool, sessions_per_day=10000, batch_size=10, init_time=datetime.now()):
        self.user_pool = user_pool
        self.cur_sessions = []
        self.init_time = init_time
        self.cur_time = init_time
        self.batch_size = batch_size
        self.sessions_per_day = sessions_per_day
        self.qty_events = 0

    def __str__(self):
        """
        Return human readable state
        """
        return "\nSIMULATION STATE\n" \
               f"Current Sessions: {self.get_len_sessions()}\n" \
               f"Current duration: {self.get_duration_str()}\n" \
               f"Current user rate: {self.get_rate_per_step()}\n" \
               f"Quantity of events: {self.qty_events}"

    def get_len_sessions(self):
        """
        Calculate amount of current active sessions
        """
        return len(self.cur_sessions)

    def get_duration(self):
        """
        Get duration of simulation
        """
        return self.cur_time - self.init_time

    def get_duration_str(self):
        """
        Get simulation duration as a string
        """
        duration_td = self.get_duration()
        days = duration_td.days
        hours = duration_td.seconds//3600
        minutes = (duration_td.seconds // 60) % 60
        seconds = duration_td.seconds % 60
        return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'

    def get_steps_per_hour(self):
        """
        Calculate how many steps are there in one hour
        """
        return 3600 / self.batch_size

    def get_rate_per_step(self):
        """
        Calculate rate of events per step
        """
        hourly_rate = self.config['visits_per_hour'][self.cur_time.hour]
        return hourly_rate * self.sessions_per_day / self.get_steps_per_hour()

    def wait(self):
        """
        Wait for given amount of time defined in batch size
        """
        self.cur_time += timedelta(seconds=self.batch_size + randrange(-self.batch_size * 0.3, self.batch_size * 0.3))

    def create_sessions(self):
        """
        Create a new session for a new user
        """
        rate = self.get_rate_per_step()
        n_users = int(rate)
        n_users += choices([1, 0], cum_weights=[(rate % 1), 1])[0]
        for n in range(n_users):
            self.cur_sessions.append(Event(self.cur_time, self.user_pool.get_user(), self.batch_size))

    def update_all_sessions(self):
        for session in list(self.cur_sessions):
            session.update(self.cur_time)
            if not session.is_active():
                self.cur_sessions.remove(session)


def simulate_events(simulation, duration_seconds):
    """
    Function to run a simulation for the given duration in seconds. Yields events.
    """
    start = time()
    while time() - start < duration_seconds:
        simulation.update_all_sessions()
        simulation.create_sessions()
        simulation.wait()
        for session in simulation.cur_sessions:
            if session.is_new_page:
                yield session.asdict()
