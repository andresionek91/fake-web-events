from fake_web_events import Simulation
import logging

logging.getLogger().setLevel(logging.INFO)

simulation = Simulation(user_pool_size=500, sessions_per_day=10000)
events = simulation.run(duration_seconds=10)

for event in events:
    print(event)
