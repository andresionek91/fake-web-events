from fake_web_events.simulation import Simulation


simulation = Simulation(user_pool_size=10000, sessions_per_day=100000)
events = simulation.run(duration_seconds=60)

for event in events:
    print(event)
