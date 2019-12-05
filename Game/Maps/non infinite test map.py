# Initalize a map profile
def initMap(screenWidth, screenHeight):
    # Game length is 2000
    gameLength = 2000

    # Set player start coords
    playerStartCoords = (screenWidth/2, screenHeight/9)

    # set the list of map sprites to an empty list
    mapList = []

    # Append cliffs
    mapList.append(('Cliff', [2, 3*screenWidth/4, screenHeight/3]))
    mapList.append(('Cliff', [1, 3*screenWidth/4, 3*screenHeight/4]))
    mapList.append(('Cliff', [4, screenWidth/4, 4*screenHeight/5]))
    mapList.append(('Cliff', [3, screenWidth/2, 2*gameLength/3]))

    # Append trees
    mapList.append(('Tree', [1, 2, screenWidth/3, 4*gameLength/5]))
    mapList.append(('Tree', [3, 1.5, screenWidth/2, screenHeight/2]))
    mapList.append(('Tree', [2, 4, screenWidth/3, gameLength/2]))

    
    # Return a map initialization tuple
    gameMap = ('load', gameLength, playerStartCoords, mapList)
    return gameMap