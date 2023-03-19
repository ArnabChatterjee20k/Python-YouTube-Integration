from pprint import pprint
from youtube import Youtube
yt = Youtube()
yt.refresh_token = "1//0glhaJscVcoJ8CgYIARAAGBASNwF-L9IrOJdeu7sWsgl3oTjPOLnb20recIij0U61zqNivwGOyTTyZAns8BIGSJzmPmCP3ss5OTQ"

with open("test.mkv","rb") as f:
    res = yt.upload_video(video_title="Arnab",file_bytes=f)
print(res)