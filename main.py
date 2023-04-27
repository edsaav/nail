import click
from app.tools.build.build_file import build_file
from app.tools.build.build_readme import build_readme
from app.tools.modify.modify_file import modify_file
from app.tools.debug.debug_file import debug_file
from app.tools.spec.build_spec_file import build_spec_file
from app.core.config_utils import save_api_key

MODEL_HELP = "Optionally specify an LLM model. " \
    + "Currently defaults to gpt-3.5-turbo and supports gpt-4."


@click.group()
def main():
    pass


@main.command()
@click.option("--api_key", prompt=True, hide_input=True,
              help="Your OpenAI API key.")
def configure(api_key):
    save_api_key(api_key)
    click.echo("API key saved successfully.")


@main.command()
@click.argument("file")
@click.option("--context-files", "-c", multiple=True, type=str,
              help="Optional list of context file paths.")
@click.option("--model", "-m", type=str, help=MODEL_HELP)
def build(file, context_files, model):
    """Build a new file with optional context files."""
    click.echo(f"Building a new file: {file}")
    if context_files:
        click.echo(f"Using context files: {', '.join(context_files)}")
    build_file(file, context_files, model)


@main.command()
@click.option("--model", "-m", type=str, help=MODEL_HELP)
def readme(model):
    """Build a new README file based on the currect directory."""
    click.echo("Generating README file.")
    build_readme("README.md", model)


@main.command()
@click.argument("file")
@click.option("--request", "-r", prompt="Requested change",
              help="The modification that you are requesting.")
@click.option("--context-files", "-c", multiple=True, type=str,
              help="Optional list of context file paths.")
@click.option("--model", "-m", type=str, help=MODEL_HELP)
def modify(file, request, context_files, model):
    """Modify an existing file."""
    click.echo(f"Modifying file: {file}")
    if context_files:
        click.echo(f"Using context files: {', '.join(context_files)}")
    modify_file(file, request, context_files, model)


@main.command()
@click.argument("file")
@click.option("--error", "-e", default=None, prompt=False,
              help="Optional error message to debug.")
@click.option("--model", "-m", type=str, help=MODEL_HELP)
def debug(file, error, model):
    """Debug an existing file. May include an optional error message"""
    click.echo(f"Debugging file: {file}")
    if error:
        click.echo(f"Error message: {error}")
    debug_file(file, error, model)


@main.command()
@click.argument("file")
@click.argument("target_path")
@click.option("--model", "-m", type=str, help=MODEL_HELP)
def spec(file, target_path, model):
    """Build a unit test file for an existing file."""
    click.echo(f"Building spec file for: {file}")
    click.echo(f"Target path: {target_path}")
    build_spec_file(file, target_path, model)


if __name__ == "__main__":
    main()
