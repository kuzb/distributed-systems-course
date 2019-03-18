import zmq

def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://10.61.2.215:1558")

    work_message = {'data': 20647%55, 'sign': ((20647**7)%55), "id":20647}
    zmq_socket.send_json(work_message)

producer()