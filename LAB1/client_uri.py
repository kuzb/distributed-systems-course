import Pyro4
import subprocess
import os
import sys

if __name__ == '__main__':
    try:
        uri = input("What is the URI of the print_sum method? ").strip()

        remote = Pyro4.Proxy(uri)
    
        int1 = input("Give the first number: ")
        int2 = input("Give the second number: ")

        response = remote.print_sum(int1, int2)

        print("Response is: " + str(response))

    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        remote.shutdown()
        remote._pyroRelease()

        print("Terminated")