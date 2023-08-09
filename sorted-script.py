import shutil
from pathlib import Path
import re

images_tuple = ('.jpeg', '.png', '.jpg', '.svg')
video_tuple = ('.avi', '.mp4', '.mov', '.mkv')
dokument_tuple = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
audio_tuple = ('.mp3', '.ogg', '.wav', '.amr')
archive_tuple = ('.zip', '.gz', '.tar')
sorting_folders = ('archives', 'video', 'audio', 'documents', 'images', 'unknown type')

TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
         1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
         1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
         1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
         1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch',
         1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y',
         1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je',
         1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}


def clean_fun(path):  # функция удаления пустых папок - опасная !
    p = Path(path)
    for folder in p.iterdir():
        if folder.name not in sorting_folders:
            if folder.is_dir():
                clean_fun(folder)
                if not any(folder.iterdir()):
                    folder.rmdir()


def normalize(path):
    p = Path(path)
    for file_or_folder in p.iterdir():
        if file_or_folder.name == 'unknown type':
            continue
        if file_or_folder.is_dir():
            new_name = file_or_folder.name
            new_name = new_name.translate(TRANS)
            new_name = re.sub(r'\W', '_', new_name)
            new_path = file_or_folder.parent / new_name
            file_or_folder.rename(new_path)
            normalize(new_path)
        elif file_or_folder.is_file():
            new_name = file_or_folder.name.replace(file_or_folder.suffix, '')
            new_name = new_name.translate(TRANS)
            new_name = re.sub(r'\W', '_', new_name)
            new_name += file_or_folder.suffix
            new_path = file_or_folder.parent / new_name
            file_or_folder.rename(new_path)


def create_folders(path, folder_list=sorting_folders):  # Функция создает папки для сортировки
    for folder in folder_list:
        folder_path = Path(path) / folder
        folder_path.mkdir(exist_ok=True)


def dearchives_func(file_name, path):  # Функция разархивирущая архивы в папки
    path_to_unpack = f'{path}/archives/'
    folder_path = Path(path_to_unpack) / Path(file_name).name.replace(Path(file_name).suffix, '')
    folder_path.mkdir(exist_ok=True)
    if file_name.suffix == '.zip':
        shutil.unpack_archive(file_name, folder_path, format='zip')
    elif file_name.suffix == '.tar':
        shutil.unpack_archive(file_name, folder_path, format='tar')
    elif file_name.suffix == '.gz':
        shutil.unpack_archive(file_name, folder_path, format='gz')


def sorted_func(file_name):  # Функция сортирующая файлы по папкам
    if file_name.suffix in dokument_tuple:  # Является ли файл документом
        target_folder = f'{my_path}/documents/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Ошибка при перемещении файла, скорее всего файл {file_name.name} - открыт !!!')
    elif file_name.suffix in images_tuple:  # Является ли файл изоброжением
        target_folder = f'{my_path}/images/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Ошибка при перемещении файла, скорее всего файл {file_name.name} - открыт !!!')
    elif file_name.suffix in video_tuple:  # Является ли файл видео-файлом
        target_folder = f'{my_path}/video/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Ошибка при перемещении файла, скорее всего файл {file_name.name} - открыт !!!')
    elif file_name.suffix in audio_tuple:  # Является ли файл аудио-файлом
        target_folder = f'{my_path}/audio/'
        try:
            shutil.move(str(file_name), target_folder)
        except PermissionError:
            print(f'Ошибка при перемещении файла, скорее всего файл {file_name.name} - открыт !!!')
    elif file_name.suffix in archive_tuple:
        dearchives_func(file_name, my_path)
    else:
        target_folder = f'{my_path}/unknown type/'
        shutil.move(str(file_name), target_folder)


def parser_func(path):
    p = Path(path)

    for items in p.iterdir():
        if items.name in sorting_folders:
            continue
        if items.is_dir():
            parser_func(items)
        elif items.is_file():
            sorted_func(items)
        print(items.name)


def main():  # Осноаная функция
    create_folders(my_path)
    parser_func(my_path)
    normalize(my_path)
    clean_fun(my_path)


my_path = 'C:/Users/siren/OneDrive/Рабочий стол/Разобрать'
parser_func(my_path)

if __name__ == '__main__':
    main()
