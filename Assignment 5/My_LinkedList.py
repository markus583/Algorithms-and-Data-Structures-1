from typing import Union

from My_ListNode import MyListNode


class MyLinkedList:
    """A base class providing a single linked storage_list representation."""

    # Do not modify this code section please!
    def __init__(self, new_head: Union[None, "MyListNode"] = None, new_tail: Union[None, "MyListNode"] = None):
        """Create a storage_list and default values are None."""
        self._header = new_head
        self._tail = new_tail

    def _get_header(self) -> Union[None, "MyListNode"]:
        return self._header

    def _get_tail(self) -> Union[None, "MyListNode"]:
        return self._tail

    def get_size(self) -> int:
        """
        returns the number of nodes in the linked storage_list
        """
        current = self._header  # start with header
        counter = 0  # initialize counter
        while current is not None:  # go through all items
            counter += 1
            current = current.get_next_node()  # go to next
        return counter

    def insert_ordered(self, integer_val: int) -> None:
        """Add the element `integer_val` to the storage_list, keeping the storage_list in descending order.

        Args:
            integer_val (int): Integer value to be added.

        Raises:
            ValueError: If integer_val is not an integer.
        """
        if not isinstance(integer_val, int):
            raise ValueError(f"{integer_val} is not an integer!")

        # List is empty, set new header
        if self._header is None:
            self._header = MyListNode(data=integer_val)
            self._tail = MyListNode(data=integer_val)
        # integer_value > header: set new header
        elif integer_val > self._header.get_data():
            old_header = self._get_header()  # save old header
            self._header = MyListNode(data=integer_val)  # insert new header
            self._header.set_next_node(old_header)  # set old header after new header; all other stay the same
        # insert at any other place
        else:
            current = self._header
            while current.get_data() > integer_val:  # get position of where to insert integer_val
                if current.get_next_node() is not None:  # in case next is tail
                    previous = current
                    current = current.get_next_node()
                else:
                    break  # done
            if current.get_data() < integer_val:
                next_node = previous.get_next_node()
                previous.set_next_node(MyListNode(data=integer_val))
                previous.get_next_node().set_next_node(next_node)
            else:
                next_node = current.get_next_node()
                current.set_next_node(MyListNode(data=integer_val))
                current.get_next_node().set_next_node(next_node)
                if current.get_next_node().get_next_node() is None:  # set new tail
                    self._tail = current.get_next_node()

    def clear(self) -> None:
        """release the memory allocated for the storage_list"""
        # just set all none
        self._header = None  # works due to garbage collection in Python!
        self._tail = None

    def remove_first(self) -> int:
        """removes the first node from the linked storage_list and returns its value
        @return the value of the node that has been removed
        """
        first_node = self._header.get_data()  # store value of header
        if self._header.get_next_node() is not None:  # make sure len(storage_list) > 1
            self._header = self._header.get_next_node()  # move header 1 to the right
        else:  # len(storage_list) == 1 --> just remove header
            self._header = None
            self._tail = None
        return first_node

    def get_first(self) -> int:
        """returns the value of the first node in the linked storage_list (without removing it)
        @return the value of the first node
        """
        return self._header.get_data()

    def contains(self, integer_val: int) -> bool:
        """returns true if integer_val is in the linked storage_list; false otherwise
        @return True or False
        @raises ValueError if integer_val is None
        """
        if integer_val is None:
            raise ValueError(f"{integer_val} is not an integer!")
        # only raising the above (as specified) seems unlogical to me
        # so I also implemented the same as in insert_ordered again
        if not isinstance(integer_val, int):
            raise ValueError(f"{integer_val} is not an integer!")
        current = self._header
        while current is not None:  # go through all nodes in storage_list
            if current.get_data() == integer_val:  # found value!
                return True
            current = current.get_next_node()  # not found; get next one
        return False  # never found

    def to_list(self):
        """returns a python storage_list representation of the linked storage_list starting from _header
        @return a python storage_list
        """
        list_list = []  # set up empty storage_list
        current = self._header  # start with header
        while current is not None:  # go through all nodes in storage_list
            list_list.append(current.get_data())  # add value to storage_list
            current = current.get_next_node()  # go to next item in storage_list
        return list_list

    def to_string(self):
        """returns a comma-delimited string representation of the linked storage_list:
        "[20]-> [8]-> [5]-> [1]"
        @return a string: "20,8,5,1"
        """
        list_string = ""  # set up empty string
        current = self._header  # start with header
        while current is not None:  # go through all nodes in storage_list
            list_string += str(current.get_data())  # add value to string
            list_string += ","  # add , to string
            current = current.get_next_node()  # go to next item in storage_list
        return list_string
