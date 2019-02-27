import Pyro4
import subprocess
import os



def terminate(remote):
    remote.shutdown()
    remote._pyroRelease()

if __name__ == '__main__':
    try:
        # uses nameserver inorder to connect the server
        remote = Pyro4.Proxy("PYRONAME:example.sum")
        
        int1 = input("Give the first number: ")
        int2 = input("Give the second number: ")

        response = remote.print_sum(int1, int2)

        print("Response is: " + str(response))

        terminate(remote)
    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        terminate(remote)
        print("Terminated")