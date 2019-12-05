import pygame

# Player trail class (the trail behind the player)
class Trail():
    # Initalize the trail
    def __init__(self, player):
        x = player.rect.centerx
        y = player.rect.centery

        # The piece of trail image
        self.r = round(player.rect.width / 3.5)
        lightGrey = pygame.Color(200, 200, 200)
        self.color = lightGrey
        self.color.a = 175
        self.coords = [[x, y]]
        self.image = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.r, self.r), self.r)

    # Update the player trail
    def update(self, player, scrolling):
        # If scrolling, then move every trail coord according to the y distance the player traveled
        if scrolling:
            dy = player.dy
            for coord in self.coords:
                coord[1] -= dy
        # If the player is on the ground, add another trail coord
        if player.height <= 0:
            x = player.rect.centerx - self.r
            y = player.rect.centery - self.r
            self.coords.append([x, y])

    # Draw the player trail, a circle for every coord
    def draw(self, screen):
        # Draw a trail image at every coord in the list
        for coord in self.coords:
            screen.blit(self.image, coord)