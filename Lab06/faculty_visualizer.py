""" TODO Your program header """

import pygame

from preferences import Preferences

class FacultyVisualizer:
    def __init__(self, root, faculty):

        # The faculty dictionary
        self.faculty = faculty

        # The root of the Engineering tree
        self.root = root

        # The screen to draw things on
        self.screen = pygame.display.set_mode(
            (Preferences.SCREEN_WIDTH, Preferences.SCREEN_HEIGHT))


    def load_image(self, node):
        """ Load and place the icon for the given Professor node.
            Return None if the node is not a Professor node or there
            is not an image for the given Professor """

        if node.data:
            try:
                path = node.data.headshot
                image = pygame.image.load(path).convert_alpha()
                # Rescale the image to be the correct height
                img_x, img_y = image.get_size()
                scale = img_y / Preferences.ICON_SIZE
                image = pygame.transform.smoothscale(
                    image,
                    (img_x / scale, Preferences.ICON_SIZE)
                )
                return image
            except FileNotFoundError:
                return None
            

    def draw_node(self, node, x, y):
        """ Draw the given node at the given position """

        # Load the appropriate image
        image = self.load_image(node)
        # Set the label height
        label_y = y + Preferences.ICON_SIZE // 2

        # If there is an image to show, place it on the screen
        if image is not None:
            self.screen.blit(image, (x - Preferences.ICON_SIZE // 2, y))
            label_y += Preferences.ICON_SIZE // 2
            
        # Place the label on the screen
        label = Preferences.LABEL_FONT.render(node.name, True, Preferences.TEXT_FONT_COLOR)
        self.screen.blit(
            label,
            (x - label.get_width() // 2, label_y)
        )


    def draw_edge(self, parent_x, parent_y, child_x, child_y):
        """ Draw the edge between two nodes """

        start = (parent_x, parent_y + Preferences.ICON_SIZE)
        end = (child_x, child_y)
        pygame.draw.line(self.screen, Preferences.EDGE_LINE_COLOR, start, end, 2)


    def draw_tree(self, node, x, y, spacing):
        """ Draw a tree starting from the given node at the given location """

        # Draw the root node
        self.draw_node(node, x, y)

        num_children = len(node.children)

        # If the node is a leaf, then stop drawing
        if num_children == 0:
            return

        # Otherwise, start drawing the next level
        child_y = y + Preferences.LEVEL_GAP
        start_x = x - spacing * (num_children - 1) / 2

        for i, child in enumerate(node.children):
            child_x = start_x + i * spacing

            self.draw_edge(x, y, child_x, child_y)
            self.draw_tree(child, child_x, child_y, spacing / num_children)


    def draw_screen(self, input_rect):
        """ Clear the screen and draw the tree """

        # Clear the screen
        self.screen.fill(Preferences.BACKGROUND_COLOR)

        # Draw the tree
        self.draw_tree(self.root, Preferences.SCREEN_WIDTH // 2, 
                       Preferences.SCREEN_HEIGHT // 10, 
                       Preferences.SCREEN_WIDTH * .23)
        
        input_prompt1 = Preferences.PROMPT_FONT.render(
            f"Type the last name of the faculty",
            True,
            Preferences.TEXT_FONT_COLOR
        )

        # Add the prompt to the screen
        self.screen.blit(input_prompt1, (Preferences.SCREEN_WIDTH * .3, 
                                        Preferences.SCREEN_HEIGHT * .9))
        
        input_prompt2 = Preferences.PROMPT_FONT.render(
              "you would like to look up:",
            True,
            Preferences.TEXT_FONT_COLOR
        )

        # Add the prompt to the screen
        self.screen.blit(input_prompt2, (Preferences.SCREEN_WIDTH * .3, 
                                        Preferences.SCREEN_HEIGHT * .9 + Preferences.PROMPT_FONT_SIZE*.75))

        # Draw the text box
        self.draw_input_box(input_rect)


    def draw_input_box(self, input_rect, user_text=''):
        """ Draw the text box """

        pygame.draw.rect(self.screen, Preferences.INPUT_BOX_COLOR, input_rect)
        text_surface = Preferences.LABEL_FONT.render(user_text, True, Preferences.TEXT_FONT_COLOR)
        
        self.screen.blit(text_surface, (input_rect.x + Preferences.TEXT_PADDING, 
                                        input_rect.y + Preferences.TEXT_PADDING))


    def show_info(self, user_text):
        """ Display information about the given faculty member """
        # get() method returns the value for the given key if it exists in the dictionary, otherwise it returns None
        prof = self.faculty.get(user_text, None) 

        if prof:
            text = str(prof)
        else:
            text = f"No record for {user_text}"

        label = Preferences.LABEL_FONT.render(text, True, Preferences.TEXT_FONT_COLOR)
        self.screen.blit(
            label,
            (Preferences.SCREEN_WIDTH * 0.65, Preferences.SCREEN_HEIGHT * 0.85)
        )

    def run(self):
        """ Run the main loop to display the screen and handle keyboard input """

        # Keep track of the time that's passed 
        clock = pygame.time.Clock()

        running = True

        # Initialize user input graphics 
        user_text = ''

        input_rect = pygame.Rect(Preferences.SCREEN_WIDTH//2, 
                                 Preferences.SCREEN_HEIGHT * .9, 
                                 Preferences.INPUT_BOX_WIDTH,
                                 Preferences.INPUT_BOX_HEIGHT)
        
        # Display the tree
        self.draw_screen(input_rect)


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle keyboard input
                if event.type == pygame.KEYDOWN:
                    # Remove the last character if backspace is pressed
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    # Show the relevant faculty info if enter is pressed
                    elif event.key == pygame.K_RETURN:
                        self.draw_screen(input_rect)
                        self.show_info(user_text.strip().capitalize())
                        user_text = ''
                    # Otherwise, add the pressed key to the textbox
                    else:
                        user_text += event.unicode

            # Update the text box
            self.draw_input_box(input_rect, user_text)
                    
            pygame.display.flip()

            clock.tick(Preferences.SLEEP_TIME)

        pygame.quit()