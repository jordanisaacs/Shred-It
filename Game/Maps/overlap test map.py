# Initalize a map profile
def initMap(screenWidth, screenHeight):
    # Game length is 2000
    gameLength = 2000

    # Set player start coords
    playerStartCoords = (screenWidth/2, screenHeight/2)

    # set the list of map sprites to an empty list
    mapList = []

    # Append a type 2 cliff
    mapList.append(('Cliff', [2, screenWidth/3, gameLength/2]))

    # Append in a loop a type 1 cliff
    for y in range(300, gameLength, 300):
        mapList.append(('Cliff', [1, 3*screenWidth/4, y]))
    
    # Append a tree
    mapList.append(('Tree', [1, 2, screenWidth/3, 4*gameLength/5]))
   
    # Commented code for demonstrating overlapping features and live reloading
    mapList.append(('Tree', (1, 1.5, screenWidth/2, screenHeight/2)))
    
    # Return a map initialization tuple
    gameMap = ('load', gameLength, playerStartCoords, mapList)
    return gameMap