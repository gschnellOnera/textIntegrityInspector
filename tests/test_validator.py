
import os
import tempfile
import pytest

from textIntegrityInspector.validator import TextIntegrityChar
from textIntegrityInspector.languageData import display_languages

@pytest.fixture(scope='function')
def textIntegrityCharStub():
    def stub_validate_file(obj, file_Path):
        obj.stub_filePaths.append(file_Path)
    textIntegrityChar = TextIntegrityChar()
    textIntegrityChar.stub_filePaths=[]
    textIntegrityChar.validate_file = stub_validate_file
    return textIntegrityChar

def createFileUTF_8(dir, name,  text):
    file_path = os.path.join(dir, name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def createFilebin(dir, name,  text):
    file_path = os.path.join(dir, name)
    with open(file_path, 'wb') as file:
        file.write(text)

@pytest.fixture(scope='module')
def root():
    """create tree test

    root
    +--- insert
    |   +--- excluded_dir
    |   |   +--- autres2
    |   |   |   +--- notfrenshFile.txt
    |   |   |   +--- notutf8.dumy
    |   |   |   +--- BOM.dumy
    |   +--- included_dir
    |   |   +--- autres
    |   |   |   +--- frenshFile.txt

    """
    with tempfile.TemporaryDirectory() as root:
        included_dir = os.path.join(root, 'insert','included_dir', 'autres')
        os.makedirs(included_dir)
        createFileUTF_8(dir=included_dir, name='frenshFile.txt', text="Ceci est un texte valide en français.\n\r\te contenant que des caractère Français")
        excluded_dir = os.path.join(root, 'insert','excluded_dir', 'autres2')
        os.makedirs(excluded_dir)
        createFileUTF_8(dir=excluded_dir, name='notfrenshFile.txt', text="Ceci est un texte non-valide en français.\nnontenant de caractère ¤ à la \n 24 colone de la ligne 2.")
        createFilebin(dir=excluded_dir, name='notutf8.dumy', text=b'ab\x01c\xf5\xde\x02\xee\x01\x02\xf3\x01\x02\03f' + "¿�𝄞𠀀".encode())
        createFilebin(dir=excluded_dir, name='BOM.dumy', text='Ceci est un utf-8-sig file\n'.encode('utf-8-sig'))
        yield root
        pass # automatic remove root directory

def test_validate_directory_valid(root):
    # Crée un fichier texte valide dans un répertoire valide
        # Valide le fichier
        textIntegrityChar = TextIntegrityChar()
        textIntegrityChar.validate_directory(os.path.join(root, 'insert', 'included_dir'), extensions=['txt'], exclude_dirs=[], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 0
        textIntegrityChar.print_lErrors()
        textIntegrityChar.print_speCar()


def test_exclude_directoryDoubleAsterix(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(root, extensions=['txt'], exclude_dirs=[os.path.join('**','excluded_dir')], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 0

def test_exclude_directoryOneAsterix(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(root, extensions=['txt'], exclude_dirs=[os.path.join(root, 'insert', 'excluded_dir', '*')], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 0

def test_exclude_directory(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(root, extensions=['txt'], exclude_dirs=[os.path.join(root, 'insert', 'excluded_dir')], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 0

def test_exclude_directory_2(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(root, extensions=['txt'], exclude_dirs=[os.path.join(root, 'insert', 'excluded_dirAppend')], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 1
        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(root, extensions=['txt'], exclude_dirs=[os.path.join(root, 'insert', 'excluded')], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 1

def test_validate_directory_invalid_language(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(os.path.join(root, 'insert', 'excluded_dir'), extensions=['txt'], exclude_dirs=[], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 1
        assert textIntegrityChar.lErrors[0]['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notfrenshFile.txt')
        assert textIntegrityChar.lErrors[0]['line'] == 2
        assert textIntegrityChar.lErrors[0]['col'] == 24
        textIntegrityChar.print_lErrors()
        textIntegrityChar.print_speCar()

def test_validate_directory_noUTF_8(root):

        textIntegrityChar = TextIntegrityChar()
        # Valide le fichier avec la langue spécifiée
        textIntegrityChar.validate_directory(os.path.join(root, 'insert', 'excluded_dir'), extensions=[], exclude_dirs=[], exclude_files=[], language='fr', additional_chars='')
        assert len(textIntegrityChar.lErrors) == 11
        
        #0
        i= 0
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'BOM.dumy')), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'BOM.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 1
        assert item['carBin'] == b'\xef\xbb\xbf'
        assert item['utf-8'] == b'\xef\xbb\xbf'.decode()
        #1
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notfrenshFile.txt')), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notfrenshFile.txt')
        assert item['line'] == 2
        assert item['col'] == 24
        assert item['errorType'] == 'NotInLanguage'
        assert item['carBin'] == b'\xc2\xa4'
        assert item['utf-8'] == '¤'
        #2
        
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 3), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 3
        assert item['carBin'] == b'\x01'
        #3
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 5), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotUtf-8'
        assert item['col'] == 5
        assert item['carBin'] == b'\xf5'
        #4
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 6), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotUtf-8'
        assert item['col'] == 6
        assert item['carBin'] == b'\xde\x02'
        #5
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 7), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotUtf-8'
        assert item['col'] == 7
        assert item['carBin'] == b'\xee\x01\x02'
        #6
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 8), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotUtf-8'
        assert item['col'] == 8
        assert item['carBin'] == b'\xf3\x01\x02\03'
        #7
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 10), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['line'] == 1
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 10
        assert item['carBin'] == '¿'.encode()
        assert item['utf-8'] == '¿'
        #8
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 11), None)
        assert item is not None
        assert item['file'] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy')
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 11
        assert item['carBin'] == '�'.encode()
        assert item['utf-8'] == '�'
        #9
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 12), None)
        assert item is not None
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 12
        assert item['carBin'] == '𝄞'.encode()
        assert item['utf-8'] == '𝄞'
        #10
        item = next((item for item in textIntegrityChar.lErrors if item["file"] == os.path.join(root, 'insert', 'excluded_dir', 'autres2', 'notutf8.dumy') and item['col'] == 13), None)
        assert item is not None
        assert item['errorType'] == 'NotInLanguage'
        assert item['col'] == 13
        assert item['carBin'] == '𠀀'.encode()
        assert item['utf-8'] == '𠀀'
        textIntegrityChar.print_lErrors()
        textIntegrityChar.print_speCar()


def test_validate_directory_exclude_dirs():
    # Crée deux répertoires, un à valider et un à exclure
    with tempfile.TemporaryDirectory() as root:
        included_dir = os.path.join(root, 'inert','included_dir', 'autres')
        excluded_dir = os.path.join(root, 'inert','excluded_dir', 'autres2')
        os.makedirs(included_dir)
        os.makedirs(excluded_dir)
        
        # Valide le répertoire en excluant le répertoire exclu
        TextIntegrityChar().validate_directory(root, extensions=['txt'], exclude_dirs=['excluded_dir'], exclude_files=[], language='fr', additional_chars='')

    
def test_is_valid_char_valid():
    # Teste un caractère valide
    # `valid_char` is a variable that stores the byte representation of the character 'a'. It is used
    # in the `test_is_valid_char_valid()` function to test if the character is considered valid by the
    # `TextIntegrityChar` class.
    valid_char = 'a'.encode()
    textIntegrityChar = TextIntegrityChar()
    textIntegrityChar.get_list_valid_chars('fr', '')
    res = True
    for byte in  [valid_char[i:i+1] for i in range(len(valid_char))] :
        res = res and  textIntegrityChar.is_valid_char(byte)
    assert res

def test_is_valid_char_invalid_language():
    # Teste un caractère invalide pour la langue spécifiée
    invalid_char = '¤'.encode()
    textIntegrityChar = TextIntegrityChar()
    textIntegrityChar.get_list_valid_chars('fr', '')
    res = True
    for byte in  [invalid_char[i:i+1] for i in range(len(invalid_char))] :
        res = res and  textIntegrityChar.is_valid_char(byte)
    assert not res

def test_is_valid_char_additional_chars():
    # Teste un caractère valide avec des caractères supplémentaires acceptés
    valid_char = '¤'.encode()
    textIntegrityChar = TextIntegrityChar()
    textIntegrityChar.get_list_valid_chars('fr', '¤')
    res = True
    for byte in  [valid_char[i:i+1] for i in range(len(valid_char))] :
        res = res and  textIntegrityChar.is_valid_char(byte)
    assert res

def test_is_valid_char_invalid_additional_chars():
    # Teste un caractère invalide avec des caractères supplémentaires non acceptés
    invalid_char = '¤'.encode()
    textIntegrityChar = TextIntegrityChar()
    textIntegrityChar.get_list_valid_chars('fr', '¤')
    res = True
    for byte in  [invalid_char[i:i+1] for i in range(len(invalid_char))] :
        res = res and  textIntegrityChar.is_valid_char(byte)
    assert res
    
def test_display_languages():
    display_languages() 

if __name__ == "__main__":
    import pytest
    pytest.main(["--verbose", "--log-cli-level=DEBUG", "--color=no",__file__])