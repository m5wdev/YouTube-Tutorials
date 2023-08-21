"""
    This class using for clean /media/ folder from empty dirs
    and for delete unused imagekit module files
"""

import os, itertools
from django.conf import settings


class CleanMedia:
    def __init__(self):
        self.MEDIA_ROOT = settings.MEDIA_ROOT

    """
        [ Delete imagekit chache file ]

        Use this method inside signal, when image instance is available e.g.:

        @receiver(post_delete, sender=Image)
        def post_clean_empty_dirs(sender, instance, **kwargs):
            cleanMedia = CleanMedia()
            cleanMedia.cleanImagekitCacheImage(instance.image_thumbnail_admin)
    """
    def cleanImagekitCacheImage(self, img_instance):
        path_to_img_cache = os.path.join(self.MEDIA_ROOT, str(img_instance))
        os.remove(path_to_img_cache)
        print('[CACHED IMG REMOVED] {}'.format(path_to_img_cache))


    """
        [ Get all empty dirs inside MEDIA_ROOT folder ]
    """
    def getEmptyDirs(self) -> list:
        empty_dirs = list()
        for root, dirs, files in os.walk(self.MEDIA_ROOT):
            # Get empty dirs
            if not len(dirs) and not len(files):
                empty_dirs.append(root)
        return empty_dirs


    """
        [ Delete one directory ]
    """
    def deleteDir(self, dir_to_delete):
        try:
            os.rmdir(dir_to_delete)
            print('[REMOVED] ' + dir_to_delete)
        except OSError as e:
            print(e)
            pass


    """
        [ Delete empty directories ]
    """
    def deleteEmptyDirs(self):
        return list(map(self.deleteDir, self.getEmptyDirs()))


    """
        [ Delete empty directories recusive ]

        Usage example:

        @receiver(post_delete, sender=Image)
        def post_clean_empty_dirs(sender, instance, **kwargs):
            cleanMedia = CleanMedia()
            cleanMedia.deleteEmptyDirsRecusive()
    """
    def deleteEmptyDirsRecusive(self, repeat=10):
        # repeat deleting iterations N times
        for _ in itertools.repeat(None, repeat):
            for directory in self.getEmptyDirs():
                self.deleteEmptyDirs()
        print('[REMOVE RECUSIVE {} TIMES]'.format(repeat))
