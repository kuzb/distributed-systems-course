import Pyro4
import random
import subprocess
import os
import sys

#restore the terminal to its original operating mode.
def handleInterrupt():
        try:
            subprocess.call(["clear"])
            sys.exit(0)
        except SystemExit:
            subprocess.call(["clear"])
            os._exit(0)

@Pyro4.expose
class Sum(object):
    def print_sum(self, int1, int2):
        num = int(int1) + int(int2)
        return num


def main():
    deamon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = deamon.register(Sum)

    print(uri)
    
    ns.register("example.sum", uri)

    print("READY")
    deamon.requestLoop()


if __name__ == '__main__':
    try:
        subp = subprocess.Popen(['python -m Pyro4.naming'])
        main()
    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        handleInterrupt()