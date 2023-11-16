
import sys
import os
from pathlib import Path
defaultSpecialFrenshChar = "éçàèùêâêîûôëïá°²ÉÊÈÀ§µ©œÔÓ±μ …"

def verify_file(myfile, specialFrenshChar = defaultSpecialFrenshChar , mode='v'):
    notAscii = b''
    numLine = 1
    numCol = 0
    lErrors = []
    lenNotAsciiRequire = 0
    with open(myfile, "rb") as f:
        while (byte := f.read(1)):
            if byte == b'\n' : 
                numLine += 1
                numCol = 0
            else :
                numCol += 1
            if int(byte.hex(), 16) > 0x7f : #see https://fr.wikipedia.org/wiki/UTF-8
                #Si first byte
                if not notAscii:
                    if int(byte.hex(), 16) >= 0xc2 and int(byte.hex(), 16) <= 0xdf: lenNotAsciiRequire = 2
                    elif int(byte.hex(), 16) >= 0xe0 and int(byte.hex(), 16) <= 0xef: lenNotAsciiRequire = 3
                    elif int(byte.hex(), 16) >= 0xf0 and int(byte.hex(), 16) <= 0xf4: lenNotAsciiRequire = 4
                    else : lenNotAsciiRequire = 1 # not utf-8
                notAscii += byte
            if notAscii and len(notAscii) == lenNotAsciiRequire:
                    numCol -= lenNotAsciiRequire - 1
                    lErrors = appendListErrors(myfile, specialFrenshChar, notAscii, numLine, numCol, lErrors)
                    notAscii = b''
    if mode == "v" and lErrors:
        print_lError(lErrors)
    return lErrors

def appendListErrors(myfile, specialFrenshChar, notAscii, numLine, numCol, lErrors):
    error = {}
    try :
        decode = notAscii.decode()
        if not decode in specialFrenshChar:
            error = {'errorType': 'NotFrench', 'utf-8': decode }
    except UnicodeDecodeError:
        error = {'errorType': 'NotUtf-8' }
    if error:
        error = {**error, 'file': myfile, 'line' : numLine, 'col': numCol, 'carBin': notAscii }
        lErrors.append(error)
    return lErrors

def print_lError(lError):
    for error in lError:
        if error['errorType'] == 'NotFrench':
            print(f"{error['utf-8']}: {error['file']}: ({error['line']},{error['col']}), le caractère {error['utf-8']} n'est pas reconnue comme un caractère affichable en français!")
        elif error['errorType'] == 'NotUtf-8':
            print(f"{error['carBin']}: {error['file']} ({error['line']},{error['col']}): le caractère {error['carBin']}  n'est pas en utf-8!")
        else:
            print(error)
def print_speCar(lError):
    lCar = set()
    for error in lError:
        if error['errorType'] == 'NotFrench':
            lCar.add(error['utf-8'])
    for c in lCar:
        print(f'{c}')



    
if __name__ == '__main__':
    #verify_file(R'D:\gschnell\Documents\WorkSpacesVSCode\Projets_compose\PyGMT\src\PyGMT\GMTSatis\Tools\PlugEditor\PRIDataFormatter.py')
    nbErr = 0
    rootDir = sys.argv[1]
    #rootDir = R"D:\gschnell\Documents\WorkSpacesVSCode\Projets_compose\PyGMT"
    if len(sys.argv) > 2:
        specialFrenshChar = sys.argv[2]
    else:
        specialFrenshChar = defaultSpecialFrenshChar

    if len(sys.argv) > 3:
        listExt = sys.argv[2]
    else:
        listExt = ['py', 'pyx', 'json', 'txt', 'md']

    if len(sys.argv) > 4:
        lExcludeDir = sys.argv[3]
    else:
        lExcludeDir = [".venv", os.path.join("src", "build")]
    lExcludeDir = [os.path.join(rootDir, p) for p in lExcludeDir]

    if len(sys.argv) > 5:
        excludeFiles = sys.argv[5]
    else:
        excludeFiles = []

    root = Path(rootDir)

    lError = []
    for root,dirs,files in os.walk(rootDir):
        seeNextDir = False
        for dir in lExcludeDir:
            if root.startswith(dir): 
                seeNextDir = True
        if seeNextDir : 
            continue
        for file in files:
            if '.' in file and file.split('.')[-1] in listExt:
                szPath = os.path.join(root,file)
                lError += verify_file(szPath, specialFrenshChar, mode = 's')
    if lError:
        print_lError(lError)
        print_speCar(lError)
        exit(1)