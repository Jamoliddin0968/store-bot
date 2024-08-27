import threading
import time

import requests  # You may need to install this using `pip install requests`
from decouple import config


def send_request():
    while True:
        try:
            # Replace the URL with the actual endpoint you want to request
            response = requests.get("https://store-bot-xbhm.onrender.com")
            # Handle the response as needed
            print(f"Response Status Code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(20)  # Wait for 20 seconds before sending the next request


def start_periodic_requests():
    # Create and start a new thread
    request_thread = threading.Thread(target=send_request, daemon=True)
    if not config('DEBUG', False, cast=bool):
        request_thread.start()


# Start the periodic requests
start_periodic_requests()

# Keep the main thread running
try:
    while True:
        time.sleep(1)  # Main thread keeps running
except KeyboardInterrupt:
    print("Program terminated.")
