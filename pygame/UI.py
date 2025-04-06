import pygame
import color
from settings import *


class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surf = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

class Dropdown:
    def __init__(self, x, y, w, h, font, main, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color.GRAY
        self.font = font
        self.main = main
        self.options = options
        self.selected = main
        self.options_rects = [pygame.Rect(x, y + (i + 1) * h, w, h) for i in range(len(options))]
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.selected, True, color.BLACK)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

        if self.active:
            for i, option in enumerate(self.options):
                pygame.draw.rect(screen, self.color, self.options_rects[i])
                text_surf = self.font.render(option, True, color.BLACK)
                screen.blit(text_surf, (self.options_rects[i].x + 5, self.options_rects[i].y + (
                            self.options_rects[i].height - text_surf.get_height()) // 2))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                for i, option_rect in enumerate(self.options_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected = self.options[i]
                        self.active = False
                        return self.options[i]
                self.active = False
        return None

class InputBox:
    def __init__(self, x, y, w, h, font, text='Input ID'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.default_text = 'Input ID'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text == self.default_text:
                    self.text = ''
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        return None

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.initial_width
        self.rect.height = self.initial_height

    def get_text(self):
        return self.text if not self.showing_default else ""

    def clear_text(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.showing_default = False

def draw_text(surface, text, pos, color, font=FONTS["medium"], pos_mode="top_left",
                shadow=False, shadow_color=(0,0,0), shadow_offset=2):
    label = font.render(text, 1, color)
    label_rect = label.get_rect()
    if pos_mode == "top_left":
        label_rect.x, label_rect.y = pos
    elif pos_mode == "center":
        label_rect.center = pos

    if shadow: # make the shadow
        label_shadow = font.render(text, 1, shadow_color)
        surface.blit(label_shadow, (label_rect.x - shadow_offset, label_rect.y + shadow_offset))

    surface.blit(label, label_rect) # draw the text



#def button(surface, pos_y, text=None, click_sound=None):
def button(surface, pos_button, text=None, click_sound=None):
    x, y = pos_button
    #rect = pygame.Rect((SCREEN_WIDTH//2 - BUTTONS_SIZES[0]//2, pos_y), BUTTONS_SIZES)
    rect = pygame.Rect((x, y), BUTTONS_SIZES)
    

    on_button = False
    if rect.collidepoint(pygame.mouse.get_pos()):
        color = COLORS["buttons"]["second"]
        on_button = True
    else:
        color = COLORS["buttons"]["default"]

    pygame.draw.rect(surface, COLORS["buttons"]["shadow"], (rect.x - 6, rect.y - 6, rect.w, rect.h)) # draw the shadow rectangle
    pygame.draw.rect(surface, color, rect) # draw the rectangle
    # draw the text
    if text is not None:
        draw_text(surface, text, rect.center, COLORS["buttons"]["text"], pos_mode="center",
                    shadow=True, shadow_color=COLORS["buttons"]["shadow"])

    if on_button and pygame.mouse.get_pressed()[0]: # if the user press on the button
        if click_sound is not None: # play the sound if needed
            click_sound.play()
        return True