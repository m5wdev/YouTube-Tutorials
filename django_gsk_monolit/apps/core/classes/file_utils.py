"""
    Some useful utilities to work with files
"""

import os


class FileUtils:

    """ [ Convert bytes to readable formats ] """
    @staticmethod
    def format_bytes(bytes_num) -> str:
        sizes = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        dblbyte = bytes_num
        while (i < len(sizes) and bytes_num >= 1024):
            dblbyte = bytes_num / float(1024)
            i = i + 1
            bytes_num = bytes_num / 1024
        return "{0} {1}".format(round(dblbyte, 2), sizes[i])


    """ [ Get folder size in bytes ] """
    @staticmethod
    def get_folder_size(path_to_folder:str):
        total_size = 0
        for root, directories, files in os.walk(path_to_folder):
            for filename in files:
                filepath = os.path.join(root, filename)
                if not os.path.islink(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size
