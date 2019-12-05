import pygame

# Class for help screen app, contains text boxes

class HelpScreenApp():
    def __init__(app, screen, screenWidth, screenHeight):
        app.screen = screen
        app.screenWidth = screenWidth
        app.screenHeight = screenHeight
        app.clock = pygame.time.Clock()
        app.frameRate = 30

        app.white = (255,255,255)
        app.blue = (0,0,255)
        app.black = (0,0,0)
        app.red = (255,0,0)

        # Title text box
        titleText = ['Intro to Shredding']
        titleFontSize = 40
        titleTextFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', titleFontSize)
        app.titleTextBox = app.createTextBox(titleTextFont, titleFontSize, titleText, app.blue, app.black, app.red)
        app.titleTextBoxRect = app.titleTextBox.get_rect()
        app.titleTextBoxRect.centerx = app.screenWidth/2
        app.titleTextBoxRect.centery = app.screenHeight/5

        # Help text box
        helpTextList = ['Goal is to have fun and get points by doing tricks off cliffs',
                        'Controls are left and right arrows for directional movement and in-air spinning',
                        'In-air you can perform grabs using the \'a\' and \'d\' keys',
                        'Explore the grabs for yourself!',
                        'Press \'p\' to pause game (and option to exit if infinite mode)']
        helpFontSize = 25
        helpTextFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', helpFontSize)
        app.helpTextBox = app.createTextBox(helpTextFont, helpFontSize, helpTextList, app.white, app.black, app.blue)
        app.helpTextBoxRect = app.helpTextBox.get_rect()
        app.helpTextBoxRect.centerx = app.screenWidth/2
        app.helpTextBoxRect.centery = app.screenHeight/2

        # Control text box
        controlText = ['Press \'m\' to return to main screen']
        controlFontSize = 20
        controlTextFont = pygame.font.Font('Fonts/EncodeSans-Black.ttf', controlFontSize)
        app.controlTextBox = app.createTextBox(controlTextFont, controlFontSize, controlText, app.white, app.black, app.red)
        app.controlTextBoxRect = app.controlTextBox.get_rect()
        app.controlTextBoxRect.centerx = app.screenWidth/2
        app.controlTextBoxRect.centery = 4*app.screenHeight/5


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
        height = textHeight + 30
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
    

    def processEvent(app, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m: # Go back to main screen if press m key
                return 'MainScreen'
        return 'HelpScreen'
    
    def displayFrame(app):
        app.screen.fill(app.white)
        app.screen.blit(app.helpTextBox, app.helpTextBoxRect)
        app.screen.blit(app.controlTextBox, app.controlTextBoxRect)
        app.screen.blit(app.titleTextBox, app.titleTextBoxRect)
        pygame.display.update()