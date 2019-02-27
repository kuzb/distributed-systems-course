import Pyro4
import random
import subprocess
import os
import sys

@Pyro4.expose
class GreetingMaker(object):
    def print_sum(self, int1, int2):
        print("Client asked for the sum of " + str(int1) + " and " + str(int2))
        num = int(int1) + int(int2)
        return num

if __name__ == '__main__':
    try:

        daemon = Pyro4.Daemon()
        
        # uses nameserver in order expose endpoint
        ns = Pyro4.locateNS()
        uri = daemon.register(GreetingMaker)
    
        # you need to run "python -m Pyro4.naming" beforing starting the server
        ns.register("example.sum", uri)
        
    
    
        print("READY")
        daemon.requestLoop()

    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        daemon.shutdown()
        print("NS is shut down and program is terminated")