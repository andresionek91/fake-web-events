from datetime import datetime, timedelta
from random import randrange, choices
from fake_web_events.event import Event
from fake_web_events.user import UserPool
from fake_web_events.utils import load_config
from time import time

from typing import Generator


class Simulation:
    """
    Keep track of the simulation state
    """
    config = load_config()

    def __init__(
            self,
            user_pool_size: int,
            sessions_per_day: int = 10000,
            batch_size: int = 10,
            init_time: datetime = datetime.now()):

        self.user_pool = UserPool(size=user_pool_size)
        self.cur_sessions = []
        self.init_time = init_time
        self.cur_time = init_time
        self.batch_size = batch_size
        self.sessions_per_day = sessions_per_day
        self.qty_events = 0
        self.rate = self.get_rate_per_step()

    def __str__(self) -> str:
        """
        Return human readable state
        """
        return "\nSIMULATION STATE\n" \
               f"Current Sessions: {self.get_len_sessions()}\n" \
               f"Current duration: {self.get_duration_str()}\n" \
               f"Current user rate: {self.rate}\n" \
               f"Quantity of events: {self.qty_events}"

    def get_len_sessions(self) -> int:
        """
        Calculate amount of current active sessions
        """
        return len(self.cur_sessions)

    def get_duration(self) -> timedelta:
        """
        Get duration of simulation
        """
        return self.cur_time - self.init_time

    def get_duration_str(self) -> str:
        """
        Get simulation duration as a string
        """
        duration_td = self.get_duration()
        days = duration_td.days
        hours = duration_td.seconds//3600
        minutes = (duration_td.seconds // 60) % 60
        seconds = duration_td.seconds % 60
        return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'

    def get_steps_per_hour(self) -> float:
        """
        Calculate how many steps are there in one hour
        """
        return 3600 / self.batch_size

    def get_rate_per_step(self) -> float:
        """
        Calculate rate of events per step
        """
        hourly_rate = self.config['visits_per_hour'][self.cur_time.hour]
        return hourly_rate * self.sessions_per_day / self.get_steps_per_hour()

    def wait(self) -> None:
        """
        Wait for given amount of time defined in batch size
        """
        self.cur_time += timedelta(seconds=self.batch_size + randrange(-self.batch_size * 0.3, self.batch_size * 0.3))
        self.rate = self.get_rate_per_step()

    def create_sessions(self) -> list:
        """
        Create a new session for a new user
        """
        n_users = int(self.rate)
        n_users += choices([1, 0], cum_weights=[(self.rate % 1), 1])[0]
        for n in range(n_users):
            self.cur_sessions.append(Event(self.cur_time, self.user_pool.get_user(), self.batch_size))

        return self.cur_sessions

    def update_all_sessions(self) -> None:
        for session in list(self.cur_sessions):
            session.update(self.cur_time)
            if not session.is_active():
                self.cur_sessions.remove(session)

    def run(self, duration_seconds: int) -> Generator[dict, None, None]:
        """
        Function to run a simulation for the given duration in seconds. Yields events.
        """
        start = time()
        while time() - start < duration_seconds:
            self.update_all_sessions()
            self.create_sessions()
            self.wait()
            for session in self.cur_sessions:
                if session.is_new_page:
                    yield session.asdict()
