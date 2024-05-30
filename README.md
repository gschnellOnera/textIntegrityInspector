# Text Integrity Inspector
![ci](https://github.com/gschnellOnera/textIntegrityInspector/actions/workflows/build.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/gschnellOnera/textIntegrityInspector/graph/badge.svg?token=IZYUWJ63CQ)](https://codecov.io/gh/gschnellOnera/textIntegrityInspector)

![Text Integrity Inspector](./doc/images/TextIntegrityLogo180.png)  

The Text Integrity Inspector package provides a tool for validating the integrity of UTF-8 text files based on language-specific character sets.

## Tnstallation

```bash
pip install textIntegrityInspector
```

## Usage

### In Commande line

```bash
textIntegrityInspector path_to_inspect_dir --extensions py txt 

# usage 
textIntegrityInspector --help

```

This will validate all files in the current directory with the `.py` or `.txt` extension.

### In python script

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

### Configuration

By default, `textIntegrityInspector` looks for the configuration file `.textIntegrityInspector.[yaml|toml]` in the current directory. The file format is as follows.

YAML format

```yaml
roots:
  - dir1
  - dir2
extensions:
  - txt
  - md
exclude-dirs:
  - tests
  - '**/temp*'
exclude-files:
  - example.txt
language: fr
additional-chars: 'ü,ö,ß'
verbose: true

```

It is possible to specify a different configuration file with the --config-file option. The TOML format is also supported.

TOML format

```toml
roots = ["dir1", "dir2"]
extensions = ["txt", "md"]
exclude-dirs = ["tests", "**/temp*"]
exclude-files = ["example.txt"]
language = "fr"
additional-chars = "ü,ö,ß"
verbose = true
silence = false
```

> [!IMPORTANT]
> The paths passed as arguments replace the `roots` list in the configuration file, while the other options are combined.


## Docker

### Usage

```bash
docker run -it -v path_to_inspect_dir:/data text_integrity_inspector --extensions py txt 
```

## Gitlab-ci integration

![GitLab CI](https://img.shields.io/badge/gitlab%20ci-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
 ```yaml
 
check-utf-8:
  image: 
    name: text_integrity_inspector
    entrypoint: [""]
  stage: test
  script:
  - textIntegrityInspector . --extensions py txt json conf  --language fr
  ```

## Contributing

Contributions are welcome! Please open a pull request or issue if you have any feedback or suggestions.

## License

The Text Integrity Inspector package is licensed under the [MIT License](LICENSE).
