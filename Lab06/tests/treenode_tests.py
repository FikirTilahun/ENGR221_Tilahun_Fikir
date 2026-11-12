import pytest

import os, sys 

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tree_node import TreeNode

@pytest.fixture 
# Define a single TreeNode for testing
def oneNode():
    return TreeNode("Hello world", TreeNode.NodeType.FACULTY)

@pytest.fixture 
# Define a small tree for testing
# Should look like
#          "Engineering"
#           /       \
#       "CompE"    "EE"
#       /     \
#  "Kubota"  "Qin"
# Or when printed:
# Engineering
#     CompE
#         Kubota
#         Qin
#     EE
def tree():
    root = TreeNode("Engineering", TreeNode.NodeType.SCHOOL)

    comp_e = TreeNode("CompE", TreeNode.NodeType.PROGAM)
    root.add_child(comp_e)

    ee = TreeNode("EE", TreeNode.NodeType.PROGAM)
    root.add_child(ee)

    kubota = TreeNode("Kubota", TreeNode.NodeType.FACULTY)
    comp_e.add_child(kubota)

    qin = TreeNode("Qin", TreeNode.NodeType.FACULTY)
    comp_e.add_child(qin)
    
    return root

####
# add_child
####

@pytest.mark.add_child
# add_child functionality for a TreeNode
def test_add_child(oneNode, capfd):
    # Insert a new faculty
    claussen = TreeNode("Claussen", TreeNode.NodeType.FACULTY)
    oneNode.add_child(claussen)
    # Print the tree
    oneNode.print_tree()
    # Capture the output
    out, _ = capfd.readouterr()
    # Confirm that the output has Claussen added
    assert out == "Hello world\n    Claussen\n"


@pytest.mark.add_child
# add_child functionality for a TreeNode
def test_add_child_tree(tree, capfd):
    # Insert a new faculty to the EE node
    claussen = TreeNode("Claussen", TreeNode.NodeType.FACULTY)
    tree.children[1].add_child(claussen)
    # Print the tree
    tree.print_tree()
    # Capture the output
    out, _ = capfd.readouterr()
    # Confirm that the output has Claussen added
    assert out == "Engineering\n    CompE\n        Kubota\n        Qin\n" + \
                  "    EE\n        Claussen\n"

####
# remove_child
####

@pytest.mark.remove_child
# remove_child functionality for TreeNode
def test_remove_child_notpresent(oneNode):
    claussen = TreeNode("Claussen", TreeNode.NodeType.FACULTY)
    oneNode.remove_child(claussen)
    # No children, so should be an empty list
    assert oneNode.children == []

@pytest.mark.remove_child
# remove_child functionality for TreeNode
def test_remove_child_present(tree, capfd):
    child = tree.children[1]
    tree.remove_child(child)
    # Print the tree
    tree.print_tree()
    # Capture the output
    out, _ = capfd.readouterr()
    # Confirm that the output has the EE child removed
    assert out == "Engineering\n    CompE\n        Kubota\n        Qin\n"

####
# is_leaf
####

@pytest.mark.is_leaf
# is_leaf functionality for a TreeNode
def test_is_leaf_true(oneNode):
    # Should return true
    assert oneNode.is_leaf()

@pytest.mark.is_leaf
# is_leaf functionality for a TreeNode
def test_is_leaf_false(tree):
    # Should return false
    assert not tree.is_leaf()

####
# depth
####

@pytest.mark.depth
# depth functionality for a TreeNode
def test_depth_root(oneNode):
    # Should return 0
    assert oneNode.depth() == 0

@pytest.mark.depth
# depth functionality for a TreeNode
def test_depth_tree_root(tree):
    # Should return 0
    assert tree.depth() == 0

@pytest.mark.depth
# depth functionality for a TreeNode
def test_depth_tree_leaf(tree):
    leaf = tree.children[0].children[0]
    # Should return 2
    assert leaf.depth() == 2

####
# height
####

@pytest.mark.height
# height functionality for a TreeNode
def test_height_root(oneNode):
    # Should return 0
    assert oneNode.height() == 0

@pytest.mark.height
# height functionality for a TreeNode
def test_height_tree_root(tree):
    # Should return 2
    assert tree.height() == 2

@pytest.mark.height
# height functionality for a TreeNode
def test_height_tree_leaf(tree):
    leaf = tree.children[0].children[0]
    # Should return 0
    assert leaf.height() == 0

####
# find
####

@pytest.mark.find
# find functionality for a TreeNode
def test_find_present(oneNode):
    node = oneNode.find("Hello world")
    assert node == oneNode

@pytest.mark.find
# find functionality for a TreeNode
def test_find_absent(oneNode):
    node = oneNode.find("Engineering")
    assert node is None

@pytest.mark.find
# find functionality for a TreeNode
def test_find_tree_present(tree):
    node = tree.find("Kubota")
    assert node is tree.children[0].children[0]

@pytest.mark.find
# find functionality for a TreeNode
def test_find_tree_absent(tree):
    node = tree.find("Ghose")
    assert node is None