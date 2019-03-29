import zmq
from abc import ABC # Abstract Base Classes 
# Used for defining abstract classes

class MapReduce(ABC):
    def MapReduce(self, NumWorker): # constructer
        pass

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
        pass

    @classmethod
    def consumer(self, data_arr):
        pass

    @classmethod
    def resultCollector(self):
        pass

    @abstractmethod
    def start(self, data_arr):
        pass

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
    pass

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

    