import Pyro4
# use this if you want to use uri
#uri = input("what is the URI of the greeting object?").strip()
#server_ref=Pyro4.Proxy(uri)

# use this in order to use nameserver
server_ref = Pyro4.Proxy("PYRONAME:example.greeting")
int1 = input("give the first number")
int2 = input("give the second number")
response=server_ref.print_sum(int1, int2)
print(response)