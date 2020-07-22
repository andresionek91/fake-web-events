from fake_web_events import Simulation
import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, TIMESTAMP, Integer, Float, Boolean
import logging

db_string = f"postgres://{os.environ['user']}:{os.environ['password']}@localhost:5432/{os.environ['dbname']}"
db = create_engine(db_string)

logging.getLogger().setLevel(logging.INFO)

meta = MetaData(db)
atomic_events_table = Table('atomic_events',
                            meta,
                            Column('event_timestamp', TIMESTAMP),
                            Column('event_type', String),
                            Column('page_url', String),
                            Column('page_url_path', String),
                            Column('referer_url', String),
                            Column('referer_url_scheme', String),
                            Column('referer_url_port', Integer),
                            Column('referer_medium', String),
                            Column('utm_medium', String),
                            Column('utm_source', String),
                            Column('utm_content', String),
                            Column('utm_campaign', String),
                            Column('click_id', String),
                            Column('geo_latitude', Float),
                            Column('geo_longitude', Float),
                            Column('geo_country', String),
                            Column('geo_timezone', String),
                            Column('geo_region_name', String),
                            Column('ip_address', String),
                            Column('browser_name', String),
                            Column('browser_user_agent', String),
                            Column('browser_language', String),
                            Column('os', String),
                            Column('os_name', String),
                            Column('os_timezone', String),
                            Column('device_type', String),
                            Column('device_is_mobile', Boolean),
                            Column('user_custom_id', String),
                            Column('user_domain_id', String)
                            )

with db.connect() as conn:
    atomic_events_table.create()

    simulation = Simulation(user_pool_size=100, sessions_per_day=10000)
    events = simulation.run(duration_seconds=900)

    for event in events:
        insert_statement = atomic_events_table.insert().values(**event)
        conn.execute(insert_statement)
