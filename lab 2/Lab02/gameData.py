""" TODO
Author: Fikir Tilahun
Survival in the frozen tundra
"""

import random

from cell import Cell
from preferences import Preferences

class GameData:
    def __init__(self):
        # The current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)] 
                                      for row in range(Preferences.NUM_ROWS)]
        
        # Whether or not the game is over
        self.gameover = False

        # The current cell containing the player
        self.player = self.board[4][4]    # I changed the starting position to be in the middle of the board
        self.player.become_player()

        # The number of empty cells on the board, accounting for the player cell
        self.num_empty_cells = Preferences.NUM_CELLS - 1

        # A list of cells containing food
        self.food = []
        # Number of food eaten
        self.score = 0

        # A list of cells containing enemies
        self.enemies = []


    #######################
    # Game Limits Methods #
    #######################

    def at_max_food(self) -> bool:
        """ Check whether we can add more food """
        return len(self.food) / self.num_empty_cells > Preferences.MAX_FOOD
    
    def at_max_enemies(self) -> bool:
        """ Check whether we can add more enemies """
        return len(self.enemies) / self.num_empty_cells > Preferences.MAX_ENEMIES

    def set_game_over(self) -> None:
        """ Turn on the game over flag """
        self.gameover = True


    ##############################
    # Neighbor Retrieval Methods #
    ##############################

    def get_west_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the left of the given cell. 
            If we are at the  edge of the map, return None. """
        # TODO 
        # //Pesudocode: Idea: one coordinate changes for each move, For west: If the cell is in column 0: return none, otherwise: return cell from the same row and one column to the left 
        if cell.get_col() == 0:
            return None
        return self.board[cell.get_row()][cell.get_col() - 1]
    def get_east_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately to the right of the given cell.
            If we are at the edge of the map, return None. """
        # TODO 
        # //If cell is in the last column return none, otherwise return the cell from same row and one column to the right 
        if cell.get_col() == Preferences.NUM_COLS - 1:
            return None
        return self.board[cell.get_row()][cell.get_col() + 1]
    def get_north_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately above the given cell.
            If we are at the edge of the map, return None. """
        # TODO
        # // For north and south we adjust the row coordinates, for north: if the cell is in row 0 return none, otherwise return cell one row above in the same column
        if cell.get_row() == 0:
            return None
        return self.board[cell.get_row() - 1][cell.get_col()]        
    def get_south_neighbor(self, cell: Cell) -> Cell:
        """ Returns the cell immediately below the given cell.
            If we are at the edge of the map, return None. """
        # TODO
        # // For south if cell is in the last row return none, otherwise return cell from one row below in same column
        if cell.get_row() == Preferences.NUM_ROWS - 1:
            return None
        return self.board[cell.get_row() + 1][cell.get_col()]

    ###########################
    # Player Movement Methods #
    ###########################
        
    def move_player_right(self) -> None:
        """ Move the player one cell to the right if it is empty """
        # TODO // Moving east, get the east of the current cell, if it exists then move player if not do nothing
        neighbor = self.get_east_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)
    def move_player_left(self) -> None:
        """ Move the player one cell to the left if it is empty """
        # TODO// Moving west get the west of the current cell, if it exists move if not do nothng
        neighbor = self.get_west_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)
    def move_player_up(self) -> None:
        """ Move the player one cell up if it is empty """
        # TODO// moving up get the north of the current cell, if exists move up if not do nothing
        neighbor = self.get_north_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)
    def move_player_down(self) -> None:
        """ Move the player one cell down if it is empty """
        # TODO// moving down get south of the current cell, if exists move down if not do nothing
        neighbor = self.get_south_neighbor(self.player)
        if neighbor is not None:
            self.move_player_to_cell(neighbor)
    def move_player_to_cell(self, cell: Cell) -> None:
        """ Move the player to the given cell """

        # If there is food in this cell, eat it
        if cell.is_food():
            self.eat_food(cell)
            self.update_player_cell(cell)
        # If there is an enemy in this cell, game over!
        elif cell.is_enemy():
            self.player.become_empty()
            self.set_game_over()
        # Otherwise, update the player location
        else:
            self.update_player_cell(cell)

    def update_player_cell(self, new_cell: Cell) -> None:
        """ Move the player to the new cell """
    
        # Empty the cell the player just moved away from
        self.player.become_empty()
        # Update the player to the new cell
        self.player = new_cell
        # Change the new cell to be the player type
        self.player.become_player()


    ########################
    # Food Related Methods #
    ########################

    def add_food(self) -> None:
        """ Adds food to a random open spot on the board """

        # Find a row on the board
        row = random.randrange(0, Preferences.NUM_ROWS)
        # Find a col on the board
        col = random.randrange(0, Preferences.NUM_COLS)

        # TODO // after retriving the random row/col, check if cell is empty and add food, add cell to food list decrease number of empty cells by one, otherwise do nothing
        cell = self.board[row][col]
        if cell.is_empty():
            cell.become_food()
            self.food.append(cell)
            self.num_empty_cells -= 1
    def eat_food(self, cell: Cell) -> None:
        """ Behavior for when the player eats food """
        # TODO// after eating food, remove the eaten food from list, increase score and reintroduce cell as empty 
        self.food.remove(cell)
        self.score += 1
        self.num_empty_cells += 1

    ##########################
    # Enemy Movement Methods #
    ##########################

    def add_enemy(self) -> None:
        """ Adds an enemy to the bottom right corner of the board """
        # TODO // add enemy to bottom right corner, if cell has player game over, if it has food from food list, change to enemy add to enemy list, if another enemy is there do nothing, if its empty then add cell to enemy list and decrease empty cells by 1
        row = random.randrange(0, Preferences.NUM_ROWS)
        col = random.randrange(0, Preferences.NUM_COLS)
        cell = self.board[row][col]
        # // Here I changed the enemies to be spawned randomly like the food is. 
        if cell.is_player():
            self.set_game_over()
        elif cell.is_food():
            self.food.remove(cell)
            cell.become_enemy()
            self.enemies.append(cell)
        elif cell.is_enemy():
            pass
        else:
            cell.become_enemy()
            self.enemies.append(cell)
            self.num_empty_cells -= 1
    def move_enemy_to_cell(self, enemy_cell: Cell, 
                           cell: Cell, idx: int) -> None:
        """ Moves the enemy cell to a new location.
            idx refpresents the index of that enemy in
             the enemies list. """
        # TODO // if destination cell has player game over, 
        # if it has food rmeove from food list
        # empty enemy's old cell
        # change destination cell to enemy and update enemies list
        #increase empty cells by 1 if food was eaten and enemys old cell
        # if destination has enother enemy do nothing
        if cell.is_player():
            enemy_cell.become_empty()
            self.num_empty_cells += 1
            self.set_game_over()
        elif cell.is_food():
            self.food.remove(cell)
            enemy_cell.become_empty()
            cell.become_enemy()
            self.enemies[idx] = cell
            self.num_empty_cells += 1
        elif cell.is_enemy():
            return 
        else:
            enemy_cell.become_empty()
            cell.become_enemy()
            self.enemies[idx] = cell
            self.num_empty_cells += 1

    def move_enemy_left(self, idx: int) -> None:
        """ Move the enemy at index idx left one cell """
        # TODO// Get the west neighbor of the enemy at index idx, if it exists move the enemy to that cell, if not do nothing
        enemy = self.enemies[idx]
        neighbor = self.get_west_neighbor(enemy)
        if neighbor is not None:
            self.move_enemy_to_cell(enemy, neighbor, idx)
    def move_enemy_right(self, idx: int) -> None:
        """ Move the enemy at index idx right one cell """
        # TODO// Get the east neighbor of the enemy at index idx, if it exists move the enemy to that cell, if not do nothing
        enemy = self.enemies[idx]
        neighbor = self.get_east_neighbor(enemy)
        if neighbor is not None:
            self.move_enemy_to_cell(enemy, neighbor, idx)
    def move_enemy_up(self, idx: int) -> None:
        """ Move the enemy at index idx up one cell """
        # TODO// Get the north neighbor of the enemy at index idx, if it exists move the enemy to that cell, if not do nothing
        enemy = self.enemies[idx]
        neighbor = self.get_north_neighbor(enemy)
        if neighbor is not None:
            self.move_enemy_to_cell(enemy, neighbor, idx)
    def move_enemy_down(self, idx: int) -> None:
        """ Move the enemy at index idx down one cell """
        # TODO// Get the south neighbor of the enemy at index idx, if it exists move the enemy to that cell, if not do nothing
        enemy = self.enemies[idx]
        neighbor = self.get_south_neighbor(enemy)
        if neighbor is not None:
            self.move_enemy_to_cell(enemy, neighbor, idx)


if __name__ == "__main__":
    gd = GameData()
    # You can modify the line below for testing!
    print(gd.get_west_neighbor(gd.player))