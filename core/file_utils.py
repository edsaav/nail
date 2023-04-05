def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)
