import os, glob
import re
import zipfile
from time import sleep
import openpyxl
from bs4 import BeautifulSoup
import csv
import dict_catalog as d


list_encum = []


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
    i = 0
    for file in list_path:
        # xml_ET = ET.parse(file).getroot()
        # xml_scrap(xml_ET)
        xml_bs(file)


def xml_bs(xml):
    with open(xml, encoding='utf-8') as file:
        bs_content = BeautifulSoup(file.read(), 'lxml')
        if bs_content.find('realty'):  # для не ЗУ
            dict_result = {
                'Кадастровый номер': bs_content.find('realty').findNext().attrs['cadastralnumber'],
                'Кадастровый номер;': bs_content.find('realty').findNext().attrs['cadastralnumber'] + ';',
                'Номер запроса': bs_content.find('declarattribute').attrs['requerynumber'],
                'Дата присвоения кадастрового номера': bs_content.find('realty').findNext().attrs['datecreated']
            }
            dict_result['Кадастровые номера иных объектов недвижимости, в пределах ' \
                        'которых расположен объект недвижимости'] = \
                chek_Nonetype(bs_content.find('cadastralnumberoks'))
            dict_result['Наименование'] = d.chek_realty_type[chek_Nonetype(bs_content.find('objecttype'))]
            if bs_content.find('param:material'):
                dict_result['Материал'] = d.wall_material[bs_content.find('param:material').attrs['wall']]
            if bs_content.find('assignationbuilding'):
                dict_result['Назначение'] = d.assignation_building[bs_content.find('assignationbuilding').text]
            # if dict_result['адрес'] == '':
            #    if bs_content.find('adrs:level3') and bs_content.find('address'):
            #         dict_result['адрес'] = bs_content.find('address').find('adrs:postalcode').text + ', ' + \
            #                                subject_num[bs_content.find('address').find('adrs:region').text] + ', ' + \
            #                                bs_content.find('adrs:street').attrs['name'] + \
            #                                bs_content.find('adrs:street').attrs['type'] + ' , ' + \
            #                                bs_content.find('adrs:level1').attrs['type'] + ' ' + \
            #                                bs_content.find('adrs:level1').attrs['value'] + ' ' + \
            #                                bs_content.find('adrs:level3').attrs['type'] + ' ' + \
            #                                bs_content.find('adrs:level3').attrs['value']
            #     else:
            #         dict_result['адрес'] = bs_content.find('address').find('adrs:postalcode').text + ', ' + \
            #                                subject_num[bs_content.find('address').find('adrs:region').text] + ', ' + \
            #                                bs_content.find('adrs:street').attrs['name'] + \
            #                                bs_content.find('adrs:street').attrs['type'] + ' , ' + \
            #                                bs_content.find('adrs:level1').attrs['type'] + ' ' + \
            #                                bs_content.find('adrs:level1').attrs['value']
            # else:
        if bs_content.find('parcels'):  # для ЗУ
            dict_result = {
                'Кадастровый номер': bs_content.find('parcels').findNext().attrs['cadastralnumber'],
                'Кадастровый номер;': bs_content.find('parcels').findNext().attrs['cadastralnumber'] + ';',
                'Номер запроса': bs_content.find('declarattribute').attrs['requerynumber'],
                'Дата присвоения кадастрового номера': bs_content.find('parcels').findNext().attrs['datecreated']
            }
            dict_result['Кадастровые номера расположенных в пределах земельного участка объектов недвижимости'] = \
                chek_Nonetype(bs_content.find('innercadastralnumbers'))
            dict_result['Наименование'] = 'Земельный участок'
            dict_result['specialnote'] = chek_Nonetype(bs_content.find('specialnote'))
            dict_result['Категория ЗУ'] = d.category_parcels_type[chek_Nonetype(bs_content.find('category'))]
            try:
                dict_result['Вид разрешенного использования'] = \
                    d.utilization_code[bs_content.find('Utilization').attrs['Utilization']]
            except:
                pass
            try:
                dict_result['Вид разрешенного использования'] = \
                    d.utilization_code[bs_content.find('utilization').attrs['utilization']]
            except:
                pass
        dict_result['адрес'] = chek_Nonetype(bs_content.find('adrs:note'))
        if bs_content.find('area'):
            dict_result['Площадь, кв.м.'] = bs_content.find('area').nextSibling.strip('\n')
        else:
            dict_result['Площадь, кв.м.'] = ''
        if bs_content.find('cadastralcost'):
            dict_result['Кадастровая стоимость'] = bs_content.find('cadastralcost').attrs['value'] + ' рублей'
        else:
            dict_result['Кадастровая стоимость'] = ''
        for elem in bs_content.find_all('encumbrance'):
            encum_str = ''
            # print(d.encum_type[elem.find('type').text], end=' ')
            encum_str = d.encum_type[elem.find('type').text]
            if elem.find('term'):
                # print(elem.find('term').text, end=' ')
                encum_str = encum_str + ' ' + elem.find('term').text
            if elem.find('stopped'):
                # print(elem.find('stopped').text, end=' ')
                encum_str = encum_str + ' ' + elem.find('stopped').text
            if elem.find('owner'):
                if elem.find('person'):
                    # print('в пользу', elem.find('person').find('content').text)
                    encum_str = encum_str + ' в пользу ' + elem.find('person').find('content').text
                elif elem.find('organization'):
                    # print('в пользу', elem.find('organization').find('content').text)
                    encum_str = encum_str + ' в пользу ' + elem.find('organization').find('content').text
            list_encum.append(encum_str)
        dict_result['Обременения'] = list_encum
        if bs_content.find('right'):
            if bs_content.find('right').find('governance'):
                dict_result['Правообладатель'] = chek_Nonetype(bs_content.find('right').find('governance').find('name'))
            try:
                # print(d.owner_type[bs_content.find('right').find('type').text])
                dict_result['Объем прав'] = d.owner_type[bs_content.find('right').find('type').text]
            except:
                pass
        else:
            dict_result['Объем прав'] = ''

        # print(dict_result)
        # print(bs_content)
        list_encum.clear()
        to_excel(dict_result)
        print(dict_result)
        print('-' * 80)
        # print(bs_content)


def chek_Nonetype(bs):
    if bs is None:
        return ''
    else:
        return bs.text


def to_excel(dictionary):
    with open('ЕГРН.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=list(dictionary.keys()))
        writer.writeheader()
        writer.writerow(dictionary)


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
# print(list_result)
if glob.glob("obj*.xml"):
    print('файл типа obj: ')
    for name_file in glob.glob("obj*.xml"):
        print(name_file)

# shutil.rmtree(new_path, True)
# print(list_result)
# print(dict_result)
