import pygame
from UI import InputBox
#import color
from settings import *
#import sys

class Difficulty:
    def __init__(self, screen, screen_width, screen_height):
        
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.difficulty = None
        self.clock = pygame.time.Clock()
        self.setting = None
        self.font = pygame.font.Font(None, 36)
        self.input_box = InputBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 250, 200, 40, self.font)

        self.difficulty = None
        self.setting = None
        self.done = False
        # Add user id
        self.user_id = ""
        print("Difficulty manager initialized")

        self.difficulties = {
            "easy": {"LEG_UP_TIME": 2, "SPAWN_TIME": 7, "VELOCITY": 3},
            "medium": {"LEG_UP_TIME": 3, "SPAWN_TIME": 7, "VELOCITY": 3},
            "hard": {"LEG_UP_TIME": 4, "SPAWN_TIME": 7, "VELOCITY": 3}
        }


    def draw_button(self, text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    
    def show_difficulty_screen(self):
        print("Displaying difficulty screen")
        self.done = False  
        
        self.screen.fill((0, 0, 0))  # Fill screen with black

        title1 = self.font.render("Input ID and Click Enter", True, (255, 255, 255))
        self.screen.blit(title1, (SCREEN_WIDTH // 2 - title1.get_width() // 2, SCREEN_HEIGHT // 2 - 300))
        title2 = self.font.render("Choose a Difficulty Level", True, (255, 255, 255))
        self.screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, SCREEN_HEIGHT // 2 - 200))
    

        button_width, button_height = 200, 50
        button_y = 200
        for difficulty in self.difficulties.keys():
            button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, button_y, button_width, button_height)
            self.draw_button(difficulty, button_rect, COLORS["buttons"]["default"])
            button_y += 100

        pygame.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(30)  # Limit the frame rate
            self.input_box.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                input_result = self.input_box.handle_event(event)
                if input_result:
                    self.user_id = input_result
                    print(f"User name is: {self.user_id}")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    button_y = 200
                    for difficulty in self.difficulties.keys():
                        button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, button_y, button_width, button_height)
                        if button_rect.collidepoint(mouse_pos):
                            #user_id = self.input_box.get_text()
                            #print(user_id)
                            self.difficulty = difficulty
                            self.setting = self.difficulties[difficulty]
                            print(f'Difficulty level selected is: {self.difficulty}')
                            print(f"Settings being returned: {self.setting}")
                            waiting = False
                            #update_difficulty_settings(self.setting["LEG_UP_TIME"])
                            #pygame.event.clear()  # Clear all events to avoid lingering inputs
                            return self.setting  # Return immediately after selection
                        button_y += 100

            # Update input box
            self.input_box.update()

            pygame.display.flip()  # Update the display

        print("Closing difficulty manager")
        return self.setting
        #return None

    def get_difficulty_settings(self):
        print("Getting difficulty setting")
        return self.setting
        

    # Add method to retrieve user id
    def get_user_id(self):
        print("Getting user id")
        return self.user_id