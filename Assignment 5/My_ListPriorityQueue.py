from My_LinkedList import MyLinkedList


class My_ListPriorityQueue:
    def __init__(self):
        self.list = MyLinkedList()

    def get_size(self) -> int:
        """returns the number of elements in the PQ
        @return number of elements
        """
        return self.list.get_size()

    def is_empty(self) -> bool:
        """determines if the PQ is empty or not
        @return True or False
        """
        # if empty, size is 0
        return self.list.get_size() == 0

    def insert(self, integer_val: int) -> None:
        """inserts integer_val into the PQ
        @param integer_val: the value to be added
        @raises ValueError if integer_val is None
        """
        if integer_val is None:
            raise ValueError(f"{integer_val} is not an integer!")
        # if integer_val is not an int, insert_ordered takes care of that
        self.list.insert_ordered(integer_val)

    def remove_max(self) -> int:
        """removes the maximum element from the PQ and returns its value
        @return the value of the removed element or None if no element exists
        """
        return self.list.remove_first()  # since first element is maximum

    def get_max(self) -> int:
        """Returns the value of the maximum element of the PQ without removing it
        @return the maximum value of the PQ or None if no element exists
        """
        return self.list.get_first()  # since first element is maximum

    def to_list(self):
        """Returns a python list representation of the PQ
        @return a python list
        """
        return self.list.to_list()

    def to_string(self):
        """Returns a comma-delimited string representation of the PQ
        @return a string
        """
        return self.list.to_string()
