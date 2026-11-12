"""
Author: Prof. Alyssa
Defines constants to be used for the program.
You do NOT need to modify this file.
"""

import pygame
import os 

class Preferences:
    """ Defines values for constant variables.
        This is good practice to avoid "magic numbers" """
    
    pygame.init()
    

    ##########
    # COLORS #
    ##########

    TEXT_FONT_COLOR = pygame.Color('black')

    INPUT_BOX_COLOR = pygame.Color('gray')

    EDGE_LINE_COLOR = pygame.Color('gray')

    BACKGROUND_COLOR = pygame.Color('white')


    ########
    # TEXT #
    ########

    LABEL_FONT_SIZE = 22
    LABEL_FONT = pygame.font.SysFont(None, LABEL_FONT_SIZE)

    PROMPT_FONT_SIZE = 24 
    PROMPT_FONT = pygame.font.SysFont(None, PROMPT_FONT_SIZE)


    ##########
    # SIZING #
    ##########

    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 500

    ICON_SIZE = 48
    LEVEL_GAP = 120

    TEXT_PADDING = 5

    INPUT_BOX_WIDTH = 200
    INPUT_BOX_HEIGHT = 32


    ##########
    # TIMING #
    ##########

    # How long to sleep between updates (ms)
    SLEEP_TIME = 50


    ######################
    # GRAPHICS and FILES #
    ######################

    # Faculty spreadsheet
    FACULTY_FILE = os.path.join(os.path.dirname(
        os.path.realpath(__file__)),
        'faculty_list.xlsx')

    # Directory containing the images
    IMG_DIR = os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 
                            'headshots')
