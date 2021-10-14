import os
import zipfile
import hashlib
import requests
import re
import os
import csv

# Задание №1
# Создать новую директорию, в которую будет распакован архив
# С помощью модуля zipfile извлечь содержимое архива в созданную директорию
directory_to_extract_to = 'C:\\new_dir'  # Директория извлечения файлов архива
# os.mkdir(directory_to_extract_to)
arch_file = 'C:\\Users\\milkw\\Downloads\\tiff-4.2.0_lab1.zip'  # путь к архиву
with zipfile.ZipFile(arch_file) as zf:
    zf.extractall(directory_to_extract_to)
zf.close()

# Задание №2.1
# Получить список файлов формата txt, находящихся в directory_to_extract_to и сохранить его в txt_files
txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        if '.txt' in i:
            txt_files.append(os.path.join(r, i))
print("Список файлов txt: ")
for i in txt_files:
    print(i)

# Задание №2.2
res = " "
for file in txt_files:
    target_file = open(file, 'rb').read()
    res = hashlib.md5(target_file).hexdigest()
    print("Значение хэша:")
    print(res)

# Задание №3
# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to
# Отобразить полный путь к искомому файлу и его содержимое на экране
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файла
for r, d, f in os.walk(directory_to_extract_to):
    for i in f:
        file = open(os.path.join(r, i), "rb").read()
        file_data = hashlib.md5(file).hexdigest()
        if target_hash == file_data:
            target_file = r
            target_file_data = file
print("Путь: ")
print(target_file)
print("Содержимое: ")
print(target_file_data)

# Задание №4
r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
headers = ''
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
# извлечение заголовков таблицы
for line in lines:
    if counter == 0:
        headers = re.sub(r'[^>]*', " ", line)
        # Удаление тегов
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
        # Извлечение списка заголовков
    tmp = re.sub(r'[^>]*', ";", line)
    tmp = re.sub(r'\xa0', '', tmp)
    tmp = re.sub(r'[*]', '', tmp)
    tmp = re.sub(r'^\W+', '', tmp)
    tmp = re.sub(r'\(.*?\)', '', tmp)
    tmp = re.sub('_', '-1', tmp)
    tmp = re.sub(';+', ';', tmp)
    tmp = re.sub(';', "|", tmp)
    tmp = re.sub(r'\|+$', '', tmp)
    tmp_split = re.split(r'\|', tmp)
    if tmp_split != headers:
        country_name = tmp_split[0]
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)
    counter += 1

# Задание №5
# Запись данных из полученного словаря в файл
output = open('data.csv', 'w')
file_w = csv.writer(output, delimiter="|")
file_w.writerow(headers)
for key, val in result_dct.items():
    file_w.writerow([key, val[0], val[1], val[2], val[3]])
output.close()

# Задание №6
# Вывод данных на экран для указанного первичного ключа
target_country = input("Введите название страны: ")
print(result_dct[target_country])