# Trot

Trot is a command-line tool that leverages OpenAI's chat API to help you build, modify, debug, and generate unit tests for your code. It can also generate a README file for your project based on the existing files in your project directory.

## Installation

To install Trot, you can use pip:

```
pip install -e .
```

This will install the required dependencies and make the `trot` command available in your terminal.

## Configuration

Before using Trot, you need to configure it with your OpenAI API key. You can do this by running:

```
trot configure
```

This will prompt you to enter your API key, which will be saved for future use.

## Usage

Trot provides several commands to help you with your code:

### Build

To build a new file with optional context files, use the `build` command:

```
trot build <file> [--context-files <file1> <file2> ...] [--model <model>]
```

The target file should contain a description of the file that you are trying to build. The more specific the specification, the more accurate the result. As an example:

```
A python script with a function that does the following:
- accepts a URL string as a parameter
- raises an error if the URL is invalid
- scrapes the specified page for heading tags
- returns an array of resulting headings
```

If the file does not exist, skink will open your default editor to fill in the prompt in-line.

The `--context-files` (or `-c`) option can be used to pass in one or more additional files that could provide useful reference. For example, you can pass in files containing modules that should be imported and used by the new file that is being built.

### Modify

To modify an existing file, use the `modify` command:

```
trot modify <file> [--request <request>] [--context-files <file1> <file2> ...] [--model <model>]
```

The request should be in the form of a command, such as "Add a new function that..." or "Refactor the existing class to...".

### Debug

To debug an existing file, use the `debug` command:

```
trot debug <file> [--error <error_message>] [--model <model>]
```

If an error message is not passed, this command will simply look for any possible issues in the given file.

### Generate Unit Tests

To generate a unit test file for an existing file, use the `spec` command:

```
trot spec <file> <target_path> [--model <model>]
```

Once they have been generated, test files can be further adjusted with the `modify` command.

### Generate README

To generate a README file for your project, use the `readme` command:

```
trot readme [--model <model>]
```

This command will gather all application files into context automatically. It will exclude a number of files irrelevant to a README, such as tests and licences. Please note, this currently only works for relatively small projects given the limited context window available for GPT.

## Models

Trot currently supports the following models:

- gpt-3.5-turbo (default)
- gpt-4

You can specify the model to use with the `--model` option for each command.

## Tests

Run the test suite using `pytest`.

## License

This project is licensed under the MIT License.
