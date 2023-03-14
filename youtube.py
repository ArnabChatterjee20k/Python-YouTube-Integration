from pyyoutube import Client
from dotenv import load_dotenv
import os
load_dotenv(".env")
from pprint import pprint

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

class Youtube:
    """A abstract class for using the pyyoutube wrapper api"""

    def __init__(self,refresh_token=None):
        self.check_client_env() # checking the environment for the dependency
        self.__refresh_token = refresh_token
        self.client = Client(client_id=client_id,client_secret=client_secret,refresh_token=self.__refresh_token)

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
        url,state = self.client.get_authorize_url()
        return url

    def set_refresh_token(self,code):
        """
            @params authorization_response_url : the url where we will be redirected as a response after getting authorisation url
            @return refresh_token
        """
        # self.client.generate_access_token(authorization_response=authorization_response_url)
        self.client.generate_access_token(code=code)
        return self.client.refresh_token
        

    def get_videos(self):
        """for getting all videos of the user"""
        videos = self.client.search.list(type="video",for_mine=True).items
        # pprint(videos[0].to_dict())
        # urls = [self.get_url(vid.id.videoId) for vid in videos]
        urls = [self.video_factory(vid) for vid in videos]

        return urls
    
    @staticmethod
    def get_url(id):
        """for building the youtube url with video id"""
        url_string = f"https://www.youtube.com/watch?v={id}"
        return url_string

    @staticmethod
    def video_factory(video_object):
        # thumbnails -> high , maxres , medium , standard
        video_id = video_object.id.videoId
        video_info = video_object.snippet
        return {
            "thumbnail":video_info.thumbnails.medium.url,
            "url" : Youtube.get_url(video_id),
            "videoId":video_id,
            "title":video_info.title,
            "description":video_info.description
        }
        
    @staticmethod
    def check_client_env():
        """For checking the environement variables for client_id and client_secret"""
        env_not_present =  not client_id or not client_secret
        if env_not_present:
            raise Exception("Please set client_id and client_secret in the environment")