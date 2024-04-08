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
1. Install [Tutor Version Manager](https://github.com/eduNEXT/tvm)
```
pip install git+https://github.com/eduNEXT/tvm.git
```

1. Install the Tutor version you wish to use.
```
tvm install v17.0.3
```


1. Create a main directory to house your tutor configs (for example `your-home folder/dev/tutor/`), ideally one that you can find easily via CLI. 
```
mkdir ~/tutor
```

## Once per TVM project

1. Create a new TVM project
Please note the project title cannot include periods, lest TVM puke. In this case, TVM will automatically create a new directory for you.
```
tvm project init quince_2 v17.0.3
```

1. enter the directory:
```
cd quince_2
```

1. Activate the environment:
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
git pull origin gym.quince.2 --recurse-submodules
```

1. On first install, from the project root folder, run the following to install packages for our customized Tutor:
```
git submodule update --init --recursive
pip install -U -r requirements.txt
```

### Tutor Dev Mode

Then to run in dev mode, make sure 11ty is running in `local` mode: `npm run local`, and available at `http://edly.io:8888`.

```
tutor config save
```

Build dev images
```
tutor images build openedx-dev --no-cache --no-registry-cache
tutor images build account-dev --no-cache --no-registry-cache
tutor images build authn-dev --no-cache --no-registry-cache
tutor images build course-about-dev --no-cache --no-registry-cache
tutor images build course-authoring-dev --no-cache --no-registry-cache
tutor images build discussions-dev --no-cache --no-registry-cache
tutor images build learner-dashboard-dev --no-cache --no-registry-cache
tutor images build learning-dev --no-cache --no-registry-cache
tutor images build profile-dev --no-cache --no-registry-cache
```

#### Dev Mode Bind Mount Setup
Add the following lines to your config.yml:

```
MOUNTS:
- ./mfe/frontend-app-account
- ./mfe/frontend-app-authn
- ./mfe/frontend-app-course-about
- ./mfe/frontend-app-learner-dashboard
- ./mfe/frontend-app-learning
- ./mfe/frontend-app-profile
- account:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend
- authn:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend
- course-about:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend
- learner-dashboard:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend
- learning:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend
- profile:./mfe/gym-frontend-components:/openedx/app/node_modules/@edx/gym-frontend

```


Since dev uses bind mounts in the config, you'll need to go to each MFE folder and run:
```
nvm use
npm install
```

### Start Tutor in Dev Mode
Theoretically, you should be able to launch tutor in dev mode:
```
tutor dev launch
```

## Tutor Local "Production" Mode
This is to run tutor in "production" mode.

### 1. Running locally:

Make sure 11ty is running locally in `tutor:local` mode: `npm run tutor:local`.


Disable development course-about plugin:
```
tutor plugins disable course-about-dev
```

Enable production course-about plugin:

```
tutor plugins enable course-about-prod
```

Save your config again:
```
tutor config save
```

#### Build images on your local machine (not a production environment)
This is assuming you're running 
If you're building on an actual production server, use the next set of instructions instead.
```
tutor images build openedx --no-cache --no-registry-cache
tutor images build mfe --no-cache --no-registry-cache
```

#### 2. Running an actual production environment
Let's use `gym.soy` as our example.
```
tutor images build openedx mfe --no-cache --no-registry-cache --build-arg NODE_ENV='production' --build-arg MARKETING_SITE_BASE_URL='https://gym.soy' --build-arg SHARED_COOKIE_DOMAIN='gym.soy'
```

And then:

```
tutor local launch
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
tutor dev restart openedx
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
tutor dev start
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

## Reindex/backfill courses after importing them

```
tutor local run cms ./manage.py cms reindex_course --all
tutor local run cms ./manage.py cms backfill_course_outlines
tutor local run cms ./manage.py cms backfill_course_tabs
tutor local run cms ./manage.py cms backfill_course_end_dates
```


## Docker Commands

#### Prune Unused Images
This is very useful when recovering from failed image builds.

`docker buildx prune -f`


# Troubleshooting

### Failed builds
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
