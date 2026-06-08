from typing import Optional, Self

# 4.2 Minimal Tree: Given a sorted (increasing order) array with unique integer elements, create a binary search tree with minimal height

test_cases = [
    [1, 2, 3],
    [1, 4, 5, 8, 9, 10],
    [3, 33, 34, 280, 281, 282, 900, 1000, 2000, 3000],
]


class Node:
    def __init__(
        self,
        value: int,
        left_child: Optional[Self] = None,
        right_child: Optional[Self] = None,
    ):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self) -> str:
        return f"Node {self.value}, left: {self.left_child}, right: {self.right_child}"


def create_minimal_tree(tree_values: Optional[list[int]]) -> Optional[Node]:
    if not tree_values:
        return None

    length = len(tree_values)
    midpoint = length // 2

    left_child = create_minimal_tree(tree_values[:midpoint])
    right_child = create_minimal_tree(tree_values[midpoint + 1 :])

    return Node(tree_values[midpoint], left_child, right_child)


print("Exercise 4.2")
for test_case in test_cases:
    root = create_minimal_tree(test_case)
    print(root)

# 4.4 Check Balanced: Implement a function to check if a binary tree is balanced. For the purposes of this question, a balanced tree is defined to be a tree such that the heights of the two subtrees of any node never differ by more than one.
# Reusing Node from previous question


def balanced_binary_tree(root: Optional[Node]) -> tuple[int, bool]:
    if not root:
        return -1, True

    left_height, left_balanced = balanced_binary_tree(root.left_child)
    if not left_balanced:
        return left_height, left_balanced
    right_height, right_balanced = balanced_binary_tree(root.right_child)
    if not right_balanced:
        return right_height, right_balanced

    balanced = abs(left_height - right_height) < 2
    return 1 + max(left_height, right_height), balanced


# 4.8 First Common Ancestor: Design an algorithm and write code to find the first common ancestor of two nodes in a binary tree. Avoid storing additional nodes in a data structure. This is not necessarily a binary search tree.


def is_node_in_subtree(root: Optional[Node], check_node: Node) -> bool:
    if not root:
        return False
    return (
        root is check_node
        or is_node_in_subtree(root.left_child, check_node)
        or is_node_in_subtree(root.right_child, check_node)
    )


def first_common_ancestor(
    root: Optional[Node], first_node: Node, second_node: Node
) -> Optional[Node]:
    if not root:
        return None
    if root is first_node or root is second_node:
        return root

    first_node_in_left = is_node_in_subtree(root.left_child, first_node)
    second_node_in_left = is_node_in_subtree(root.left_child, second_node)

    if first_node_in_left ^ second_node_in_left:
        return root
    if first_node_in_left:
        return first_common_ancestor(root.left_child, first_node, second_node)
    else:
        return first_common_ancestor(root.right_child, first_node, second_node)
