from core.file_utils import read_file, write_file
from core.chat_utils import predict_code


def build_file(file_path, context_file_paths=None):
    # Read the main file
    prompt = read_file(file_path)

    # If context_file_paths is provided, read their contents and add them to the beginning of the prompt
    context_prefix = ""
    if context_file_paths:
        context_prefix += "Existing files for context:\n\n"
        for context_file_path in context_file_paths:
            context_content = read_file(context_file_path)
            context_prefix += f"[[{context_file_path}]]\n```\n{context_content}\n```\n\n"
        context_prefix += "Given the above context, draft a new file using the following request:\n\n"

    # Predict code based on the prompt
    draft_contents = predict_code(f"{context_prefix}{prompt}")

    # Write the predicted code back to the file
    write_file(file_path, draft_contents)
