from typing import Any


class TreeNode:
    def __init__(
            self, key: int, value: Any, right: "TreeNode" = None, left: "TreeNode" = None, parent: "TreeNode" = None
    ):
        """Initialize TreeNode.

        Args:
            key (int): Key used for sorting the node into a BST.
            value (Any): Whatever data the node shall carry.
            right (TreeNode, optional): Node to the right, with a larger key. Defaults to None.
            left (TreeNode, optional): Node to the left, with a lesser key. Defaults to None.
            parent (TreeNode, optional): Parent node. Defaults to None.

        Raises:
            ValueError:
                - When any of the inputs are not of their fields type.
                - When the right/left node do not follow BST properties.
        """
        self.key = key
        self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def __repr__(self) -> str:
        return f"TreeNode({self.key}, {self.value})"

    @property
    def depth(self) -> int:
        """Return depth of the node, i.e. the number of parents/grandparents etc.

        Returns:
            int: Depth of node
        """

        # Essentially the same as in height, but self/node instead of only self._root
        def get_height_recursively(node):
            if node is None:  # external node is reached
                return 0
            # go deeper
            height_left = get_height_recursively(node.left)
            height_right = get_height_recursively(node.right)

            # Check which node's structure is longer
            if height_right > height_left:
                # right is larger
                return height_right + 1  # increment height of subtree
            # left is larger
            return height_left + 1  # increment height of subtree

        # get height of the tree, starting from the root
        # had to set up helper function, since depth only allows for (self)
        # -1 to account for our definition: height(node) = 0; we start counting height at 0
        return get_height_recursively(self) - 1

    @property
    def is_external(self) -> bool:
        """Return if node is an external node."""
        return not self.is_internal

    @property
    def is_internal(self) -> bool:
        """Return if node is an internal node."""
        return bool(self.left or self.right)
