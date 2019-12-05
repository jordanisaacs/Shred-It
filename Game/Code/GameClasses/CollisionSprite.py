import pygame

# Just a barebones sprite class for collision sprites
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()