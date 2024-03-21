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
tvm install v17.0.1
```


1. Create a main directory to house your tutor configs (for example `your-home folder/dev/tutor/`), ideally one that you can find easily via CLI. 
```
mkdir ~/tutor
```

## Once per TVM project

1. Create a new TVM project
Please note the project title cannot include periods, lest TVM puke. In this case, TVM will automatically create a new directory for you.
```
tvm project init quince_1 v17.0.1
```

1. enter the directory:
```
cd quince_1
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

1. Run tutor once to ensure it is set up properly
```
tutor local launch
```

Once you've confirmed it's running successfully, let's go about implementing the customizations:

1. Stop Tutor:
```
tutor local stop
```



1.  Clone the this repo into the directory
```
git init .
git remote add origin https://github.com/gymnasium/gym-custom-tutor-config
git pull origin gym.quince.1 --recurse-submodules
```


## Custom Tutor Initialization
The following commands should be executed from the project root folder. Make sure your static site is running at port 8888.

On first install, run the following to install packages for our customized Tutor:
```
git submodule update --init --recursive
pip install -U -r requirements.txt
```
Install our custom plugins (from the project root)
```
pip install -e plugins/gym-theme
pip install -e plugins/gym-mfe
```

```
tutor config save
<!-- tutor dev do init -->

tutor images build all
tutor dev launch


tutor dev do settheme gym-theme
tutor dev restart openedx

tutor images build openedx-dev?
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