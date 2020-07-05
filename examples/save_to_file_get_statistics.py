from fake_web_events.user import UserPool
from fake_web_events.simulation import Simulation, simulate_events
import json
import pandas as pd
import matplotlib.pyplot as plt


def create_events_file():
    user_pool = UserPool(size=200)
    simulation = Simulation(user_pool=user_pool, sessions_per_day=10000)
    events = simulate_events(simulation, duration_seconds=20)

    with open('events.json', 'w') as f:
        f.write(json.dumps(list(events)))


create_events_file()

df = pd.read_json('events.json', orient='records')
df['event_hour'] = pd.to_datetime(df['event_timestamp']).dt.strftime('%Y-%m-%d %H')

events_per_hour = df.groupby('event_hour')['user_domain_id'].count()
print(events_per_hour)

events_per_hour.plot.line()
plt.show()

page_count = df['page_url_path'].value_counts()
print(page_count)