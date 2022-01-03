from My_ListNode import My_ListNode


class MyDoublyLinkedList:
    """A base class providing a doubly linked storage_list representation."""
    _myList_head = None
    _myList_tail = None
    _myList_size = 0

    def __init__(self, new_head=None, new_tail=None, new_size=0):
        """Create a storage_list and default values are None."""
        self._header = new_head
        self._tail = new_tail
        self._size = new_size

    def _len_(self):
        """Return the number of elements in the storage_list."""
        return self._size

    def list_is_empty(self):
        """Return True if storage_list is empty."""
        return self._size == 0

    def _get_header(self):
        return self._header

    def _get_tail(self):
        return self._tail

    """/*********************************************************
    * EXAMPLE 1
    * The following methods are required for example 1.
    *********************************************************/"""

    def insert_ordered(self, integer_val):

        new_node = My_ListNode(data=integer_val)  # instantiate new node
        if not isinstance(integer_val, int):
            raise ValueError(f"{integer_val} is not an integer!")
        # if storage_list is empty
        if self._header is None:
            self._header = new_node
            self._tail = new_node
            self._size += 1
        # insert at position 0; integer_value is largest element in storage_list
        elif self._header.data < new_node.data:
            new_node._set_next_val(self._header)
            self._header._set_prev_val(new_node)
            self._header = new_node
            self._size += 1
        else:
            # set up values to compare new_node to
            prev = self._header
            cur = self._header._get_next_val()
            while hasattr(cur, "data"):
                if cur.data < new_node.data:
                    # proper position is found
                    # change links
                    prev._set_next_val(new_node)
                    new_node._set_prev_val(prev)
                    new_node._set_next_val(cur)
                    cur._set_prev_val(new_node)
                    self._size += 1
                    return new_node
                # move position, one element to the right
                prev = cur
                cur = cur._get_next_val()
            # in case if integer_val is smallest value
            prev._set_next_val(new_node)
            new_node._set_prev_val(prev)
            self._tail = new_node
            self._size += 1
            return new_node

    def get_integer_value(self, index):
        cur = self._header
        iteration = 0  # counter variable
        while cur is not None:
            if iteration == index:
                return cur.data
            cur = cur._get_next_val()  # move one to the right
            iteration += 1
        # tail is reached, index out of range
        else:
            raise ValueError("Index is out of range!")

    def _remove(self, integer_val, del_all=True):
        # del_all controls whether we only want to delete one occurrence or all of them.
        # By default, (as specified in the assignment, all occurrences of an element are deleted.)

        if not isinstance(integer_val, int):
            raise ValueError(f"{integer_val} is not an integer!")
        if self._len_() == 0:
            return False

        # if integer_val is header
        if self._header.data == integer_val:
            # just move header to the right
            if del_all:
                while hasattr(self._header, "data") and self._header.data == integer_val:
                    # move as long as values are the same
                    self._header = self._header._get_next_val()
                    if self._header is None:
                        self._tail = None
                        self._size -= 1
                        return True
                    self._header._set_prev_val(None)
                    self._size -= 1
            else:
                self._header = self._header._get_next_val()
                self._size -= 1
            return True

        # if integer_val is tail
        elif self._tail.data == integer_val:
            # set value to the right of value to the left of tail to None, then set tail one to the left
            if del_all:
                while self._tail.data == integer_val:  # move as long as values are the same
                    self._tail._get_prev_val()._set_next_val(None)
                    self._tail = self._tail._get_prev_val()
                    self._size -= 1
            else:
                self._tail._get_prev_val()._set_next_val(None)
                self._tail = self._tail._get_prev_val()
                self._size -= 1
            return True

        # if integer_val is somewhere in between
        else:
            prev = self._header
            cur = prev._get_next_val()
            num_of_del_elements = 0
            while cur is not None:
                if cur.data == integer_val:  # occurrence is found
                    prev._set_next_val(cur._get_next_val())  # change links
                    cur._get_next_val()._set_prev_val(prev)
                    self._size -= num_of_del_elements + 1
                    return True
                prev = cur
                cur = cur._get_next_val()
                if cur is None:  # if cur is exhausted
                    return False
                if del_all:
                    while cur.data == integer_val:  # move as long as values are the same
                        if cur._get_next_val().data != integer_val:
                            break
                        cur = cur._get_next_val()  # final occurrence is found
                        num_of_del_elements += 1
            return False

    def remove_duplicates(self):
        if self._header is None:  # cannot remove duplicates; storage_list is empty
            return None

        cur = self._header
        while cur is not None:
            index = cur._get_next_val()
            while index is not None:
                if cur.data == index.data:  # duplicate found
                    index._get_prev_val()._set_next_val(index._get_next_val())  # change links
                    self._size -= 1
                    if index._get_next_val() is not None:  # check if duplicate is tail
                        index._get_next_val()._set_prev_val(index._get_prev_val())  # change links
                index = index._get_next_val()  # move index
            cur = cur._get_next_val()  # move index

    def reorder_list(self):
        from My_ListNode import My_ListNode

        main = self._header
        even_counter = 0
        uneven_counter = 0
        max_even = None
        while self._size > (even_counter + uneven_counter):  # stop if every element has been considered
            if main.data % 2 == 0:  # check if even
                # set up new, even node
                tmp = My_ListNode(data=main.data, next=main._get_next_val(), prev=main._get_prev_val())
                # tmp is same as header
                if tmp.data == self._header.data:
                    self._header = self._header._get_next_val()  # just move header one the right
                    max_even = tmp.data  # store value of maximum even value
                else:
                    tmp._get_prev_val()._set_next_val(tmp._get_next_val())  # skip tmp in links
                if max_even < tmp.data:
                    max_even = tmp.data  # store value of maximum even value
                if tmp._get_next_val() is not None:  # check if tmp is tail
                    tmp._get_next_val()._set_prev_val(tmp._get_prev_val())  # skip tmp in other link
                self._tail._set_next_val(tmp)  # change tail to tmp
                tmp._set_prev_val(self._tail)  # make link from old tail to tail/new tail
                tmp._set_next_val(None)
                self._tail = tmp  # set new tail
                even_counter += 1
            else:
                uneven_counter += 1
            main = main._get_next_val()

        # set up things to get proper return value: index of greatest even number; if only odd numbers there, return -1
        if max_even is None:  # no even value found
            return -1
        even_index = 0  # set up counter variable
        cur = self._header
        while cur is not None:
            if cur.data == max_even:  # max even value is found
                return even_index
            even_index += 1  # move index to the right
            cur = cur._get_next_val()  # move to the right
        else:
            return -1
