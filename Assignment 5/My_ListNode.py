from typing import Union


class MyListNode:
    def __init__(self, data: int, next_node: Union[None, "MyListNode"] = None):
        self._data = data
        self._next_node = next_node

    def get_data(self) -> int:
        return self._data

    def set_data(self, new_data: int) -> None:
        self._data = new_data

    def get_next_node(self) -> Union[None, "MyListNode"]:
        return self._next_node

    def set_next_node(self, _node: Union[None, "MyListNode"]) -> None:
        self._next_node = _node
