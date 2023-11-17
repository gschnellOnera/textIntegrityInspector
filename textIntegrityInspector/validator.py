
import sys
import os
from pathlib import Path
acuteAccentsLower="á, é, í, ó, ú"
acuteAccentsUpper="Á, É, Í, Ó, Ú"
graveAccentLower="à, è, ù"
graveAccentUpper="À, È, Ù"
circumflexAccentsLower="â, ê, î, ô, û"
circumflexAccentssUpper="Â, Ê, Î, Ô, Û"
diaeresisaLower="ä, ë, ï, ö, ü, ÿ"
diaeresisaUppwer="Ä, Ë, Ï, Ö, Ü"
cedilla="Ç, ç"
ligatures="Œ, œ, Æ, æ"
ponctunation=" …"
math="²±μ"
unit="°€"
edition="§©"
#"éçàèùêâêîûüôëïá°²ÉÊÈÀÇ§µ©œŒÆæÔÓ±μ …"
defaultSpecialFrenshChar = (acuteAccentsLower + acuteAccentsUpper 
    + graveAccentLower + graveAccentUpper 
    + circumflexAccentsLower + circumflexAccentssUpper 
    + diaeresisaLower + diaeresisaUppwer 
    + cedilla + ligatures + ponctunation 
    + math + unit + edition).replace(",","").replace(" ","")

class TextIntegrityChar :

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
        self.lErrors = []
        self.currentFile = myfile
        with open(myfile, "rb") as f:
            while (byte := f.read(1)):
                if byte == b'\n' : 
                    self.numLine += 1
                    self.numCol = 0
                else :
                    self.numCol += 1
                self.is_valid_char(byte)
        if mode == "v" and self.lErrors:
            self.print_lErrors()

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

    def print_lErrors(self):
        for error in self.lErrors:
            if error['errorType'] == 'NotInLanguage':
                print(f"{error['utf-8']}: {error['file']}: ({error['line']},{error['col']}), le caractère {error['utf-8']} n'est pas reconnue comme un caractère affichable en français!")
            elif error['errorType'] == 'NotUtf-8':
                print(f"{error['carBin']}: {error['file']} ({error['line']},{error['col']}): le caractère {error['carBin']}  n'est pas en utf-8!")
            else:
                print(error)
        if not self.lErrors:
            print("No bad characters found")

    def print_speCar(self):
        lCar = set()
        for error in self.lErrors:
            if error['errorType'] == 'NotInLanguage':
                lCar.add(error['utf-8'])
        for c in lCar:
            print(f'{c}')

    def get_list_valid_chars(self, language, additional_chars):

        self.spetialChars = additional_chars
        if language == 'fr':
            self.spetialChars += defaultSpecialFrenshChar
        #TODO uniq
        return self.spetialChars

    def validate_directory(self, root, extensions, exclude_dirs, exclude_files, language, additional_chars):
        self.get_list_valid_chars(language, additional_chars)
        for foldername, subfolders, filenames in os.walk(root):
            # Exclure les répertoires spécifiés
            subfolders[:] = [folder for folder in subfolders if folder not in exclude_dirs]
            for filename in filenames:
                file_path = os.path.join(foldername, filename)

                # Exclure les fichiers spécifiés
                if file_path not in exclude_files and filename.split('.')[-1] in extensions:
                    self.validate_file(file_path)
        # root = Path(rootDir)
        # for root,dirs,files in os.walk(rootDir):
        #     seeNextDir = False
        #     for dir in lExcludeDir:
        #         if root.startswith(dir): 
        #             seeNextDir = True
        #     if seeNextDir : 
        #         continue
        #     for file in files:
        #         if '.' in file and file.split('.')[-1] in extensions and file not in exclude_files :
        #             szPath = os.path.join(root,file)
        #             lError += validate_file(szPath, specialFrenshChar, mode = 's')

        
  
        