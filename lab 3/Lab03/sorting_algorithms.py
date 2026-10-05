""" TODO
Author: Your name here!
Add a description here!
"""

import random
import time

from preferences import Preferences

class SortingAlgorithms:
    def __init__(self):
        # The algorithm to sort
        self.array = []

        # Any indices to highlight
        self.inner_idx = -1
        self.outer_idx = -1 

        # A string representing the current sorting algorithm
        self.current_alg = None

        # Store the method of the sorting algorithm being run
        self.alg_method = None
    
    def create_new_array(self, length=Preferences.NUM_ELEMENTS) -> list:
        """ Create a new array to sort """
        return [random.randint(0, Preferences.MAX_VAL) 
                      for _ in range(length)]
    
    def get_next_step(self) -> None:
        """ Updates the value of self.selected_idx whenever we reach 
            a "yield" statement in any of the below sorting algorithms. """
        
        try:
            # Treats the current sorting algorithm as an iterator
            # and sets self.selected_idx to be the next "element"
            self.outer_idx, self.inner_idx = next(self.alg_method)
        # Clear the selected_idx value when we reach the end of the method
        except StopIteration:
            self.outer_idx, self.inner_idx = -1, -1

    def restart(self, new_alg, length=Preferences.NUM_ELEMENTS) -> None:
        """ Restart the sorting process with the new algorithm. 
            Creates a new array to sort. """
        
        self.current_alg = new_alg
        self.alg_method = {
            "selection" : self.selection_sort,
            "insertion" : self.insertion_sort,
            "bubble" : self.bubble_sort
        }[self.current_alg]()
        self.array = self.create_new_array(length)
        self.outer_idx, self.inner_idx = -1, -1

    def selection_sort(self):
        """ An implementation of the Selection sorth algorithm. 
            A generator function which creates an iterator that 
            iterates through each "yielded" value. """
        
        # TODO What selection sort does is it finds the minimum value in the unsorted portion of the array and swaps it with the first unsorted element. It repeats this process for each position in the array until the entire array is sorted.
                
        n = len(self.array)

        for i in range(n):
            yield -1, i
            min_idx = i

            for j in range(i + 1, n):
                yield min_idx, j

                if self.array[j] < self.array[min_idx]:
                    min_idx = j 
            
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            yield i, min_idx
                

    def insertion_sort(self):
        """ TODO sort self.array using insertion sort """
        for i in range(1, len(self.array)):
            j = i
            yield -1, j 

            while j > 0 and self.array[j-1] > self.array[j]:
                yield j-1, j
                self.array[j], self.array[j-1] = self.array[j-1], self.array[j]
                j -= 1
                yield j, j+1

    def bubble_sort(self):
        n = len(self.array)

        for i in range(n - 1):
            
            for j in range(n - 1 - i):
                yield i, j 

                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    yield i, j + 1

    def get_runtime(self) -> float:
        """ Returns the length of time (in seconds) that it took for 
            the function_to_run to sort a list of length list_length """

        # Get the time before running
        start_time = time.time()
        # Sort the given list
        for _ in self.alg_method:
            pass
        # Get the time after running
        end_time = time.time()
        # Return the difference
        return end_time - start_time

if __name__ == "__main__":
    s = SortingAlgorithms()
    s.restart("bubble", 10000)
    print(s.get_runtime())