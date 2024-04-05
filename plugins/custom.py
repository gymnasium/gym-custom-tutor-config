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
if response.status_code == 200:
    data = response.json()
else:
    # Print an error message
    print('Error fetching config JSON data! Make sure the marketing front end site is running locally, or point to a remote site.')

hooks.Filters.ENV_PATCHES.add_item(
    (
"mfe-dockerfile-post-npm-install",
"""
ADD https://api.github.com/repos/gymnasium/gym-frontend-components/git/refs/heads/gym.quince.2 /tmp/gitref-frontend-components-v0

ADD https://api.github.com/repos/gymnasium/brand-openedx/git/refs/heads/gym.quince.1 /tmp/gitref-brand

RUN npm install '@edx/gym-frontend@git+https://git@github.com/gymnasium/gym-frontend-components.git#gym.quince.2' --registry=$NPM_REGISTRY

RUN npm install '@edx/brand@git+https://git@github.com/gymnasium/brand-openedx.git#gym.quince.1' --registry=$NPM_REGISTRY
"""
    ),
    priority=hooks.priorities.LOW
)

hooks.Filters.ENV_PATCHES.add_item(
    (
"mfe-lms-common-settings",
f"""
# Custom LMS Settings
# Account specific
# MFE_CONFIG["ENABLE_DEMOGRAPHICS_COLLECTION"] = 'false'
# MFE_CONFIG["ENABLE_COPPA_COMPLIANCE"] = 'false'
# MFE_CONFIG["ENABLE_ACCOUNT_DELETION"] = 'false'
# MFE_CONFIG["ENABLE_DOB_UPDATE"] = 'false'

# # Authn specific
# MFE_CONFIG["REFRESH_ACCESS_TOKEN_ENDPOINT"] = '{data["urls"]["lms"]}/login_refresh'
# MFE_CONFIG["LOGIN_ISSUE_SUPPORT_LINK"] = '{data["urls"]["root"]}/support'
# MFE_CONFIG["TOS_AND_HONOR_CODE"] = '{data["urls"]["root"]}/honor'
# MFE_CONFIG["TOS_LINK"] = '{data["urls"]["root"]}/tos'
# MFE_CONFIG["PRIVACY_POLICY"] = '{data["urls"]["root"]}/privacy-policy/'
# MFE_CONFIG["AUTHN_PROGRESSIVE_PROFILING_SUPPORT_LINK"] = '/welcome'
# MFE_CONFIG["ENABLE_DYNAMIC_REGISTRATION_FIELDS"] = 'true'
# MFE_CONFIG["MARKETING_EMAILS_OPT_IN"] = 'false'
# MFE_CONFIG["ENABLE_PROGRESSIVE_PROFILING_ON_AUTHN"] = 'true'
# MFE_CONFIG["SHOW_CONFIGURABLE_EDX_FIELDS"] = 'true'
"""
    ),
    priority=hooks.priorities.LOW
)
