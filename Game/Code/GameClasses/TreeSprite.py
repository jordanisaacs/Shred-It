import pygame
from .CollisionSprite import CollisionSprite

class Tree(pygame.sprite.Sprite):
    def __init__(self, args):
        super().__init__()
        # Parse the args
        name = args[0]
        scale = args[1]
        x = args[2]
        y = args[3]

        # Set the image
        self.setImg(str(name), scale)
        # Set the image rects
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.collision.rect = self.collision.image.get_rect()
        self.collision.rect.centerx = x
        self.collision.rect.centery = y

        # Store original y for map preview mode
        self.originalY = y
    

    # Set image of collision and normal images + scale them
    def setImg(self, name, scale):
        self.image = pygame.image.load('Sprites/Map/Trees/Tree ' + name + '.png').convert_alpha()
        scaleWidth = round(self.image.get_width() * scale)
        scaleHeight = round(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (scaleWidth, scaleHeight))
        self.collision = CollisionSprite()
        self.collision.image = pygame.image.load('Sprites/Map/Trees/Tree ' + name + ' Collision.png')
        self.collision.image = pygame.transform.scale(self.collision.image, (scaleWidth, scaleHeight))
        self.collision.mask = pygame.mask.from_surface(self.collision.image)
        self.imageName = name

    # Move the cliff accordingly if scrolling
    def update(self, game):
        if game.scrollingY == True:
            self.setY(self.rect.centery - game.player.dy)
    
    # Update used in the map preview mode
    def previewUpdate(self, scrolly):
        self.setY(self.originalY - scrolly)

    # Set y value of both the collision image and the cliff image
    def setY(self, y):
        self.rect.centery = y
        self.collision.rect.centery = y