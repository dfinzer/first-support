import os

from customerio import CustomerIO


def track_event(user_id, event_name, **kwargs):
    cio = CustomerIO(os.environ['CUSTOMER_IO_SITE_ID'], os.environ['CUSTOMER_IO_API_KEY'])
    cio.track(customer_id=user_id, name=event_name, **kwargs)
