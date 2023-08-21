"""
    This class using for optimization uploaded images with PIL.Image
"""

import os
from PIL import Image
from django.conf import settings

from apps.core.classes.file_utils import FileUtils


class ImageOptimizer:
    def __init__(self, path_to_img):
        self.path_to_img = path_to_img

        if settings.MAX_IMG_WIDTH and settings.MAX_IMG_WIDTH > 1280:
            self.MAX_IMG_WIDTH = settings.MAX_IMG_WIDTH
        else:
            self.MAX_IMG_WIDTH = 1980

        if settings.IMG_QUALITY:
            self.IMG_QUALITY = settings.IMG_QUALITY
        else:
            self.IMG_QUALITY = 70

    def openImg(self):
        return Image.open(self.path_to_img)

    def getFormat(self) -> str:
        return self.openImg().format

    def getMode(self) -> str:
        return self.openImg().mode

    def getWidth(self) -> str:
        width, height = self.openImg().size
        return width

    def getHeight(self) -> str:
        width, height = self.openImg().size
        return height

    def getSizeInBytes(self) -> str:
        return os.stat(self.path_to_img).st_size

    def getSize(self) -> str:
        fu = FileUtils()
        return fu.format_bytes(self.getSizeInBytes())

    def convertToRGB(self):
        return self.openImg().convert('RGB')

    def convertToRGBA(self):
        return self.openImg().convert('RGBA')

    def fixImgMode(self):
        if self.getFormat() == 'JPEG' and self.getMode() != 'RGB':
            return self.convertToRGB()
        if self.getFormat() == 'PNG' and self.getMode() != 'RGBA':
            return self.convertToRGBA()
        else:
            return self.openImg()

    # This method count new image height proportional to seted with
    def newHeight(self, width):
        width_percent = (width / float(self.getWidth()))
        return int(float(self.getHeight()) * float(width_percent))

    # This method combines fixImgMode() and PIL.Image resize() method
    def fixModeAndResize(self, width):
        return self.fixImgMode().resize((self.MAX_IMG_WIDTH, self.newHeight(width)), Image.ANTIALIAS)

    def resizeImg(self):
        if self.getWidth() > self.MAX_IMG_WIDTH:
            return self.fixModeAndResize(self.MAX_IMG_WIDTH)
        # Enlarge image
        # if 1000 <= self.getWidth() < 1280:
        #     return self.fixModeAndResize(1280)
        # Skip image less then 640px width
        # if self.getWidth() < 640:
        #     print('Image is too small')
        #     return self.fixImgMode()
        else:
            return self.fixImgMode()

    def optimizeAndSaveImg(self):
        return self.resizeImg().save(self.path_to_img, quality=self.IMG_QUALITY, optimize=True)
