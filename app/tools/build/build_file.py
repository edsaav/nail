from app.core.file_utils import read_file, write_file
from app.core.chat_utils import predict_code
from app.core.context_utils import build_context_prefix


def build_file(file_path, context_file_paths=None, model=None):
    prompt = read_file(file_path)
    context_prefix = build_context_prefix(context_file_paths)
    draft_contents = predict_code(f"{context_prefix}{prompt}", model=model)
    write_file(file_path, draft_contents)
