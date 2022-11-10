import os
import hashlib
import time
import base64
import operations as op
import pathlib

BLOCK_SIZE = 65536

# Change path to your case
web = {'path': r'C:\Users\esteb\OneDrive\Escritorio\Ciclo ll\Seguridad informatica\Proyecto\FileIntegrityMonitor-Toolkit\src\web', 'recursive': True}
backup = {'path': r'C:\Users\esteb\OneDrive\Escritorio\Ciclo ll\Seguridad informatica\Proyecto\FileIntegrityMonitor-Toolkit\src\backup', 'recursive': True}

filesWeb = {}
filesBackup = {}

exceptionsTypes = [
    '.png', '.jpg', '.jpeg', '.gif', '.css', '.txt'
]

# Change path to your case
exceptionsDir = [
    r'C:\Users\esteb\OneDrive\Escritorio\Ciclo ll\Seguridad informatica\Proyecto\FileIntegrityMonitor-Toolkit\src\web\public',
    r'C:\Users\esteb\OneDrive\Escritorio\Ciclo ll\Seguridad informatica\Proyecto\FileIntegrityMonitor-Toolkit\src\web\resources',
]


def getFiles(directory):
    filesList = []
    if os.path.isdir(directory['path']):
        if directory['recursive']:
            filesList.extend([os.path.join(root, f) for (
                root, dirs, files) in os.walk(directory['path']) for f in files])
        else:
            filesList.extend([item for item in os.listdir(
                directory['path']) if os.path.isfile(item)])
    elif os.path.isfile(directory['path']):
        filesList.append(directory['path'])
    return filesList


def getBytes(file):
    return base64.b64encode(open(file, "rb").read())


def getHash(fileList, files):
    for file in fileList:
        hash = hashlib.sha256()
        with open(file, 'rb') as f:
            data = f.read(BLOCK_SIZE)
            while len(data) > 0:
                hash.update(data)
                data = f.read(BLOCK_SIZE)
        sha256 = hash.hexdigest()
        files[file] = {'sha256': sha256, 'bytes': getBytes(file)}


def hash_compare():
    getHash(getFiles(web), filesWeb)
    for hashWeb in filesWeb:
        backupMirror = str(hashWeb).replace(r'\web', r'\backup')
        if backupMirror in filesBackup:
            if filesWeb[hashWeb]['sha256'] == filesBackup[backupMirror]['sha256']:
                print('1) No cambio', hashWeb)
            else:
                fileExtension = pathlib.Path(hashWeb).suffix
                fileDirectory = pathlib.Path(hashWeb).resolve().parent
                if str(fileDirectory) in exceptionsDir and fileExtension in exceptionsTypes:
                    print('2) Cambio. Se acepta', hashWeb)
                    if fileExtension in exceptionsTypes and fileExtension != '.css' and fileExtension != '.txt':
                        op.imageSave(str(hashWeb), backupMirror)
                    else:
                        op.fileWrite(op.fileRead(hashWeb), backupMirror)
                else:
                    print('2) Cambio. No se acepta', hashWeb, backupMirror)
                    op.fileWrite(op.fileRead(backupMirror), hashWeb)
        else:
            fileExtension = pathlib.Path(hashWeb).suffix
            fileDirectory = pathlib.Path(hashWeb).resolve().parent
            if str(fileDirectory) in exceptionsDir and fileExtension in exceptionsTypes:
                print('2) Cambio. Se acepta', hashWeb)
                if fileExtension in exceptionsTypes and fileExtension != '.css' and fileExtension != '.txt':
                    op.imageSave(str(hashWeb), backupMirror)
                else:
                    op.fileWrite(op.fileRead(hashWeb), backupMirror)

            else:
                print('2) Cambio. No se acepta', hashWeb, backupMirror)
                op.fileWrite(op.fileRead(backupMirror), hashWeb)


def file_exist():
    getHash(getFiles(web), filesWeb)
    routesWeb = getFiles(web)
    routesBackup = getFiles(backup)
    for dir in routesWeb:
        backupMirror = str(dir).replace(r'\web', r'\backup')
        if (backupMirror not in routesBackup):
            print('no existe')
            os.remove(dir)
            print("eliminado")


getHash(getFiles(backup), filesBackup)

while True:
    print('\n-----------EJECUCION-----------')
    hash_compare()
    file_exist()
    time.sleep(30)
    print('-----------FIN EJECUCION-----------')
