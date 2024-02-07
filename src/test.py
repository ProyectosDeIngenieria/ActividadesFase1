import re 

def open_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

text = open_file('./html/002.html')
regx = '<(\S?\d+)[^>]>(.?)|<.*?\>'

print(re.sub(regx, '', text))