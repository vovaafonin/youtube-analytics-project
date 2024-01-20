import os
from googleapiclient.discovery import build
import json

api_key = os.getenv('YOUTUBE_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]
        self.dict = {"title": self.title, "description": self.description, "url": self.url,
                     "subscriber_count": self.subscriber_count,
                     "video_count": self.video_count, "self.view_count": self.view_count}

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        """Возвращает сумму подписчиков двух каналов"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Возвращает разность подписчиков двух каналов"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """Возвращает True, если у первого канала количество подписчиков больше, чем у второго канала """
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Возвращает True, если у первого канала количество подписчиков больше или равно, чем у второго канала """
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """Возвращает True, если у первого канала количество подписчиков меньше, чем у второго канала"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Возвращает True, если у первого канала количество подписчиков меньше или равно, чем у второго канала"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """Возвращает True, если у первого канала количество подписчиков равно количеству подписчиков второго канала"""
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращающий объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        channel_dict = self.dict
        with open(filename, 'w', encoding="windows-1251") as file:
            json.dump(channel_dict, file, ensure_ascii=False)
