from gymmfe.hooks import MFE_APPS
from tutor import hooks
import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.get('http://local.edly.io/feeds/config.json')
if response.status_code == 200:
    data = response.json()
else:
    # Print an error message
    print('Error fetching config JSON data!')

@MFE_APPS.add()

# Remove select MFEs (useful for testing, etc)
def _remove_stock_mfes(mfes):
    # mfes.pop("communications")
    # mfes.pop("course-authoring")
    # mfes.pop("gradebook")
    # mfes.pop("ora-grading")
    return mfes

# Add custom MFEs
def mfe_forks(mfes):
    # mfes["account"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-account",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-account/git/refs/heads",
    #     "port": 1997,
    #     "name": "account",
    # }
    # mfes["authn"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-authn",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-authn/git/refs/heads",
    #     "port": 1999,
    #     "name": "authn",
    # }
    # mfes["communications"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-communications",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-communications/git/refs/heads",
    #     "port": 1984,
    #     "name": "communications",
    # }
    # mfes["course-about"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-course-about",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-course-about/git/refs/heads",
    #     "port": 3000,
    #     "name": "course-about",
    # }
    # mfes["course-authoring"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-course-authoring",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-course-authoring/git/refs/heads",
    #     "port": 2001,
    #     "name": "course_authoring",
    # }
    # mfes["discussions"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-discussions",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-discussions/git/refs/heads",
    #     "port": 2002,
    #     "name": "discussions",
    # }
    # mfes["gradebook"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-gradebook",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-gradebook/git/refs/heads",
    #     "port": 1994,
    #     "name": "gradebook",
    # }
    # mfes["home"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-home",
    #     "version": "gym.palm",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-home/git/refs/heads",
    #     "port": 3001,
    #     "name": "home",
    # }
    # mfes["learner-dashboard"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-learner-dashboard",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-learner-dashboard/git/refs/heads",
    #     "port": 1996,
    # }
    # mfes["learning"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-learning",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-learning/git/refs/heads",
    #     "port": 2000,
    #     "name": "learning",
    # }
    # mfes["ora-grading"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-ora-grading",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-ora-grading/git/refs/heads",
    #     "port": 1993,
    #     "name": "ora-grading",
    # }
    # mfes["profile"] = {
    #     "repository": "https://github.com/gymnasium/frontend-app-profile",
    #     "version": "gym.quince.1",
    #     "refs": "https://api.github.com/repos/gymnasium/frontend-app-profile/git/refs/heads",
    #     "port": 1995,
    #     "name": "profile",
    # }
    
    return mfes



# Update common settings
hooks.Filters.ENV_PATCHES.add_items([
(
"openedx-lms-common-settings",
f"""
CORS_ORIGIN_WHITELIST.append("{data["urls"]["root"]}")
CSRF_TRUSTED_ORIGINS.append("{data["urls"]["root"]}")
LOGIN_REDIRECT_WHITELIST.append("{data["urls"]["root"]}")

SESSION_COOKIE_DOMAIN="edly.io"
SHARED_COOKIE_DOMAIN = "edly.io"

""",
),
(
"mfe-lms-common-settings",
f"""
# Custom LMS Settings
MFE_CONFIG["LOGO_URL"] = '{data["urls"]["cms"]}{data["logos"]["main"]["black"]["src"]}'
MFE_CONFIG["LOGO_TRADEMARK_URL"] = '{data["urls"]["cms"]}{data["logos"]["main"]["black"]["src"]}'
MFE_CONFIG["LOGO_WHITE_URL"] = '{data["urls"]["cms"]}{data["logos"]["main"]["white"]["src"]}'
MFE_CONFIG["INFO_EMAIL"] = 'help@thegymnasium.com'
MFE_CONFIG["PASSWORD_RESET_SUPPORT_LINK"] = 'mailto:help@thegymnasium.com'
MFE_CONFIG["SITE_NAME"] = '{data["meta"]["title"]}'
MFE_CONFIG["CONTACT_MAILING_ADDRESS"] = ""
MFE_CONFIG["FAVICON_URL"] = '{data["urls"]["cms"]}/favicon.ico'
MFE_CONFIG["MARKETING_SITE_BASE_URL"] = '{data["urls"]["root"]}'
MFE_CONFIG["MARKETING_SITE_ROOT"] = '{data["urls"]["root"]}'
"""
),
# (
# "mfe-dockerfile-pre-npm-install",
# """
# """
# ),
(
"mfe-dockerfile-post-npm-install",
"""
ADD https://api.github.com/repos/gymnasium/brand-openedx/git/refs/heads/gym.quince.1 /tmp/gitref-brand
RUN npm install '@openedx/brand-openedx@file:../brand-openedx' --registry=$NPM_REGISTRY

# ADD https://api.github.com/repos/gymnasium/gym-frontend-components/git/refs/heads/gym.quince.1 /tmp/gitref-components

RUN git clone --depth 1 -b gym.quince.1 https://github.com/gymnasium/gym-frontend-components.git /openedx/app/src/gym-frontend-components

""",
),
],
priority=hooks.priorities.LOW
)