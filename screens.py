"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import pygame.font


class Info_Screen():
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    red = (255, 0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 600, 600
        self.rect_color = (255, 255, 0)  # Display Color Yellow Background Box
        self.text_color = (0, 0, 0)      # Display Color Black for Text
        self.font = pygame.font.SysFont(None, 30)
        self.title_font = pygame.font.SysFont(None, 100)
        self.title = 'Space Invaders'
        self.title_color = (255, 0, 0)    # Display Color Red
        self.subtitle = ' - programmed by Dai Kieu'
        self.subtitle_font = pygame.font.SysFont(None, 25)
        self.subtitle_color = (255, 0, 0)  # Display Color Red
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.msgs = ['The rule is simple: KILL or BE KILLED',
                     'To survive you have to kill everything',
                     'I grant you 3 chances to play',
                     'Useful Info: Press Q to rage quit',
                     'Spam SPACEBAR to shoot the bullets',
                     'Use <-  -> " arrow keys to move your ship',
                     'Beat the HI-Score. GGWP Enjoy ^^',
                     'Click more to see the score assigned for each enemy',]

        self.prep_msgs(self.msgs)
        self.status = False

    def prep_msgs(self, msgs):
        # Generate the index for each line of message appear
        # Display Color Text Blue, and Yellow Background for each line of game instructions
        self.msg_image_1 = self.font.render(msgs[0], True, self.red, self.yellow)
        self.msg_image_2 = self.font.render(msgs[1], True, self.blue, self.yellow)
        self.msg_image_3 = self.font.render(msgs[2], True, self.blue, self.yellow)
        self.msg_image_4 = self.font.render(msgs[3], True, self.blue, self.yellow)
        self.msg_image_5 = self.font.render(msgs[4], True, self.blue, self.yellow)
        self.msg_image_6 = self.font.render(msgs[5], True, self.blue, self.yellow)
        self.msg_image_7 = self.font.render(msgs[6], True, self.blue, self.yellow)
        self.msg_image_8 = self.font.render(msgs[7], True, self.blue, self.yellow)

        # Surround each line of code with Rect
        self.msg_image_rect_1 = self.msg_image_1.get_rect()
        self.msg_image_rect_2 = self.msg_image_2.get_rect()
        self.msg_image_rect_3 = self.msg_image_3.get_rect()
        self.msg_image_rect_4 = self.msg_image_4.get_rect()
        self.msg_image_rect_5 = self.msg_image_5.get_rect()
        self.msg_image_rect_6 = self.msg_image_6.get_rect()
        self.msg_image_rect_7 = self.msg_image_7.get_rect()
        self.msg_image_rect_8 = self.msg_image_8.get_rect()

        # Create a Rect box in the center
        self.msg_image_rect_1.center = self.rect.center
        self.msg_image_rect_2.center = self.rect.center
        self.msg_image_rect_3.center = self.rect.center
        self.msg_image_rect_4.center = self.rect.center
        self.msg_image_rect_5.center = self.rect.center
        self.msg_image_rect_6.center = self.rect.center
        self.msg_image_rect_7.center = self.rect.center
        self.msg_image_rect_8.center = self.rect.center

        # Y-coordinates in Center
        self.msg_image_rect_1.centery = self.rect.centery - 180 + 50
        self.msg_image_rect_2.centery = self.rect.centery - 130 + 50
        self.msg_image_rect_3.centery = self.rect.centery - 80 + 50
        self.msg_image_rect_4.centery = self.rect.centery - 30 + 50
        self.msg_image_rect_5.centery = self.rect.centery + 20 + 50
        self.msg_image_rect_6.centery = self.rect.centery + 70 + 50
        self.msg_image_rect_7.centery = self.rect.centery + 120 + 50
        self.msg_image_rect_8.centery = self.rect.centery + 170 + 50

        # Title text: SPACE INVADER
        self.title_image = self.title_font.render(self.title, True, self.title_color, self.rect_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.center = self.rect.center
        self.title_image_rect.top = self.rect.top + 20

        # Programmed by Dai Kieu text
        self.sub_img = self.subtitle_font.render(self.subtitle, True, self.subtitle_color, self.rect_color)
        self.sub_img_rect = self.sub_img.get_rect()
        self.sub_img_rect.right = self.rect.right - 20
        self.sub_img_rect.bottom = self.title_image_rect.bottom + 20

    def draw_screen(self):
        self.screen.fill(self.rect_color, self.rect)
        self.screen.blit(self.title_image, self.title_image_rect)
        self.screen.blit(self.sub_img, self.sub_img_rect)

        self.screen.blit(self.msg_image_1, self.msg_image_rect_1)
        self.screen.blit(self.msg_image_2, self.msg_image_rect_2)
        self.screen.blit(self.msg_image_3, self.msg_image_rect_3)
        self.screen.blit(self.msg_image_4, self.msg_image_rect_4)
        self.screen.blit(self.msg_image_5, self.msg_image_rect_5)
        self.screen.blit(self.msg_image_6, self.msg_image_rect_6)
        self.screen.blit(self.msg_image_7, self.msg_image_rect_7)
        self.screen.blit(self.msg_image_8, self.msg_image_rect_8)

