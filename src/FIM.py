import os
import hashlib
import time
import base64

web = {'path': './web', 'recursive': True}
backup = {'path': './backup', 'recursive': True}

filesWeb = {}
filesBackup = {}


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
        with open(file) as f:
            for chunk in iter(lambda: f.read(2048), ""):
                hash.update(chunk.encode('utf-8'))
        sha256 = hash.hexdigest()
        files[file] = {'sha256': sha256, 'bytes': getBytes(file)}


getHash(getFiles(web), filesWeb)
print('Directory: ', web)
print('Files: ', getFiles(web))
print('Hash Files: ', filesWeb)


# while True:

#     time.sleep(1)
