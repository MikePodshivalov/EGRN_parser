import os, glob
import re
import zipfile
import xml.etree.ElementTree as ET
import shutil
from time import sleep
import openpyxl
from bs4 import BeautifulSoup

list_result = []
dict_result = {}


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
    return glob.glob("kv*.xml")


def xml_read(list_path):
    '''получаем список xml файлов и возвращаем элемент ET'''
    for file in list_path:
        xml_ET = ET.parse(file).getroot()
        xml_scrap(xml_ET)
        xml_bs(file)


def xml_bs(xml):
    with open(xml, encoding='utf-8') as file:
        bs_content = BeautifulSoup(file.read(), 'lxml')
        if bs_content.find('realty'):   # для не ЗУ
            print(bs_content.find('realty').findNext().attrs['cadastralnumber'])
            print(bs_content.find('realty').findNext().attrs['datecreated'])
            if bs_content.find('cadastralnumberoks'):
                print(bs_content.find('cadastralnumberoks').text)
            if bs_content.find('adrs:note'):
                print(bs_content.find('adrs:note').text)
            print(bs_content.find('cadastralcost').attrs['value'], 'рублей')
            print('-' * 50)
        if bs_content.find('parcels'):  # для ЗУ
            print(bs_content.find('parcels').findNext().attrs['cadastralnumber'])
            print(bs_content.find('parcels').findNext().attrs['datecreated'])
            if bs_content.find('innercadastralnumbers'):
                print(bs_content.find('innercadastralnumbers').text)
            if bs_content.find('adrs:note'):
                print(bs_content.find('adrs:note').text)
            print(bs_content.find('cadastralcost').attrs['value'], 'рублей')
            print('-' * 50)
        if bs_content.find('innercadastralnumbers') is not None:
            list_result.append(bs_content.find('innercadastralnumbers').text)
            list_result.append(bs_content.find('innercadastralnumbers').text)
        # print(bs_content.find('innercadastralnumbers').text)
        # print(bs_content.find('CadastralNumberOKS').text)
        # print(bs_content.find('Area').text)
        # print(bs_content.find('Note').text)
        # print(bs_content.find('CadastralCost').text + ' рублей')
        # print(bs_content.find('Note').text)


def xml_scrap(xml):
    '''собираем всю информацию (tag, attrib, text всех элементов) в 3 списка, далее...'''
    mylist1 = [item.tag for item in xml.iter()]
    mylist2 = [item.attrib for item in xml.iter()]
    mylist3 = [item.text for item in xml.iter()]
    new_list = list(zip(mylist1, mylist2, mylist3))
    list_parser(new_list)


# [2][1]['CadastralNumber']
# [2][1]['DateCreated']
def list_parser(nl):
    # print(nl)
    # if 'KPOKS' in nl[0][0]:
    wb = openpyxl.Workbook()
    sheet = wb.active
    # col = 'A'  # буква столбца, куда будет писаться информация
    # wb['A1'] = nl[2][1]['CadastralNumber']
    # wb[col + str(i)] = nl[2][1]['DateCreated']
    wb.save('ЕГРН.xlsx')
    list_result.append(nl[2][1]['CadastralNumber'])
    list_result.append(nl[2][1]['DateCreated'])
    dict_result['Кадастровый номер'] = nl[2][1]['CadastralNumber']
    dict_result['Дата присвоения кадастрового номера'] = nl[2][1]['DateCreated']


# def bs_parse():
#     with open("C:\\Users\\derip\\OneDrive\\Рабочий стол\\Новая папка (4)\\kv_3e204e14-80d8-4fae-88d5-"
#               "1daa89fe47b5.xml", encoding='utf-8') as file:
#         bs_content = BeautifulSoup(file.read(), 'lxml')
#         print(bs_content.find('innercadastralnumbers').text)
#         print(bs_content)


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
# print(list_result)
# print(dict_result)
