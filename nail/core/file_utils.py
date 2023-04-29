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


def apply_changes(file_path, content):
    """
    Takes a file and content string as inputs. It generates a diff comparing
    the string to the contents of the file. It then displays the diff and asks
    the user to confirm the changes. If they confirm, it writes the content
    to the file.
    """
    diff = _calculate_diff(file_path, content)
    confirmed = _get_confirmation(diff)
    if confirmed:
        write_file(file_path, content)
        print(f"Changes applied to {file_path}")
        return True
    print("Discarding changes.")
    return False


def _get_confirmation(diff):
    _print_diff(diff)
    confirm = input(CONFIRMATION_REQUEST)
    if confirm.lower() == 'y':
        return True
    return False


def _calculate_diff(file_path, content):
    if os.path.exists(file_path):
        file_content = read_file(file_path)
    else:
        file_content = ''
    return difflib.unified_diff(
        file_content.splitlines(), content.splitlines(), lineterm='')


def _print_diff(diff):
    for line in diff:
        _print_colored_line(line)


def _print_colored_line(line):
    if line.startswith('+'):
        print(colored(line, 'green'))
    elif line.startswith('-'):
        print(colored(line, 'red'))
    else:
        print(line)
