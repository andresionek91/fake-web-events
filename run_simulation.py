from fake_web_events.user import UserPool
from fake_web_events.simulation import Simulation, simulate_events


user_pool = UserPool(size=200)
simulation = Simulation(user_pool=user_pool, sessions_per_day=100000)
events = simulate_events(simulation, duration=1)


for event in events:
    print(event)