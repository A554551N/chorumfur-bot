from collections import namedtuple
from datetime import datetime

Event = namedtuple('Event','event_name event_currency_name event_currency_id')
march_event = Event('March Event','Clover',29)
