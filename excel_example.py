import os, glob
import re
import zipfile
import xml.etree.ElementTree as ET
import shutil
from time import sleep
import openpyxl
import lxml
from bs4 import BeautifulSoup
import io


content = []
# Read the XML file
with open("C:\\Users\\derip\\OneDrive\\Рабочий стол\\Новая папка (4)\\kv_3e204e14-80d8-4fae-88d5-"
          "1daa89fe47b5.xml", encoding='utf-8') as file:
    bs_content = BeautifulSoup(file.read(), 'lxml')
    print(bs_content.find('innercadastralnumbers').text)
    print(bs_content)
