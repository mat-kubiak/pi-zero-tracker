import os, json

def read_file(path):
    try:
        with open(path, 'r') as file:
            text = ''.join(file.readlines())
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
    return text

def write_file(path, text):
    try:
        with open(path, 'w') as file:
            file.writelines(text)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

def read_json_file(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
    return data