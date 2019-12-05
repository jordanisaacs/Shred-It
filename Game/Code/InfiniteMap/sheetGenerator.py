import random
import pygame
from ..GameClasses.PlayerSprite import Player
from ..GameClasses.CliffSprite import Cliff
from ..GameClasses.TreeSprite import Tree

# Randomly generates a sheet that will be used for infinite scrolling in the gameMode

def sheetGenerator(screenWidth, sheetLength, yOffset):
    # Set map list
    mapList = []

    group = pygame.sprite.Group()

    # Maybe initialize the largest cliff (type 4) at a random location
    largestCliffInit = random.choice([True, False])
    if largestCliffInit:
        # Random x and y
        xRange = (250, screenWidth-250)
        x = random.randrange(xRange[0], xRange[1])
        yRange = (yOffset+225, yOffset+sheetLength)
        y = random.randrange(yRange[0], yRange[1])

        # Initalize and also turn it into a sprite to be able to do collision detection (do not want overlapping sprites)
        cliffInit = ('Cliff', [4, x, y])
        cliff = Cliff(cliffInit[1])
        group.add(cliff)
        mapList.append(cliffInit)
    
    # Initalize large cliffs (type 2) and check to make sure no overlap
    if largestCliffInit:
        count = random.randrange(1, 3)
    else:
        count = random.randrange(2, 5)
    i = 0
    while i < count:
        # Random x and y
        xRange = (175, screenWidth-175)
        x = random.randrange(xRange[0], xRange[1])
        yRange = (yOffset+225, yOffset+sheetLength)
        y = random.randrange(yRange[0], yRange[1])

        # Initalize and also turn it into a sprite to be able to do collision detection (do not want overlapping sprites)
        cliffInit = ('Cliff', [3, x, y])
        cliff = Cliff(cliffInit[1])
        if pygame.sprite.spritecollide(cliff, group, dokill=False):
            continue
        else:
            i += 1
            group.add(cliff)
            mapList.append(cliffInit)
    
    # Initalize mid size cliffs (type 3)
    if largestCliffInit:
        count = random.randrange(3, 6)
    else:
        count = random.randrange(2, 4)
    i = 0
    while i < count:
        # Random x and y
        xRange = (150, screenWidth-150)
        x = random.randrange(xRange[0], xRange[1])

        yRange = (yOffset+175, yOffset+sheetLength)
        y = random.randrange(yRange[0], yRange[1])

        # Initalize and also turn it into a sprite to be able to do collision detection (do not want overlapping sprites)
        cliffInit = ('Cliff', [3, x, y])
        cliff = Cliff(cliffInit[1])
        if pygame.sprite.spritecollide(cliff, group, dokill=False):
            continue
        else:
            i += 1
            group.add(cliff)
            mapList.append(cliffInit)

    # Initalize small cliffs (type 1)
    if largestCliffInit:
        count = random.randrange(2, 4)
    else:
        count = random.randrange(3, 6)
    i = 0
    while i < count:
        # Random x and y
        xRange = (40, screenWidth-40)
        x = random.randrange(xRange[0], xRange[1])
        yRange = (yOffset+125, yOffset+sheetLength)
        y = random.randrange(yRange[0], yRange[1])
        cliffInit = ('Cliff', [1, x, y])
        cliff = Cliff(cliffInit[1])
        if pygame.sprite.spritecollide(cliff, group, dokill=False):
            continue
        else:
            i += 1
            group.add(cliff)
            mapList.append(cliffInit)
    
    # Initalize tree options
    treeTypes = [1, 2, 3]
    count = random.randrange(5, 15)
    i = 0
    if count > 10:
        treeScale = (0.5, 1.5)
    else:
        treeScale = (1, 2)
    while i < count:
        # Random scale and tree type
        scale = random.uniform(treeScale[0], treeScale[1])
        treeType = random.choice(treeTypes)
        
        # Random x and y
        xRange = (40, screenWidth-40)
        x = random.randrange(xRange[0], xRange[1])
        yRange = (yOffset+125, yOffset+sheetLength)
        y = random.randrange(yRange[0], yRange[1])

        # Initalize and also turn it into a sprite to be able to do collision detection (do not want overlapping sprites)
        treeInit = ('Tree', [treeType, scale, x, y])
        tree = Tree(treeInit[1])
        if pygame.sprite.spritecollide(tree, group, dokill=False):
            continue
        else:
            i += 1
            group.add(tree)
            mapList.append(treeInit)

    return mapList