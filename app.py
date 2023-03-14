from flask import Flask , request
from youtube import Youtube

app = Flask(__name__)


@app.get('/youtube_auth_access_url')
def get_youtube_access_request_url():
    return {'uri':Youtube().get_authorization_url()}, 200


@app.get('/youtube_auth_access_token')
def get_youtube_access_token():
    code = request.args.get("code")
    # TODO : get access token using Youtube().set_refresh_token(the redirected url)
    refresh_token = Youtube().set_refresh_token(code=code)
    return {"refresh_token":refresh_token},200

@app.get('/get_youtube_videos')
def get_youtube_videos():
    data = request.headers

    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return {"status":"refresh_token not present in the header","success":False},400
    

    try:
        youtube_client = Youtube()
        youtube_client.refresh_token = refresh_token

        videos = youtube_client.get_videos()
        
        return {"videos":videos,"success":True},200

    except:
        return {"videos":"Internal Server Error"},500

app.run(debug=True)