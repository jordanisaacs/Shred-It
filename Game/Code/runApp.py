import pygame
import math
from .gameMode import GameApp
from .mainScreenMode import MainScreenApp
from .mapPreviewMode import MapPreviewApp
from .helpScreenMode import HelpScreenApp

# Multi-Modal framework for running pygame

# Font from https://www.fontsquirrel.com/fonts/encode-sans

# the actual running of pygame
def runGame():
    # Start pygame
    pygame.init()
    # Set the caption to "Shred-it"
    pygame.display.set_caption("Shred-it!")
    # Icon got from https://www.flaticon.com/free-icon/skiing-stickman_1227
    icon = pygame.image.load('Sprites/icon.png')
    pygame.display.set_icon(icon)
    running = True
    screenWidth = 1200
    screenHeight = 800

    # Set timers
    WELCOMEANIMATION = pygame.USEREVENT+1
    welcomeAnimationTimer = 400
    pygame.time.set_timer(WELCOMEANIMATION, welcomeAnimationTimer)
    UPDATEDISP = pygame.USEREVENT+2
    displayTimer = 200
    pygame.time.set_timer(UPDATEDISP, displayTimer)
    
    # Set user events
    RESET = pygame.USEREVENT+4
    resetEvent = pygame.event.Event(RESET)
    LOADERROR = pygame.USEREVENT+5
    loadErrorEvent = pygame.event.Event(LOADERROR)

    # Set the playGameMap (what is loaded when press play game button) and have it be the loaded map
    playGameMap = ('infinite',)
    loadedMap = playGameMap

    # Initalize screen, and mainScreen and set active mode
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    game = None
    mapPreview = None
    helpScreen = HelpScreenApp(screen, screenWidth, screenHeight)
    mainScreen = MainScreenApp(screen, screenWidth, screenHeight, WELCOMEANIMATION, welcomeAnimationTimer)
    activeMode = 'MainScreen'

    # Commented code if want to start on game mode (speeds up debugging)
    #game = GameApp(screen, screenWidth, screenHeight, UPDATEDISP, displayTimer, resetEvent, loadedMap)
    #activeMode = 'Game'

    # Commented code if want to start on load map mode (speeds up debugging)
    #mapPreview = MapPreviewApp(screen, screenWidth, screenHeight)
    #activeMode = 'MapPreview'

    # Loop game until running is false
    while running:
        if activeMode == 'MainScreen': # If active mode is mainscreen, then run that game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else: # Process the event within the mainScreen class and it returns the active mode
                    activeMode = mainScreen.processEvent(event)
    
                # If active mode is not mainscreen, break the event loop
                if activeMode != 'MainScreen':
                    break
            
            # If active mode is not mainscreen skip the rest of the game loop
            if activeMode != 'MainScreen':
                # If the new active mode will be game, initalize the game app
                if activeMode == 'Game':
                    loadedMap = playGameMap
                    game = GameApp(screen, screenWidth, screenHeight, UPDATEDISP, displayTimer, resetEvent, loadedMap)
                elif activeMode == 'MapPreview':
                    mapPreview = MapPreviewApp(screen, screenWidth, screenHeight, loadErrorEvent)
                continue

            pygame.mouse.set_visible(True)
            mainScreen.runLogic()
            mainScreen.displayFrame()
            mainScreen.clock.tick(mainScreen.frameRate)
        elif activeMode == 'Game': # If active mode is game, then run that game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == RESET: # If the event is the userevent RESET, then re-initalize the game class and break the event loop
                    game = GameApp(screen, screenWidth, screenHeight, UPDATEDISP, displayTimer, resetEvent, loadedMap)
                    break
                else: # Process the event in the game class and returns the active mode
                    activeMode = game.processEvent(event)
                
                # If active mode is not game break the event loop
                if activeMode != 'Game':
                    break
            
            # If active mode is not game skip the rest of the game loop
            if activeMode != 'Game':
                continue

            pygame.mouse.set_visible(False)
            game.runLogic()                 # run game logic
            game.displayFrame()             # Display everything 
            game.clock.tick(game.frameRate) # Run game according to framerate
        elif activeMode == 'MapPreview':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == LOADERROR: # If you close the load gui on the main screen
                    activeMode = 'MainScreen'
                else:
                    activeMode = mapPreview.processEvent(event)
                
                if activeMode != 'MapPreview':
                    break
            
            if activeMode != 'MapPreview':
                if activeMode == 'Game': # Change loaded map and activate game
                    loadedMap = mapPreview.gameMap
                    game = GameApp(screen, screenWidth, screenHeight, UPDATEDISP, displayTimer, resetEvent, loadedMap)
                continue
            
            pygame.mouse.set_visible(True)

            if mapPreview.filePath == None: # Load the file if no file is loaded, otherwise run pygame
                mapPreview.loadFile()
            else:
                mapPreview.runLogic()
                mapPreview.displayFrame()
                mapPreview.clock.tick(mapPreview.frameRate)
        elif activeMode == 'HelpScreen': # Framework for help screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    activeMode = helpScreen.processEvent(event)
                
                if activeMode != 'HelpScreen':
                    break
            
            if activeMode != 'HelpScreen':
                continue

            pygame.mouse.set_visible(True)
            
            helpScreen.displayFrame()
            helpScreen.clock.tick(helpScreen.frameRate)
            
    # quit pygame
    pygame.quit()