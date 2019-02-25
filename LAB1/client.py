import Pyro4
# use this if you want to use uri
#uri = input("what is the URI of the greeting object?").strip()
#server_ref=Pyro4.Proxy(uri)

# use this in order to use nameserver
server_ref = Pyro4.Proxy("PYRONAME:example.greeting")
name = input("what is your name?").strip()
response=server_ref.get_fortune(name)
print(response)