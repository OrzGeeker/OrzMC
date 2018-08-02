import hashlib
import os


def checkFileExist(filePath, hash):
    if not os.path.exists(filePath):
        return False
    
    with open(filePath, 'rb') as f:
        computeHash = hashlib.sha1(f.read()).hexdigest()
        ret = (computeHash == hash)
        if not ret:
            print('sha1 check failed: ' + filePath)
        return ret