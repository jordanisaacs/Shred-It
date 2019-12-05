import pygame
from .CollisionSprite import CollisionSprite

# Cliff sprite class
class Cliff(pygame.sprite.Sprite):
    # Initalize variables
    def __init__(self, args):
        super().__init__()
        name = args[0]
        x = args[1]
        y = args[2]
        self.setImg(str(name))
        self.rect = self.image.get_rect()
        self.collision.rect = self.collision.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.originalY = y
        self.collision.rect = self.rect
        self.activeJump = False
        # Heights for all the cliffs
        heights = [25, 75, 40, 100]
        # Set cliff height depending on name
        self.height = heights[name-1]
    
    # Set image to the cliff number and also grab the collision image
    def setImg(self, name):
        self.image = pygame.image.load('Sprites/Map/Cliffs/Cliff ' + name + '.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.collision = CollisionSprite()
        self.collision.image = pygame.image.load('Sprites/Map/Cliffs/Cliff ' + name + ' Collision.png')
        self.collision.mask = pygame.mask.from_surface(self.collision.image)

        self.imageName = name

    # Move the cliff accordingly if scrolling
    def update(self, game):
        if game.scrollingY == True:
            self.setY(self.rect.centery - game.player.dy)
    
    def previewUpdate(self, scrolly):
        self.setY(self.originalY - scrolly)

    # Set y value of both the collision image and the cliff image
    def setY(self, y):
        self.rect.centery = y
        self.collision.rect.centery = y