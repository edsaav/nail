from app.core.chat_utils import predict_code
from app.core.file_utils import read_file, write_file


def build_spec_file(file_path, target_file_path):
    # Read the content of the initial file
    initial_file_content = read_file(file_path)

    # Send the content to the predict_code function with a request to build a unit test file
    prompt = f"Create a unit test file for the following code:\n\n```\n{initial_file_content}\n```"
    test_file_content = predict_code(prompt)

    # Write the contents of the test file to the target file path
    write_file(target_file_path, test_file_content)
