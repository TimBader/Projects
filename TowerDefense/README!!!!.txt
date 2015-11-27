Keys have been changed with multiple directions
Added tile engine integration:

Press T to place a tower at the mouse position

Simply create a new .tmx file from the Tiled map maker and put it in the levels folder:
***Make sure you use the same TilesetFull.png for every level
***Bug: the enemies atm will only spawn at the 5th row , so make sure the level has height (in number of tiles) of at least 5
In the tile set every tile is given a number in rows from left to right starting at one.  So the tile in the top left corner is 1. The next one in that row is 2.
When the game runs the tile engine will create a list of rows in which the rows is another list containing the number associated with the tile  
The tile engine will create a background surface and will blit that surface containing the level and where the tiles go to the screen as the background
If a new tile has been added to the TilesetFull.png that indications a new path direction/s. Go add the number of that tile to the Key Library and give that key a list of the direction/s of that tile:

As an example. I just drew a new T shaped tile and I added it to the TilesetFull.png.  I also created a new level using the Tiled map creator called LevelAwesome.tmx .
So i need to manually count the tile's number inside of the TilesetFull.png.  The number of my new tile turned out to be 25.
Now i also need to figure out all the directions in degrees the Tshaped tile uses.  In this case it is 0, 270, and 180.
Next i need to go into the code and find TMapDtileKey library on Line 374 in the main.py . Then manually append tile'snumber:[direction/s] as 25:[0, 270, 180] to the end of the library

previously:
TMapDtileKey = {1:[0, 270], 3:[180, 270], 17:[90, 0], 19:[90, 180]}

after:
TMapDtileKey = {1:[0, 270], 3:[180, 270], 17:[90, 0], 19:[90, 180], 25:[0, 180, 270]}

To load the new level make sure the level is in the levels folder in the game's directory and find the line: //line 362 in the main.py
TMap.initializeNewMap("LevelAwesome")

Then just replace your lv's name within the "qoutes" with out the .tmx extention like above

and it shouldwork!


It "smartly" chooses what direction to go based off of current direciton

enemy going right - Collides with Direciton tile with Left, Down direction - will choose Down every the time instead of choosing the backwards direciton 

direction choosen will be anyone of the direciton tiles but the one going in the opposite direction, logicly


Press one of the keys listed to place a direction tile at the mouse's possition snapped to a grid

Direction order doesn't matter
Q ~ Down, Right
W ~ Up
E ~ Down, Left
D ~ Right
C ~ Up, Left
X ~ Down
Z ~ Up, Right
A ~ Left
S ~ Up, Down, Right, Left, UpRight, DownRight, DownLeft, UpLeft - All the directions


To add a new direction tile Copy and paste this code right after all the other code in the main loop
Change the type of key where "pygame.K_z" is.
Change the directions, in degrees, in the last list. That is the list of all the directions the tile uses 


        if evt.key == pygame.K_z:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[90, 0]]);

^ Looking at the code, a new direction tile will be added to the list of direction tiles
with the [0] = position of the mouse and [1] = list of directions for the direction tile to use