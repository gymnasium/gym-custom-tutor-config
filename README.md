# Installation and local development

If you are using direnv, activate the virtualenv with:

    direnv allow

Otherwise create and activate a Python virtualenv with your favourite library.
Then setup requirements and prime the databases (required just the first time)  with:

```
git submodule update --init
pip install -U -r requirements.txt
tutor config save
tutor dev do init
```

Start/stop services with:

```
tutor dev start
tutor dev stop
```

Example services endpoints for the development environment:

* http://localhost:8000 or http://local.overhang.io:8000 (LMS)
* http://localhost:8001 or http://local.overhang.io:8001 (CMS)
* http://localhost:1994/gradebook/ or http://apps.local.overhang.io:1994/gradebook/ (Gradebook MFE)
* http://localhost:1995/profile/ or http://apps.local.overhang.io:1995/profile/ (Profile MFE)
* http://localhost:1997/account/ or http://apps.local.overhang.io:1997/account/ (Account MFE)
* http://localhost:2000/learning/ or http://apps.local.overhang.io:2000/learning/ (Learning MFE)
* http://localhost:3000/about/ or http://apps.local.overhang.io:3000/course_about/ (Course About MFE)
* http://localhost:3001/home/ or http://apps.local.overhang.io:3001/home/ (Home MFE)

Example services endpoints for the production like environment:

* http://local.overhang.io (Home MFE)
* http://local.overhang.io/courses (LMS)
* http://studio.local.overhang.io (CMS)
* http://apps.local.overhang.io/profile/u/abstract (Profile MFE)
* http://apps.local.overhang.io/gradebook/course-v1:Test+101+01 (Gradebook MFE)
* http://apps.local.overhang.io/account (Account MFE)
* http://apps.local.overhang.io/learning/course/course-v1:Test+101+01 (Learning MFE)
* http://local.overhang.io/courses/course-v1:Test+101+01/about (Course About MFE)

## Add admin user

```
tutor dev do createuser --staff --superuser admin admin@example.com
```

## MFE development

Read the [Tutor docs](https://github.com/overhangio/tutor-mfe#mfe-development) on MFE development.

TL;DR

Start the services in development mode. Be careful when using `tutor dev start` as it will start all services, requiring a lot of resources (it nearly crashed my system). Specifying individual services might be needed.

In this example we'll start development of the Profile MFE. In order to render it properly it needs to be access throught the LMS with an authenticated user, thus we are starting only the `lms` and `authn` MFE services.

```
tutor dev start lms authn
```

Then start the profile MFE mounting our local fork in a different shell:

```
mfe_dev profile
```

It's important that MFE directories names start with the `frontend-app` magic words, otherwise this won't work.

The MFE application will be accessible at `http://apps.local.overhang.io:{{ PORT }}/{{ NAME }}/`. The `PORT` and `NAME` parameters for the specific MFE can be found in `config.yml`.
(e.g. http://apps.local.overhang.io:1995/profile/)


## Building customized MFEs dev images

In order to build dev images of custom MFE run:

    tutor images build mfe -d "-t=docker.io/overhangio/openedx-{{name}}-dev:15.0.5" --target {{name}}-dev

## Building and runnning the Home MFE in development mode

Build the dev image:

    tutor images build mfe -d "-t=docker.io/overhangio/openedx-home-dev:15.0.5" --target home-dev

Then you should be able to run:

    mfe_dev home

And browse the MFE at http://apps.local.overhang.io:3001/home/

## Building and runnning MFEs in production mode

If you want to test the MFEs in a production like environment (e.g. the platform root page will be replaced by the Home MFE application) you can do so by running:

    tutor images build mfe
    tutor local start mfe caddy
