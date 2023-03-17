from treelib import Tree, Node
import numpy as np

def build_tree(root_node):
    # Create an empty tree with the root node as the first node
    tree = Tree()
    tree.create_node(tag=str(root_node.board), identifier=root_node.identifier, data=root_node)

    # Add child nodes recursively
    def add_children(node):
        for child, _ in node.children:
            tree.create_node(tag=str(child.board), identifier=child.identifier, data=child, parent=node.identifier)
            add_children(child)
    add_children(root_node)

    # Define a custom node formatter to display node information
    def node_formatter(node):
        return f"Visits: {node.data.visits} - Score: {node.data.score} - Mean: {(node.data.score / node.data.visits) if node.data.visits != 0 else node.data.score} - Game score: {np.sum(node.data.board.tiles)}"

    # Set the node formatter
    for node in tree.all_nodes():
        node.tag = node_formatter(node)

    # Print the tree
    tree.show()

    return tree
