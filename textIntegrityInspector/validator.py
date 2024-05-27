
import sys
import os

import logging
from fnmatch import fnmatch

from textIntegrityInspector.languageData import languageData, elementaryData, get_special_characters



def get_max_filename_length():
    import os
    import platform
    import subprocess
    import logging
    import ctypes
    max_length = -1
    try:
        system = platform.system()
        if system == 'Windows':
            max_length = int(subprocess.check_output("getconf NAME_MAX /", shell=True))
            #max_length = os.path.getconf('PC_NAME_MAX')
        elif system == 'Darwin':
            max_length = os.pathconf('/', 'PC_NAME_MAX')
        else:
            libc = ctypes.CDLL('libc.so.6')
            max_length = libc.fpathconf('/', 261)
    except Exception as e:
        logging.exception("get_max_filename_length_other")
        pass
    if max_length == -1 : max_length = float('inf')
    return max_length



class TextIntegrityChar :

    FILE_MAX_NAME = get_max_filename_length()

    def __init__(self):
        self.numCol = 0
        self.numLine = 1
        self.lErrors = []
        self.notAscii = b''
        self.spetialChars = ""
        self.currentFile = ""
        self.lenNotAsciiRequire = 0


    def is_valid_char(self, byte):
                
        isValide = True
        valHex = int(byte.hex(), 16)
        
        if not self.notAscii: # not in read utf-8 with more then 1 byte 
            if valHex < 0x1f and byte not in "\t\n\r".encode() :  # Control char see https://fr.wikipedia.org/wiki/Caract%C3%A8re_de_contr%C3%B4le
                self.lenNotAsciiRequire = 1
                self.notAscii += byte
            elif valHex > 0x7f : #see https://fr.wikipedia.org/wiki/UTF-8
                #Si first byte
                    if valHex >= 0xc2 and valHex <= 0xdf: self.lenNotAsciiRequire = 2
                    elif valHex >= 0xe0 and valHex <= 0xef: self.lenNotAsciiRequire = 3
                    elif valHex >= 0xf0 and valHex <= 0xf4: self.lenNotAsciiRequire = 4
                    else : self.lenNotAsciiRequire = 1 # not utf-8
                    self.notAscii += byte
            else :
                self.notAscii = b'' # ASCII display char
        else :
            self.notAscii += byte

        if self.notAscii and len(self.notAscii) == self.lenNotAsciiRequire:
                self.numCol -= self.lenNotAsciiRequire - 1
                isValide = self.appendListErrors()
                self.notAscii = b''
        return isValide
    
    def validate_file(self, myfile , mode='v'):
        self.notAscii = b''
        self.numLine = 1
        self.numCol = 0
        self.currentFile = myfile
        try :
            with open(myfile, "rb") as f:
                while (byte := f.read(1)):
                    if byte == b'\n' : 
                        self.numLine += 1
                        self.numCol = 0
                    else :
                        self.numCol += 1
                    self.is_valid_char(byte)
        except Exception as e:
            if len(myfile) >= self.FILE_MAX_NAME :
                logging.warning(f'The file "{myfile}" has exceeded the maximum character limit allowed by the system.')
            else :
                logging.exception(f"Erreur on open file {myfile} for read")

    def appendListErrors(self):
        error = {}
        try :
            decode = self.notAscii.decode()
            if not decode in self.spetialChars:
                error = {'errorType': 'NotInLanguage', 'utf-8': decode }
        except UnicodeDecodeError:
            error = {'errorType': 'NotUtf-8' }
        if error:
            error = {**error, 'file': self.currentFile, 'line' : self.numLine, 'col': self.numCol, 'carBin': self.notAscii }
            self.lErrors.append(error)
            return False
        return True

    def print_lErrors(self, fileName = None):
        if self.lErrors:
            print("Non-printable characters were found:")
            for error in self.lErrors:
                if not fileName or  error['file'] == fileName :
                    if error['errorType'] == 'NotInLanguage':
                        print(f"{error['utf-8']}: {error['file']} ({error['line']},{error['col']}), the character {error['utf-8']} is not recognized as a printable character in your language!")
                    elif error['errorType'] == 'NotUtf-8':
                        print(f"{error['carBin']}: {error['file']} ({error['line']},{error['col']}): the character {error['carBin']} is not in UTF-8 encoding!")
                    else:
                        print(error)
        else :
            print("No non-printable characters were found. Your files are UTF-8 compliant.")

    def print_speCar(self):
        lCar = set()
        for error in self.lErrors:
            if error['errorType'] == 'NotInLanguage':
                lCar.add(error['utf-8'])
        if lCar:
            print ('List of Non-printable characters is: [', end ='')
            lCar = [f"'{c}'" for c in lCar]
            print(', '.join(lCar), end='')
            print(']')

    def get_list_valid_chars(self, language, additional_chars):

        self.spetialChars = additional_chars
        if language in set(languageData.keys()):
            self.spetialChars += get_special_characters(language)
        #TODO uniq
        return set(self.spetialChars)
    
    
    @staticmethod
    def exclude_directory(path, exclude_patterns):
        for pattern in exclude_patterns:
            if fnmatch(path, pattern) or fnmatch(os.path.basename(path), pattern):
                return True
        return False

    def validate_directory(self, root, extensions, exclude_dirs, exclude_files, language, additional_chars):
        self.get_list_valid_chars(language, additional_chars)
        for foldername, subfolders, filenames in os.walk(root):
            logging.info(f"Analyzing directory: {foldername}")
            # Exclure les répertoires spécifiés
            subfolders[:] = [folder for folder in subfolders if not TextIntegrityChar.exclude_directory(os.path.abspath(os.path.join(foldername, folder)), exclude_dirs)]
            for filename in filenames:
                file_path = os.path.join(foldername, filename)

                # Exclure les fichiers spécifiés
                if os.path.abspath(file_path) not in exclude_files and (not extensions or  filename.split('.')[-1] in extensions):
                    self.validate_file(file_path)


        
