import zmq
import time
import threading
import multiprocessing
from abc import ABC, abstractmethod  # Abstract Base Classes 
# Used for defining abstract classes

def chunks(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


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
        #print("I am producer")
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://127.0.0.1:5557")
        # Start your result manager and workers before you start your producers
        
        # split data_arr and send it
        data_arrs = chunks(data_arr, self.NumWorker)

        i = 1
        work_message = []
        for arr in data_arrs:
            work_message.append({ 'arr' : arr, 'id' : i })
            i += 1
        
        for i in range(self.NumWorker*10):
            for message in work_message:
                #print("Producer: Sending " + str(message))                           
                zmq_socket.send_json(message)
            


    #@classmethod
    def consumer(self, i):
        consumer_id = i
        
        #print("I am consumer #%s" % (consumer_id))
        context = zmq.Context()

        # recieve work
        consumer_receiver = context.socket(zmq.PULL)
        consumer_receiver.connect("tcp://127.0.0.1:5557")

        # send work
        consumer_sender = context.socket(zmq.PUSH)
        consumer_sender.connect("tcp://127.0.0.1:5558")

        
        while True:
            #print("Consumer: Polling with id: " + str(consumer_id))
            work = consumer_receiver.recv_json()
            if consumer_id == work['id']:            
                arr = work['arr']
                data = self.Map(arr)
                #print("Consumer: Sending: " + str(data) + " with id: " + str(consumer_id))
                result = { 'id' : consumer_id, 'result' : data }
                consumer_sender.send_json(result)
                break

    #@classmethod
    def resultCollector(self):
        #print("I am result collector")
        context = zmq.Context()
        results_receiver = context.socket(zmq.PULL)
        results_receiver.bind("tcp://127.0.0.1:5558")
        workers = set()
        arr = []
        while(len(workers) < self.NumWorker):
            #print("Result Collector: Number of workers: " + str(len(workers)))
            result = results_receiver.recv_json()
            if not result['id'] in workers:
                #print("Result Collector: Reciving: " + str(result['result']) + " from consumer id: " + str(result['id']))
                workers.add(result['id'])
                arr.append(result['result'])

        reduced = self.Reduce(arr)
        print("Result Collector: Final Result: " + str(reduced))
        

    #@classmethod
    def start(self, data_arr):
        resultCollectorThread = threading.Thread(target = self.resultCollector)
        resultCollectorThread.start()

        consumers = []
        for i in range(self.NumWorker):
            p = multiprocessing.Process(target=self.consumer, args=(i+1, ))
            consumers.append(p)
            p.start()

        time.sleep(1)
        producerThread = threading.Thread(target = self.producer, args = (data_arr, ))
        producerThread.start()

        producerThread.join()

        for Consumer in consumers:
            Consumer.join()

        resultCollectorThread.join()



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
        return sum(data_arr)
    # Reduce function should map it to a single integer value.
    pass

if __name__ == "__main__":
    #maxxer = FindMax(5)
    #maxxer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])

    #summer = FindSum(5)
    #summer.start([15,12,11,19,12,15,31,32,4365,546346,3425342,32,13,34,4234523,565,4334,243323])
    negativeCounter = FindNegativeCount(5)
    negativeCounter.start([15,-12,11,19,12,-15,31,32,4365,-546346,3425342,-32,13,34,4234523,-565,4334,243323])
