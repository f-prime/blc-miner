import socket
import multiprocessing
import string
import random
import json
import hashlib
import sys
import time

class BLCMiner:
    def __init__(self):
        self.ip = "server.bloocoin.org"
        self.port = 3122
        self.strs = string.uppercase+string.lowercase+string.digits
        self.diff = self.difficulty()
        
    def main(self):
        while True:
            ss = self.generate()
            num = 0
            print "Difficulty:", str(self.diff), "String:", ss
            while True:
                data = hashlib.sha512(ss+str(num)).hexdigest()
                if data.startswith("0"*self.diff):
                    self.submit(ss+str(num), data)
                    break
                else:
                    num += 1
    def difficulty(self):
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
        except:
            print "Could not connect to server"
        else:
            s.send(json.dumps({"cmd":"get_coin"}))
            data = s.recv(1024)
            if data:
                data = json.loads(data)
                if data['success']:
                    return data['payload']['difficulty']
                else:
                    print data['message']
                    exit()
            else:
                return
    
    def submit(self, string_, hash):
        print "Found wining solution", string_, hash
        s = socket.socket()
        try:
            s.connect((self.ip, self.port))
        except:
            print "Can't connect to server"
        else:
            s.send(json.dumps({"cmd":"check", "winning_string":string_, "winning_hash":hash, "addr":sys.argv[2]}))
            data = s.recv(1024)
            data = json.loads(data)
            if data['success']:
                print "Mined a coin!"
            else:
                print "Coin is a fake!"
        self.diff = self.difficulty()

    def generate(self):
        startstr = ""
        for x in xrange(5):
            startstr = startstr+random.choice(self.strs)            
        return startstr

if __name__ == "__main__":
    
    for x in range(int(sys.argv[1])):

        multiprocessing.Process(target=BLCMiner().main).start()
