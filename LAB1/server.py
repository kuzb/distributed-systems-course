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
class GreetingMaker(object):
    def get_fortune(self,name):
        print(name + " is calling the method")
        num = random.randint(0, 10)
        return ("Hello, " + name + " your lucky number is " + str(num))
    def print_sum(self, int1, int2):
        #print("Going to add following intergers" + str(int1) + " and " + str(int2))
        num = int(int1) + int(int2)
        return num



def main():
    deamon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = deamon.register(GreetingMaker)

    # Instead connecting using the uri, we are using ns to connect using "example.greeting" tag
    ns.register("example.greeting", uri)
    # you need to run "python -m Pyro4.naming" beforing starting the server


    print("READY")
    deamon.requestLoop()


if __name__ == '__main__':
    try:
        subp = subprocess.Popen(['python -m Pyro4.naming'])
        main()
    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        handleInterrupt()