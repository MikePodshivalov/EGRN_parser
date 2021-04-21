import os, glob
import re
import zipfile
import xml.etree.ElementTree as ET
import shutil
from time import sleep
import openpyxl
from bs4 import BeautifulSoup
import csv

list_encum = []
chek_realty_type = {
    '002001002000': 'Здание',
    '002001003000': 'Помещение',
    '002001004000': 'Сооружение',
    '002001005000': 'Объект незавершённого строительства',
    '002001006000': 'Предприятие как имущественный комплекс',
    '002001008000': 'Единый недвижимый комплекс',
    '002001009000': 'Машино-место',
    '002001010000': 'Иной объект недвижимости'
}
owner_type = {
    '001001000000': 'Собственность (индивидуальная)',
    '001002000000': 'Долевая собственность',
    '001003000000': 'Совместная собственность',
    '001004000000': 'Хозяйственное ведение',
    '001005000000': 'Оперативное управление',
    '001006000000': 'Пожизненное наследуемое владение',
    '001007000000': 'Постоянное (бессрочное) пользование',
    '001009000000': 'Владение, пользование и распоряжение Центральным банком Российской Федерации',
    '001011000000': 'Отказ от права собственности, постоянного (бессрочного) пользования, пожизненного наследуемого '
                    'владения на земельный участок либо об отказе от права собственности на земельную долю',
    '022010000000': 'Доверительное управление (ПИФ)',
    '022006000000': 'Аренда',
    '022097001000': 'Концессия'
}
encum_type = {
    '022001000000': 'Сервитут',
    '022001001000': 'Публичный сервитут',
    '022001002000': 'Частный сервитут',
    '022002000000': 'Арест',
    '022003000000': 'Запрещение регистрации',
    '022004000000': 'Ограничения прав на земельный участок, предусмотренные статьями '
                    '56, 56.1 Земельного кодекса Российской Федерации',
    '022004001000': 'Ограничения прав на земельный участок, предусмотренные статьей '
                    '56 Земельного кодекса Российской Федерации',
    '022004002000': 'Ограничения прав на земельный участок, предусмотренные статьей 56.1 '
                    'Земельного кодекса Российской Федерации',
    '022005000000': 'Решение об изъятии земельного участка, жилого помещения',
    '022006000000': 'Аренда',
    '022007000000': 'Ипотека',
    '022008000000': 'Ипотека в силу закона',
    '022009000000': 'Безвозмездное (срочное) пользование земельным/лесным участком',
    '022010000000': 'Доверительное управление',
    '022011000000': 'Рента',
    '022012000000': 'Запрет на совершение действий в сфере ГКУ в отношении ОН',
    '022013000000': 'Наем жилого помещения',
    '022014000000': 'Безвозмездное пользование (ссуда)',
    '022015000000': 'Объект культурного наследия',
    '022016000000': 'Концессия',
    '022017000000': 'Ограничение оборотоспособности земельных участков, '
                    'предусмотренное статьей 11 Федерального закона 119-ФЗ',
    '022018000000': 'Залог в качестве меры пресечения',
    '022099000000': 'Прочие ограничения прав и обременения объекта недвижимости'
}

subject_num = {'01': 'Республика Адыгея (Адыгея)', '02': 'Республика Башкортостан', '03': 'Республика Бурятия',
               '04': 'Республика Алтай', '05': 'Республика Дагестан', '06': 'Республика Ингушетия',
               '07': 'Кабардино-Балкарская Республика', '08': 'Республика Калмыкия',
               '09': 'Карачаево-Черкесская Республика',
               '10': 'Республика Карелия', '11': 'Республика Коми', '12': 'Республика Марий Эл',
               '13': 'Республика Мордовия',
               '14': 'Республика Саха (Якутия)', '15': 'Республика Северная Осетия Алания',
               '16': 'Республика Татарстан (Татарстан)',
               '17': 'Республика Тыва', '18': 'Удмуртская Республика', '19': 'Республика Хакасия',
               '20': 'Чеченская Республика',
               '21': 'Чувашская Республика Чувашия', '22': 'Алтайский край', '23': 'Краснодарский край',
               '24': 'Красноярский край',
               '25': 'Приморский край', '26': 'Ставропольский край', '27': 'Хабаровский край', '28': 'Амурская область',
               '29': 'Архангельская область', '30': 'Астраханская область', '31': 'Белгородская область',
               '32': 'Брянская область',
               '33': 'Владимирская область', '34': 'Волгоградская область', '35': 'Вологодская область',
               '36': 'Воронежская область',
               '37': 'Ивановская область', '38': 'Иркутская область', '39': 'Калининградская область',
               '40': 'Калужская область',
               '41': 'Камчатский край', '42': 'Кемеровская область', '43': 'Кировская область',
               '44': 'Костромская область',
               '45': 'Курганская область', '46': 'Курская область', '47': 'Ленинградская область',
               '48': 'Липецкая область',
               '49': 'Магаданская область', '50': 'Московская область', '51': 'Мурманская область',
               '52': 'Нижегородская область',
               '53': 'Новгородская область', '54': 'Новосибирская область', '55': 'Омская область',
               '56': 'Оренбургская область',
               '57': 'Орловская область', '58': 'Пензенская область', '59': 'Пермский край', '60': 'Псковская область',
               '61': 'Ростовская область', '62': 'Рязанская область', '63': 'Самарская область',
               '64': 'Саратовская область',
               '65': 'Сахалинская область', '66': 'Свердловская область', '67': 'Смоленская область',
               '68': 'Тамбовская область',
               '69': 'Тверская область', '70': 'Томская область', '71': 'Тульская область', '72': 'Тюменская область',
               '73': 'Ульяновская область', '74': 'Челябинская область', '75': 'Забайкальский край',
               '76': 'Ярославская область',
               '77': 'г. Москва', '78': 'г. Санкт-Петербург', '79': 'Еврейская автономная область',
               '83': 'Ненецкий автономный округ', '86': 'Ханты-Мансийский автономный округ – Югра',
               '87': 'Чукотский автономный округ', '89': 'Ямало-Ненецкий автономный округ', '91': 'Республика Крым',
               '92': 'г. Севастополь', '99': 'Иные территории, включая город и космодром Байконур'
               }


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
            print(bs_content.find('realty').findNext().attrs['cadastralnumber'])
            print(bs_content.find('realty').findNext().attrs['cadastralnumber'], ';', sep='')
            print(bs_content.find('declarattribute').attrs['requerynumber'])
            print(bs_content.find('realty').findNext().attrs['datecreated'])
            if bs_content.find('cadastralnumberoks'):
                print('Кадастровые номера иных объектов недвижимости, '
                      'в пределах которых расположен объект недвижимости', bs_content.find('cadastralnumberoks').text)
                dict_result['Кадастровые номера иных объектов недвижимости, в пределах ' \
                            'которых расположен объект недвижимости'] = bs_content.find('cadastralnumberoks').text
            else:
                dict_result['Кадастровые номера иных объектов недвижимости, в пределах ' \
                            'которых расположен объект недвижимости'] = '-'
            print('')
            print(chek_realty_type[bs_content.find('objecttype').text])
            dict_result['Наименование'] = chek_realty_type[bs_content.find('objecttype').text]
            if bs_content.find('adrs:note'):
                print(bs_content.find('adrs:note').text)
                dict_result['адрес'] = bs_content.find('adrs:note').text
            else:
                print(bs_content.find('address').find('adrs:postalcode').text, end=', ')
                print(bs_content.find('address').find('adrs:region').text, end=', ')
                if bs_content.find('adrs:urbandistrict'):
                    print(bs_content.find('adrs:urbandistrict').attrs['name'],
                          bs_content.find('adrs:urbandistrict').attrs['type'], sep=' ', end=', ')
                print(bs_content.find('adrs:street').attrs['name'],
                      bs_content.find('adrs:street').attrs['type'], sep=' ', end=', ')
                print(bs_content.find('adrs:level1').attrs['type'],
                      bs_content.find('adrs:level1').attrs['value'], sep=' ', end=', ')
                # print(bs_content.find('adrs:level3').attrs['type'],
                #       bs_content.find('adrs:level3').attrs['value'], sep=' ')
                if bs_content.find('adrs:level3'):
                    dict_result['адрес'] = bs_content.find('address').find('adrs:postalcode').text + ', ' + \
                                           subject_num[bs_content.find('address').find('adrs:region').text] + ', ' + \
                                           bs_content.find('adrs:street').attrs['name'] + \
                                           bs_content.find('adrs:street').attrs['type'] + ' , ' + \
                                           bs_content.find('adrs:level1').attrs['type'] + ' ' + \
                                           bs_content.find('adrs:level1').attrs['value'] + ' ' + \
                                           bs_content.find('adrs:level3').attrs['type'] + ' ' + \
                                           bs_content.find('adrs:level3').attrs['value']
                else:
                    dict_result['адрес'] = bs_content.find('address').find('adrs:postalcode').text + ', ' + \
                                           subject_num[bs_content.find('address').find('adrs:region').text] + ', ' + \
                                           bs_content.find('adrs:street').attrs['name'] + \
                                           bs_content.find('adrs:street').attrs['type'] + ' , ' + \
                                           bs_content.find('adrs:level1').attrs['type'] + ' ' + \
                                           bs_content.find('adrs:level1').attrs['value']
            print(bs_content.find('area').nextSibling)
            dict_result['Площадь, кв.м.'] = bs_content.find('area').nextSibling.strip('\n')
            print(bs_content.find('cadastralcost').attrs['value'], 'рублей')
            dict_result['Кадастровая стоимость'] = bs_content.find('cadastralcost').attrs['value']
        if bs_content.find('parcels'):  # для ЗУ
            dict_result = {
                'Кадастровый номер': bs_content.find('parcels').findNext().attrs['cadastralnumber'],
                'Кадастровый номер;': bs_content.find('parcels').findNext().attrs['cadastralnumber'] + ';',
                'Номер запроса': bs_content.find('declarattribute').attrs['requerynumber'],
                'Дата присвоения кадастрового номера': bs_content.find('parcels').findNext().attrs['datecreated']
            }
            print(bs_content.find('parcels').findNext().attrs['cadastralnumber'])
            print(bs_content.find('parcels').findNext().attrs['cadastralnumber'], ';', sep='')
            print(bs_content.find('declarattribute').attrs['requerynumber'])
            print(bs_content.find('parcels').findNext().attrs['datecreated'])
            print('')
            if bs_content.find('innercadastralnumbers'):
                print('Кадастровые номера расположенных в пределах земельного '
                      'участка объектов недвижимости', bs_content.find('innercadastralnumbers').text.strip('\n'))
                dict_result['Кадастровые номера расположенных в пределах земельного участка объектов недвижимости'] = \
                    bs_content.find('innercadastralnumbers').text
            else:
                dict_result['Кадастровые номера расположенных в пределах земельного участка объектов недвижимости'] = \
                    '-'
            print('Земельный участок')
            dict_result['Наименование'] = 'Земельный участок'
            print(bs_content.find('area').findNext().nextSibling)
            dict_result['Площадь, кв.м.'] = bs_content.find('area').findNext().nextSibling.strip('\n')
            print('specialnote')
            if bs_content.find('specialnote'):
                print(bs_content.find('specialnote').text)
                dict_result['specialnote'] = bs_content.find('specialnote').text
            if bs_content.find('adrs:note'):
                print(bs_content.find('adrs:note').text)
                dict_result['адрес'] = bs_content.find('adrs:note').text
            print(bs_content.find('cadastralcost').attrs['value'], 'рублей')
            dict_result['Кадастровая стоимость'] = bs_content.find('cadastralcost').attrs['value']
        for elem in bs_content.find_all('encumbrance'):
            encum_str = ''
            print(encum_type[elem.find('type').text], end=' ')
            encum_str = encum_type[elem.find('type').text]
            if elem.find('term'):
                print(elem.find('term').text, end=' ')
                encum_str = encum_str + ' ' + elem.find('term').text
            if elem.find('stopped'):
                print(elem.find('stopped').text, end=' ')
                encum_str = encum_str + ' ' + elem.find('stopped').text
            if elem.find('owner'):
                if elem.find('person'):
                    print('в пользу', elem.find('person').find('content').text)
                    encum_str = encum_str + ' в пользу ' + elem.find('person').find('content').text
                elif elem.find('organization'):
                    print('в пользу', elem.find('organization').find('content').text)
                    encum_str = encum_str + ' в пользу ' + elem.find('organization').find('content').text
            list_encum.append(encum_str)
            print('-' * 30)
        dict_result['Обременения'] = list_encum
        list_encum.clear()
        if bs_content.find('right'):
            try:
                dict_result['Объем прав'] = owner_type[bs_content.find('right').find('type').text]
            except KeyError:
                pass
        else:
            dict_result['Объем прав'] = '-'
        to_excel(dict_result)
        # print(dict_result)
        print('-' * 50)
        # print(bs_content)


def to_excel(dictionary):
    with open('ЕГРН.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=list(dictionary.keys()))
        writer.writeheader()
        writer.writerow(dictionary)





# def writer_to_excel(text):
#     wb = openpyxl.Workbook()
#     # sheet = wb.active
#     # # col = 'A'  # буква столбца, куда будет писаться информация
# # wb['A1'] = nl[2][1]['CadastralNumber']
# # wb[col + str(i)] = nl[2][1]['DateCreated']
# wb.save('ЕГРН.xlsx')


# def xml_scrap(xml):
#     '''собираем всю информацию (tag, attrib, text всех элементов) в 3 списка, далее...'''
#     mylist1 = [item.tag for item in xml.iter()]
#     mylist2 = [item.attrib for item in xml.iter()]
#     mylist3 = [item.text for item in xml.iter()]
#     new_list = list(zip(mylist1, mylist2, mylist3))
#     list_parser(new_list)


# [2][1]['CadastralNumber']
# [2][1]['DateCreated']
# def list_parser(nl):
# # print(nl)
# # if 'KPOKS' in nl[0][0]:
# wb = openpyxl.Workbook()
# sheet = wb.active
# # col = 'A'  # буква столбца, куда будет писаться информация
# # wb['A1'] = nl[2][1]['CadastralNumber']
# # wb[col + str(i)] = nl[2][1]['DateCreated']
# wb.save('ЕГРН.xlsx')
# list_result.append(nl[2][1]['CadastralNumber'])
# list_result.append(nl[2][1]['DateCreated'])
# dict_result['Кадастровый номер'] = nl[2][1]['CadastralNumber']
# dict_result['Дата присвоения кадастрового номера'] = nl[2][1]['DateCreated']


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
xml_read(list_xml_files)
# print(list_result)
if glob.glob("obj*.xml"):
    print('файл типа obj: ')
    for name_file in glob.glob("obj*.xml"):
        print(name_file)

# shutil.rmtree(new_path, True)
# print(list_result)
# print(dict_result)
