from functools import wraps
from pyyoutube import PyYouTubeException
def youtube_exception_handler(function):
    @wraps(function)
    def inner(*args,**kwargs):
        try:
            return function(*args,**kwargs)
        except PyYouTubeException as error:
            return {"message":error.message},error.status_code

    return inner