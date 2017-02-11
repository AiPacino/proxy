from tetread import reproxylist


list = reproxylist('./')

print(type(list))

#

class Check():
    def __init__(self, proxylist = [], url = None):
        self.url = url
        self.proxylist = proxylist

    def run(self):
        while proxylist