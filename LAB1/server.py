import Pyro4
import random

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self,name):
        print(name + " is calling the method")
        num = random.randint(0, 10**6)
        return ("Hello, " + name + " your lucky number is " + str(num))

deamon = Pyro4.Daemon()
uri = deamon.register(GreetingMaker)


print(uri)

print("READY")
deamon.requestLoop()
