"""
    This class using for namig upload files e.g.: lowercase filename and it's extention,
    and to determinate file upload paths
"""

import os, uuid
from django.utils.text import slugify
from transliterate import translit


class FileProcessing:
    def __init__(self, filename):
        self.filename = filename

    def lowercaseFilename(self) -> str:
        return self.filename.lower()

    def getFileName(self) -> str:
        name, ext = os.path.splitext(self.lowercaseFilename())
        return name

    def getFileExt(self) -> str:
        name, ext = os.path.splitext(self.lowercaseFilename())
        return ext

    def translitFileName(self) -> str:
        return translit(self.getFileName(), 'ru', reversed=True)

    def slugifyFileName(self) -> str:
        return slugify(self.getFileName())

    def translitAndSlugify(self) -> str:
        return slugify(self.translitFileName())

    def genarateFileName(self) -> str:
        return uuid.uuid4()

    def newFileNameTranslitSlugify(self) -> str:
        return "{0}{1}".format(self.translitAndSlugify(), self.getFileExt())

    def newFileNameGenerated(self) -> str:
        return "{0}{1}".format(self.genarateFileName(), self.getFileExt())

    def newFileNameGenplan(self) -> str:
        return "{0}{1}".format('genplan', self.getFileExt())

    def newFileNameFromField(self, fieldname, prefix: str = None, postfix: str = None) -> str:
        fieldname = slugify(translit(fieldname, 'ru', reversed=True))
        if prefix and postfix:
            return "{prefix}_{fieldname}_{postfix}{extention}".format(fieldname=fieldname, extention=self.getFileExt(), prefix=prefix, postfix=postfix)
        elif prefix:
            return "{prefix}_{fieldname}{extention}".format(fieldname=fieldname, extention=self.getFileExt(), prefix=prefix)
        elif postfix:
            return "{fieldname}_{postfix}{extention}".format(fieldname=fieldname, extention=self.getFileExt(), postfix=postfix)
        else:
            return "{fieldname}{extention}".format(fieldname=fieldname, extention=self.getFileExt())
