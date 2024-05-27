
import pytest
import tempfile
import os
from textIntegrityInspector.__main__ import main_args, parse_arguments

@pytest.fixture(scope='module')
def root():
    with tempfile.TemporaryDirectory() as root:
        yield root
        pass # automatic remove root directory

def create_temp_config_file(content, file_format):
    _, file_path = tempfile.mkstemp(suffix=f'.{file_format}')
    with open(file_path, 'w', encoding='utf-8') as config_file:
        config_file.write(content)
    return file_path

def test_parse_yaml_file():
    yaml_content = """
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
    """

    file_path = create_temp_config_file(yaml_content, 'yaml')
    config = parse_arguments([f'--config-file={file_path}', '--extensions', 'py','cpp', '--exclude-dirs', '.git', '.cache'  ])
    assert config.roots == ['.']
    assert set(config.extensions) == set(['txt', 'md', 'py','cpp'])
    assert set(config.exclude_dirs) == set([os.path.abspath('tests'), os.path.abspath('**/temp*'),os.path.abspath('.git'), os.path.abspath('.cache')])
    assert set(config.exclude_files) == set([os.path.abspath('example.txt')])
    assert config.language == 'fr'
    assert config.additional_chars == 'ü,ö,ß'
    assert config.verbose == True

def test_parse_toml_file():
    toml_content = """
    roots = ["dir1", "dir2"]
    extensions = ["txt", "md"]
    exclude-dirs = ["tests", "**/temp*"]
    exclude-files = ["example.txt"]
    language = "fr"
    additional-chars = "ü,ö,ß"
    verbose = true
    """
    file_path = create_temp_config_file(toml_content, 'toml')
    config = parse_arguments([f'--config-file={file_path}'])
    assert config.roots == ['dir1', 'dir2']
    assert set(config.extensions) == {'txt', 'md'}
    assert set(config.exclude_dirs) == {os.path.abspath('tests'), os.path.abspath('**/temp*')}
    assert set(config.exclude_files) == {os.path.abspath('example.txt')}
    assert config.language == 'fr'
    assert config.additional_chars == 'ü,ö,ß'
    assert config.verbose == True

    
def test_parse_root_priority():
    toml_content = """
    roots = ["dir1", "dir2"]
    extensions = ["txt", "md"]
    exclude-dirs = ["tests", "**/temp*"]
    exclude-files = ["example.txt"]
    language = "fr"
    additional-chars = "ü,ö,ß"
    verbose = true
    """
    file_path = create_temp_config_file(toml_content, 'toml')
    config = parse_arguments([f'--config-file={file_path}', 'dir3', 'dir4'])
    assert config.roots == ['dir3', 'dir4']
    assert set(config.extensions) == {'txt', 'md'}
    assert set(config.exclude_dirs) == {os.path.abspath('tests'), os.path.abspath('**/temp*')}
    assert set(config.exclude_files) == {os.path.abspath('example.txt')}
    assert config.language == 'fr'
    assert config.additional_chars == 'ü,ö,ß'
    assert config.verbose == True

def test_main(root):
    with tempfile.TemporaryDirectory() as root:
        main_args(parse_arguments([root]))
    
if __name__ == "__main__":
    import pytest
    pytest.main(["--verbose", "--log-cli-level=DEBUG", "--color=no",__file__])