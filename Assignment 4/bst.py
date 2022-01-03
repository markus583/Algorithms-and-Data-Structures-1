from typing import Any, Generator, Tuple

from tree_node import TreeNode


def get_smallest_recursively(node):
    """
    Helper function to get the smallest key in the tree, starting from a specific node (here: node).
    :param node:
    :return:
    """
    current_node = node
    # Go left as long as left child is not None
    while current_node.left is not None:
        current_node = current_node.left
    return current_node  # and return last node where child is not None


class BinarySearchTree:
    """Binary-Search-Tree implemented for didactic reasons."""

    def __init__(self, root: TreeNode = None):
        """Initialize BinarySearchTree.

        Args:
            root (TreeNode, optional): Root of the BST. Defaults to None.

        Raises:
            ValueError: root is not a TreeNode or not None.
        """
        if root is not None and not isinstance(root, TreeNode):
            raise ValueError("Root is not a TreeNode or not None.")
        self._root = root
        self._size = 0 if root is None else 1

    def insert(self, key: int, value: Any) -> None:
        """Insert a new node into BST.

        Args:
            key (int): Key which is used for placing the value into the tree.
            value (Any): Value to insert.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is already present in the tree.
        """
        if not isinstance(key, int):
            raise ValueError("Key is not an integer!")

        def insert_bst_helper(current_node, value, key):
            """
            Helper function for insert, as defined in the lecture slides
            """
            # Case 1: current node's key < key to insert
            if current_node.key < key:
                if current_node.right:
                    insert_bst_helper(current_node.right, value, key)
                else:
                    current_node.right = TreeNode(value=value, key=key, parent=current_node)
            # Case 2: current node's key > key to insert
            elif current_node.key > key:
                if current_node.left:
                    insert_bst_helper(current_node.left, value, key)
                else:
                    current_node.left = TreeNode(value=value, key=key, parent=current_node)
            # Case 3: current node's key == key to insert
            # This means key is already present in the tree --> not allowed; raise KeyError
            elif current_node.key == key:
                raise KeyError("Key is already present in the tree!")

        self._size += 1
        if self._root is None:  # tree is empty, add node as root
            self._root = TreeNode(key=key, value=value)
        else:  # tree not empty, add node at correct position
            insert_bst_helper(current_node=self._root, value=value, key=key)

    def search_bst_helper(self, current_node, key, n_comparisons=0, compare=False):
        """
        Helper function for find(self, key) and find_comparison
        :param current_node: current node for comparison to key
        :param key: key which we want to find
        :param n_comparisons: how many comparison we have made. Only used for find_comparison.
        :param compare: True or False. If True, n_comparisons is returned, else return current_node.
        :return: depends on compare.
        """
        if key == current_node.key:  # key is found
            n_comparisons += 1  # had to make 1 comparison
            if compare:
                return n_comparisons
            return current_node
        if key < current_node.key:
            if current_node.left:
                n_comparisons += 2  # had to make 2 comparisons
                return self.search_bst_helper(current_node.left, key, n_comparisons=n_comparisons, compare=compare)
            raise KeyError("Key is not present in the tree!")
        if key > current_node.key:
            n_comparisons += 3  # had to make 3 comparisons
            if current_node.right:
                return self.search_bst_helper(current_node.right, key, n_comparisons=n_comparisons, compare=compare)
            raise KeyError("Key is not present in the tree!")

    def find(self, key: int) -> TreeNode:
        """Return node with given key.

        Args:
            key (int): Key of node.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            TreeNode: Node
        """
        # KeyError is raised by search_bst_helper if key is not present in the tree
        if not isinstance(key, int):
            raise ValueError("Key is not an integer!")
        if self._root:  # tree is not empty, do search
            compare = False
            return self.search_bst_helper(self._root, key, compare=compare)
        raise KeyError("There is no root in the tree. Therefore, the key is not present in the tree!")

    @property
    def size(self) -> int:
        """Return number of nodes contained in the tree."""

        def get_size_recursively(node):
            """
            Helper function to get size of the tree. Start with the root.
            """
            if node is None:
                return 0  # next node is not existent, do not increase count
            # increase count: from size of left/right subtree recursively, and current node (1)
            return get_size_recursively(node.left) + 1 + get_size_recursively(node.right)

        return get_size_recursively(self._root)  # Start with root

    # If users instead call `len(tree)`, this makes it return the same as `tree.size`
    # __len__ = self.size
    # For some reason not working for me, so I implemented it again
    def __len__(self) -> int:
        return self.size

    # This is what gets called when you call e.g. `tree[5]`
    def __getitem__(self, key: int) -> Any:
        """Return value of node with given key.

        Args:
            key (int): Key to look for.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.

        Returns:
            Any: [description]
        """
        if not isinstance(key, int):
            raise ValueError("Key is not an integer!")
        # KeyError is handled by find/its helper function
        return self.find(key).value  # given the description, I assume we have to return the value of the dict
        # alternatively, do (or something similar) instead:
        # return self.find(key)
        # return {self.find(key).key: self.find(key).value}

    def transplant(self, node_1, node_2):
        """
        Helper function for remove. node_1 is changing places with node_2.
        :return: None
        """
        if node_1.parent is None:  # node_1 is root
            self._root = node_2
        elif node_1 == node_1.parent.left:  # node_1 is left child
            node_1.parent.left = node_2
        else:  # node_1 is right child
            node_1.parent.right = node_2
        if node_2 is not None:  # change parent relationship
            node_2.parent = node_1.parent

    def remove(self, key: int) -> None:
        """Remove node with given key, maintaining BST-properties.

        Args:
            key (int): Key of node which should be deleted.

        Raises:
            ValueError: If key is not an integer.
            KeyError: If key is not present in the tree.
        """
        if not isinstance(key, int):
            raise ValueError("Key is not an integer!")
        # KeyError is handled by next line
        key_to_remove = self.find(key)  # size always changes only by 1, since there are no duplicate keys
        # CASE 1: node has no child node
        if (not key_to_remove.right) and (not key_to_remove.left):
            parent = key_to_remove.parent
            if key_to_remove.key <= parent.key:
                parent.left = None
            elif key_to_remove.key > parent.key:
                parent.right = None
            self._size -= 1

        # CASE 2: node has only one child; replace it by child node
        # Case 2a: child is on the left to key_to_remove
        elif key_to_remove.left and not key_to_remove.right:
            parent = key_to_remove.parent
            child = key_to_remove.left
            if key_to_remove.key <= parent.key:
                parent.left = child
            elif key_to_remove.key > parent.key:
                parent.right = child
            self._size -= 1

        # Case 2b: child is on the right to key_to_remove
        elif not key_to_remove.left and key_to_remove.right:
            parent = key_to_remove.parent
            child = key_to_remove.right
            if key_to_remove.key <= parent.key:
                parent.left = child
            elif key_to_remove.key > parent.key:
                parent.right = child
            self._size -= 1

        # CASE 3: Node has 2 child node
        elif key_to_remove.left and key_to_remove.right:
            right_child = key_to_remove.right
            next_successor = get_smallest_recursively(right_child)  # get next in-order successor of key_to_remove
            if next_successor.parent != key_to_remove:  # make sure it is not a child of itself
                self.transplant(next_successor, next_successor.right)  # swap them
                next_successor.right = key_to_remove.right  # change links
                next_successor.right.parent = next_successor

            self.transplant(key_to_remove, next_successor)  # swap them
            next_successor.left = key_to_remove.left  # change links
            next_successor.left.parent = next_successor
            self._size -= 1

    # Hint: The following 3 methods can be implemented recursively, and
    # the keyword `yield from` might be extremely useful here:
    # http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-1.html

    # Also, we use a small syntactic sugar here:
    # https://www.pythoninformer.com/python-language/intermediate-python/short-circuit-evaluation/

    def inorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in inorder."""
        node = node or self._root

        # left, root, right
        def inorder_recursively(current_node):
            if current_node:
                yield from inorder_recursively(current_node.left)
                yield current_node
                yield from inorder_recursively(current_node.right)

        # This is needed in the case that there are no nodes.
        if not node:
            return iter(())
        return inorder_recursively(node)

    def preorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in preorder."""
        node = node or self._root

        # root, left, right
        def preorder_recursively(current_node):
            if current_node:
                yield current_node
                yield from preorder_recursively(current_node.left)
                yield from preorder_recursively(current_node.right)

        if not node:
            return iter(())
        return preorder_recursively(node)

    def postorder(self, node: TreeNode = None) -> Generator[TreeNode, None, None]:
        """Yield nodes in postorder."""
        node = node or self._root

        # left, right, root
        def postorder_recursively(current_node):
            if current_node:
                yield from postorder_recursively(current_node.left)
                yield from postorder_recursively(current_node.right)
                yield current_node

        if not node:
            return iter(())
        return postorder_recursively(node)

    # this allows for e.g. `for node in tree`, or `list(tree)`.
    def __iter__(self) -> Generator[TreeNode, None, None]:
        yield from self.preorder()

    @property
    def is_valid(self) -> bool:
        """Return if the tree fulfills BST-criteria."""

        # use min and max values to compare current node to
        def is_valid_recursively(node, minimum, maximum):
            """
            Checks whether a tree is a valid BST recursively.
            :param node: node in a a tree to check
            :param minimum: current minimum value. Must be smaller than node.key.
            :param maximum: current maximum value. Must be larger than node.key.
            :return: True if valid, False otherwise
            """
            # check if correct
            if node.key <= minimum:
                return False
            if node.key >= maximum:
                return False
            good_left = True
            good_right = True
            # check next child nodes recursively, if they exist
            if node.left is not None:
                # with left child as node to check, current minimum value and current node's key
                # it should hold: minimum <= node.left <= node.key
                good_left = is_valid_recursively(node.left, minimum, node.key)
            if node.right is not None:
                # with right node as node to chick, current node's key and current maximum value
                # it should hold: node.key <= node.right <= maximum
                good_right = is_valid_recursively(node.right, node.key, maximum)

            # root has been reached
            if self._root is None:
                return True

            # return True iff both are True
            return good_left and good_right

        # start out with -inf and +inf as comparing (dummy) variables
        return is_valid_recursively(self._root, float("-inf"), float("inf"))

    def return_min_key(self) -> TreeNode:
        """Return the node with the smallest key."""
        node = self._root  # set first node to start with
        return get_smallest_recursively(node)

    def find_comparison(self, key: int) -> Tuple[int, int]:
        """Create an inbuilt python list of BST values in preorder
        and compute the number of comparisons needed for finding the key both in the list and in the BST.

           Return the numbers of comparisons for both, the list and the BST
        """
        python_list = list(node.key for node in self.preorder())  # had to change self._preorder() to self.preorder()
        py_list_comparisons = False  # in case something goes wrong
        for python_counter, list_key in enumerate(python_list, start=1):  # start with 1
            if list_key == key:  # key is found
                py_list_comparisons = python_counter  # store key in dict
                break  # finally, stop loop
        compare = True
        tree_comparisons = self.search_bst_helper(self._root, key, compare=compare)
        return py_list_comparisons, tree_comparisons  # tuple: python list first, then BST

    @property
    def height(self) -> int:
        """Return height of the tree."""

        def get_height_recursively(node):
            """
            Helper function to get the height of a tree
            """
            if node is None:  # external node is reached
                return 0
            # go deeper
            height_left = get_height_recursively(node.left)
            height_right = get_height_recursively(node.right)

            # Check which node's structure is longer
            if height_right > height_left:
                # right is longer
                return height_right + 1  # increment height of subtree
            # left is longer
            return height_left + 1  # increment height of subtree

        # get height of the tree, starting from the root
        # had to set up helper function, since height only allows for (self)
        # -1 to account for our definition: height(root) = 0; we start counting height at 0
        return get_height_recursively(self._root) - 1

    @property
    def is_complete(self) -> bool:
        """Return if the tree is complete."""
        num_needed_nodes = 2 ** (self.height + 1) - 1  # from the definition in the slides
        return bool(self.size == num_needed_nodes)

    def __repr__(self) -> str:
        return f"BinarySearchTree({list(self.inorder())})"
