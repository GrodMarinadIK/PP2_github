import random
import pygame
import constants

# Enemy class 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice10\\racer\\images\\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, constants.SCREEN_WIDTH-40), 0) 

    def move(self):
        self.rect.move_ip(0, constants.SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            
            
# Player class 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice10\\racer\\images\\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < constants.SCREEN_WIDTH:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
                
# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice10\\racer\\images\\Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, constants.SCREEN_WIDTH-40), 0) 

    def move(self):
        self.rect.move_ip(0, constants.SPEED//1.5)  # Coins fall slower than enemies
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
        
    