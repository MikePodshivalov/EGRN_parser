import os, glob
import re
import zipfile
import xml.etree.ElementTree as ET
import shutil
from time import sleep
import openpyxl


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
        xml_scrap(xml_ET)
        sleep(1)


def xml_scrap(xml):
    '''собираем всю информацию (tag, attrib, text всех элементов) в 3 списка, далее...'''
    mylist1 = [item.tag for item in xml.iter()]
    mylist2 = [item.attrib for item in xml.iter()]
    mylist3 = [item.text for item in xml.iter()]



def list_parser(list1, list2, list3):
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
print(xml_read(list_xml_files))
sleep(2)
shutil.rmtree(new_path, True)
