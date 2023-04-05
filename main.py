import click
from tools.build.build_file import build_file
from tools.modify.modify_file import modify_file
from tools.debug.debug_file import debug_file


@click.group()
def main():
    pass


@main.command()
@click.argument("file")
@click.option("--context-files", multiple=True, type=str, help="Optional list of context file paths.")
def build(file, context_files):
    """Build a new file with optional context files."""
    click.echo(f"Building a new file: {file}")
    if context_files:
        click.echo(f"Using context files: {', '.join(context_files)}")
    build_file(file, context_files)


@main.command()
@click.argument("file")
@click.option("--request", prompt="Requested change", help="The modification that you are requesting.")
def modify(file, request):
    """Modify an existing file."""
    click.echo(f"Modifying file: {file}")
    modify_file(file, request)


@main.command()
@click.argument("file")
@click.option("--error", default=None, prompt=False, help="Optional error message to debug.")
def debug(file, error):
    """Debug an existing file. May include an optional error message"""
    click.echo(f"Debugging file: {file}")
    if error:
        click.echo(f"Error message: {error}")
    debug_file(file, error)


if __name__ == "__main__":
    main()
