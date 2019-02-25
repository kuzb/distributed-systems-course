import Pyro4

uri = input("what is the URI of the greeting object?").strip()
server_ref=Pyro4.Proxy(uri)

name = input("what is your name?").strip()
response=server_ref.get_fortune(name)
print(response)