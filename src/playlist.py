import os

import datetime

import isodate

from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.get_service().playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails,snippet',
            maxResults=50, ).execute()
        self.channel_id = self.playlist_videos['items'][0]['snippet'][
            'channelId']
        self.playlists = PlayList.get_service().playlists().list(
            channelId=self.channel_id,
            part='contentDetails,snippet',
            maxResults=50, ).execute()
        for playlist in self.playlists['items']:
            if playlist['id'] == self.playlist_id:
                self.title = playlist['snippet']['title']
        self.url = (f"https://www.youtube.com/playlist?list="
                    f"{self.playlist_id}")

    @property
    def total_duration(self):
        """Возвращает суммарную длительность всех видео плейлиста"""

        total_duration = datetime.timedelta()  # по умолчанию все по нулям

        video_response = self.get_video_response()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        video_response = self.get_video_response()
        max_count_likes = 0
        id_of_best_video = ''

        for video in video_response['items']:
            if int(video["statistics"]["likeCount"]) > max_count_likes:
                max_count_likes = int(video["statistics"]["likeCount"])
                id_of_best_video = video["id"]
        return f"https://youtu.be/{id_of_best_video}"

    def get_video_response(self):
        """достает список из словарей с информацией по каждому видео из плейлиста"""
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails', maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)).execute()
        return video_response

    @classmethod
    def get_service(cls):
        api_key = os.getenv("YOUTUBE_API_KEY")
        return build("youtube", 'v3', developerKey=api_key)
