from pprint import pprint
from youtube import Youtube
# generating authorisation url
yt = Youtube()
# url = yt.get_authorization_url()
# print(url)

# using the url
# refresh_token = yt.set_refresh_token("https://localhost/?state=Python-YouTube&code=4/0AWtgzh6J8etr26aqgfd8wXDGz0UEpLdf06bpgYFNV8P-vy8k8f2cVHMSwVVVGvGQFCjV3Q&scope=profile%20https://www.googleapis.com/auth/youtube%20https://www.googleapis.com/auth/userinfo.profile")
# 1//0gyzyssrwsi3TCgYIARAAGBASNwF-L9IrKG2BlnC7uoNjUPcwMEC8Z6ht5lWqHT_6puXAFr47IHNVp3I1Ug6BzLbWIjM0o2_vG9k

# setting the refresh token
yt.refresh_token = "1//0gyzyssrwsi3TCgYIARAAGBASNwF-L9IrKG2BlnC7uoNjUPcwMEC8Z6ht5lWqHT_6puXAFr47IHNVp3I1Ug6BzLbWIjM0o2_vG9k"

# using it to get details
videos = yt.get_videos()
token = videos.get("next_page_taken")
# # print(videos.id.videoId)
pprint(videos)

pprint(yt.get_videos(page_token=token,q="2023"))
# for vid in videos:
#     pprint(vid.id.videoId)

channel = yt.channel_data()
# pprint(chanel)