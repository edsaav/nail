import os
import subprocess

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def open_editor(file_path):
    editor = os.environ.get('EDITOR', 'vim')
    subprocess.call([editor, file_path])
