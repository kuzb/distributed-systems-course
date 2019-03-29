import zmq
import time
import threading
import multiprocessing
from abc import ABC, abstractmethod, classmethod  # Abstract Base Classes 
# Used for defining abstract classes


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class MapReduce(ABC):
    def __init__(self, NumWorker): # constructer
        self.NumWorker = NumWorker
        self.id = 0 # but ids of worker start by 1 look at giveId

    def giveId():
        self.id += 1
        return self.id

    # data arr is an integer array
    @abstractmethod
    def Map(self, data_arr):
        pass
    # Map function should map it to a single integer value.
    @abstractmethod
    def Reduce(self, data_arr):
        pass
    # Reduce function should map it to a single integer value.

    @classmethod
    def producer(self, data_arr):
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://127.0.0.1:5557")
        # Start your result manager and workers before you start your producers
        
        # split data_arr and send it
        size = data_arr.length()
        portions = size // self.NumWorker
        data_arrs = chunks(data_arr, portions)

        i = 1
        for arr in data_arrs:
            for x in range(10):
                work_message = { 'arr' : arr, 'id' : i }            
                zmq_socket.send_json(work_message)
            i += 1
        pass


    @classmethod
    def consumer(self, i):
        consumer_id = i
        
        print("I am consumer #%s" % (consumer_id))
        context = zmq.Context()

        # recieve work
        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect("tcp://127.0.0.1:5557")

        # send work
        consumer_sender = context.socket(zmq.PUSH)
        consumer_sender.connect("tcp://127.0.0.1:5558")

        while True:
            work = consumer_receiver.recv_json()
            if consumer_id == work['id']:
                for x in range(10):
                    arr = work['arr']
                    data = self.Map(arr)
                    result = { 'id' : consumer_id, 'result' : data }
                    consumer_sender.send_json(result)

    @classmethod
    def resultCollector(self):
        context = zmq.Context()
        results_receiver = context.socket(zmq.PULL)
        results_receiver.bind("tcp://127.0.0.1:5558")
        workers = Set()
        arr = []
        while(len(workers) < self.NumWorker):
            result = results_receiver.recv_json()
            if not result['id'] in workers:
                workers.add(result['id'])
                arr.append(result['result'])

        reduced = self.Reduce(arr)
        print(reduced)
        

    @abstractmethod
    def start(self, data_arr):
        resultCollectorThread = threading.Thread(target = self.resultCollector)
        consumers = []
        for i in range(self.NumWorker):
            p = multiprocessing.Process(target=self.consumer, args=i+1)
            consumers.append(p)
            p.start
        producerThread = threading.Thread(target = self.producer, args = data_arr)



# A subclass of MapReduce, which finds the maximum element
# in the given integer array.   
class FindMax(MapReduce):
    @abstractmethod
    def Map(self, data_arr):
        pass
    # Map function should map it to a single integer value.
    @abstractmethod
    def Reduce(self, data_arr):
        pass
    # Reduce function should map it to a single integer value.
    pass

# A subclass of MapReduce, which sums up the integer array.
class FindSum(MapReduce):
    @abstractmethod
    def Map(self, data_arr):
        pass
    # Map function should map it to a single integer value.
    @abstractmethod
    def Reduce(self, data_arr):
        pass
    # Reduce function should map it to a single integer value. 


# A subclass of MapReduce, which finds the number
# of elements which are less than 0.
class FindNegativeCount(MapReduce):
    @abstractmethod
    def Map(self, data_arr):
        pass
    # Map function should map it to a single integer value.
    @abstractmethod
    def Reduce(self, data_arr):
        pass
    # Reduce function should map it to a single integer value.
    pass

if __name__ == "__main__":
    maxxer = FindMax(10)
    maxxer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])

    summer = FindSum(10)
    summer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])

    negativeCounter = FindNegativeCount(10)
    negativeCounter.start([15,-12,11,19,12,-15,31,32,4365,-546346,3425342,-32,13,34,4234523,-565,4334,243323])


    pass