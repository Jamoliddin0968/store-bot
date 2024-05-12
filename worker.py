import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from src.config import WEBHOOK_URL


def send_request():

    url = WEBHOOK_URL
    requests.get(url)


# Create a scheduler instance
scheduler = BackgroundScheduler()

# Add a job to the scheduler
scheduler.add_job(send_request, 'interval', seconds=1)

# Start the scheduler
scheduler.start()
is_work = True
