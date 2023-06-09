from pyyoutube import Client
from dotenv import load_dotenv
import os
load_dotenv(".env")
from pprint import pprint
from pyyoutube.media import Media
import pyyoutube.models as mds
from io import BytesIO

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
video_per_query = os.environ.get("video_per_query") # for pagination purpose

class Youtube:
    """A abstract class for using the pyyoutube wrapper api"""

    video_sort_accepted_values = ["publishedAt","title"]

    def __init__(self,refresh_token=None):
        self.check_client_env() # checking the environment for the dependency
        self.__refresh_token = refresh_token
        self.client = Client(client_id=client_id,client_secret=client_secret,refresh_token=self.__refresh_token)
        self.client.DEFAULT_SCOPE = [
            'https://www.googleapis.com/auth/youtube', 
            'https://www.googleapis.com/auth/youtube.force-ssl', 
            'https://www.googleapis.com/auth/youtube.readonly', 
            'https://www.googleapis.com/auth/youtube.upload', 
            'https://www.googleapis.com/auth/youtubepartner', 
            ]


    def __repr__(self):
        data = {
            "access_token":self.client.access_token,
            "refresh_token":self.refresh_token
        }
        return str(data)

    @property
    def refresh_token(self):
        """For getting refresh token"""
        return self.client.refresh_token
    
    @refresh_token.setter
    def refresh_token(self,token):
        """For setting refresh_tokens"""
        access_token = self.client.refresh_access_token(token).access_token
        self.client.access_token = access_token

    def get_authorization_url(self):
        """For getting authorisation url"""
        url,state = self.client.get_authorize_url(prompt="consent")
        return url

    def set_refresh_token(self,code):
        """
            @params authorization_response_url : the url where we will be redirected as a response after getting authorisation url
            @return refresh_token
        """
        # self.client.generate_access_token(authorization_response=authorization_response_url)
        self.client.generate_access_token(code=code)
        return self.client.refresh_token
        
    # Videos
    def get_videos(self,page_token=None,q=None,order=None,descending=True):
        """
        for getting all videos of the user
        @params page_token for getting the page
        @params q for searching any video with any queries like name to get the matching results
        @params order for sorting data.
            Accepted values -> publishedAt,title
        @returns dict(next_page_taken,videos)
        """


        order = order if order in self.video_sort_accepted_values else None
        # nextPageToken is None if all videos are retrieved
        videos_details = self.client.search.list(type="video",for_mine=True,max_results=video_per_query,page_token=page_token,q=q)
        
        if order:
            videos = sorted(videos_details.items,key=lambda x: getattr(x.snippet,order), reverse=descending)
        
        else:
            videos = videos_details.items

        urls = [self.video_factory(vid) for vid in videos]

        return {
            "next_page_taken":videos_details.nextPageToken, 
            "videos":urls
        }
    
    @staticmethod
    def get_video_url(id):
        """for building the youtube url with video id"""
        url_string = f"https://www.youtube.com/watch?v={id}"
        return url_string

    @staticmethod
    def video_factory(video_object):
        # thumbnails -> high , maxres , medium , standard
        video_id = Youtube.__get_id(video_object).videoId
        return {
            "thumbnail":Youtube.__get_thumbnails(video_object),
            "url" : Youtube.get_video_url(video_id),
            "videoId":video_id,
            "title":Youtube.__get_title(video_object),
            "description":Youtube.__get_description(video_object)
        }
    
    # Channel
    def channel_data(self):
        """For getting the channel data of the connected user"""
        channel = self.client.channels.list(mine=True).items[0]
        return self.channel_factory(channel)

    @staticmethod
    def channel_factory(channel_object):
        # thumbnails -> high , maxres , medium , standard
        id = Youtube.__get_id(resource=channel_object)
        return {
            "id":id,
            "url":Youtube.get_channel_url(id),
            "channel_name" : Youtube.__get_title(channel_object),
            "thumbnail":Youtube.__get_thumbnails(channel_object)
        }
    
    @staticmethod 
    def get_channel_url(channel_id):
        return f"https://www.youtube.com/channel/{channel_id}"


    @staticmethod
    def check_client_env():
        """For checking the environement variables for client_id and client_secret"""
        env_not_present =  not client_id or not client_secret or not video_per_query
        if env_not_present:
            raise Exception("Please set client_id and client_secret and video_per_query in the environment")
    
    ## upload video
    def upload_video(self,video_file,video_title=None):
        file_bytes = BytesIO(video_file)
        body = mds.VideoSnippet(title=video_title)
        media = Media(fd=file_bytes)
        upload = self.client.videos.insert(
            body=body,media=media,parts=["snippet"]
        )
        response = None
        while response is None:
            status, response = upload.next_chunk()
            if status is not None:
                print(f"Uploading video progress: {status.progress()}...")

        video = mds.Video.from_dict(response)
        return video.id
    
    def upload_caption(self,video_id,caption_file):
        file_bytes = BytesIO(caption_file)
        snippet = {
            'videoId': video_id,
            'language': 'en',
            "name": "English",
        }   
        caption = mds.CaptionSnippet(**snippet)
        body = mds.Caption(snippet=caption)
        srt_file = Media(fd=file_bytes)
        upload = self.client.captions.insert(body=body,media=srt_file)
        response = None
        while response is None:
            status,response = upload.next_chunk()
            if status is not None:
                print(f"Uploading video progress: {status.progress()}...")

        return response

    # Utility methods
    @staticmethod
    def __get_info(resource):
        """
        @params resource -> channel,video,etc
        """
        attribute_name = "snippet"
        return getattr(resource,attribute_name,None)
    
    @staticmethod
    def __get_id(resource):
        """
        @params resource -> channel,video,etc
        """
        attribute_name = "id"
        return getattr(resource,attribute_name)
    
    @staticmethod
    def __get_title(resource):
        resource_info = Youtube.__get_info(resource)
        return getattr(resource_info,"title",None)
    
    @staticmethod
    def __get_description(resource):
        resource_info = Youtube.__get_info(resource)
        return getattr(resource_info,"description",None)
    
    @staticmethod
    def __get_thumbnails(resource,thumbnail_size="medium"):
        # thumbnails -> high , maxres , medium , standard
        # resource.thumbnails.medium.url
        resource_info = Youtube.__get_info(resource)
        thumbnail = getattr(resource_info,"thumbnails",None)

        if thumbnail == None:
            return None

        medium_thumnail = getattr(thumbnail,thumbnail_size,None)      
        if medium_thumnail==None:
            return None
        
        return medium_thumnail.url