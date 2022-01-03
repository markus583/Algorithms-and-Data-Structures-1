from typing import Union


# set up some helper functions as suggested in the assignment sheet
def parent(index):
    return (index - 1) // 2


def left_child(index):
    return 2 * index + 1


def right_child(index):
    return 2 * index + 2


class MyHeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.size = 0

    def up_heap(self, index):
        if self.heap[index] > self.heap[parent(index)]:  # if child > parent
            self.swap(index, parent(index))  # then: swap
            if not parent(index) == 0:  # make sure that if parent is reached, no more swapping is done
                self.up_heap(parent(index))  # recursively call up_heap

    def down_heap(self, index, integer_val):
        # get children
        left = left_child(index)
        right = right_child(index)
        # initialize largest --> current root
        largest = self.heap[index]
        if left < self.size:  # to take care of bounds
            if self.heap[left] > self.heap[largest]:  # left child is larger than current root
                largest = left
        if right < self.size:  # to take care of bounds
            if self.heap[right] > self.heap[largest]:  # right child is larger than current root AND left child
                largest = right

        if largest != integer_val:  # check if violation: one child > parent
            self.swap(index, largest)  # swap larger child and parent
            self.down_heap(largest, integer_val=integer_val)  # down heap recursively with same stopping criterion

    def swap(self, index1, index2):
        """
        Function that swaps the position of 2 elements.
        """
        self.heap[index1], self.heap[index2] = (self.heap[index2], self.heap[index1])

    def get_heap(self):
        """
        for testing purposes only
        """
        return self.heap

    def insert(self, integer_val: int) -> None:
        """inserts integer_val into the max heap
        @param integer_val: the value to be inserted
        @raises ValueError if integer_val is None
        """
        if not isinstance(integer_val, int):
            raise ValueError(f"{integer_val} is not an integer!")
        # Heap is empty; just insert into empty list
        if self.size == 0:
            self.heap.append(integer_val)
            self.size += 1
        # heap not empty; up heap
        else:
            self.heap.append(integer_val)  # append value to list --> insert 1 far right on lowest level
            self.size += 1  # change size
            self.up_heap(len(self.heap) - 1)  # upheap from last element in list, i.e. integer_val

    def is_empty(self) -> bool:
        """returns True if the max heap is empty, False otherwise
        @return True or False
        """
        return self.size == 0

    def get_max(self) -> Union[None, int]:
        """returns the value of the maximum element of the PQ without removing it
        @return the maximum value of the PQ or None if no element exists
        """
        # Largest element is by definition root of tree, i.e. first element in list
        if self.size != 0:  # make sure there is a root <--> tree is not empty
            return self.heap[0]
        return None

    def remove_max(self) -> int:
        """removes the maximum element from the PQ and returns its value
        @return the value of the removed element or None if no element exists
        """
        self.size -= 1  # since root = 1 element gets removed
        max_value = self.heap.pop(0)  # delete and store max value
        self.heap.insert(0, self.heap[-1])  # copy lowest far right node to the root
        integer_val = self.heap.pop(-1)  # and delete it from lowest far right node
        self.down_heap(0, integer_val)  # 0 is index of max element
        return max_value

    def get_size(self) -> int:
        """returns the number of elements in the PQ
        @return number of elements
        """
        return self.size
