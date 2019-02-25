import Pyro4
import random
import subprocess
import os
import sys

@Pyro4.expose
class Sum(object):
    def print_sum(self, int1, int2):
        print("Client asked for the sum of " + str(int1) + " and " + str(int2))
        num = int(int1) + int(int2)
        return num


if __name__ == '__main__':
    try:
        daemon = Pyro4.Daemon()
        uri = daemon.register(Sum)
    
        print("URI of print_sum is the following: ")
        print(uri)
        print("\nReady for access")
        
        daemon.requestLoop()

    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        daemon.shutdown()
        print("Terminated")