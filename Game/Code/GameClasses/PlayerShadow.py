import pygame
import math


# The Shadow class, generates the shadow
class Shadow(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        # Sun is x high, and sun is at coordinates (sunX, sunY)
        self.sunHeight = 1000
        self.sunX = 0
        self.sunY = 0

        # Set the shadow image
        r = round(player.rect.width / 2)
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        grey = pygame.Color(67, 70, 75)
        pygame.draw.circle(self.image, grey, (r, r), r)
    
    def update(self, player, pixPerFoot):
        # Height distance from sun converted to pixels
        heightFromSun = (self.sunHeight - player.height) * pixPerFoot
        pixelHeight = player.height * pixPerFoot

        # Distance from sun in x direction in pixels
        sunDistX = (player.rect.centerx - self.sunX)
        # The angle the sun hits the person in the x direction
        sunAngleX = math.atan(sunDistX / heightFromSun)
        # Getting the shadow x location and converting back into pixels
        self.rect.centerx = player.rect.centerx + round((math.tan(sunAngleX) * pixelHeight))

        # Distance from sun in y direction in feet
        sunDistY = (player.rect.centery - self.sunY)
        # The angle the sun hits the person in the y direction
        sunAngleY = math.atan(sunDistY / heightFromSun)
        # Getting the shadow y location and converting back into pixels
        self.rect.centery = player.rect.centery + round((math.tan(sunAngleY) * pixelHeight))

    def draw(self, screen):
        screen.blit(self.image, self.rect)