# Tutor Custom

- These instructions are WIP.
- These instructions are currently specific to Mac OS.

## Prerequisites
This proof-of-concept Tutor config depends on a separate marketing frontend running at `local.overhang.io`. See the [gym-eleventy](https://github.com/gymnasium/gym-eleventy) repo for specific instructions running the netlify CLI locally.

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

1. Create a directory to house your tutor configs (for example `your-home folder/dev/tutor/tutor_version`), ideally one that you can find easily via CLI.
```
mkdir 
```

1. Create a new TVM project
Please note the project title cannot include periods, lest TVM puke.
```
tvm project init <tutor-version>@<project-name>
# tvm project init gym-quince-1 v17.0.1
```


1. enter the project directory and clone the relevant branch of this repo:
```
cd gym-quince-1
```

1. Allow direnv access to the folder (only needed initially)
```
direnv allow
```

1. Activate the environment:
```
source .tvm/bin/activate
```

1. Clone either the specific branch or the entire repo as determined by your needs.
```
git clone --branch <branchname> <remote-repo-url>
# git clone --branch gym.quince.1 https://github.com/gymnasium/custom-tutor-hackery.git
```

## Tutor Initialization

On first install, run the following to initialize Tutor:
```
git submodule update --init --recursive
pip install -U -r requirements.txt
tutor config save
tutor dev do init
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

* LMS: http://local.overhang.io:8000
* Studio: http://local.overhang.io:8001
* Account: http://apps.local.overhang.io:1997/account/
* Authn: http://apps.local.overhang.io:1999/authn/
* Course About: http://apps.local.overhang.io:3000/courses/{course-id}/about
* Learning (Courseware): http://apps.local.overhang.io:2000/learning/course/{course-id}/home
* Profile: http://apps.local.overhang.io:1995/profile/u/{username}

### Tutor "Production" Endpoints:

* LMS: http://local.overhang.io
* Studio: http://studio.local.overhang.io
* Account: http://apps.local.overhang.io/account/
* Course About: http://apps.local.overhang.io/courses/{course-id}/about
* Learning (Courseware): http://apps.local.overhang.io/learning/course/{course-id}/home
* Profile: http://apps.local.overhang.io/profile/u/{username}

## Add Admin User(s)

```
tutor dev do createuser --staff --superuser admin admin@example.com
```

## Running MFEs in Development Mode

To run an MFE in development mode, you would need to clone it and to mount it's directory

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
1. Simliar to adding the header we can also add other pkgs, like footer, brand, paragon...etc.

## Building and runnning MFEs in production mode

If you want to test the MFEs in a production like environment (e.g. the platform root page will be replaced by the Home MFE application) you can do so by running:

    tutor images build mfe
    tutor local start mfe caddy
