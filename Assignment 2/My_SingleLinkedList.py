class Node:
    """
    A simple representation of a node for a singly linked list.
    Contains only node itself and reference to the next value.
    """

    def __init__(self, data):
        self.data = data
        self.next_val = None


class MySingleLinkedList:
    """A base class providing a single linked list representation."""

    _myList_head = None
    _myList_tail = None

    def __init__(self, new_head=None, new_tail=None):
        """Create a list and default values are None."""
        self._header = new_head
        self._tail = new_tail

    def _get_header(self):
        return self._header

    def _get_tail(self):
        return self._tail

    """/*********************************************************
    * EXAMPLE 2
    * The following methods are required for example 2.
    *********************************************************/"""

    def prepend(self, integer_val):
        new_node = Node(integer_val)  # create new node from class
        if self._header is None:  # if list is empty, also change tail
            self._tail = new_node
        new_node.next_val = self._header
        self._header = new_node  # set header to new node, thereby insert it at the start
