# Text Integrity Inspector

The Text Integrity Inspector package provides a tool for validating the integrity of UTF-8 text files based on language-specific character sets.

## Usage

```python
from textIntegrityInspector.validator import TextIntegrityChar

validator = TextIntegrityChar()
validator.validate_directory(
    root=".",
    extensions=["py"],
    exclude_dirs=[],
    exclude_files=[],
    language="fr",
    additional_chars="",
)
```

This will validate all files in the current directory with the `.py` extension.

## MainFunctions

* `validate_file(file_path, mode='v')`: Validates the characters in a file against the language-specific character set.
* `is_valid_char(byte)`: Determines whether a given byte represents a valid character within the specified language-specific character set.
* `appendListErrors()`: Appends error messages to the `lErrors` list.
* `print_lErrors()`: Prints out the error messages from the `lErrors` list.
* `get_list_valid_chars(language, additional_chars)`: Returns a list of valid characters for the given language.
* `validate_directory(root, extensions, exclude_dirs, exclude_files, language, additional_chars)`: Validates all files in a directory and its subdirectories.

## Examples

**Validate all files in the current directory with the `.py` extension:**

```python
from textIntegrityInspector.validator import TextIntegrityChar

validator = TextIntegrityChar()
validator.validate_directory(
    root=".",
    extensions=["py"],
    exclude_dirs=[],
    exclude_files=[],
    language="en",
    additional_chars="",
)
```

**Validate a file with a specific language:**

```python
from textIntegrityInspector.validator import TextIntegrityChar

validator = TextIntegrityChar()
validator.validate_file(file_path="my_file.fr", language="fr")
```

**Validate a file with additional characters:**

```python
from textIntegrityInspector.validator import TextIntegrityChar

validator = TextIntegrityChar()
validator.validate_file(
    file_path="my_file.py",
    language="en",
    additional_chars="é, ê, ô",
)
```


## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Contributing

Contributions are welcome! Please open a pull request or issue if you have any feedback or suggestions.

## License

The Text Integrity Inspector package is licensed under the MIT License.
