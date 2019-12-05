import pygame
import tkinter
import importlib.machinery
import importlib.util
from tkinter.filedialog import askopenfilename
from .GameClasses.PlayerSprite import Player
from .GameClasses.CliffSprite import Cliff
from .GameClasses.TreeSprite import Tree

# The MapPreview class, contains everything for loading and previewing maps

class MapPreviewApp():
    def __init__(app, screen, width, height, loadErrorEvent):
        # Store important overall variables
        app.loadErrorEvent = loadErrorEvent
        app.screen = screen
        app.screenWidth = width
        app.screenHeight = height
        app.clock = pygame.time.Clock()
        app.frameRate = 30

        # Store some well used colors
        app.red = (255, 0, 0)
        app.white = (255, 255, 255)
        app.black = (0, 0, 0)

        # Set scroll to zero
        app.scrollY = 0

        # Map file loading variables
        app.filePath = None
        app.gameMap = None
        app.legalMap = True
        app.mapCrashed = False
        
        # Text box that will show if crashes while parsing
        crashedFontSize = 26
        crashedFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', crashedFontSize)
        crashedText = ['ERROR: Map parser crashed, please review code','\'r\' to reload', '\'l\' to load new map', '\'m\' to return to main screen']
        app.crashedTextBox = app.createTextBox(crashedFont, crashedFontSize, crashedText, app.white, app.white, app.black)
        app.crashedTextBoxRect = app.crashedTextBox.get_rect()
        app.crashedTextBoxRect.centerx = app.screenWidth/2
        app.crashedTextBoxRect.centery = app.screenHeight/2

        # Text box that will show if map features overlap
        overlapFontSize = 20
        overlapFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', crashedFontSize)
        overlapText = ['The map contains overlapping features', 'Game cannot be played until fixed', 'Please review code']
        app.overlapTextBox = app.createTextBox(overlapFont, overlapFontSize, overlapText, app.black, app.white, app.white)
        app.overlapTextBox.set_colorkey(app.white)
        app.overlapTextBoxRect = app.overlapTextBox.get_rect()
        app.overlapTextBoxRect.centerx = app.screenWidth/2
        app.overlapTextBoxRect.y = 30

        # Text box displaying preview info
        infoFontSize = 15
        infoFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', infoFontSize)
        infoText = ['Preview Mode, up and down arrows to explore map', '\'p\' to play map', '\'r\' to reload file', '\'l\' to load new map', '\'m\' to return to main screen']
        app.infoTextList = []
        y = 10
        for text in infoText:
            app.infoTextList.append((infoFont.render(text, True, app.black), (10, y)))
            y += infoFontSize + 3

        # Text to show if an infinite map
        infiniteText = 'This is an infinite map'
        app.infiniteText = infoFont.render(infiniteText, True, app.black)
        app.infiniteTextRect = app.infiniteText.get_rect()
        app.infiniteTextRect.centerx = app.screenWidth/2
        app.infiniteTextRect.bottom = app.screenHeight - 10

        # Map parsing variables
        app.gameLength = None
        app.scrollLength = None
        app.mapList = None
        app.player = None
        app.playerGroup = pygame.sprite.Group()
        app.mapGroup = pygame.sprite.Group()
        app.cliffGroup = pygame.sprite.Group()
        app.treeGroup = pygame.sprite.Group()

    # Create a text box depending on the inputs
    def createTextBox(app, font, textSize, textList, textColor, borderColor, fillColor):
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

    # Prompt, display gui, and logic for loading file
    def loadFile(app):
        # Using tkinter because pygame does not have a file prompt
        gui = tkinter.Tk()

        # tkinter opens a background box so hide it
        gui.withdraw()

        # Prompt for file and store it
        title = 'Select Map'
        mapDir = 'Maps/'
        tempPath = askopenfilename(title=title, initialdir=mapDir, filetypes=[('Map Files','*map.py')], multiple=False)

        # Close tkinter
        gui.destroy()

        if tempPath != '': # If a file is selected (no file returns empty string) set file path and parse
            app.filePath = tempPath
            app.parseMap()
        elif app.filePath == None: # Otherwise if no file path is set then post a loadErrorEvent
            pygame.event.post(app.loadErrorEvent)

    def parseMap(app):
        # Reset all the sprite groups and assume a legal map
        app.playerGroup = pygame.sprite.Group()
        app.mapGroup = pygame.sprite.Group()
        app.cliffGroup = pygame.sprite.Group()
        app.treeGroup = pygame.sprite.Group()
        app.legalMap = True
        app.scrollY = 0
        

        # Attempt to parse map, if fail then set mapCrashed to true
        try:
            # Cited/Modified from: https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3
            # Loads, then specs, then creates, then executes a module
            # The module is the game map and is complicated because is loaded using a file path, using python's recommended way of loading modules with a file path
            loader = importlib.machinery.SourceFileLoader('gameMap', app.filePath)
            spec = importlib.util.spec_from_loader(loader.name, loader)
            mapModule = importlib.util.module_from_spec(spec)
            loader.exec_module(mapModule)
            
            # Load map
            app.gameMap = mapModule.initMap(app.screenWidth, app.screenHeight)

            # Get gamemode
            app.gameMode = app.gameMap[0]

            # Initialize the game length
            app.gameLength = app.gameMap[1]
            app.scrollLength = app.gameLength - app.screenHeight

            # Initalize the player
            playerCoords = app.gameMap[2]
            app.player = Player('Player1', playerCoords)
            app.playerGroup.add(app.player)

            # Initalize the map
            mapList = app.gameMap[3]
            for item in mapList:
                itemType = item[0]
                initArgs = item[1]
                if itemType == 'Cliff':
                    sprite = Cliff(initArgs)
                    app.cliffGroup.add(sprite)
                elif itemType == 'Tree':
                    sprite = Tree(initArgs)
                    app.treeGroup.add(sprite)
                app.mapGroup.add(sprite)

            # Check if any overlapping objects and if so then not a legal map
            for item in app.mapGroup:
                collisions = pygame.sprite.spritecollide(item, app.mapGroup, dokill=False)
                if len(collisions) > 1 or pygame.sprite.collide_rect(item, app.player):
                    app.legalMap = False
            
            app.mapCrashed = False
        except:
            app.mapCrashed = True

    def processEvent(app, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m: # Press m to go back to main screen and reset filePath
                app.filePath = None
                return 'MainScreen'
            elif event.key == pygame.K_r: # Press r to reparse the map
                app.parseMap()
            elif event.key == pygame.K_l: # Press l to load a new file
                app.loadFile()
            elif event.key == pygame.K_p and app.legalMap and not(app.mapCrashed): # Press p to play game, but only if a legal map and not a crashed map
                app.filePath = None
                return 'Game'
        return 'MapPreview'

    # Scroll the screen and update sprite locations
    def screenScroll(app, dScroll):
        app.scrollY += dScroll
        if app.scrollY < 0:
            app.scrollY = 0
        elif app.scrollY > app.gameLength - app.screenHeight:
            app.scrollY = app.gameLength - app.screenHeight
        for item in app.mapGroup:
            item.previewUpdate(app.scrollY)
        app.player.previewUpdate(app.scrollY)

    def runLogic(app): # Mode logic
        app.processKeys()
    
    def processKeys(app): # Process key states (allow for holding down keys)
        keyStates = pygame.key.get_pressed()
        if keyStates[pygame.K_UP]: # Up arrow scroll the map upward
            app.screenScroll(-12)
        elif keyStates[pygame.K_DOWN]: # Down arrow scroll the map downward
            app.screenScroll(12)
                

    # Display the screen
    def displayFrame(app):
        # Display the error if a crashed map
        if app.mapCrashed:
            app.screen.fill(app.red)
            app.screen.blit(app.crashedTextBox, app.crashedTextBoxRect)
        else: # Otherwise display the map and also if anything overlaps
            app.screen.fill(app.white)
            app.mapGroup.draw(app.screen)
            app.playerGroup.draw(app.screen)
            for (text, coords) in app.infoTextList:
                app.screen.blit(text, coords)
            if not(app.legalMap):
                app.screen.blit(app.overlapTextBox, app.overlapTextBoxRect)
            if app.gameMode == 'infiniteload':
                app.screen.blit(app.infiniteText, app.infiniteTextRect)

        pygame.display.update()