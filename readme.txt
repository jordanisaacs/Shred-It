----------------------------
|   Welcome to Shred-it!   |
----------------------------
Created by Jordan Isaacs and inspired by Gnarshmallow

----------------------------
|         Description          |
----------------------------
A top down ski simulator with semi-realistic physics where you can hit cliffs and do tricks. You can play with one of the pre-built maps or make one yourself (see below) and share it with friends!
The origins of the Shred-it name can be traced back to a paper shredding company in my hometown of Seattle. Their fleet of trucks roamed the streets always inspiring us to go big and Shred-it!

----------------------------
|      Running Shred-it!     |
----------------------------
- Open the game folder and run 'startGame.py'

----------------------------
|     Required Libraries    |
----------------------------
- External: pygame
- Internal: re, importlib, tkinter, math, copy, random

----------------------------
|          Commands          |
----------------------------
In Map Preview:
- R to reload map
- L to prompt to load a new map
- M to return to main screen
- P to play game (Only if a valid map)

In Game:
- P to pause game (Only can be done when in middle of game, use the pause menu to exit an infinite map)
- R to restart map (Only can be done when reach end of map or in the pause menu)
- M to return to main screen (Only can be done when reach end of map or in the pause menu)
- B to show/hide collision boxes (Displays all the extra collision boxes in the game, for debugging and visualizing collision development)

----------------------------
|    Programming Maps    |
----------------------------
Template (Map files MUST end in map.py):
def initMap(screenWidth, screenHeight):
	gameLength = XXXXXX
	playerStartCoords = (center x,  center y)
	mapList = []
	mapList.append(map item)
	gameMap = (mapType, gameLength, playerStartCoords, mapList)
	return gameMap

Player Coords:
Player center y must in the top half of the screen

MapType Options:
'load' will just load the map once (not infinite scroll)
'infiniteload' will seamlessly generate the map again once reach the end (infinite scroll)

Cliff Items:
Cliff Type 1 is a 20 footer
Cliff Type 2 is a 75 footer
Cliff Type 3 is a 40 footer
Cliff Type 4 is a 100 footer
Appending a cliff: ('Cliff', [type number, center x, center y])

Tree Items:
Check tree folder in Game/Sprites/Map/Trees for different looking trees and their type number
Can scale them to different sizes
Appending a tree: ('Tree', [type number, scale, center x, center y])