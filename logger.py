class Logger:
    def __init__(self, filename):
        self.filename = filename + '.txt'
    def write(self, text):
        with open(self.filename,'a') as f:
            f.write(str(text) +'\n')
    
