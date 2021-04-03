import os, glob
import re
import zipfile
import xml.etree.ElementTree as ET


def input_path_zip():
    '''вводим путь до выписок ЕГРН
    возвращаем список zip архивов и путь к ним'''
    while True:
        path_zip_files = input('Введите путь, по которому находятся выписки ЕГРН: ')
        if re.match(r'^[A-Z]:\\', path_zip_files) is not None:
            try:
                list_files = os.listdir(path_zip_files)
                return list_files, path_zip_files
            except FileNotFoundError:
                print('Введенный путь отсутствует, попробуйте ввести другой')
        else:
            print('Введен неверный путь, попробуйте еще раз')


def zipfile_extractall_first(list_file, path):
    '''разархивируем первый раз в папку \test и возвращаем список файлов'''
    for file in list_file:
        try:
            with zipfile.ZipFile(path + '\\' + file, 'r') as z:
                z.extractall(path + '\\test')
        except PermissionError:
            print('Extracting...')
    return os.listdir(path + '\\test')


def zipfile_extractall_second(list_file, path):
    '''разархивируем второй раз в папку \test и возвращаем список xml файлов'''
    for file in list_file:
        if zipfile.is_zipfile(path + file):
            try:
                with zipfile.ZipFile(path + file, 'r') as z:
                    z.extractall(path)
            except FileNotFoundError:
                print('Extracting...')
    os.chdir(path)
    return glob.glob("*.xml")


def xml_read(list_path):
    '''получаем список xml файлов и возвращаем элемент ET'''
    for file in list_path:
        xml_ET = ET.parse(file).getroot()
        xml_parse(xml_ET)


def xml_parse(xml):
    pass


list_zip_files, path_zip = input_path_zip()
# создаем папку \test:
try:
    os.mkdir(path_zip + '\\test')
except FileExistsError:
    print('папка \\test уже создана')

list_test = zipfile_extractall_first(list_zip_files, path_zip)
new_path = path_zip + '\\test\\'

list_xml_files = zipfile_extractall_second(list_test, new_path)
xml_read(list_xml_files)
