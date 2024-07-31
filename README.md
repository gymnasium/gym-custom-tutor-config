# Tutor Custom

- These instructions are WIP.
- These instructions are currently specific to Mac OS.

## Prerequisites
This proof-of-concept Tutor config depends on a separate marketing frontend running either locally at `edly.io:8888`, or remotely at a domain specified in the `.env` files. See the [gym-eleventy](https://github.com/gymnasium/gym-eleventy) repo for specific instructions on running locally it using the netlify CLI.

## env variables
The `.env` file in the project root folder is set with default values for running tutor locally. When running in a production environment, rename `.env.production.example` to `.env.production` and update the value(s) to match your production environment accordingly.

## Installation
These instructions use direnv for convenience. If you'd rather create your own python virtualenv, the instructions will vary a bit.

### direnv
1. Install direnv
```
brew install direnv
```

Be sure to add the relevant hook to your shell: https://direnv.net/docs/hook.html

### TVM (Tutor Version Manager)
- Install [Tutor Version Manager](https://github.com/eduNEXT/tvm)
```
pip install git+https://github.com/eduNEXT/tvm.git
```

- Install the Tutor version you wish to use.
```
tvm install v18.1.1
```


- Create a main directory to house your tutor configs (for example `your-home folder/dev/tutor/`), ideally one that you can find easily via CLI. 
```
mkdir ~/tutor
```

### Once per TVM project

- Create a new TVM project
Please note the project title cannot include periods, lest TVM puke. In this case, TVM will automatically create a new directory for you.
```
tvm project init gym.redwood v18.1.1
```

- enter the directory:
```
cd redwood
```

- Activate the environment:
You'll need to do this each time you spawn the root directory in your terminal.

In the root directory, type the following. If you're also using `direnv` you may be prompted to give it permissions to access the folder.
```
source .tvm/bin/activate
```

Test this by confirming your Tutor root:
```
echo $TUTOR_ROOT
```
The output should match the directory you're in.


1.  Clone the this repo into the directory
```
git init .
git remote add origin https://github.com/gymnasium/gym-custom-tutor-config
git pull origin redwood --recurse-submodules
```

1. On first install only run the following in the root folder to install packages for our customized Tutor:
```
git submodule update --init --recursive
pip install -U -r requirements.txt
```

1. Check to make sure the env variables are set properly for your enviroment
```
python -m dotenv list
```
If you don't see the following set properly, be sure to update the .env file accordingly.

```
BASE_DOMAIN=yourdomain
MARKETING_SITE_BASE_URL=http(s)://yourdomain
SESSION_COOKIE_DOMAIN=yourdomain
SHARED_COOKIE_DOMAIN=yourdomain
```

1. Run Tutor once without some plugins enabled to make sure you can get it up and running, and to add site configs.

Check your active plugins by running `tutor plugins list` and make sure only the following are active:

```
- forum
- mfe
```

Startup your tutor in dev mode.
```
tutor dev launch
```

Once it's running, create a superuser login for yourself and proceed with the customizations: `tutor dev do createuser --staff --superuser admin admin@example.com`

#### Continue with the customizations

- Update the tutor config with the Gymnasium customizations:
```
cat config-custom.yml >> config.yml
tutor config save
```

- Activate the remaining plugins:
`tutor plugins enable caddy-csp course-about-dev gym-theme mfe-disable mfe-forks shared-cookies`

## Tutor Dev Mode
For development, it's best to run tutor in dev mode instead of local mode.

Make sure 11ty is running in `dev:tutor` mode: `npm run dev:tutor`, and available at `http://edly.io:8888`.

### Build dev images
Build all the dev images:
```
tutor images build openedx-dev account-dev authn-dev course-about-dev discussions-dev learner-dashboard-dev learning-dev profile-dev
```

If you run into trouble, you can try building each image individually. 

openedx:
```
tutor images build openedx-dev
```

mfes:
```
tutor images build account-dev
tutor images build authn-dev
tutor images build course-about-dev
tutor images build discussions-dev
tutor images build learner-dashboard-dev
tutor images build learning-dev
tutor images build profile-dev
```

If something fails, see the troubleshooting area below.

#### Dev Mode Bind Mount Setup
Using bind mounts is essential when developing MFEs. Use the examples below to populate your `config.yml` file.

#### Account-specific bind mounts
```
MOUNTS:
- ./mfe/frontend-app-account
- account:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- account:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Authn-specific bind mounts
```
MOUNTS:
- ./mfe/frontend-app-authn
- authn:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- authn:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Course About-specific bind mounts
```
MOUNTS:
- ./mfe/frontend-app-course-about
- course-about:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- course-about:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Discussions-specific bind mounts
```
MOUNTS:
- ./mfe/frontend-app-discussions
- discussions:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- discussions:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Learner Dashboard-specific bind mounts
```
MOUNTS:
- ./mfe/frontend-app-learner-dashboard
- learner-dashboard:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- learner-dashboard:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Learning bind mounts
```
MOUNTS:
- ./mfe/frontend-app-learning
- learning:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- learning:./mfe/module.config.js:/openedx/app/module.config.js
```

#### Profile bind mounts
```
MOUNTS:
- ./mfe/frontend-app-profile
- profile:./mfe/gym-frontend-components:/openedx/app/@edx/gym-frontend
- profile:./mfe/module.config.js:/openedx/app/module.config.js
```

When using bind mounts, you'll need to go to the corresponding MFE folder and run:
```
nvm use
npm install
```

## Start Tutor in Dev Mode
Theoretically, you should be able to launch tutor in dev mode:
```
tutor dev launch
```
---
## Tutor Local "Production" Mode
Run tutor in emulated "production" mode (do not enable SSL if you're on your local machine).

## Local Mode
Before running Tutor in local mode, have your dev instance running. Login to the site admin using your superuser: `local.edly.io:8000/admin` and go to Site Configurations. Edit the config called `local.edly.io` to include the following:

```
{
    "ENABLE_PROFILE_MICROFRONTEND": "true",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
    "BASE_URL": "http://edly.io:8888",
    "CMS_HOST": "studio.local.edly.io",
    "COLLECT_YEAR_OF_BIRTH":"false",
    "CONTACT_URL":"http://edly.io:8888/support/",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "DATA_API_BASE_URL":"http://local.edly.io",
    "ENABLE_ACCOUNT_DELETION": "false",
    "ENABLE_COPPA_COMPLIANCE": "true",
    "ENABLE_DEMOGRAPHICS_COLLECTION": "false",
    "ENABLE_DOB_UPDATE": "false",
    "ENABLE_EDX_PERSONAL_DASHBOARD": "false",
    "ENABLE_JUMPNAV": "false",
    "FAVICON_URL": "http://edly.io:8888/favicon.svg",
    "INFO_EMAIL": "help@thegymnasium.com",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "http://local.edly.io",
    "LOGIN_ISSUE_SUPPORT_LINK": "http://edly.io:8888/support/",
    "LOGIN_URL": "http://local.edly.io/login",
    "LOGOUT_URL": "http://local.edly.io/logout",
    "LOGO_TRADEMARK_URL": "http://studio.local.edly.io/static/studio/gym-theme/images/studio-logo.png",
    "LOGO_URL": "http://studio.local.edly.io/static/studio/gym-theme/images/studio-logo.png",
    "LOGO_WHITE_URL": "http://studio.local.edly.io/static/studio/gym-theme/images/studio-logo.png",
    "MARKETING_EMAILS_OPT_IN": "",
    "MARKETING_SITE_BASE_URL": "http://edly.io:8888",
    "MFE_CONFIG_API_URL": "http://local.edly.io/api/mfe_config/v1",
    "NODE_ENV": "production",
    "ORDER_HISTORY_URL": "http://edly.io:8888",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:help@thegymnasium.com",
    "PRIVACY_POLICY": "http://edly.io:8888/privacy-policy/",
    "PRIVACY_POLICY_URL": "http://edly.io:8888/privacy-policy/",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://local.edly.io/login_refresh",
    "SEARCH_CATALOG_URL":"http://edly.io:8888/courses/",
    "SECURE_COOKIES": "true",
    "SEGMENT_KEY": "",
    "SHOW_ACCESSIBILITY_PAGE": "false",
    "site_domain": "edly.io",
    "SITE_NAME": "Gymnasium",
    "STUDIO_BASE_URL": "http://studio.local.edly.io",
    "SUPPORT_URL": "http://edly.io:8888/support/",
    "SUPPORT_URL_TO_UNLINK_SOCIAL_MEDIA_ACCOUNT": "http://edly.io:8888/support/",
    "SESSION_COOKIE_DOMAIN": "edly.io",
    "SHARED_COOKIE_DOMAIN": "edly.io",
    "SUPPORT_EMAIL": "mailto:help@thegymnasium.com",
    "TERMS_OF_SERVICE_URL": "http://edly.io:8888",
    "TOS_AND_HONOR_CODE": "http://edly.io:8888",
    "TOS_LINK": "http://edly.io:8888",
    "USER_INFO_COOKIE_NAME": "edx-user-info"
}
```
Note: some of the above may be overkill. We will likely be able to get away with fewer configs, TBD.

Stop dev tutor: `tutor dev stop`

### 1. Running in "local" mode on your local machine:

Make sure 11ty is running locally in `local:tutor` mode: `npm run local:tutor`.


Disable development plugins, enable production plugins:
```
tutor plugins disable course-about-dev; tutor plugins enable course-about-prod
```

Save your config again:
```
tutor config save
```

1. (Re)Build Images
```
tutor images build openedx mfe

```
If you have issues, you could try the command above with the ` --no-cache --no-registry-cache` flags.

Start tutor in local mode:
`tutor local launch`


#### 2. Running an actual production environment
Let's use `gym.soy` as our example.  Rename `.env.production.example` to `.env.production` and update the value(s) to match the `gym.soy` production environment accordingly.

1. On first launch:
```
tutor images build openedx --no-cache --no-registry-cache
tutor images build mfe --no-cache --no-registry-cache
tutor local launch
```

If the image fails to build, run the command again without the flags, and it will pick up from where it left off: `tutor images build openedx` or `tutor images build mfe`

On subsequent launches, start tutor in detached mode.

```
tutor local start -d
```

## Additional WIP instructions:

### Setting a theme
This theme is set automatically via a shell script, but just in case, here is how to do it manually.
```
tutor local do settheme gym-theme
```

### Other commands

Restart LMS in tutor local mode:
```
tutor local restart openedx
```

Restart specific MFEs in tutor dev mode:
```
tutor dev restart learning-dev
```

Subsequently, start up as follows:

```
git submodule update --recursive --remote
tutor config save
tutor dev launch
```

## Getting Started

Start/stop services with:

```
tutor dev start -d
tutor dev stop
```

### Tutor Dev Endpoints:

* Marketing site: http://edly.io:8888
* LMS: http://local.edly.io:8000
* Studio: http://local.edly.io:8001
* Account: http://apps.local.edly.io:1997/account/
* Authn: http://apps.local.edly.io:1999/authn/
* Course About: http://apps.local.edly.io:3000/courses/{course-id}/about
* Learner Dashboard: http://apps.local.edly.io:1996/learner-dashboard/ or http://local.edly.io:8000/dashboard/
* Learning (Courseware): http://apps.local.edly.io:2000/learning/course/{course-id}/home
* Profile: http://apps.local.edly.io:1995/profile/u/{username}

### Tutor Local "Production" Endpoints:

* Marketing site: http://edly.io:8888
* LMS: http://local.edly.io
* Studio: http://studio.local.edly.io
* Account: http://apps.local.edly.io/account/
* Authn: http://apps.local.edly.io/authn/
* Course About: http://local.edly.io/courses/{course-id}/about
* Learner Dashboard: http://apps.local.edly.io/learner-dashboard/ or http://local.edly.io/dashboard/
* Learning (Courseware): http://apps.local.edly.io/learning/course/{course-id}/home
* Profile: http://apps.local.edly.io/profile/u/{username}

## Add Admin User(s)

Dev:
```
tutor dev do createuser --staff --superuser admin admin@example.com
```

Local:
```
tutor local do createuser --staff --superuser admin admin@example.com
```

# Troubleshooting

## Reindex/backfill courses after importing them

```
tutor local run cms ./manage.py cms reindex_course --all
tutor local run cms ./manage.py cms backfill_course_outlines
tutor local run cms ./manage.py cms backfill_course_tabs
tutor local run cms ./manage.py cms backfill_course_end_dates
```

## Migrations
`manage.py makemigrations` (make new migrations)
`manage.py migrate` (apply migrations)

## Verbose Output During Image Builds
- `tutor images build mfe --docker-arg --progress=plain`

## Docker Commands

### Removing build cache:
`docker buildx prune -f`

### Clear entire docker system:
`docker system prune -f`

### Prune only build cache:
`docker builder prune`

### Prune images not associated with container:
`docker image prune -a`

### Remove dangling build cache/images:
`docker image prune -f`

### Remove all images (including ones tagged or associated with a container):
`docker image prune -a -f`

### Show unused containers:
`docker ps --filter status=exited --filter status=dead -q`

## Parallelism
Docker's default is to utilize all available CPUs in parallel, and this can often cause the MFE image builds to fail. In this event, you can run the following command to limit builds to 1 CPU.

```
docker buildx create --use --name=singlecpu --config=./buildkitd-single.toml
```
Alternately, here are some multi-CPU configs:

Dual:
```
docker buildx create --use --name=dualcpu --config=./buildkitd-dual.toml
```

Triple:
```
docker buildx create --use --name=dualcpu --config=./buildkitd-triple.toml
```

Quad:
```
docker buildx create --use --name=dualcpu --config=./buildkitd-quad.toml
```

Note: personally, I've had the most success running a single CPU build.

**Note:** Sometimes `tutor images build` will fail due to network connectivity issues. If this happens, simply retry the command.
