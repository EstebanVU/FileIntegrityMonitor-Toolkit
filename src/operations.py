def fileWrite(file, dir):
    with open(dir, 'w') as f:
        f.write(file)


def fileRead(dir):
    with open(dir, 'r') as f:
        return f.read()
