#Koch Snowflake
#Fikir Tilahun ENGR 221 Lab 05
import turtle
import time 
from memory_profiler import memory_usage

class KochSnowflake:
    def __init__(self, init_length=500, init_depth=3):
        # Initialize the turtle
        self.t = None  

        # Length of one edge at 0 depth
        self.init_length = init_length  
        # Number of "layers" to draw
        self.init_depth = init_depth    
    

    def init_turtle(self):
        """ Initialize the turtle and move it to the 
            appropriate location on the screen """
        
        t = turtle.Turtle() # Initialize the turtle
        t.speed(8) # Increase the turtle's speed
        # Move the turtle to the upper left corner
        t.teleport(-200,-200)
        self.t = t


    ######################
    # Draw curve methods #
    ######################

    def draw_curve_recursive(self):
        """ The 'entry point' into the recursive curve method """
        self.draw_curve_recursive_helper(self.init_length, self.init_depth)


    def draw_curve_recursive_helper(self, length, depth):
        """ TODO docstring """

        # Raise an error if depth is negative
        if depth < 0:
            raise "Depth cannot be negative"

        # Base case
        elif depth == 0:
            self.t.forward(length)

        # Recursive case, 
        else:
            self.draw_curve_recursive_helper(length/3, depth-1)# draws segment 
            self.t.left(60) #changes direction of turtle. 
            self.draw_curve_recursive_helper(length/3, depth-1)
            self.t.right(120)# turn 120 degrees to face downwards creates tip of the triangle
            self.draw_curve_recursive_helper(length/3, depth-1)
            self.t.left(60)
            self.draw_curve_recursive_helper(length/3, depth-1)


    def draw_curve_stack(self):
        """ TODO docstring """
        
        commands = [("add_curve", self.init_length, self.init_depth)]# creates the stack/list of commands to be executed. 

        while commands: # keep looping as long as there are commands in the stack
            command = commands.pop()# removes the last element/command of the list and returns it.
            action = command[0] # retrieves first element, tells what type of command we process, add curve or turn left?
            if action == "add_curve": # if add_curve command is found, we need to check if we are at the base case or not.
                length = command[1] # retrives second element of the command, which is the length of the segment to draw
                depth = command[2] # retrieves third element of the command, which is the depth of the curve to draw
                if depth == 0:
                    self.t.forward(length)
                else: # 3 angle changes + 4 segments = 7 commands to add to the stack
                    # Last in first out, so we add the commands in reverse order of how we want them executed
                    commands.append(("add_curve", length/3, depth-1))# adds the first segment of the curve to the stack
                    commands.append(("turn_left", 60))# adds first turn to the stack
                    commands.append(("add_curve", length/3, depth-1))# 
                    commands.append(("turn_right", 120))
                    commands.append(("add_curve", length/3, depth-1))
                    commands.append(("turn_left", 60))
                    commands.append(("add_curve", length/3, depth-1)) 
            elif action == "turn_left": # these handle turning commands depending on left or right. 
                self.t.left(command[1]) 
            elif action == "turn_right":
                self.t.right(command[1]) 
# keeps going until stack is empty, meaning one side of the snowflake has been drawn.

    ##########################
    # Draw snowflake methods #
    ##########################

    def draw_snowflake_recursive(self):
        """ Draw the three edges of the Koch snowflake using the 
            recursive curve method """

        self.init_turtle()

        for _ in range(3):
            self.draw_curve_recursive()
            self.t.left(120)
            
        turtle.clearscreen()


    def draw_snowflake_stack(self):
        """ Draw the three edges of the Koch snowflake using the 
            non-recursive curve method """

        self.init_turtle()

        for _ in range(3):
            self.draw_curve_stack()
            self.t.left(120)

        turtle.clearscreen()


    #########################@#
    # Compare the approaches! #
    ##########################@

    def compare_snowflake(self):
        """ Compare how much time and memory the recursive and non-recursive 
            implementations of drawing the Koch Snowflake used """
        
        rec_time, rec_mem = self.get_time_and_mem(self.draw_snowflake_recursive)
        nonrec_time, nonrec_mem = self.get_time_and_mem(self.draw_snowflake_stack)

        print(f"Recursive memory usage: {rec_mem} MB")
        print(f"Non-recursive memory usage: {nonrec_mem} MB")
        print()
        print(f"Recursive time taken: {rec_time:.5f} s")
        print(f"Non-recursive time taken: {nonrec_time:.5f} s")
        

    def get_time_and_mem(self, func):
        """ Find the time and memory used by the given function """

        # Start the timer
        time_start = time.perf_counter()
        # Run the function and find the memory used
        mem_usage = memory_usage((func, ), include_children=True, multiprocess=True)
        # End the timer
        time_end = time.perf_counter()

        # Find the total time taken
        time_taken = time_end - time_start 
        # Find the total memory used
        mem_used = max(mem_usage) - min(mem_usage)

        return time_taken, mem_used


if __name__ == "__main__":
    s = KochSnowflake(500, 2)
    s.compare_snowflake()

