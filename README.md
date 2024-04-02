# Tutor Custom

- These instructions are WIP.
- These instructions are currently specific to Mac OS.

## Prerequisites
This proof-of-concept Tutor config depends on a separate marketing frontend running at `edly.io:8888`. See the [gym-eleventy](https://github.com/gymnasium/gym-eleventy) repo for specific instructions on running locally it using the netlify CLI.

## Installation


### direnv
1. Install direnv
```
brew install direnv
```

Be sure to add the relevant hook to your shell: https://direnv.net/docs/hook.html

### TVM
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
git pull origin gym.quince.1 --recurse-submodules
```


## Custom Tutor Initialization
The following commands should be executed from the project root folder. Make sure your static site is running at port 8888.

### Setup
On first install, run the following to install packages for our customized Tutor:
```
git submodule update --init --recursive
pip install -U -r requirements.txt
```
Install our custom plugins (from the project root)
```
pip install -e plugins/gym-theme
```
Then, enable the plugins:

```
tutor plugins enable gym-theme
```

Save the config again:
```
tutor config save
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

#### Bind Mounts
Since dev uses bind mounts in the config, you'll need to go to each MFE folder and run:
```
nvm use
npm install
```

###n Start Tutor in Dev Mode
Theoretically, you should be able to:
```
tutor dev launch
```

### Tutor Local Mode
This is to run tutor in "production" mode.

#### Instructions TBD/WIP:

Make sure eleventy is running in `tutor:local` mode: `npm run tutor:local`.


Disable development course-about plugin:
```
tutor plugins disable course-about-mfe
```

Enable production course-about plugin:

```
tutor plugins enable course-about-mfe-production
```


```
tutor images build openedx --no-cache --no-registry-cache
tutor images build mfe --no-cache --no-registry-cache
```


And then:

```
tutor local launch
```

## TODO: sort out more instructions:

### Setting a theme
This theme is set automatically via a shell script, but just in case, here is how to do it manually.
```
tutor local do settheme gym-theme
```

### Other commands

Restart LMS:
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
* Learning (Courseware): http://apps.local.edly.io:2000/learning/course/{course-id}/home
* Profile: http://apps.local.edly.io:1995/profile/u/{username}

### Tutor "Production" Endpoints:

* Marketing site: http://edly.io:8888
* LMS: http://local.edly.io
* Studio: http://studio.local.edly.io
* Account: http://apps.local.edly.io/account/
* Course About: http://apps.local.edly.io/courses/{course-id}/about
* Learning (Courseware): http://apps.local.edly.io/learning/course/{course-id}/home
* Profile: http://apps.local.edly.io/profile/u/{username}

## Add Admin User(s)

```
tutor dev do createuser --staff --superuser admin admin@example.com
```

## Running MFEs in Development Mode

To run an MFE in development mode, you would need to clone it and to mount its directory

 Assuming you need to modify `frontend-app-account`.

1. Clone it _if it's not already_ 
2. from within the MFE directory, `npm install` _make sure you are on the correct node version `node --version` it shall match `cat .nvmrc`_
3. from the tutor root directory, `tutor mounts add "./mfe/frontend-app-account"`. 

### How do I override specific npm pks?

The following is an example of overriding a header

1. Clone it _if it's not already_
1. `npm install` _make sure you are on the correct node version `node --version` it shall match `cat .nvmrc`_
1. Mount the pkg to the container `tutor  mounts add "account:./mfe/frontend-component-header:/openedx/frontend-component-header"` scheme: `service:host_path:containter_path`
1. Mount the `module.config.js` file, assuming it's `mfe/`, `tutor mounts add account:./mfe/module.config.js:/openedx/app/module.config.js`
1. then run `npm install` _Note: in step 2 we run it inside header, now inside account mfe_
1. Similar to adding the header we can also add other pkgs, like footer, brand, paragon...etc.

## Building and runnning MFEs in production mode

If you want to test the MFEs in a production like environment (e.g. the platform root page will be replaced by the Home MFE application) you can do so by running:

    tutor images build mfe
    tutor local start mfe caddy


## Reindex/backfill courses after importing them

```
tutor local run cms ./manage.py cms reindex_course --all
tutor local run cms ./manage.py cms backfill_course_outlines
tutor local run cms ./manage.py cms backfill_course_tabs
tutor local run cms ./manage.py cms backfill_course_end_dates
```


## Docker Commands

#### Prune Unused Images
This is very useful when building tutor images.
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