from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()

def mfe_forks(mfes):
    mfes["account"] = {
        "repository": "https://github.com/gymnasium/frontend-app-account.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-account/git/refs/heads",
        "port": 1997,
        "name": "account",
    }
    mfes["authn"] = {
        "repository": "https://github.com/gymnasium/frontend-app-authn.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-authn/git/refs/heads",
        "port": 1999,
        "name": "authn",
    }
    mfes["course-about"] = {
        "repository": "https://github.com/gymnasium/frontend-app-course-about.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-course-about/git/refs/heads",
        "port": 3000,
        "name": "course-about",
    }
    mfes["discussions"] = {
        "repository": "https://github.com/gymnasium/frontend-app-discussions.git",
        "version": "gym.quince.1",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-discussions/git/refs/heads",
        "port": 2002,
        "name": "discussions",
    }
    mfes["learner-dashboard"] = {
        "repository": "https://github.com/gymnasium/frontend-app-learner-dashboard.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-learner-dashboard/git/refs/heads",
        "port":1996,
        "name": "learner-dashboard",
    }
    mfes["learning"] = {
        "repository": "https://github.com/gymnasium/frontend-app-learning.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-learning/git/refs/heads",
        "port": 2000,
        "name": "learning",
    }
    mfes["profile"] = {
        "repository": "https://github.com/gymnasium/frontend-app-profile.git",
        "version": "gym.quince.3",
        "refs": "https://api.github.com/repos/gymnasium/frontend-app-profile/git/refs/heads",
        "port": 1995,
        "name": "profile",
    }
    return mfes
