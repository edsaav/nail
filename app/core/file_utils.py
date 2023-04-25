import os
import subprocess
import difflib
from termcolor import colored

CONFIRMATION_REQUEST = "Do you want to apply the changes? (y/n): "


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


def print_colored_diff_line(line):
    if line.startswith('+'):
        print(colored(line, 'green'))
    elif line.startswith('-'):
        print(colored(line, 'red'))
    else:
        print(line)


def confirm_diff(file_path, content):
    """
    Takes a file and content string as inputs. It generates a diff comparing the string to the contents of the file.
    It then displays the diff and asks the user to confirm the changes. Returns true if they confirm.
    """
    if os.path.exists(file_path):
        file_content = read_file(file_path)
    else:
        file_content = ''
    diff = difflib.unified_diff(
        file_content.splitlines(), content.splitlines(), lineterm='')
    for line in diff:
        print_colored_diff_line(line)
    confirm = input(CONFIRMATION_REQUEST)
    if confirm.lower() == 'y':
        return True
    return False


def apply_changes(file_path, content):
    """
    Takes a file and content string as inputs. It generates a diff comparing the string to the contents of the file.
    It then displays the diff and asks the user to confirm the changes. If they confirm, it writes the content to the file.
    """
    if confirm_diff(file_path, content):
        write_file(file_path, content)
        print(f"Changes applied to {file_path}")
        return True
    print("Discarding changes.")
    return False
