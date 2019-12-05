import pygame

# Class for the main screen, contains animations and buttons

class MainScreenApp():
    def __init__(main, screen, width, height, WELCOMEANIMATION, welcomeTimer):
        # Initalize colors
        main.white = (255, 255, 255)
        main.black = (0, 0, 0)
        main.blue = (0, 0, 255)
        main.green = (38, 106, 46)

        # Store screen and its dimensions
        main.screen = screen
        main.screenWidth = width
        main.screenHeight = height

        # Set framerate and clock
        main.frameRate = 30
        main.clock = pygame.time.Clock()

        # Store timer information
        main.welcomeAnimationTimer = welcomeTimer
        main.WELCOMEANIMATION = WELCOMEANIMATION

        # Initalize the truck image
        main.initalizeImage()
        
        # Initalize the welcome display
        main.initalizeWelcome()

        # Initalize the play game button
        main.initalizePlayGameButton()

        # Initalize the map creator button
        main.initalizeMapLoadButton()
    
        # Initalize the help button
        main.initalizeHelpButton()
        
    def initalizeImage(main):
        # Truck photo downloaded and edited from https://www.washtrust.com/Portals/0/Uploads/Images/ShredDay_Truck.jpg
        main.image = pygame.image.load('Sprites/Main/Shred-It Truck.png').convert_alpha()
        main.originalImage = main.image

        # Set scale to zero (animation will eventually change the scale)
        main.imageScale = 0
        main.image = pygame.transform.scale(main.originalImage, (round(main.originalImage.get_width()*main.imageScale), round(main.originalImage.get_height()*main.imageScale)))
        
        # Set initial location of image
        main.imageRect = main.image.get_rect()
        main.imageRect.centerx = main.screenWidth

        # Set image animation to be active
        main.imageAnimation = True
        
        # Set welcome animation variables
        main.welcomeAnimation = False
        main.welcomeAnimationTime = 2

    def initalizeWelcome(main):        
        # Set welcome display
        fontSize = 40
        welcomeFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', fontSize)
        welcomeText = 'Are you ready to Shred-It?'
        main.welcomeDisplay = welcomeFont.render(welcomeText, True, main.blue)
        main.welcomeDisplayRect = main.welcomeDisplay.get_rect()
        main.welcomeDisplayRect.centerx = main.screenWidth/2
        main.welcomeDisplayRect.y = 20

    def initalizePlayGameButton(main):
        # Initalize the button surface
        main.playButton = pygame.Surface((round(main.screenWidth/3), round(main.screenHeight/13)))
        main.playButtonRect = main.playButton.get_rect()
        main.playButtonOriginalRect = main.playButton.get_rect()

        # Fill black (will be border)
        main.playButton.fill(main.black)

        # Fill a smaller rect with blue
        main.playButton.fill(main.blue, rect=main.playButtonRect.inflate(-10, -10))

        # Render text
        buttonText = 'Play Infinite Game'
        fontSize = round(main.playButtonRect.height / 2)
        buttonFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', fontSize)

        # Blit text onto button surface
        main.playButtonText = buttonFont.render(buttonText, True, main.white)
        main.playButtonTextRect = main.playButtonText.get_rect()
        main.playButtonTextRect.centerx = round(main.playButtonRect.width / 2)
        main.playButtonTextRect.centery = round(main.playButtonRect.height / 2)
        main.playButton.blit(main.playButtonText, main.playButtonTextRect)

        # Set button location
        main.playButtonRect.centerx = main.screenWidth/4
        main.playButtonRect.centery = main.screenHeight/6

    def initalizeMapLoadButton(main):
        # Initalize the button surface
        main.mapLoadButton = pygame.Surface((round(main.screenWidth/3), round(main.screenHeight/13)))
        main.mapLoadButtonRect = main.mapLoadButton.get_rect()
        main.mapLoadOriginalRect = main.mapLoadButton.get_rect()

        # Fill black (will be border)
        main.mapLoadButton.fill(main.black)

        # Fill a smaller rect with blue
        main.mapLoadButton.fill(main.blue, rect=main.mapLoadButtonRect.inflate(-10, -10))

        # Render text
        buttonText = 'Load Map'
        fontSize = round(main.mapLoadButtonRect.height / 2)
        buttonFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', fontSize)

        # Blit text onto button surface
        main.mapLoadButtonText = buttonFont.render(buttonText, True, main.white)
        main.mapLoadButtonTextRect = main.mapLoadButtonText.get_rect()
        main.mapLoadButtonTextRect.centerx = round(main.mapLoadButtonRect.width / 2)
        main.mapLoadButtonTextRect.centery = round(main.mapLoadButtonRect.height / 2)
        main.mapLoadButton.blit(main.mapLoadButtonText, main.mapLoadButtonTextRect)

        # Set button location
        main.mapLoadButtonRect.centerx = 3*main.screenWidth/4
        main.mapLoadButtonRect.centery = main.screenHeight/6
    
    def initalizeHelpButton(main):
        # Initalize the button surface
        main.helpButton = pygame.Surface((round(main.screenWidth/3), round(main.screenHeight/13)))
        main.helpButtonRect = main.helpButton.get_rect()
        main.helpButtonOriginalRect = main.helpButton.get_rect()

        # Fill black (will be border)
        main.helpButton.fill(main.black)

        # Fill a smaller rect with blue
        main.helpButton.fill(main.blue, rect=main.helpButtonRect.inflate(-10, -10))

        # Render text
        buttonText = 'Help'
        fontSize = round(main.helpButtonRect.height / 2)
        buttonFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', fontSize)

        # Blit text onto button surface
        main.helpButtonText = buttonFont.render(buttonText, True, main.white)
        main.helpButtonTextRect = main.helpButtonText.get_rect()
        main.helpButtonTextRect.centerx = round(main.helpButtonRect.width / 2)
        main.helpButtonTextRect.centery = round(main.helpButtonRect.height / 2)
        main.helpButton.blit(main.helpButtonText, main.helpButtonTextRect)

        # Set button location
        main.helpButtonRect.centerx = main.screenWidth/2
        main.helpButtonRect.centery = round(main.screenHeight/3.5)

    def processEvent(main, event):
        # If the welcome animation timer hits and welcome animation is active, run the animation
        if event.type == main.WELCOMEANIMATION and main.welcomeAnimation:
            main.runWelcomeAnimation()
        # If no animations are running
        elif not(main.welcomeAnimation) and not(main.imageAnimation):
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
                if main.playButtonRect.collidepoint(mousepos): # If click the play button, return the new mode
                    return 'Game'
                elif main.mapLoadButtonRect.collidepoint(mousepos): # If click the map create button, return the new mode
                    return 'MapPreview'
                elif main.helpButtonRect.collidepoint(mousepos):
                    return 'HelpScreen'
            elif event.type == pygame.MOUSEMOTION:
                # If mouse moves over button, new fill is green (otherwise it is blue)
                mousepos = pygame.mouse.get_pos()
                main.playButton.fill(main.black)
                main.playButton.fill(main.blue, rect=main.playButtonOriginalRect.inflate(-10, -10))
                main.playButton.blit(main.playButtonText, main.playButtonTextRect)
                main.mapLoadButton.fill(main.black)
                main.mapLoadButton.fill(main.blue, rect=main.mapLoadOriginalRect.inflate(-10, -10))
                main.mapLoadButton.blit(main.mapLoadButtonText, main.mapLoadButtonTextRect)
                main.helpButton.fill(main.black)
                main.helpButton.fill(main.blue, rect=main.helpButtonOriginalRect.inflate(-10, -10))
                main.helpButton.blit(main.helpButtonText, main.helpButtonTextRect)
                if main.playButtonRect.collidepoint(mousepos):
                    main.playButton.fill(main.black)
                    main.playButton.fill(main.green, rect=main.playButtonOriginalRect.inflate(-10, -10))
                    main.playButton.blit(main.playButtonText, main.playButtonTextRect)
                elif main.mapLoadButtonRect.collidepoint(mousepos):
                    main.mapLoadButton.fill(main.black)
                    main.mapLoadButton.fill(main.green, rect=main.mapLoadOriginalRect.inflate(-10, -10))
                    main.mapLoadButton.blit(main.mapLoadButtonText, main.mapLoadButtonTextRect)
                elif main.helpButtonRect.collidepoint(mousepos):
                    main.helpButton.fill(main.black)
                    main.helpButton.fill(main.green, rect=main.helpButtonOriginalRect.inflate(-10, -10))
                    main.helpButton.blit(main.helpButtonText, main.helpButtonTextRect)
        return 'MainScreen'

    def runLogic(main):
        # Run truck animation
        main.runImageAnimation()
    
    def runWelcomeAnimation(main):
        # If welcome display is nothing, initialize it
        if main.welcomeDisplay == None:
            main.initalizeWelcome()
        # If welcome display is something, set it to none (flashes the welcome display essentially)
        else:
            main.welcomeDisplay = None
        
        # Subtract time from the total animaiton time
        main.welcomeAnimationTime -= main.welcomeAnimationTimer/1000
        
        # If the timer is less then zero, end animation and initalize the welcome display
        if main.welcomeAnimationTime < 0:
            main.initalizeWelcome()
            main.welcomeAnimation = False

    def runImageAnimation(main):
        # Run animation if the image has not reached the center
        if main.imageRect.centerx > main.screenWidth/2:
            # Move image by 3 closer to the center
            main.imageRect.centerx -= 3
            # Store the center of x
            tempX = main.imageRect.centerx
            # Set image scale as a ratio of how far along traveled to center
            main.imageScale = (main.screenWidth-main.imageRect.centerx) / (main.screenWidth/2.2)
            # Scale image
            main.image = pygame.transform.scale(main.originalImage, (round(main.originalImage.get_width()*main.imageScale), round(main.originalImage.get_height()*main.imageScale)))
            # Set image to location
            main.imageRect = main.image.get_rect()
            main.imageRect.bottom = main.screenHeight
            main.imageRect.centerx = tempX
            # If reached center, stop image animation and start welcome animation
            if main.imageRect.centerx <= main.screenWidth/2:
                main.welcomeAnimation = True
                main.imageAnimation = False

    def displayFrame(main):
        # Background is white
        main.screen.fill(main.white)
        # Blit the truck onto the screen
        main.screen.blit(main.image, main.imageRect)
        # If its not the image animation and welcome display is not none, blit it
        if not(main.imageAnimation) and main.welcomeDisplay != None:
            main.screen.blit(main.welcomeDisplay, main.welcomeDisplayRect)
        # If both animations are over, show the play button
        if not(main.imageAnimation) and not(main.welcomeAnimation):
            main.screen.blit(main.mapLoadButton, main.mapLoadButtonRect)
            main.screen.blit(main.playButton, main.playButtonRect)
            main.screen.blit(main.helpButton, main.helpButtonRect)
        pygame.display.update()
