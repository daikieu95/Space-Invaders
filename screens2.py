"""
CPSC 386 - Project 3
Create a Space Invaders game
Name: DAI KIEU
"""
import pygame.font


class Info_Screen2():
    green = (7, 249, 121)
    blue = (0, 0, 255)
    purple = (128, 7, 249)
    red = (255, 0, 0)
    orange = (255, 69, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 600, 600
        self.rect_color = (255, 255, 0)   # Display Background Color Yellow
        self.font = pygame.font.SysFont(None, 30)
        self.font2 = pygame.font.SysFont(None, 50)

        self.title_font = pygame.font.SysFont(None, 100)
        self.title = 'Space Invaders'
        self.title_color = (255, 0, 0)  # Display color Red

        self.subtitle = ' - programmed by Dai Kieu'
        self.subtitle_font = pygame.font.SysFont(None, 25)
        self.subtitle_color = (255, 0, 0)  # Display color Red

        # Alien Images
        self.image_of_alien_1 = pygame.image.load('images/alien1.png')
        self.rect_alien_1 = self.image_of_alien_1.get_rect()

        self.image_of_alien_2 = pygame.image.load('images/alien2.png')
        self.rect_alien_2 = self.image_of_alien_1.get_rect()

        self.image_of_alien_3 = pygame.image.load('images/alien3.png')
        self.rect_alien_3 = self.image_of_alien_1.get_rect()

        self.image_of_alien_UFO = pygame.image.load('images/UFO.png')
        self.rect_alien_UFO = self.image_of_alien_UFO.get_rect()

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Locate the position of all the Scores Color from x and y-coordinates
        self.rect1 = pygame.Rect(125 + 340, self.rect.centery - 7, 50, 15)
        self.rect2 = pygame.Rect(125 + 340, self.rect.centery + 50 - 7, 50, 15)
        self.rect3 = pygame.Rect(125 + 340, self.rect.centery + 100 - 7, 50, 15)
        self.rect4 = pygame.Rect(125 + 340, self.rect.centery + 150 - 7, 50, 15)
        self.msgs = ['____ENEMIES SCORE VALUE____',
                     '100',
                     '150',
                     '200',
                     '???????']

        self.prep_msgs(self.msgs)
        self.status = False

    def prep_msgs(self, msgs):
        self.msg_image_1 = self.font2.render(msgs[0], True, self.white, self.orange)       # Display Color for ENEMIES SCORE VALUE in the text and background
        self.msg_image_2 = self.font.render(msgs[1], True, self.green, self.rect_color)    # Display Color Green for Alien 1 in the text
        self.msg_image_3 = self.font.render(msgs[2], True, self.blue, self.rect_color)     # Display Color Blue for Alien 2 in the text
        self.msg_image_4 = self.font.render(msgs[3], True, self.purple, self.rect_color)   # Display Color Purple for Alien 3 in text
        self.msg_image_5 = self.font.render(msgs[4], True, self.red, self.rect_color)      # Display Color Red for UFO (Boss) in the text

        self.msg_image_rect_1 = self.msg_image_1.get_rect()
        self.msg_image_rect_2 = self.msg_image_2.get_rect()
        self.msg_image_rect_3 = self.msg_image_3.get_rect()
        self.msg_image_rect_4 = self.msg_image_4.get_rect()
        self.msg_image_rect_5 = self.msg_image_5.get_rect()

        # Locate the Box Color x-coordinates from the right position
        self.msg_image_rect_1.center = self.rect.center
        self.msg_image_rect_2.left = self.rect.right - 350
        self.msg_image_rect_3.left = self.rect.right - 350
        self.msg_image_rect_4.left = self.rect.right - 350
        self.msg_image_rect_5.left = self.rect.right - 350

        # Locate the Box Color y-coordinates from the center position
        self.msg_image_rect_1.centery = self.rect.centery - 150 + 50
        self.msg_image_rect_2.centery = self.rect.centery - 50 + 50
        self.msg_image_rect_3.centery = self.rect.centery + 0 + 50
        self.msg_image_rect_4.centery = self.rect.centery + 50 + 50
        self.msg_image_rect_5.centery = self.rect.centery + 100 + 50

        # Locate the position of all the Images Aliens from the x-coordinate (start from the right)
        self.rect_alien_1.left = self.rect.right - 550
        self.rect_alien_2.left = self.rect.right - 550
        self.rect_alien_3.left = self.rect.right - 550
        self.rect_alien_UFO.left = self.rect.right - 600

        # Locate the position of all the Images Aliens from the y-coordinate(start from center)
        self.rect_alien_1.centery = self.rect.centery - 100 + 100
        self.rect_alien_2.centery = self.rect.centery - 150 + 200
        self.rect_alien_3.centery = self.rect.centery - 195 + 300
        self.rect_alien_UFO.centery = self.rect.centery - 230 + 400


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
        self.screen.fill((7, 249, 121), self.rect1)   # Display Color Green for Alien 1 in the Rectangle Box
        self.screen.fill((0, 0, 255), self.rect2)     # Display Color Blue for Alien 2 in the Rectangle Box
        self.screen.fill((128, 7, 249), self.rect3)   # Display Color Purple for Alien 3 in the Rectangle Box
        self.screen.fill((255, 0, 0), self.rect4)     # Display Color Red for UFO (Boss) in the Rectangle Box
        self.screen.blit(self.title_image, self.title_image_rect)
        self.screen.blit(self.sub_img, self.sub_img_rect)

        # Draw the Boxes of Instructions
        self.screen.blit(self.msg_image_1, self.msg_image_rect_1)
        self.screen.blit(self.msg_image_2, self.msg_image_rect_2)
        self.screen.blit(self.msg_image_3, self.msg_image_rect_3)
        self.screen.blit(self.msg_image_4, self.msg_image_rect_4)
        self.screen.blit(self.msg_image_5, self.msg_image_rect_5)

        # Draw the images of the Aliens
        self.screen.blit(self.image_of_alien_1, self.rect_alien_1)
        self.screen.blit(self.image_of_alien_2, self.rect_alien_2)
        self.screen.blit(self.image_of_alien_3, self.rect_alien_3)
        self.screen.blit(self.image_of_alien_UFO, self.rect_alien_UFO)