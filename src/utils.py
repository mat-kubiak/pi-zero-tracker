import os, json

def read_file(path):
    with open(path, 'r') as file:
        text = ''.join(file.readlines())
    return text

def write_file(path, text):
    with open(path, 'w') as file:
        file.writelines(text)

def read_json_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data