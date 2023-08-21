from django import template

from apps.core.classes.file_utils import FileUtils
from apps.core.classes.file_processing import FileProcessing


register = template.Library()

@register.filter(name='bytes_to_mb')
def bytes_to_mb(value):
    return FileUtils.format_bytes(value)


@register.filter(name='get_folder_size')
def get_folder_size(value):
    return FileUtils.get_folder_size(value)


@register.filter(name='get_file_ext')
def get_file_ext(value):
    file = FileProcessing(value)
    return file.getFileExt()


@register.filter(name='split_thousands')
def split_thousands(value):
    return '{:,}'.format(float(value)).replace(',', ' ').replace('.0', '')


@register.filter(name='round_million')
def round_million(value):
    if value:
        value = round(value / 1000000, 1)
        return '{}'.format(value).replace('.0', '')


@register.filter(name='remove_trailing_zero')
def remove_trailing_zero(value):
    return '{}'.format(value).rstrip("0")
