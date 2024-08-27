import asyncio
import threading
from asyncio import sleep

import requests  # You may need to install this using `pip install requests`
from decouple import config

# import time


async def send_request():
    while True:
        try:
            await sleep(20)
            # Replace the URL with the actual endpoint you want to request
            response = requests.get("https://store-bot-xbhm.onrender.com")
            # Handle the response as needed
            print(f"Response Status Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
          # Wait for 20 seconds before sending the next request


async def start_periodic_requests():
    # Create and start a new thread
    request_thread = threading.Thread(target=send_request, daemon=True)
    if not config('DEBUG', False, cast=bool):
        await send_request()



