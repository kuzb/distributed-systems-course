import zmq
import time
import threading
import multiprocessing
from abc import ABC, abstractmethod  # Abstract Base Classes 
# Used for defining abstract classes


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class MapReduce(ABC):
    def __init__(self, NumWorker): # constructer
        self.NumWorker = NumWorker
        self.id = 0 # but ids of worker start by 1 look at giveId
        super().__init__()

    # data arr is an integer array
    @abstractmethod
    def Map(self, data_arr):
        pass
    # Map function should map it to a single integer value.
    @abstractmethod
    def Reduce(self, data_arr):
        pass
    # Reduce function should map it to a single integer value.

    #@classmethod
    def producer(self, data_arr):
        print("I am producer")
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://127.0.0.1:5557")
        # Start your result manager and workers before you start your producers
        
        # split data_arr and send it
        size = len(data_arr)
        portions = size // self.NumWorker
        data_arrs = chunks(data_arr, portions)

        i = 1
        for arr in data_arrs:
            for x in range(10):
                print("Producer: Sending " + str(arr) + " to " + str(i))
                work_message = { 'arr' : arr, 'id' : i }            
                zmq_socket.send_json(work_message)
            i += 1
        pass


    #@classmethod
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
                arr = work['arr']
                data = self.Map(arr)
                print("Consumer: Sending " + str(data) + " with id " + str(consumer_id))
                result = { 'id' : consumer_id, 'result' : data }
                for x in range(10):
                    consumer_sender.send_json(result)

    #@classmethod
    def resultCollector(self):
        print("I am result collector")
        context = zmq.Context()
        results_receiver = context.socket(zmq.PULL)
        results_receiver.bind("tcp://127.0.0.1:5558")
        workers = set()
        arr = []
        while(len(workers) < self.NumWorker):
            result = results_receiver.recv_json()
            if not result['id'] in workers:
                print("Result Collector: Reciving " + str(result['result']) + " from " + str(result['id']))
                workers.add(result['id'])
                arr.append(result['result'])

        reduced = self.Reduce(arr)
        print(reduced)
        

    #@classmethod
    def start(self, data_arr):
        resultCollectorThread = threading.Thread(target = self.resultCollector)
        resultCollectorThread.start()
        consumers = []
        for i in range(self.NumWorker):
            p = multiprocessing.Process(target=self.consumer, args=(i+1, ))
            consumers.append(p)
            p.start()
        producerThread = threading.Thread(target = self.producer, args = (data_arr, ))
        producerThread.start()


# A subclass of MapReduce, which finds the maximum element
# in the given integer array.   
class FindMax(MapReduce):
    def Map(self, data_arr):
        return max(data_arr)
    # Map function should map it to a single integer value.

    def Reduce(self, data_arr):
        return max(data_arr)
    # Reduce function should map it to a single integer value.

# A subclass of MapReduce, which sums up the integer array.
class FindSum(MapReduce):
    def Map(self, data_arr):
        return sum(data_arr)
    # Map function should map it to a single integer value.

    def Reduce(self, data_arr):
        return sum(data_arr)
    # Reduce function should map it to a single integer value. 


# A subclass of MapReduce, which finds the number
# of elements which are less than 0.
class FindNegativeCount(MapReduce):
    def __init__(self, numWorker):
        super().__init__(numWorker)

    def Map(self, data_arr):
        return sum(1 for i in data_arr if i < 0)
    # Map function should map it to a single integer value.

    def Reduce(self, data_arr):
        return sum(1 for i in data_arr if i < 0)
    # Reduce function should map it to a single integer value.
    pass

if __name__ == "__main__":
    maxxer = FindMax(5)
    maxxer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])

    #summer = FindSum(10)
    #summer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])
    #negativeCounter = FindNegativeCount(10)
    #negativeCounter.start([15,-12,11,19,12,-15,31,32,4365,-546346,3425342,-32,13,34,4234523,-565,4334,243323])
