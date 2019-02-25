import Pyro4
import random

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self,name):
        print(name + " is calling the method")
        num = random.randint(0, 10)
        return ("Hello, " + name + " your lucky number is " + str(num))

deamon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = deamon.register(GreetingMaker)

# Instead connecting using the uri, we are using ns to connect using "example.greeting" tag
ns.register("example.greeting", uri)
# you need to run "python -m Pyro4.naming" beforing starting the server


print("READY")
deamon.requestLoop()
