import pygame
import math
import re

from .PlayerShadow import Shadow
from .PlayerTrail import Trail
from .CollisionSprite import CollisionSprite
from .CliffSprite import Cliff

# Player class, contains all info necessary for player actions
class Player(pygame.sprite.Sprite):
    # Takes in X and Y as the center of sprite
    def __init__(self, name, coords):
        super().__init__()
        self.name = name
        self.scale = 0.7
        self.setImg('Forward')

        # Set location of images
        self.rect = self.image.get_rect()
        self.bottomCollision.rect = self.bottomCollision.image.get_rect()
        self.rect.center = coords
        self.originalY = self.rect.y
        self.bottomCollision.rect.center = self.rect.center
        self.midCollision.rect = self.midCollision.image.get_rect()
        self.midCollision.rect.center = self.rect.center
        self.entireCollision.rect = self.entireCollision.image.get_rect()
        self.entireCollision.rect.center = self.rect.center

        # Player dependent physics
        self.velocity = 0       # Unit: pixels/frame
        self.displacement = 0   # Unit: pixels
        self.heightVelocity = 0 # Unit: feet/frame
        self.height = 0         # Unit: feet
        # x and y and height change from the physics
        self.xDisplacement = 0
        self.yDisplacement = 0
        self.heightDisplacement = 0
        # the actual change for x and y including such things as collision
        self.dy = 0
        self.dx = 0

        # Stats variables
        self.airtime = 0
        self.dispAirtime = 0
        self.distTraveled = 0
        self.dispDistTraveled = 0
        self.crashed = False
        self.spin = 0
        self.points = 0
        self.newPoints = 0
        self.trickName = ''

        # Variables for rotating sprite
        self.rotateSpeed = 7
        self.pointing = 'Forward'
        self.angle = 0

        # Grabbing variable for in air tricks and the variable that stores grabs done
        self.grabbing = False
        self.grabs = []
        self.newGrab = False
        self.grabTimer = 0.15
        self.grabTime = 0
        self.oldGrab = False

        # ski term for skiing backwards
        self.switch = False

        # The trail behind the player
        self.trail = Trail(self)

        # The player shadow
        self.shadow = Shadow(self)
        
    # Equal if player names are the same
    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name
    
    # Hash the unique player name
    def __hash__(self):
        return hash(self.name)

    # Set the sprite image and all its collision box images
    def setImg(self, name):
        # Set image of sprite and create mask
        self.image = pygame.image.load('Sprites/Player/Ski ' + name + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (round(self.image.get_rect().width*self.scale), round(self.image.get_rect().height*self.scale)))
        self.mask = pygame.mask.from_surface(self.image)
        self.originalImage = self.image
        
        # Get the first word of the name (will always be direction) aka strips grab names
        dirImgName = re.search("^\w+", name).group()

        # Set image of the bottom collision box and its mask
        self.bottomCollision = CollisionSprite()
        self.bottomCollision.image = pygame.image.load('Sprites/Player/Ski ' + dirImgName + ' Bottom Collision.png').convert_alpha()
        self.bottomCollision.image = pygame.transform.scale(self.bottomCollision.image, (round(self.bottomCollision.image.get_rect().width*self.scale), round(self.bottomCollision.image.get_rect().height*self.scale)))
        self.bottomCollision.mask = pygame.mask.from_surface(self.bottomCollision.image)
        self.bottomCollision.originalImage = self.bottomCollision.image
        
        # Set image of the mid collision box and its mask
        self.midCollision = CollisionSprite()
        self.midCollision.image = pygame.image.load('Sprites/Player/Ski ' + dirImgName + ' Mid Collision.png').convert_alpha()
        self.midCollision.image = pygame.transform.scale(self.midCollision.image, (round(self.midCollision.image.get_rect().width*self.scale), round(self.midCollision.image.get_rect().height*self.scale)))
        self.midCollision.mask = pygame.mask.from_surface(self.midCollision.image)
        self.midCollision.originalImage = self.midCollision.image
        
        # Set entire collision box
        self.entireCollision = CollisionSprite()
        self.entireCollision.image = pygame.image.load('Sprites/Player/Ski ' + dirImgName + ' Entire Collision.png').convert_alpha()
        self.entireCollision.image = pygame.transform.scale(self.entireCollision.image, (round(self.entireCollision.image.get_rect().width*self.scale), round(self.entireCollision.image.get_rect().height*self.scale)))
        self.entireCollision.mask = pygame.mask.from_surface(self.entireCollision.image)
        self.entireCollision.originalImage = self.entireCollision.image


    # Rotate images redo masks
    def rotate(self):
        # Rotate image and set mask
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.mask = pygame.mask.from_surface(self.image)

        # Rotate bottom collision box and set mask
        self.bottomCollision.image = pygame.transform.rotate(self.bottomCollision.originalImage, self.angle)
        self.bottomCollision.mask = pygame.mask.from_surface(self.bottomCollision.image)

        # Rotate mid collision box and set mask
        self.midCollision.image = pygame.transform.rotate(self.midCollision.originalImage, self.angle)
        self.midCollision.mask = pygame.mask.from_surface(self.midCollision.image)

        # Rotate entire collision box and set mask
        self.entireCollision.image = pygame.transform.rotate(self.entireCollision.originalImage, self.angle)
        self.entireCollision.mask = pygame.mask.from_surface(self.entireCollision.image)

        # Align the images
        self.alignImage()
        
    # Re-align image and collision image
    def alignImage(self):
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.bottomCollision.rect = self.bottomCollision.image.get_rect()
        self.bottomCollision.rect.center = (x, y)
        
        self.midCollision.rect = self.midCollision.image.get_rect()
        self.midCollision.rect.center = (x, y)

        self.entireCollision.rect = self.entireCollision.image.get_rect()
        self.entireCollision.rect.center = (x, y)
    
    # Set the x of the player and all the collision boxes
    def setX(self, x):
        self.rect.x = x
        self.bottomCollision.rect.x = x
        self.midCollision.rect.x = x
        self.entireCollision.rect.x = x

    # Set the y of the player and all the collision boxes
    def setY(self, y):
        self.rect.y = y
        self.bottomCollision.rect.y = y
        self.midCollision.rect.y = y
        self.entireCollision.rect.y = y

    # Move logic for player
    def move(self, game):
        if self.height <= 0:
            # Kinematic equation, turn velocity into the distance to be traveled for the frame
            self.displacement = (self.velocity + (self.velocity - game.acceleration)) / 2
            # Can't travel faster than maxTravel
            if self.displacement > game.maxDisplacement:
                self.velocity -= game.acceleration
                self.displacement = (self.velocity + (self.velocity - game.acceleration)) / 2

            # Extra logic for moving up the hill
            if 90 < self.angle < 270:
                # Decelerate the player because facing up hill
                self.velocity -= game.acceleration * game.slowdown
                # If about to move backwards instead rotate 180 degrees change sprite to forward/backward
                if self.velocity < 0:
                    self.velocity = 0
                    self.flipSelf(game)
            else: # If not moving up hill, just do normal acceleration
                self.velocity += game.acceleration

            # Turn the total travel in specific x and y travel
            (self.xDisplacement, self.yDisplacement) = self.getXYDisplacement(game)

        # Add the xDisplacement and yDisplacment to toal dx and dy
        self.dx += self.xDisplacement
        self.dy += self.yDisplacement

    # Flip self both sprite and angle wise
    def flipSelf(self, game):
        # Set angle the opposite direction
        self.angle = (self.angle - 180) % 360

        # If switch, then now a forward sprite and not switch, and vis versa
        if self.switch:
            self.setImg('Forward')
            self.switch = False
        else:
            cliff = self.checkCollisions(game)
            if isinstance(cliff, Cliff):
                self.dy += 7
            self.setImg('Backward')
            self.switch = True

        # Align image then rotate image
        self.alignImage()
        self.rotate()

    # Return true if mask colliding with any cliff objects
    def checkCollisions(self, game):
        for cliff in game.cliffGroup:
            if pygame.sprite.collide_mask(self.entireCollision, cliff):
                if cliff.activeJump == False:
                    return cliff
        for tree in game.treeGroup:
            if pygame.sprite.collide_mask(self.entireCollision, tree.collision):
                return tree
        return False

    # Turn the total travel into x and y travel
    def getXYDisplacement(self, game):
        # Turn angle and travel into dx and dy, round because can only display integers
        dy = round(math.cos(math.radians(self.angle)) * self.displacement)
        dx = round(math.tan(math.radians(self.angle)) * self.displacement)
        # If pointing uphill then dx is negative
        if 90 < self.angle < 270:
            dx *= -1

        # Set an artifical max speed for changing X (makes game feel more fluid)
        maxDX = game.maxDisplacement * 0.8
        if dx > maxDX:
            dx = maxDX
        elif dx < -1 * maxDX:
            dx = -1 * maxDX
        
        return (dx, dy)

    # Logic for actually changing the x and y of player
    def changeXY(self, game):
        # set X to itself + dx
        self.setX(self.rect.x + self.dx)
 
        # Scrolling logic
        halfScreenHeight = game.screenHeight / 2
        if game.scrollingY == False: # If not scrolling, change Y then check if scrolling should be true
            self.setY(self.rect.y + self.dy)
            if game.scrollLength >= game.scrollY and self.rect.y >= halfScreenHeight:
                game.scrollingY = True
        else: # If scrolling, change scroll then check if scrolling should be false
            game.scrollY += self.dy
            if game.scrollY >= game.scrollLength:
                game.scrollingY = False
        
        # Perform bounds detection after changing x and y
        self.boundsDetection(game) 

    # Bounds detection for screen, keep player from traveling off map
    # Game over if touching bottom of map (aka finished the scroll)
    def boundsDetection(self, game):
        if self.rect.left < 0:
            self.setX(0)
        elif self.rect.right > game.screenWidth:
            self.setX(game.screenWidth - self.rect.width)
        if self.rect.top < 0:
            self.setY(0)
        elif self.rect.bottom > game.screenHeight:
            self.setY(game.screenHeight - self.rect.height)
            game.over = True
   
    # Change angle of sprite
    def changeAngle(self, game):
        oldAngle = self.angle
        if self.pointing == 'LEFT':
            if self.height <= 0:
                self.angle = (self.angle - self.rotateSpeed) % 360
            else: # If in air, spin faster and store the spin
                self.spin += self.rotateSpeed*2
                self.angle = (self.angle - self.rotateSpeed*2) % 360
        elif self.pointing == 'RIGHT':
            if self.height <= 0:
                self.angle = (self.angle + self.rotateSpeed) % 360
            else: # If in air, spin faster and store the spin
                self.spin -= self.rotateSpeed*2
                self.angle = (self.angle + self.rotateSpeed*2) % 360
        self.rotate()

        if self.height <= 0:
            # If the new angle collides with anything revert to old angle
            if self.checkCollisions(game) != False:
                self.angle = oldAngle
                self.rotate()

    def heightUpdate(self, game):
        if self.height > 0 or self.heightVelocity > 0:
            # No new points if in air and not crashed
            self.newPoints = 0
            self.crashed = False

            # Player physics:
            # original height velocity per frame
            velocity0 = self.heightVelocity
            # Set height velocity per frame after accelerating the gravity per frame
            self.heightVelocity -= game.gravity
            # Height displacement per frame based on kinematic equation
            self.heightDisplacement = (self.heightVelocity + velocity0) / 2
            
            # Turn dy into distance in feet traveled
            adjustedDY = self.dy / game.pixPerFoot
            adjustedDX = self.dx / game.pixPerFoot

            # Add the height gained due to traveling above a slope
            self.heightDisplacement += adjustedDY * math.tan(game.slope)

            # Ensure not traveling faster than the set terminal speed
            if self.heightDisplacement < game.maxFallDisplacement:
                self.heightVelocity += game.gravity
                self.heightDisplacement = game.maxFallDisplacement
            
            # Add the height accordingly
            self.height += self.heightDisplacement

            # Update stats
            self.airtime += game.clock.get_time()/1000
            self.distTraveled += adjustedDY
            self.dispAirtime = self.airtime
            self.dispDistTraveled = self.distTraveled

            # If a grabbing update, update the player image
            if self.newGrab == True:
                self.updateGrabs()
            
            # If grabbing then start grab timer, append the grab to the grab list if that specific instance of the grab is not already added
            if self.grabbing != False:
                self.grabTime += game.clock.get_time()/1000

            # If the height is now less than zero, then the player has landed
            if self.height <= 0:
                if self.switch:
                    self.setImg('Backward')
                else:
                    self.setImg('Forward')
                self.alignImage()
                self.rotate()
                self.processLanding(game)
        
        if self.height <= 0:
            # Reset stats
            self.grabs = []
            self.oldGrab = False
            self.grabbing = False
            self.grabTime = 0
            self.spin = 0
            self.height = 0
            self.heightVelocity = 0
            self.heightDisplacement = 0
            self.airtime = 0
            self.distTraveled = 0

    def updateGrabs(self):
        # Set the beginning of what the name of the image file will be
        if self.switch:
            imgName = 'Backward'
        else:
            imgName = 'Forward'
        
        # Add the image name of the grab type
        if self.grabbing != False:
            # Append the type of grab to the image name
            imgName += ' ' + self.grabbing
        
        # If the previous grab was a grab, then add the grab to the trick list and the time it was held for
        if self.oldGrab != False:
            self.grabs.append((self.oldGrab, self.grabTime))
    
        # Set the image
        self.setImg(imgName)
        self.alignImage()
        self.rotate()
        self.newGrab = False
        self.grabTime = 0

    # Process landing (player was in air and now is not) logic
    def processLanding(self, game):
        # Set trickHistoryUpdate to true so text displays update and reset the timer
        game.trickHistoryUpdate = True
        game.trickDisplayTime = game.trickDisplayTimer

        # Check for collisions
        cliff = self.checkCollisions(game)

        # Don't care which way was spinned
        self.spin = abs(self.spin)

        # Get the distance spun from original angle
        spinFromOriginalAngle = self.spin % 360

        # If collided with a cliff
        if isinstance(cliff, Cliff):
            # Change dy so that player will be below the cliff
            self.dy += cliff.rect.bottom - self.rect.top

            # If the midCollision collides with cliff then crashed, otherwise ignore
            if pygame.sprite.collide_mask(self.midCollision, cliff):
                # Do not change x, no velocity, and crashed
                self.dx = 0
                self.velocity = 0
                self.crashed = True
                self.trickName = 'crashed'
            else:
                self.processTrick()
                if 90 < spinFromOriginalAngle < 270:
                    self.flipSelf(game)
        # Elif not pointing wthin 45 degrees of original spin (forwards or backwards)
        elif 45 < spinFromOriginalAngle < 145 or 225 < spinFromOriginalAngle < 315:
            # Crashed
            self.trickName = 'crashed'
            self.velocity = 0
            self.crashed = True
        # Else landed properly so process trick
        else:
            self.processTrick()
            # If landed facing up hill, flip self
            if 90 < spinFromOriginalAngle < 270:
                self.flipSelf(game)
            
    def processTrick(self):
        # Set trick name to nothing
        self.trickName = ''
        
        # Set spin error to 45
        spinError = 45

        if self.grabbing != False:
            self.grabs.append((self.grabbing, self.grabTime))

        # Process grab tricks
        for grab in self.grabs:
            grabName = grab[0]
            grabTime = grab[1]
            if grabTime >= 0.3:
                self.trickName += grabName + ' '
                if grabName in ['Left Safety', 'Right Safety']:
                    self.newPoints += round(grabTime, 2) * 2
                elif grabName == 'Double Safety':
                    self.newPoints += round(grabTime, 2) * 4

        # If did above a 360
        if self.spin >= 360-spinError:
            # Get how many spins done
            spins = round(self.spin / 360)
            # Spin name starts at zero spin
            spinName = 0
            # Landed opposite means landed in opposite direction (did an extra 180)
            landedOpposite = self.spin % 360 > 180-spinError

            # If took off switch, get two points
            if self.switch:
                self.newPoints += 2
                self.trickName += 'switch '
            
            # If did an extra 180, then get three points and spinname is 180
            if landedOpposite:
                self.newPoints += 3
                spinName = 180

            # Get six points for every 360
            self.newPoints += 6*spins

            # Add spin to spinName and add it to trickName
            spinName += 360 * spins
            self.trickName += str(spinName)
        # Else if spin is great enough to be a 180
        elif self.spin >= 180-spinError:
            # Get three points
            self.newPoints += 3
            
            # If a switch 180, get two points
            if self.switch:
                self.newPoints += 2
                self.trickName += 'switch '

            # Add 180 to trick name
            self.trickName += '180'
        # Else, just was switch
        elif self.switch:
            # Trick is called zero spin
            self.trickName += 'zero spin'
            self.newPoints += 2
        
        if self.trickName == '':
            self.trickName = 'no trick'
        
        self.trickName = self.trickName.strip()
        # Add the new points to total points
        self.points += self.newPoints

    # Logic for updating
    def update(self, game):
        self.dx = 0
        self.dy = 0

        # Update location of self
        self.move(game)
        
        # Process rotating of sprite
        self.changeAngle(game)

        # Process height movements of sprite
        self.heightUpdate(game)

        # Only changeXY at the very end because dx and dy are getting changed multiple times by lots of logic
        self.changeXY(game)

        # Only now update the trail and shadow
        self.trail.update(self, game.scrollingY)
        self.shadow.update(self, game.pixPerFoot)


    def previewUpdate(self, scrollY):
        self.setY(self.originalY - scrollY)