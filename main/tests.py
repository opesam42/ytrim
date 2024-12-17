import os

def checkDirectory(filename, dir):
    if not os.path.exists(dir):
        filename = filename
    if os.path.exists(dir):
        files = os.listdir(dir)
    if not files:
        filename = filename
    else:
        for file in files:
            if file == filename:
                i = 1
                filename = f'{filename}{i}'