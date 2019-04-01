# distributed-systems-course-project

### LAB1

> For URI version i.e. Client connects to Server via its URI

Then respectively the Server and the Client is ran at different terminals.

```
$ python server.py
```

```
$ python client.py
```

Enter the URI of server to the Client and then enter the requested input.

> For NS version i.e. Client automatically connects to server using the nameserver to match the "topic"

Pyro's Name Server should be installed and It can be run as follows.

```
$ pyro4-ns
```

Then respectively the Server and the Client is ran at different terminals.

```
$ python server.py
```

```
$ python client.py
```

Enter the requested input to the Client.

### LAB2

Server stores an random number, and client makes requests to guess that random number.

Initially run the server

```
$ python server.py
```

then the client

```
$ python client.py
```

### LAB3

Super basically implements Push/Pull pattern to push student id and its rsa signed version

### LAB4

Simple program that implements async tasks. Routes are bound to async tasks
defined using celery. 

/todo/<:todo> route is used to create todos

/status/<:task_id> route is used to check the status of task with task_id


To run it: 
In seperate terminal emulators:

> celery -A server.celery worker # for flask

> python server.py # for app

### HW1

### HW2
#TODO
Gracefully handle interupts!
Producer has to know that consumer has consumed
