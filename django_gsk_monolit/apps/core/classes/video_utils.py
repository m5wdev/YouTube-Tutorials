"""
    Some useful utilities to work with video
"""

import re


class VideoUtils:

    """ [ Get video id form YouTube link ] """
    @staticmethod
    def get_youtube_video_id(video_url) -> str:
        regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
        match = regex.match(video_url)
        if not match:
            print('This is NOT YouTube video url =(')
        return match.group('id')
