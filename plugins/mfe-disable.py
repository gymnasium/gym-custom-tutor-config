from tutormfe.hooks import MFE_APPS
from tutor import hooks

@MFE_APPS.add()

# Remove select MFEs (useful for testing, etc)
def _remove_stock_mfes(mfes):
    # if ("account" in mfes):
    #     mfes.pop("account")
    if ("communications" in mfes):
        mfes.pop("communications")
    if ("course-about" in mfes):
        mfes.pop("course-about")
    if ("course-authoring" in mfes):
        mfes.pop("course-authoring")
    # if ("discussions" in mfes):
    #     mfes.pop("discussions")
    if ("gradebook" in mfes):
        mfes.pop("gradebook")
    if ("ora-grading" in mfes):
        mfes.pop("ora-grading")
    if ("profile" in mfes):
        mfes.pop("profile")
    return mfes
