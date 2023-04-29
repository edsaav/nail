import os
import subprocess
import difflib
from termcolor import colored


class FileEditor:
    CONFIRMATION_REQUEST = "Do you want to apply the changes? (y/n): "
    DEFAULT_EDITOR = 'vim'

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        """
        Reads the file and returns the content as a string.
        """
        with open(self.file_path, "r") as file:
            content = file.read()
        return content

    def write(self, content):
        """
        Takes a content string as input. Writes the content to the file.

        :param content: The content to be written to the file
        """
        with open(self.file_path, "w") as file:
            file.write(content)

    def open_editor(self):
        """
        Opens the file in the default editor
        """
        editor = os.environ.get('EDITOR', self.DEFAULT_EDITOR)
        subprocess.call([editor, self.file_path])

    def apply_changes(self, content):
        """
        Takes a file and content string as inputs. It generates a diff
        comparing the string to the contents of the file. It then displays
        the diff and asks the user to confirm the changes. If they confirm,
        it writes the content to the file.

        :param content: The content to be written to the file
        """
        diff = self._calculate_diff(content)
        confirmed = self._get_confirmation(diff)
        if confirmed:
            self.write_file(content)
            print(f"Changes applied to {self.file_path}")
            return True
        print("Discarding changes.")
        return False

    def _get_confirmation(self, diff):
        self._print_diff(diff)
        confirm = input(self.CONFIRMATION_REQUEST)
        if confirm.lower() == 'y':
            return True
        return False

    def _calculate_diff(self, content):
        if os.path.exists(self.file_path):
            file_content = self.read_file()
        else:
            file_content = ''
        return difflib.unified_diff(
            file_content.splitlines(), content.splitlines(), lineterm='')

    def _print_diff(self, diff):
        for line in diff:
            self._print_colored_line(line)

    def _print_colored_line(self, line):
        if line.startswith('+'):
            print(colored(line, 'green'))
        elif line.startswith('-'):
            print(colored(line, 'red'))
        else:
            print(line)
