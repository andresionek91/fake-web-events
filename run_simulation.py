from fake_web_events.simulation import Simulation, simulate_events

simulation = Simulation()
events = simulate_events(simulation, duration=100)


for event in events:
    print(event)