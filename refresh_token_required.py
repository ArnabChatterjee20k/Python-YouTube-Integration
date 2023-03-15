from functools import wraps
from flask import request , g
def refresh_token_required(function):
    @wraps(function)
    def inner(*args,**kwargs):
        data = request.headers

        refresh_token = data.get("refresh_token")
        if not refresh_token:
            return {"status":"refresh_token not present in the header","success":False},400

        # setting the refresh_token in g to access it later
        g.refresh_token = refresh_token
        return function(*args,**kwargs)

    return inner