import re


def transliterate(string):
    vocabulary = {
                    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
                    'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': 'ie', 'ы': 'y', 'ь': '', 'э': 'e',
                    'ю': 'iu', 'я': 'ia', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
                    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                    'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh',
                    'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': 'Ie', 'Ы': 'y', 'Ь': '', 'Э': 'E',
                    'Ю': 'Iu', 'Я': 'Ia', '/': '', '\\': '', ' ': '', '#': '', '_': '-', '┃': '', '|': '',
                }

    for key in vocabulary:
        if key in string:
            string = string.replace(key, vocabulary[key])
    return string


def generate_slug(string: str):
    string = re.sub(' +', ' ', string).split(' ')
    slug = ''
    for word in string:
        slug += transliterate(word) + '-'
    slug = slug[:-1].lower().replace('--', '-')
    return slug
