import pygame
import math
import copy
from .GameClasses.PlayerSprite import Player
from .GameClasses.CliffSprite import Cliff
from .GameClasses.TreeSprite import Tree
from .InfiniteMap.sheetGenerator import sheetGenerator

# The game mode, runs the game and game logic and displays game

class GameApp():
    def __init__(game, screen, width, height, UPDATEDISP, displayTimer, resetEvent, gameMap):
        # Store screen and screen info
        game.screenWidth = width
        game.screenHeight = height
        game.screen = screen
        
        # Set game variables
        game.frameRate = 30
        game.over = False
        game.paused = False
        game.clock = pygame.time.Clock()

        # Initalize some game colors and the font
        game.currentStatsSize = 20
        game.currentStatsFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', game.currentStatsSize)
        game.oldStatsSize = 12
        game.oldStatsFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', game.oldStatsSize)
        game.trickSize = 25
        game.trickFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', game.trickSize)
        game.pointsSize = 20
        game.pointsFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', game.pointsSize)
        game.white = (255, 255, 255)
        game.blue = (0,0,255)
        game.black = (0, 0, 0)

        # Initalize Text variables
        game.statsDisplay = []
        game.trickHistory = []
        game.trickDisplay = []
        game.pointsDisplay = None
        game.trickDisplayTimer = 2
        game.trickDisplayTime = 0
        game.trickHistoryUpdate = False

        # Store timer and event info
        game.displayTimer = displayTimer
        game.UPDATEDISP = UPDATEDISP
        game.resetEvent = resetEvent


        # Initalize Groups
        game.playerGroup = pygame.sprite.Group()
        game.mapGroup = pygame.sprite.Group()
        game.cliffGroup = pygame.sprite.Group()
        game.treeGroup = pygame.sprite.Group()

        # Initalize information about the scrolling
        game.scrollingY = False
        game.scrollY = 0

        game.mode = gameMap[0]
        if game.mode == 'load' or game.mode == 'infiniteload':
            # Initalize the player
            playerCoords = gameMap[2]

            game.player = Player('Player1', playerCoords)
            game.playerGroup.add(game.player)
            
            # Length of sheet/map
            length = gameMap[1]

            # Initalize the map/sheet depending on moad
            game.mapList = gameMap[3]
            if game.mode == 'load':
                # Initialize the game length
                game.scrollLength = length - game.screenHeight

                # Parse map
                game.parseMap(game.mapList)
            else: # It is an infinite map
                game.yTravel = 0
                # Scroll length is infinity
                game.scrollLength = math.inf
                # Sheet length is length of map
                game.sheetLength = length
                # Initalize two sheets (aka two user maps)
                game.numSheets = 2
                game.sheetList = []#
                for sheetNum in range(game.numSheets):
                    sheet = game.mapList
                    game.parseMap(sheet, sheetNum*game.sheetLength)
                    game.sheetList.append(sheet)

        elif game.mode == 'infinite':
            # Set player
            playerYCoord = round(game.screenHeight/12)
            playerCoords = (game.screenWidth/2, playerYCoord)
            game.player = Player('Player1', playerCoords)
            game.playerGroup.add(game.player)

            # Keep track of how far traveled down sheet
            game.yTravel = 0

            # Scroll for infinity
            game.scrollLength = math.inf

            # Set sheet length to be twice the screen height
            game.sheetLength = game.screenHeight * 2

            # Create two sheets to start
            game.numSheets = 2
            game.sheetList = []
            for sheetNum in range(game.numSheets):
                sheet = sheetGenerator(game.screenWidth, game.sheetLength, sheetNum*game.sheetLength)
                game.parseMap(sheet)
                game.sheetList.append(sheet)

        # Initalize physics
        game.initPhysics()
        
        # Initalize the pause display
        game.initPauseDisplay()
        # Initalize the game over display
        game.initGameOverDisplay()

        # Option to draw collision boxes or not
        game.showCollisionBoxes = False

    def initPauseDisplay(game):
        # Set the font of pauseText
        pauseTextSize = 30
        pauseTextFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', pauseTextSize)

        # Set text of pauseText, must be in a list because pygame does not render new lines
        pauseText = []
        pauseText.append('Game Paused')
        pauseText.append('Press \'p\' to resume')
        pauseText.append('Press \'r\' to restart')
        pauseText.append('Press \'m\' to return to main screen')
        
        # Create the actual pauseDisplay and set location
        game.pauseDisplay = game.createTextBox(pauseTextFont, pauseTextSize, pauseText, game.white, game.black, game.blue)
        game.pauseDisplayRect = game.pauseDisplay.get_rect()
        game.pauseDisplayRect.centerx = game.screenWidth/2
        game.pauseDisplayRect.y = 10
    
    
    def initGameOverDisplay(game):
        # Set the font for gameOver
        gameOverTextSize = 30
        gameOverFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', gameOverTextSize)

        # Set the text
        gameOverText = []
        gameOverText.append('Game Over')
        gameOverText.append('Press \'r\' to restart')
        gameOverText.append('Press \'m\' to return to main screen')
        
        # Create and set location of the game over display
        green = (34,139,34)
        game.gameOverDisplay = game.createTextBox(gameOverFont, gameOverTextSize, gameOverText, green, green, game.black)
        game.gameOverDisplayRect = game.gameOverDisplay.get_rect()
        game.gameOverDisplayRect.centerx = game.screenWidth/2
        game.gameOverDisplayRect.centery = game.screenHeight/2


    # Create a text box depending on the inputs
    def createTextBox(game, font, textSize, textList, textColor, borderColor, fillColor):
        maxWidth = 0
        textHeight = 0
        # List to store the text renders
        textDisplays = []

        # Loop through the list of text and render text and find the text line that is longest and store the pixel width
        # Also store sum of the height of the text
        for text in textList:
            textDisplay = font.render(text, True, textColor)
            textDisplays.append(textDisplay)
            if textDisplay.get_width() > maxWidth:
                maxWidth = textDisplay.get_width()
            textHeight += textDisplay.get_height()

        # Set the text box to a little larger than the text
        height = textHeight + 20
        width = maxWidth + 20

        # Create the text box surface and fill it with border color, fill a deflated rect with the fill color
        textBox = pygame.Surface((width, height))
        textBoxRect = textBox.get_rect()
        textBox.fill(borderColor)
        border = -7
        textBox.fill(fillColor, rect=textBoxRect.inflate(border, border))

        # Draw the text onto the box surface
        y = abs(border)
        for textDisplay in textDisplays:
            x = textBoxRect.width/2 - textDisplay.get_width()/2
            textBox.blit(textDisplay, (x, y))
            y += textSize + 10
        return textBox

    # Initalize game physics
    def initPhysics(game):
        # Length of ski is 60 inches
        game.pixPerFoot = (game.player.rect.height * 12) / 60
        # Max speed is 12 mph
        maxSpeed = 12
        game.maxDisplacement = (maxSpeed * 5280 * game.pixPerFoot) / 60 / 60 / game.frameRate
        # Max fall speed is 3.5 mph
        maxFall = -3.5
        game.maxFallDisplacement = (maxFall * 5280 * game.pixPerFoot) / 60 / 60 / game.frameRate
        # Ski slope is 35 degrees
        game.slope = math.radians(35)
        # Gravity is 9.8 ft / second^2
        totalGravity = 9.8
        # Snow friction is 2 ft / second^2
        snowFriction = 2
        game.gravity = totalGravity / game.frameRate
        # Acceleration on a 15 degree slope
        totalAcceleration = (totalGravity / math.sin(game.slope) - snowFriction) / game.frameRate
        # adjusted per frame
        game.acceleration = (totalAcceleration * game.pixPerFoot) / game.frameRate
        # Rate to decelerate per frame when pointed uphill
        game.slowdown = 2

    # Parse map and load
    def parseMap(game, mapList, offset=0):
        for item in mapList:
            itemType = item[0]
            initArgs = copy.deepcopy(item[1])
            if itemType == 'Cliff':
                initArgs[2] += offset
                sprite = Cliff(initArgs)
                game.cliffGroup.add(sprite)
            elif itemType == 'Tree':
                initArgs[3] += offset
                sprite = Tree(initArgs)
                game.treeGroup.add(sprite)
            
            game.mapGroup.add(sprite)

    # Process events logic
    def processEvent(game, event):
        # If the timer UPDATEDDISP is called update text displays
        if event.type == game.UPDATEDISP:
            game.updateTextDisplays()

        if event.type == pygame.KEYUP:
            # If press m and game is over or game is paused, return to main screen
            if event.key == pygame.K_m and (game.paused or game.over):
                return 'MainScreen'
            # If press r and game is over or game is paused, post the resetEvent
            elif event.key == pygame.K_r and (game.paused or game.over):
                pygame.event.post(game.resetEvent)
            # If press p and the game is not over, pause game
            elif event.key == pygame.K_p and not(game.over):
                game.paused = not(game.paused)
            elif event.key == pygame.K_b:
                game.showCollisionBoxes = not(game.showCollisionBoxes)
        return 'Game'
    
    # Run game logic
    def runLogic(game):
        # Update the actual game if not game over and not game paused
        if not(game.over) and not(game.paused):
            game.processKeys()
            game.playerGroup.update(game)
            game.mapGroup.update(game)
            game.mapCollisions()
            game.yTravel = game.scrollY + game.screenHeight/2
        
        # Infinite Scrolling generate new sheet logic
        if game.mode in ['infinite', 'infiniteload']:
            # Length of game with current number of sheets
            gameLength = game.numSheets * game.sheetLength
            # When one sheet away from last sheet, generate a new sheet
            if game.yTravel > gameLength - game.sheetLength:
                # Player never exactly at one sheet away so account for that in offset
                yOffset = game.sheetLength + game.screenHeight/2 - (game.yTravel % game.sheetLength)
                # Generate new sheet one sheet away and parse
                if game.mode == 'infinite': # Use the built in sheetGenerator
                    newSheet = sheetGenerator(game.screenWidth, game.sheetLength, yOffset)
                    game.parseMap(newSheet)
                else: # Otherwise use the loaded user map
                    newSheet = game.mapList
                    game.parseMap(newSheet, yOffset)
                # Now have one more sheet
                game.numSheets += 1

    # Check map collisions
    def mapCollisions(game):
        # Check cliff collisions
        for cliff in game.cliffGroup:
            # If rough collide (only compare rects)
            if pygame.sprite.collide_rect(cliff, game.player):
                # If player somehow starts the jump but does not follow through, then not active jump
                if game.player.midCollision.rect.top > cliff.collision.rect.bottom:
                    cliff.activeJump = False

                # If pixel perfect collision of the cliff collision box and the player bottom collision box and player not in air, and not activated collision
                # Then active jump
                if cliff.activeJump == False and game.player.height <= 0 and pygame.sprite.collide_mask(cliff.collision, game.player.bottomCollision):
                    cliff.activeJump = True
                # Elif pixel perfect collision of the cliff and the player entire collision box, the player is not in the air, and not active jump
                # Then undo previous movement (with addition of two so not still colliding) and set player velocity to zero
                elif cliff.activeJump == False and game.player.height <= 0 and pygame.sprite.collide_mask(cliff, game.player.entireCollision):
                    if game.player.bottomCollision.rect.top < cliff.collision.rect.bottom:
                        game.player.dx = (game.player.dx * -1)
                        if game.player.dx > 0:
                            game.player.dx += 2
                        else:
                            game.player.dx -= 2
                        game.player.dy = (game.player.dy * -1)
                        if game.player.dy > 0:
                            game.player.dy += 2
                        else:
                            game.player.dy -= 2
                        game.player.velocity = 0
                        game.player.changeXY(game)
                # Elf pixel perfect collision of mid collision box and acivated jump, then go into the air
                elif cliff.activeJump == True and pygame.sprite.collide_mask(cliff, game.player.midCollision):
                    game.player.height = cliff.height
                    cliff.activeJump = False
                
                return None
        
        # Tree collisions if no cliff collisions
        for tree in game.treeGroup:
            if pygame.sprite.collide_mask(tree.collision, game.player.entireCollision):
                game.player.dy = (game.player.dy * -1)
                if game.player.dx > 0:
                    game.player.dx += 1
                else:
                    game.player.dx -= 1
                game.player.dx = (game.player.dx * -1)
                if game.player.dy > 0:
                    game.player.dy += 1
                else:
                    game.player.dy -= 1
                game.player.velocity = 0
                game.player.changeXY(game)
                return None

    def updateTextDisplays(game):
        # If the player height is above zero, update the StatsDisplay
        if game.player.height > 0:
            game.updateStatsDisplay()
        # Else if trickHistoryUpdate is true, set statsDisplay to nothing and update trickhistory, pointsdisplay, and trickdisplay
        elif game.trickHistoryUpdate:
            game.statsDisplay = []
            game.updateTrickHistory()
            game.updateTrickDisplay()
            game.updatePointsDisplay()
        
        # If trickDisplayTime is greater than zero, subtract the display timer from it
        if game.trickDisplayTime > 0:
            game.trickDisplayTime -= game.displayTimer / 1000
            # If trickDisplayTime is less than zero set it to zero
            if game.trickDisplayTime < 0:
                game.trickDisplayTime = 0


    def updateStatsDisplay(game):
        # Set the text list and display to empty list
        textList = []
        game.statsDisplay = []
        # Set text and round variables to two decimal places
        textList.append(f'Airtime: {round(game.player.dispAirtime, 2)} seconds')
        textList.append(f'Dist. Traveled Downhill: {round(game.player.dispDistTraveled, 2)} feet')
        # For text in the list, append the rendered blue text into the statsDisplay list
        for text in textList:
            game.statsDisplay.append(game.currentStatsFont.render(text, True, game.blue))
    
    
    def updateTrickDisplay(game):
        # Set the trickDisplay list and textList to zero
        game.trickDisplay = []
        textList = []

        # Set what the trick portion of trickDisplay text will say
        tempText = 'You '
        if game.player.crashed:
            tempText += f'{game.player.trickName} :('
        else:
            if game.player.trickName == 'no trick':
                tempText += f'did {game.player.trickName}'
            else:
                tempText += f'did a {game.player.trickName}'
        textList.append(tempText)

        # Set what the points portion of trickDisplay text will say
        if game.player.newPoints == 1:
            tempText = f'Gained {game.player.newPoints:.2f} point'
        else:
            tempText = f'Gained {game.player.newPoints:.2f} points'

        # append text
        textList.append(tempText)
        
        # for text in list, append rendered text
        for text in textList:
            game.trickDisplay.append(game.trickFont.render(text, True, game.blue))
    
    def updateTrickHistory(game):
        # Set what text will be added to trick history
        tempText = []
        tempText.append(f'Airtime: {round(game.player.dispAirtime, 2)} seconds')
        tempText.append(f'Dist. Traveled: {round(game.player.dispDistTraveled, 2)} feet')

        # Setting what the trick and points part of trick History will show
        if game.player.crashed:
            tempText.append(f'{game.player.trickName} :(')
            tempText.append(f'Gained {game.player.newPoints:.2f} points')
        else:
            tempText.append(f'{game.player.trickName}!')
            tempText.append(f'Gained {game.player.newPoints:.2f} points!')

        # If not the first item in trick History, also add segmenter text
        if len(game.trickHistory) > 0:
            tempText.append('----------------')

        # Store the display as a surface because rendered text cannot be set as transparent
        tempDisplay = []
        for text in tempText:
            # Render text
            dispText = game.oldStatsFont.render(text, True, game.black)

            # Create a surface the size of the text
            display = pygame.Surface(dispText.get_size())

            # Fill surface with white then set that as transparent (do not need a white background for text)
            display.fill(game.white)
            display.set_colorkey(game.white)

            # Blit the text onto the display, will show the exact same thing as a normal text render but now is a surface so can be transparent
            display.blit(dispText, (0,0))

            # Add the display to the tempDisplay List
            tempDisplay.append(display)
        
        # Add the new trick and its info at the beginning of the list, turn trickHistoryUpdate to false because updated
        game.trickHistory = tempDisplay + game.trickHistory
        game.trickHistoryUpdate = False

    # Update points display
    def updatePointsDisplay(game):
        # Update the points text and render text
        pointsText = f'{game.player.points:.2f} total points'
        game.pointsDisplay = game.pointsFont.render(pointsText, True, game.black)

        # Set location of points display
        game.pointsDisplayRect = game.pointsDisplay.get_rect()
        game.pointsDisplayRect.right = game.screenWidth - 10
        game.pointsDisplayRect.top = 10

    # Check key states (different than events because can hold keys)
    def processKeys(game):
        keyStates = pygame.key.get_pressed()
        # If right, then going to rotate in right direction (positive angle change)
        if keyStates[pygame.K_RIGHT]:
            game.player.pointing = 'RIGHT'
        # If left, then going to rotate in left direction (negative angle change)
        elif keyStates[pygame.K_LEFT]:
            game.player.pointing = 'LEFT'
        # Else, just pointing forward (no angle change)
        else:
            game.player.pointing = 'FORWARD'

        if game.player.height > 0:
            if keyStates[pygame.K_a] and keyStates[pygame.K_d]:
                grab = 'Double Safety'
            elif keyStates[pygame.K_a]:
                grab = 'Left Safety'
            elif keyStates[pygame.K_d]:
                grab = 'Right Safety'
            else:
                grab = False
            
            if game.player.grabbing != grab:
                game.player.oldGrab = game.player.grabbing
                game.player.grabbing = grab
                game.player.newGrab = True
            else:
                game.player.newGrab = False

    # Display the game
    def displayFrame(game):
        # Refill background
        game.screen.fill(game.white)

        # Draw the player trail for the player
        game.player.trail.draw(game.screen)

        # Draw the map sprites onto the screen
        game.cliffGroup.draw(game.screen)

        # Draw the player 
        if game.player.height > 0:
            game.player.shadow.draw(game.screen)

        # If showing collision boxes is true, draw them onto the screen
        if game.showCollisionBoxes:
            for cliff in game.cliffGroup:
                game.screen.blit(cliff.collision.image, cliff.collision.rect)

            for player in game.playerGroup:
                game.screen.blit(player.entireCollision.image, player.entireCollision.rect)
                game.screen.blit(player.midCollision.image, player.midCollision.rect)
                game.screen.blit(player.bottomCollision.image, player.bottomCollision.rect)
        
        # Draw all the players onto the screen
        game.playerGroup.draw(game.screen)

        # Draw all trees onto the screen (leaves will be above player)
        game.treeGroup.draw(game.screen)

        # Show tree collision boxes if active
        if game.showCollisionBoxes:
            for tree in game.treeGroup:
                    game.screen.blit(tree.collision.image, tree.collision.rect)

        # Draw the left side text displays
        if game.statsDisplay != [] or game.trickHistory != []:
            y = 10
            # For every display text in statsDisplay, blit it a bit lower than the previous one
            for dispText in game.statsDisplay:
                game.screen.blit(dispText, (10, y))
                y += int(game.currentStatsSize*1.2)
            
            # Store count and inital alpha
            alpha = 255
            count = 1

            # Blit every text display lower, and also lower opacity for every text history chunk
            for textDisp in game.trickHistory:
                textDisp.set_alpha(alpha)
                game.screen.blit(textDisp, (10, y))
                y += int(game.oldStatsSize*1.2)
                if count % 5 == 0:
                    alpha -= round(alpha / 7)
                    if alpha < 0:
                        alpha = 0
                count += 1
        
        # Draw the big centered trick display
        if game.trickDisplayTime > 0:
            y = game.screenHeight / 3
            for dispText in game.trickDisplay:
                x = game.screenWidth/2 - dispText.get_width()/2
                game.screen.blit(dispText, (x, y))
                y += int(game.trickSize*1.2)

        # Draw the points display
        if game.pointsDisplay != None:
            game.screen.blit(game.pointsDisplay, game.pointsDisplayRect)

        # if paused, draw pause display
        if game.paused:
            game.screen.blit(game.pauseDisplay, game.pauseDisplayRect)
        
        if game.over:
            game.screen.blit(game.gameOverDisplay, game.gameOverDisplayRect)

        # Update the display with the new screen
        pygame.display.update()