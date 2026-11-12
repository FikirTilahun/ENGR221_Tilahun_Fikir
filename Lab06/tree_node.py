""" TODO Your program header """

from enum import Enum


class TreeNode:
    def __init__(self, name, node_type, data=None):
        self.name = name
        self.node_type = node_type
        self.data = data
        self.parent = None
        self.children = [] # unique list for every node, so that we can have a tree structure with multiple children for each node


    def add_child(self, child) -> None:
        """ TODO Add a docstring here """
        
        self.children.append(child)  # adds child to the parents list of childrne
        child.parent = self # tells child what node is its parent 

    def remove_child(self, child) -> None:
        """ TODO Add a docstring here """
        if child in self.children: # prevents error if list is empty or child is not in the list
            self.children.remove(child)  # removes child from the parents list of children



    def is_leaf(self) -> bool:
        """ TODO Add a docstring here """
        if len(self.children) == 0: # checks if the list of children is empty, meaning the node is a leaf
            return True
        else:
            return False
        


    def depth(self) -> int: # depth follows parent
        """ TODO Add a docstring here """
        depth = 0
        current = self # current node we are on
        while current.parent is not None: # keeps going until we reach the root node, which has no parent
            depth += 1 # increments depth for each level we go up
            current = current.parent # make current node = to its parent so it moves up the tree to the parent node
        return depth


    def height(self) -> int: # height follows children 
        """ TODO Add a docstring here """
        if self.is_leaf(): # if the node is a leaf, its height is 0
            return 0
        max_height = 0 
        for child in self.children: # loop runs for every child in self.children list 
            child_height = child.height() # recursive calls height method
            if child_height > max_height: # update max height 
                max_height = child_height   
        return max_height + 1 # add 1 

    

    def find(self, name):
        """ TODO Add a docstring here """
        if self.name == name: # base case, if our target name is equal to the current name return self
            return self
        for child in self.children: # loops through all children of current node
            result = child.find(name) # recursive call, calls method on target nodes children
            if result is not None: # checks if result exists 
                return result # returns the result if it exists
        return None # if the name is not found 


    
    def print_tree(self, indent=0):
        """ Prints the tree with indentation. """
        print("    " * indent + str(self))

        for child in self.children:
            child.print_tree(indent + 1)


    def __str__(self):
        return self.name
    

    class NodeType(Enum):
        SCHOOL = "School"
        PROGAM = "Program"
        FACULTY = "Faculty"

        @classmethod
        def init_from_str(cls, node_type):
            return cls[node_type.strip().upper()]

if __name__ == "__main__":
    root = TreeNode("Engineering", TreeNode.NodeType.SCHOOL)

    comp_e = TreeNode("CompE", TreeNode.NodeType.PROGAM)
    root.add_child(comp_e)

    ee = TreeNode("EE", TreeNode.NodeType.PROGAM)
    root.add_child(ee)

    kubota = TreeNode("Kubota", TreeNode.NodeType.FACULTY)
    comp_e.add_child(kubota)

    qin = TreeNode("Qin", TreeNode.NodeType.FACULTY)
    comp_e.add_child(qin)

    root.print_tree()