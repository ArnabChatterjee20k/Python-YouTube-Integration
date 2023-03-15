from flask import Flask , request , redirect , g
from youtube import Youtube
from refresh_token_required import refresh_token_required
app = Flask(__name__)


@app.get('/youtube_auth_access_url')
def get_youtube_access_request_url():
    return redirect(Youtube().get_authorization_url())


@app.get('/youtube_auth_access_token')
def get_youtube_access_token():
    code = request.args.get("code")
    # TODO : get access token using Youtube().set_refresh_token(the redirected url)
    refresh_token = Youtube().set_refresh_token(code=code)
    return {"refresh_token":refresh_token},200

@app.get('/get_youtube_videos')
@refresh_token_required
def get_youtube_videos():

    try:
        youtube_client = Youtube()
        youtube_client.refresh_token = g.refresh_token

        videos = youtube_client.get_videos()
        
        return {"videos":videos,"success":True},200

    except:
        return {"videos":"Internal Server Error"},500


@app.get("/get_channel_info")
@refresh_token_required
def get_channel_info():
    try:
        youtube_client = Youtube()
        youtube_client.refresh_token = g.refresh_token

        channel = youtube_client.channel_data()
        
        return {"channel":channel,"success":True},200

    except:
        return {"videos":"Internal Server Error"},500

app.run(debug=True) 