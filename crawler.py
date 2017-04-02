from os import listdir, path
import threading
import hashlib
import time
import os

if __name__ == '__main__':
    thread_list = {}
    for filename in listdir('.'):
        name = path.splitext(filename)[0]
        ext = path.splitext(filename)[1]
        if name[0:2] == '__' and ext == '.py':
            pure_name = name[2:]
            run = __import__(path.splitext(filename)[0])
            t = threading.Thread(target=run.Run)
            thread_list[pure_name] = hashlib.md5(open(filename, 'rb').read()).hexdigest()
            t.setDaemon(True)
            t.setName(path.splitext(filename)[0])
            t.start()
    while True:
        for filename in listdir('.'):
            name = path.splitext(filename)[0]
            ext = path.splitext(filename)[1]
            if filename[0:2] == '__' and name == '.py':
                pure_name = name[2:]
                if thread_list.get(pure_name) != hashlib.md5(open(filename, 'rb').read()).hexdigest():
                    os.exit(0)
        time.sleep(20)
