""" TODO
Fikir Tilahun
Logic for the game data and board
"""

import random
from enum import Enum, auto

from cell import Cell
from preferences import Preferences
from search_structure import Queue, Stack

class GameData:
    def __init__(self, ai_type):
        # The current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)] 
                                 for row in range(Preferences.NUM_ROWS)]

        # Whether or not the game is over
        self.gameover = False

        # The current movement mode
        self.current_mode = self.MoveMode.AI_MODE

        # The AI type to run
        self.ai_type = ai_type

        # A list of cells containing food
        self.food = []

        # A list of cells containing the body
        self.body = self.init_player()

        # Number of food eaten
        self.score = 0

    
    ##########################
    # Initialization methods #
    ##########################

    def init_player(self):
        """ Initialize the player cell """

        # Get the top left cell
        player = self.get_cell(0,0)
        # Convert it to the player
        player.become_player()
        # Return a list with the player cell
        return [player]


    ###################################
    # Get information about the board #
    ###################################

    def in_ai_mode(self):
        """ Returns whether or not we are in AI mode """

        return self.current_mode == self.MoveMode.AI_MODE
    
    def get_cell(self, row, col):
        """ Returns the cell at the given row and column """

        if (row >= 0 and row < Preferences.NUM_ROWS) and \
                (col >= 0 and col < Preferences.NUM_COLS):
            return self.board[row][col]
        # Implied else
        raise Exception('get_cell() tried to access cell outside of board: ({}, {})'.format(
            row, col))
    
    def get_player(self):
        """ Returns the head of the body list """

        return self.body[0]
    
    def get_tail(self):
        """ Returns the end of the body list """

        return self.body[-1]
    
    def at_max_food(self) -> bool:
        """ Check whether we can add more food """

        return len(self.food) / Preferences.NUM_CELLS > Preferences.MAX_FOOD


    ###################################
    # Set information about the board #
    ###################################

    def set_game_over(self) -> None:
        """ Turn on the game over flag """

        self.gameover = True

    def set_going_north(self) -> None:
        """ Set the mode to north """

        self.current_mode = self.MoveMode.GOING_NORTH 

    def set_going_south(self) -> None:
        """ Set the mode to south """

        self.current_mode = self.MoveMode.GOING_SOUTH 

    def set_going_east(self) -> None: 
        """ Set the mode to east """

        self.current_mode = self.MoveMode.GOING_EAST 

    def set_going_west(self) -> None:
        """ Set the mode to west """

        self.current_mode = self.MoveMode.GOING_WEST 

    def set_ai_mode(self) -> None:
        """ Set the mode to AI mode """

        self.current_mode = self.MoveMode.AI_MODE


    ##############################
    # Neighbor Retrieval Methods #
    ##############################

    def get_next_cell(self):
        """ Returns the next cell to move to based on the current direction """

        return {
            self.MoveMode.GOING_NORTH : self.get_north_neighbor(self.get_player()),
            self.MoveMode.GOING_SOUTH : self.get_south_neighbor(self.get_player()),
            self.MoveMode.GOING_WEST : self.get_west_neighbor(self.get_player()),
            self.MoveMode.GOING_EAST : self.get_east_neighbor(self.get_player())
        }.get(self.current_mode)
    
    def get_west_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the left of the given cell. 
            If we are at the boundary, return None. """
            
        if cell.get_col() - 1 < 0:
            return None 
        else:
            return self.board[cell.get_row()][cell.get_col()-1]
        
    def get_east_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the right of the given cell.
            If we are at the edge of the map, return None. """
        
        if cell.get_col() + 1 >= Preferences.NUM_COLS:
            return None 
        else:
            return self.board[cell.get_row()][cell.get_col()+1]
    
    def get_north_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately above the given cell.
            If we are at the edge of the map, return None. """
        
        if cell.get_row() - 1 < 0:
            return None 
        else:
            return self.board[cell.get_row()-1][cell.get_col()]
        
    def get_south_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately below the given cell.
            If we are at the edge of the map, return None. """
        
        if cell.get_row() + 1 >= Preferences.NUM_ROWS:
            return None 
        else:
            return self.board[cell.get_row()+1][cell.get_col()]
        
    def get_neighbors(self, center: Cell):
        """ Get all valid neighbors surrounding the center cell.
            Always returns a list in order north, south, east, west """
        
        return list(filter(lambda x: x is not None, 
                [self.get_north_neighbor(center),
                self.get_south_neighbor(center),
                self.get_east_neighbor(center),
                self.get_west_neighbor(center)]))
    
    def get_random_neighbor(self, center: Cell) -> Cell:
        """ Get a random neighbor from the given cell """

        neighbors = self.get_neighbors(center)
        return random.choice(neighbors)


    ###########################
    # Player Movement Methods #
    ###########################

    def move_player(self) -> None:
        """ Move the player to the next step based on the current
            direction or as directed by AI """
        print("Current mode: ", self.current_mode)

        if self.in_ai_mode():
            print("AI is running")
            next_cell = self.get_next_cell_ai()
        else:
            next_cell = self.get_next_cell()
        # Move the snake to the next cell
        self.move_player_to_cell(next_cell)

    def move_player_left(self) -> None:
        """ Move the player one cell to the left if it is empty """

        neighbor = self.get_west_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)
        
    def move_player_right(self) -> None:
        """ Move the player one cell to the right if it is empty """

        neighbor = self.get_east_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_up(self) -> None:
        """ Move the player one cell up if it is empty """

        neighbor = self.get_north_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_down(self) -> None:
        """ Move the player one cell down if it is empty """

        neighbor = self.get_south_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_to_cell(self, cell: Cell) -> None:
        """ Move the player to the given cell """
        
        # If the cell is a body or off the map, game over
        if not cell or cell.is_body():            
            self.set_game_over()
            return
            
        eating = cell.is_food()

    # Change the old head into a body segment
        self.get_player().become_body()

        if eating:
            # Remove the collected duck and increase the score
            self.food.remove(cell)
            self.score += 1

        else:
            # Remove the old tail from the board and body list
            self.get_tail().become_empty()
            self.body.remove(self.get_tail())

        # Add the new head to the beginning of the body list
        cell.become_player()
        self.body.insert(0, cell)


    ########################
    # Food Related Methods #
    ########################

    def add_food(self) -> None:
        """ Adds food to a open spot on the board """

        # Find a row on the board
        row = random.randrange(0, Preferences.NUM_ROWS)
        # Find a col on the board
        col = random.randrange(0, Preferences.NUM_COLS)
        # Get the cell at that location
        cell = self.get_cell(row, col)

        # If it is empty, add food
        if cell.is_empty():
            cell.become_food()
            self.food.append(cell)

    def ate_food(self, food_cell: Cell) -> None:
        """ Eat the food """

        # Change the current head to a body
        self.get_player().become_body()

        # The food becomes the new player
        food_cell.become_player()
        # Add the new cell to the body
        self.body.append(food_cell)
        # Remove the cell from the food list
        self.food.remove(food_cell)

        # Increment the player's score
        self.score += 1

    ##############
    # AI methods #
    ##############

    def get_next_cell_ai(self) -> None:
        """ TODO Add a docstring here """
        
        # Prepare all the tiles to search
        self.reset_cells_for_search()

        # Initialize a structure to hold the tiles to search
        if self.ai_type == "dfs":
            cells_to_search = Stack()
        else:
            cells_to_search = Queue() #cells_to_search represents the search structure, which can be either a stack or a queue

        
        # adding the player cell to Queue() or Stack() depending on the ai_type
        player = self.get_player() # returns the head of the body
        player.set_added_to_search_list() # Marks the player as added to the search list
        cells_to_search.add(player) # Add the player to the search structure, to either stack or queue

        while not cells_to_search.is_empty():  
            current = cells_to_search.remove() # Remove the next cell from the search list(by doing this we explore an already discovred cell)
            print("Exploring:", current.get_row(), current.get_col()) # keeps track of the current cell being explored, used to understand dfs bheavior
            if current.is_food(): # If the current cell is food, we are done
                return self.get_first_cell_in_path(current) # Return the first cell in the path to the food
             
            for neighbor in self.get_neighbors(current): # using get_neighbors() to get all valid neighbors of the current cell  
                if not neighbor.on_search_list(): # checks if the neighbor has already been added to the search list
                    if not neighbor.is_body():# checks if the neighbor is not part of the body
                        neighbor.set_search_parent(current) # records which cell led to this cell, which is used to trace back the path to the food
                        neighbor.set_added_to_search_list() # Mark the neighbor as added to the search list     
                        cells_to_search.add(neighbor) # Add the neighbor to the search structure, to either stack or queue
          

        # if no path found choose random neighbor of the player to move to
        return self.get_random_neighbor(self.get_player())
    
    def get_first_cell_in_path(self, cell) -> Cell: # this method is used to trace back the path from the food cell to the player cell
        player = self.get_player() # get the player cell
        while cell.search_parent != player: # while the parent of the current cell is not the player cell, keep tracing back the path
            cell = cell.search_parent # move to the parent of the current cell
        return cell # return the first cell in the path to the food

    def reset_cells_for_search(self):
        """ Clears all the search info for each cell """
        for row in self.board:
            for cell in row:
                cell.clear_search_info()

    def print_search_path(self):
        """ A helper method for printing the path """

        out = ""
        for row in self.board:
            for cell in row:
                out += "{}\t".format(cell.parent_string())
            out += "\n"
        return out

    def __str__(self):
        """ Format the board to string form for debugging """
        
        out = ""
        for row in self.board:
            for cell in row:
                out += str(cell)
            out += "\n"
        return out

    class MoveMode(Enum):
        GOING_NORTH = auto()
        GOING_SOUTH = auto()
        GOING_EAST = auto()
        GOING_WEST = auto()
        AI_MODE = auto()
