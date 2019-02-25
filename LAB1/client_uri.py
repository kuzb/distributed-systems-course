import Pyro4
import subprocess
import os

#restore the terminal to its original operating mode.
def handleInterrupt():
        try:
            subprocess.call(["clear"])
            sys.exit(0)
        except SystemExit:
            subprocess.call(["clear"])
            os._exit(0)

# use this if you want to use uri
#uri = input("what is the URI of the greeting object?").strip()
#server_ref=Pyro4.Proxy(uri)

# use this in order to use nameserver
server_ref = Pyro4.Proxy("PYRONAME:example.greeting")
name = input("what is your name?").strip()
response=server_ref.get_fortune(name)
print(response)

if __name__ == '__main__':
    try:
        matrix = Rain()
    except KeyboardInterrupt: # To handle keyboardinterrupt more gracefully
        handleInterrupt()