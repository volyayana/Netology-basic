from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

columns_name = contacts_list[0]
contacts_list.remove(columns_name)
new_contacts_list = []

for row in contacts_list:
    new_row = re.findall('[А-Я]?[а-я]+', row[0] + row[1] + row[2])  # находим ФИО как прописнаяБуква_строчныеБуквы
    if len(new_row) == 2:  # если нет отчества, добавим пустой элемент
        new_row.append('')
    # проверяем, дублируются ли записи
    existing_row = None
    for i in new_contacts_list:
        if new_row[0] == i[0] and new_row[1] == i[1] and (new_row[2] == '' or i[2] == '' or new_row[2] == i[2]):
            existing_row = i 

    if existing_row is not None:  # если уже есть люди с такими ФИО, то остальные данные берем сновой строки
        if row[3] != '':
            existing_row[3] = row[3]   # место работы
        if row[4] != '':
            existing_row[4] = row[4]  # должность
        if row[5] != '':
            phone = re.findall('\d', row[5])
            existing_row[5] = (f'+7({"".join(phone[1:4])}){"".join(phone[4:7])}-{"".join(phone[7:9])}-{"".join(phone[9:11])}')
        if row[6] != '':
            existing_row[6] = row[6]  # email
    else:  # новая запись
        new_row.append(row[3])  # место работы
        new_row.append(row[4])  # должность
        
        if row[5] != '':  # телефон
            phone = re.findall('\d', row[5])
            new_row.append(f'+7({"".join(phone[1:4])}){"".join(phone[4:7])}-{"".join(phone[7:9])}-{"".join(phone[9:11])}')
        else:
            new_row.append('')
        new_row.append(row[6])  # email
        new_contacts_list.append(new_row)

# код для записи файла в формате CSV
with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows([columns_name] + new_contacts_list)