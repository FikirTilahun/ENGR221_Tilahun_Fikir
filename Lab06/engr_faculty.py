""" TODO Your program header """

import pandas as pd

from professor import Professor
from faculty_visualizer import FacultyVisualizer
from tree_node import TreeNode
from preferences import Preferences

class ENGR_Faculty:
    def __init__(self):
        
        # Dictionary containing the faculty nodes
        # Keys are last names, values are Professors
        self.faculty_dict = self.import_faculty()

        # Tree representing the Engineering faculty
        self.program_structure = self.build_structure()

        # Visualize the faculty tree
        self.visualizer = FacultyVisualizer(
            self.program_structure, self.faculty_dict)

        
    def import_faculty(self): # reads excel file and adds faculty to dictionary
        """ Reads the Excel file containing the faculty member information
            and adds them to the faculty dictionary """
        
        # The dictionary to store the faculty
        faculty_dict = {}

        # Read the Excel file into a pandas data frame
        df = pd.read_excel(Preferences.FACULTY_FILE)
        print(df.columns.tolist())

        # Add each row of the data frame (professor) to the dictionary
        df.apply((lambda x: self.add_prof(x, faculty_dict)), axis=1)
        #df.apply() tells panda to apply function to DF 
        # axis=1 tells panda to process one row at a time then.. 
        # ((lambda x:....)) takes the current row (x) and pass arguments to add_prof()
        # then add_prof() creates professor object, adds to dictionary, last name is key, professor object is value
        return faculty_dict


    def add_prof(self, prof, faculty_dict) -> None: # reads a row of the data frame and adds it to the dictionary
        """ TODO Add a docstring here """
        # Create a Professor object from the row of the data frame(the professors information)
        professor = Professor(*prof) 

        # Add the professor to the dictionary, where the key-value pair is made
        # key = last name, value = professor object
        faculty_dict[professor.last_name] = professor



    def build_structure(self) -> TreeNode: # builds faculty tree structure, returns root node
        """ TODO Add a docstring here """

        # We are all under the School of Engineering
        root = TreeNode("School of Engineering", TreeNode.NodeType.SCHOOL) # creates root for the tree
        # "school or engr"= name of node, TreeNode.NodeType.SCHOOL = type of node, 

        # Create a node for each SoE program 
        for program in Professor.Program: # # loops through all the programs in the Program enum(reps all programs)
            program_node = TreeNode(program.value, TreeNode.NodeType.PROGAM) # creates new node for each program
            root.add_child(program_node) # adds new node to root node, root is parent, new node is child

            for last_name in self.faculty_dict: # loops through all last names in faculty dict
                professor = self.faculty_dict[last_name] # using last name as key, gets professor object from faculty dict

                if professor.program == program: # checks if the professors program is equal to the current program in the loop
                    # Create a node for the professor and add it to the program node
                    professor_node = TreeNode(professor.last_name, TreeNode.NodeType.FACULTY, professor)
                    program_node.add_child(professor_node) # adds new node, program is parent, professor is child

        return root


    def visualize_faculty(self):
        """ Build and show the tree visualizing the faculty """
        self.visualizer.run()
        

if __name__ == '__main__':
    f = ENGR_Faculty()
    f.visualize_faculty()