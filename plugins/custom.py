from tutor import hooks
import requests

response = requests.get('http://edly.io:8888/feeds/config.json')
if response.status_code == 200:
    data = response.json()
else:
    # Print an error message
    print('Error fetching config JSON data! Make sure the marketing front end site is running locally, or point to an remote site.')

hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-dockerfile-post-npm-install",
            """
ADD https://api.github.com/repos/gymnasium/gym-frontend-components/git/refs/heads/gym.quince.1 /tmp/gitref-components
ADD https://api.github.com/repos/gymnasium/brand-openedx/git/refs/heads/gym.quince.1 /tmp/gitref-brand

RUN npm install '@edx/gym-frontend@git+https://git@github.com/gymnasium/gym-frontend-components.git#gym.quince.1' --registry=$NPM_REGISTRY
RUN npm install '@edx/brand@git+https://git@github.com/gymnasium/brand-openedx.git#gym.quince.1' --registry=$NPM_REGISTRY
            """,
        ),
    ]
)

hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "openedx-lms-common-settings",
            f"""
CORS_ORIGIN_WHITELIST.append('{data["urls"]["root"]}')
CSRF_TRUSTED_ORIGINS.append('{data["urls"]["root"]}')
LOGIN_REDIRECT_WHITELIST.append('{data["urls"]["root"]}')

CORS_ORIGIN_WHITELIST.append("https://gym.soy")
CSRF_TRUSTED_ORIGINS.append("https://gym.soy")
LOGIN_REDIRECT_WHITELIST.append("https://gym.soy")

SESSION_COOKIE_DOMAIN="edly.io"
SHARED_COOKIE_DOMAIN = "edly.io"
            """,
        ),
    ]
)

hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-lms-common-settings",
            f"""
# Custom LMS Settings
MFE_CONFIG["MARKETING_SITE_BASE_URL"] = '{data["urls"]["root"]}'
MFE_CONFIG["MARKETING_SITE_ROOT"] = '{data["urls"]["root"]}'
MFE_CONFIG["CMS_BASE_URL"] = '{data["urls"]["cms"]}'
MFE_CONFIG["LMS_BASE_URL"] = '{data["urls"]["lms"]}'
MFE_CONFIG["LOGIN_URL"] = '{data["urls"]["lms"]}/login'
MFE_CONFIG["LOGOUT_URL"] = '{data["urls"]["lms"]}/logout'
MFE_CONFIG["SUPPORT_URL"] = '{data["urls"]["root"]}/support'
MFE_CONFIG["INFO_EMAIL"] = 'help@thegymnasium.com'
MFE_CONFIG["PASSWORD_RESET_SUPPORT_LINK"] = 'mailto:help@thegymnasium.com'
MFE_CONFIG["SITE_NAME"] = '{data["meta"]["title"]}'
MFE_CONFIG["CONTACT_MAILING_ADDRESS"] = ""
MFE_CONFIG["FAVICON_URL"] = '{data["urls"]["root"]}/favicon.svg'

# These images are only applied to non-public facing/internal use MFEs (course authoring, communications, grading, ora-grading, etc)
MFE_CONFIG["LOGO_URL"] = '{data["urls"]["cms"]}/static/studio/gym-theme/images/studio-logo.png'
MFE_CONFIG["LOGO_TRADEMARK_URL"] = '{data["urls"]["cms"]}/static/studio/gym-theme/images/studio-logo.png'
MFE_CONFIG["LOGO_WHITE_URL"] = '{data["urls"]["cms"]}/static/studio/gym-theme/images/studio-logo.png'

# Account specific
MFE_CONFIG["ENABLE_DEMOGRAPHICS_COLLECTION"] = 'false'
MFE_CONFIG["ENABLE_COPPA_COMPLIANCE"] = 'false'
MFE_CONFIG["ENABLE_ACCOUNT_DELETION"] = 'false'
MFE_CONFIG["ENABLE_DOB_UPDATE"] = 'false'

# Authn specific
MFE_CONFIG["REFRESH_ACCESS_TOKEN_ENDPOINT"] = '{data["urls"]["lms"]}/login_refresh'
MFE_CONFIG["LOGIN_ISSUE_SUPPORT_LINK"] = '{data["urls"]["root"]}/support'
MFE_CONFIG["TOS_AND_HONOR_CODE"] = '{data["urls"]["root"]}/honor'
MFE_CONFIG["TOS_LINK"] = '{data["urls"]["root"]}/tos'
MFE_CONFIG["PRIVACY_POLICY"] = '{data["urls"]["root"]}/privacy-policy/'
MFE_CONFIG["AUTHN_PROGRESSIVE_PROFILING_SUPPORT_LINK"] = '/welcome'
MFE_CONFIG["ENABLE_DYNAMIC_REGISTRATION_FIELDS"] = 'true'
MFE_CONFIG["MARKETING_EMAILS_OPT_IN"] = 'false'
MFE_CONFIG["ENABLE_PROGRESSIVE_PROFILING_ON_AUTHN"] = 'true'
MFE_CONFIG["SHOW_CONFIGURABLE_EDX_FIELDS"] = 'true'

          """,
        ),
    ]
)