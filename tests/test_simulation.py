from fake_web_events.simulation import Simulation
import pytest
from faker import Faker
import random
from datetime import datetime, timedelta


@pytest.fixture()
def mock_simulation():
    random.seed(0)
    Faker.seed(0)
    simulation = Simulation(10, 10000, 10, datetime(2020, 7, 7, 0, 0, 0, 0))
    return simulation


@pytest.fixture()
def mock_create_sessions(mock_simulation):
    for idx in range(100):
        mock_simulation.create_sessions()


@pytest.fixture()
def mock_wait(mock_simulation):
    for idx in range(100):
        mock_simulation.wait()


@pytest.fixture()
def mock_update(mock_simulation):
    for idx in range(100):
        mock_simulation.update_all_sessions()
        mock_simulation.create_sessions()
        mock_simulation.wait()


class TestSimulation:

    def test_get_len_sessions(self, mock_simulation, mock_create_sessions):
        assert mock_simulation.get_len_sessions() == 81

    def test_get_duration(self, mock_simulation, mock_wait):
        assert mock_simulation.get_duration() == timedelta(seconds=939)

    def test_get_duration_str(self, mock_simulation, mock_wait):
        assert mock_simulation.get_duration_str() == '0 days, 0 hours, 15 minutes, 39 seconds'

    def test_get_steps_per_hour(self, mock_simulation):
        assert mock_simulation.get_steps_per_hour() == 360

    def test_get_rate_per_step(self, mock_simulation):
        assert round(mock_simulation.get_rate_per_step(), 5) == 0.75833

    def test_update(self, mock_simulation, mock_update):
        assert mock_simulation.get_len_sessions() == 4

    def test_max_unique_user_ids(self, mock_simulation):
        # after running the simulation for some time, the max unique user ids must be equal to the pool size
        events = list(mock_simulation.run(2))
        user_domain_ids = set(event['user_domain_id'] for event in events)
        assert len(user_domain_ids) == 10