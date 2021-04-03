import zipfile
import os
import re


def input_path_zip():
    path_zip_files = input('Введите путь, по которому находятся выписки ЕГРН: ')
    if re.match(r'^[A-Z]:\\', path_zip_files) is not None:

        print('Правильный адрес')

    # try:
    #     list_files = os.listdir(path_zip_files)
    # except FileNotFoundError:
    #     print('Вы ввели неверный путь, попробуйте еще раз')
    #     input_path_zip()


input_path_zip()
