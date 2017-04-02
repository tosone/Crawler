from os import listdir, path

if __name__ == '__main__':
    for filename in listdir('.'):
        if filename[0:2] == '__' and path.splitext(filename)[1] == '.py':
            run = __import__(path.splitext(filename)[0])
            run.Run()
