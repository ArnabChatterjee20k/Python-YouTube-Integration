from flask import Flask , request , redirect , g
from youtube import Youtube
from refresh_token_required import refresh_token_required
from youtube_exception_handler import youtube_exception_handler

app = Flask(__name__)


@app.get('/youtube_auth_access_url')
@youtube_exception_handler
def get_youtube_access_request_url():
    return Youtube().get_authorization_url()


@app.get('/youtube_auth_access_token')
@youtube_exception_handler
def get_youtube_access_token():
    code = request.args.get("code")
    # TODO : get access token using Youtube().set_refresh_token(the redirected url)
    refresh_token = Youtube().set_refresh_token(code=code)
    return {"refresh_token":refresh_token},200

@app.get('/get_youtube_videos')
@youtube_exception_handler
@refresh_token_required
def get_youtube_videos():
    # we cant use page token and video name together as we are fetching the initial results
    page_token = request.args.get("page_token")
    video_name = request.args.get("title")
    sort = request.args.get("sort")
    sort_type = request.args.get("sort_type")

    sort_type = True if sort_type=="descending" else False
    print(sort_type)

    youtube_client = Youtube()
    youtube_client.refresh_token = g.refresh_token
    videos = youtube_client.get_videos(page_token=page_token,q=video_name,order=sort,descending=sort_type)
    
    return {"data":videos,"success":True},200



@app.get("/get_channel_info")
@youtube_exception_handler
@refresh_token_required
def get_channel_info():
    youtube_client = Youtube()
    youtube_client.refresh_token = g.refresh_token

    channel = youtube_client.channel_data()
    
    return {"channel":channel,"success":True},200

@app.post("/upload_video")
@youtube_exception_handler
@refresh_token_required
def upload_video():
    youtube_client = Youtube()
    youtube_client.refresh_token = g.refresh_token

    video = request.files.get("video")
    caption = request.files.get("caption")

    video_id = youtube_client.upload_video(video_title=video.filename,video_file=video.read())
    if caption is not None:
        youtube_client.upload_caption(video_id=video_id,caption_file=caption.read())
    return {"id":video_id,"youtube_studio_url":f"https://studio.youtube.com/video/{video_id}/edit"}

@app.post("/upload_caption/<video_id>")
@youtube_exception_handler
@refresh_token_required
def upload_caption(video_id):
    youtube_client = Youtube()
    youtube_client.refresh_token = g.refresh_token
    caption = request.files.get("caption")
    youtube_client.upload_caption(video_id=video_id,caption_file=caption.read())
    return {"id":video_id,"youtube_studio_url":f"https://studio.youtube.com/video/{video_id}/edit"}



app.run(debug=True) 