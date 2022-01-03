from math import floor, inf


def parent(index):
    return (index - 1) // 2


def left_child(index):
    return 2 * index + 1


def right_child(index):
    return 2 * index + 2


class MaxHeap:
    def __init__(self, storage_list):
        """
        @param storage_list from which the heap should be created
        @raises ValueError if sort_list is None.
        Creates a bottom-up maxheap in place.
        """
        self.heap = None
        self.size = 0
        if storage_list is None:
            raise ValueError

        n = len(storage_list)
        self.size = n  # store length
        # use trick: store very large value at beginning of storage_list to make life easier in bottom-up construction
        storage_list.insert(0, inf)
        # store copy of array
        self.array = storage_list

        # create heap in-place, bottom-up
        for i in range(floor(n // 2), 0, -1):
            k = i
            v = self.array[k]
            heap = False
            while not heap and 2 * k <= n:
                j = 2 * k
                if j < n:
                    if self.array[j] < self.array[j + 1]:
                        j = j + 1
                if v >= self.array[j]:
                    heap = True
                else:
                    self.array[k] = self.array[j]
                    k = j
            self.array[k] = v

        del self.array[0]  # now, delete large value at start of storage_list - no more needed
        self.heap = self.array  # store heap as storage_list in self.heap

    # re-use function from assignment 5, but with slight corrections
    # set up some helper functions as suggested in the assignment sheet
    def swap(self, index1, index2):
        """
        Function that swaps the position of 2 elements.
        """
        self.heap[index1], self.heap[index2] = (self.heap[index2], self.heap[index1])

    def down_heap(self, index, integer_val, max_index=inf):
        # get children
        left = left_child(index)
        right = right_child(index)
        # initialize largest --> current root
        largest = index
        if left < self.size:  # to take care of bounds
            if self.heap[left] > self.heap[largest]:  # left child is larger than current root
                largest = left
        if right < self.size:  # to take care of bounds
            if self.heap[right] > self.heap[largest]:  # right child is larger than current root AND left child
                largest = right

        if self.heap[largest] != integer_val:  # check if violation: one child > parent
            if largest <= max_index:
                self.swap(index, largest)  # swap larger child and parent
                # down heap recursively with same stopping criterion
                # max_index specifies how deep we are allowed to go
                self.down_heap(largest, integer_val=integer_val, max_index=max_index)

    def get_heap(self):
        # helper function for testing, do not change
        return self.heap

    def get_size(self):
        """
        @return size of the max heap
        """
        return self.size

    def contains(self, val):
        """
        @param val to check if it is contained in the max heap
        @return True if val is contained in the heap else False
        @raises ValueError if val is None.
        Tests if an item (val) is contained in the heap. Do not search the entire array sequentially,
        but use the properties of a heap
        """
        if val is None:
            raise ValueError

        def search_helper(index, val):
            if self.heap[index] == val:
                return True  # value found!
            # get children of current index
            left = left_child(index)
            right = right_child(index)

            if left < self.size:  # to take care of bounds
                if self.heap[left] >= val:  # go deeper
                    var = search_helper(left, val)
                    if var:  # value found
                        return True
            else:
                return False  # not found
            if right < self.size:  # to take care of bounds
                if self.heap[right] >= val:  # go deeper
                    var = search_helper(right, val)
                    if var:  # value found
                        return True
                return False  # not found
            var = False  # not found
            return var

        return search_helper(0, val)

    def is_empty(self):
        """
        @return True if the heap is empty, False otherwise
        """
        return bool(self.size != 0)

    def remove_max(self, endpoint=None):
        """
        Removes and returns the maximum element of the heap
        @return maximum element of the heap or None if heap is empty
        """
        if endpoint is None:
            # no endpoint given; consider entire heap
            endpoint = self.get_size()
        if self.is_empty():
            return None
        self.size -= 1  # since root = 1 element gets removed
        max_value = self.heap.pop(0)  # delete and store max value
        if self.size == 0:  # in case only 1 element was left
            return max_value
        self.heap.insert(0, self.heap[endpoint - 2])  # copy lowest far right node to the root
        integer_val = self.heap.pop(endpoint - 1)  # and delete it from lowest far right node
        self.down_heap(0, integer_val, max_index=endpoint - 2)  # 0 is index of max element
        return max_value

    def sort(self):
        """
        This method sorts (ascending) the storage_list in-place using HeapSort, e.g. [1,3,5,7,8,9]
        """
        n = self.get_size()  # get initial size
        m = n  # set up counter variable for position to insert removed max element
        # m is also used to specify the number of unsorted elements
        for _ in range(n):
            current_max = self.remove_max(m)  # remove max, but only compare elements in heap up to index m
            m -= 1  # change insertion place
            self.heap.insert(m, current_max)
        return self.heap
