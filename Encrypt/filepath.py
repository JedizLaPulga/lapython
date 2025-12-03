

#file
class myFile:
    def __init__(self, fileName:str):
        self.fileName = fileName

    def readFile(self):
        with open(self.fileName, 'r') as file:
            data = file.read()
        return data

    def writeFile(self, data):
        with open(self.fileName, 'w') as file:
            file.write(data)

    def checkFile(self):
        import os;
        os.path.isfile(self.filename)