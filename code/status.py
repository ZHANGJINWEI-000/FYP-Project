class gameStatus():
    def __init__(self):
        self.status = ["map"]
    
    def change(self, status):
        self.status = [status]
    
    def add(self, status):
        if not self.exist(status):
            self.status.append(status)
    
    def remove(self, status):
        if self.exist(status):
            self.status.remove(status)
        if not len(self.status):
            self.change("implement")
    
    def exist(self, status):
        return status in self.status