from tutor import hooks
import os
import requests
from dotenv import load_dotenv

load_dotenv(".env", override=True)
load_dotenv(".env.local",override=False)
load_dotenv(".env.development",override=False)
load_dotenv(".env.staging",override=False)
load_dotenv(".env.production",override=False)

endpoint = os.getenv("MARKETING_SITE_BASE_URL") + "/feeds/config.json"

response = requests.get(endpoint)

print('using JSON config @ ' + endpoint)
if response.status_code == 200:
    data = response.json()
else:
    data = None
    # Print an error message
    print('Error fetching config JSON data! Make sure the marketing front end site is running locally, or point to a remote site.')

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-production-settings",
        f"""
BASE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
MARKETING_SITE_BASE_URL = "{ os.getenv("MARKETING_SITE_BASE_URL") }"
SHARED_COOKIE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
SESSION_COOKIE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
CORS_ORIGIN_WHITELIST.append("{ os.getenv("MARKETING_SITE_BASE_URL") }")
CSRF_TRUSTED_ORIGINS.append("{ os.getenv("MARKETING_SITE_BASE_URL") }")
LOGIN_REDIRECT_WHITELIST.append("{ os.getenv("BASE_DOMAIN") }")
"""
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-cms-production-settings",
        f"""
BASE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
MARKETING_SITE_BASE_URL = "{ os.getenv("MARKETING_SITE_BASE_URL") }"
SHARED_COOKIE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
SESSION_COOKIE_DOMAIN = "{ os.getenv("BASE_DOMAIN") }"
CORS_ORIGIN_WHITELIST.append("{ os.getenv("MARKETING_SITE_BASE_URL") }")
CSRF_TRUSTED_ORIGINS.append("{ os.getenv("MARKETING_SITE_BASE_URL") }")
LOGIN_REDIRECT_WHITELIST.append("{ os.getenv("BASE_DOMAIN") }")
"""
    )
)
