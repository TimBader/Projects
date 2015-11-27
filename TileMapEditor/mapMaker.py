from random import randint;
from time import time;
from os import listdir;
from os import walk;
import pygame;
import tileLoader;
import classes;
import util;

def drawPausedDialogueBox(surface, centerX,centerY,font,text,extXOffset=0):
    s = font.size(text);
    extXOffset -= s[0]//2;
    pygame.draw.rect(surface,(0,0,0),(centerX-130, centerY-55,260,110));
    pygame.draw.rect(surface,(255,255,0),(centerX-130, centerY-55,260,110),4);
    drawText = font.render(text, True, (255, 255, 0))
    surface.blit(drawText, (centerX+extXOffset, centerY-s[1]//2));
    pygame.display.flip();

#InitVaribles
### Game Initialization
tW = 64
tH = 64
cols = 14 #14
rows = 10 #10            
mapWidth = tW*cols;
mapHeight = tH*rows;
mapXOffset = 3*tW;
mapYOffset = 1*tH;
windowW = mapWidth+mapXOffset;
windowH = mapHeight+mapYOffset;
timeS = time();

#testinz
allLayersList=[["backgrounds",True],["decals",False],["tileBasedObjects",True],["entities",False]];

LAYERLIST = [];
for l in allLayersList:
    tileType = [];
    tileLoader.checkBankForUpdate(l[0],tileLoader.findAllFiles("art/"+l[0]+"/"),l[1], True);
    tmp = tileLoader.getBankedData(open(l[0]+ ".txt","r+"), l[1], True);
    nameCatch = tmp[0];
    #if l[1]:
    #    asciiCatch = tmp[1];
    i = 0
    while i < len(nameCatch):
        img = pygame.image.load("art/" + l[0] + "/" + str(nameCatch[i]));
        if l[1]:
            tileType.append([tmp[1][i],pygame.transform.scale(img,(tW,tH))])
        if l[1] == False:
            print(nameCatch[i])
            tileType.append([nameCatch[i],pygame.transform.scale(img,(tW,tH))]);
        i+=1;
    LAYERLIST.append(classes.layerData(l[0], tileType, l[1]));

window = pygame.display.set_mode((windowW, windowH));
    
pygame.font.init();
GameFont = pygame.font.SysFont(None, 40)
    
TileMap = classes.tileMap(LAYERLIST, cols, rows, tW, tH, mapXOffset, mapYOffset);
TileMap.updateGrid();
TileSelector = classes.tileSelector(LAYERLIST, tW,tH,tW/4,mapYOffset, rows*tH);

gridShow = 1;

TileSelector.update();

mouseDown = -1;
prevMouseListPos = [];

currentLayerIdx = 0;

print("\nMap Making ready!")
print("\nControls:  \n<mouseLeft>: select/place selected tile down at mouse position, \n<mouseRight>: remove tile at mouse position, \n<ScrollDown,Up arrow key,ScrollUp,Down arrow key>: move selection up/down respectivly, \n<w, x>: switch between layers respectivly, \n<g>: turn on/off grid, \n<s>: save map, \n<l>: load in map");

end = False
#Main Game Loop
while end == False:
    #Updates
    dtime = time()-timeS;
    timeS = time();

    evtList = [];
    evtList.append(pygame.event.poll());
    for evt in evtList:
        if evt.type == pygame.QUIT:
            end = True;
            break;
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_s:
                drawPausedDialogueBox(window, int(windowW/2),int(windowH/2),GameFont,"Saving");
                TileMap.saveMap();
            if evt.key == pygame.K_DOWN:
                TileSelector.moveSelection(-1);
                TileSelector.update();
            if evt.key == pygame.K_UP:
                TileSelector.moveSelection(1);
                TileSelector.update();
            if evt.key == pygame.K_l:
                drawPausedDialogueBox(window, int(windowW/2),int(windowH/2),GameFont,"Loading");
                TileMap.loadMap();
            if evt.key == pygame.K_w:
                if currentLayerIdx+1 < len(LAYERLIST):
                    currentLayerIdx += 1;
                    TileMap.currentLayer = TileMap.layerList[currentLayerIdx];
                    TileSelector.currentLayer = TileSelector.layerList[currentLayerIdx];
                    TileSelector.update();
            if evt.key == pygame.K_x:
                if currentLayerIdx-1 >= 0:
                    currentLayerIdx -= 1;
                    TileMap.currentLayer = TileMap.layerList[currentLayerIdx];
                    TileSelector.currentLayer = TileSelector.layerList[currentLayerIdx];
                    TileSelector.update();
            if evt.key == pygame.K_g:
                if TileMap.gridShow == 0:
                    TileMap.gridShow = 1;
                else:
                    TileMap.gridShow = 0;
                TileMap.updateGrid();
        if evt.type == pygame.MOUSEBUTTONDOWN and mouseDown == -1:        
            if evt.button == 1 or evt.button == 3:
                mpos = [evt.pos[0], evt.pos[1]];
                if TileMap.currentLayer.tileBased:
                    mouseDown = evt.button;
                elif mpos[0] >= mapXOffset and mpos[1] >= mapYOffset:
                    if evt.button == 1:
                        TileMap.placeTile(mpos, TileSelector.currentLayer.selectedTile)
                    else:
                        TileMap.deleteNonTileBasedThing(mpos);
                if mpos[0] >= tW/4 and mpos[0] < tW/4+TileSelector.surfW and mpos[1] >= mapYOffset and mpos[1] <= mapYOffset+TileSelector.surfH:
                    TileSelector.select(mpos);
        if evt.type == pygame.MOUSEBUTTONUP:
            if evt.button == 4:
                TileSelector.moveSelection(-1);
                TileSelector.update();
            elif evt.button == 5:
                TileSelector.moveSelection(1);
                TileSelector.update();
            elif evt.button == 1 or evt.button == 3:
                prevMouseListPos = [];
                mouseDown = -1;

    if mouseDown != -1:
        mpos = list(pygame.mouse.get_pos());
        if mpos[0] >= mapXOffset and mpos[1] >= mapYOffset:
            listPos = TileMap.listPosConverter(mpos);
            found = False;
            for i in prevMouseListPos:
                if i == listPos:
                    found = True;
                    break;
            if found == False:
                if mouseDown == 1:
                    TileMap.placeTile(listPos, TileSelector.currentLayer.selectedTile);                    
                else:
                    TileMap.placeTile(listPos, -1);                    
                prevMouseListPos.append(listPos);

    #Render
    window.fill((0,0,0));
    for layer in TileMap.layerList:
        window.blit(layer.surface,(mapXOffset,mapYOffset));            
    window.blit(TileMap.gridSurface,(mapXOffset,mapYOffset));
    window.blit(TileSelector.currentLayer.surface,(tW/4,mapYOffset));
    pygame.display.flip();

pygame.quit();
    
