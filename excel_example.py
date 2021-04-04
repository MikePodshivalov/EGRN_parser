from openpyxl import Workbook

wb = Workbook()
ws = wb.active
rows = [
           ['Название', 'Язык'],
           ['Ivan', 'PHP'],
           ['Egor', 'Python'],
           ['Anton', 'Ruby'],
           ['Roman', 'Javascript']
       ]

# циклом записываем данные
for row in rows:
    ws.append(row)


wb.save("sample.xlsx")