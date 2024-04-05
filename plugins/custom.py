from tutor import hooks
import os
import requests

# dotenv
from dotenv import load_dotenv

load_dotenv(".env", override=True)
load_dotenv(".env.local",override=False)
load_dotenv(".env.development",override=False)
load_dotenv(".env.staging",override=False)
load_dotenv(".env.production",override=False)

endpoint = os.getenv("MARKETING_SITE_BASE_URL") + "/feeds/config.json"

response = requests.get(endpoint)

print('endpoint: ' + endpoint)
if response.status_code == 200:
    data = response.json()
else:
    data = None
    # Print an error message
    print('Error fetching config JSON data! Make sure the marketing front end site is running locally, or point to a remote site.')

hooks.Filters.ENV_PATCHES.add_item(
    (
"mfe-lms-common-settings",
f"""

"""
    ),
    priority=hooks.priorities.LOW
)
