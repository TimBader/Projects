import pygame
from random import randint
import util;

def getIdxFromList(lst, char):
    i = 0;
    while i < len(lst):
        if lst[i][0] == char:
            return i;
        i+=1;
    return -1;

class nonTileBasedThing(object):
    def __init__(self, imageName, image, pos):
        self.imageName = imageName;
        self.image = image;
        self.pos = pos;
        self.deleteMe = False;
        
    def checkForCollision(self, pos):
        pass;

    def draw(self, surface):
        #pygame.draw.circle(surface,(255,0,0,255),(int(self.pos[0]+32), int(self.pos[1]+32)), int(64/5), True);
        surface.blit(self.image,self.pos);

class layerData(object):
    def __init__(self, layerName, tileTypes, tileBased):
        self.name = layerName;
        self.tileTypes = tileTypes;#copy of all the posible tiles to choose from
        self.tileBased = tileBased;#is the layer tile based or not

class mapLayer(object):
    '''Basicly a copied version of layerData that is more usefull to the tileMap'''
    def __init__(self, layerName, tileTypes, tileBased, tileList, surface):
        self.name = layerName;
        self.tileTypes = tileTypes;
        self.tileBased = tileBased;
        if tileBased:
            self.tileList = tileList;#the list coresponding with column and row positions in which ascii characters can be placed
        else:
            self.tileList = [];
        self.surface = surface;self.surface = self.surface.convert_alpha();

class selectorLayer(object):
    '''Basicly a copied version of layerData that is more usefull to the tileSelector'''
    def __init__(self, layerName, tileTypes, tileSelections, surface):
        self.name = layerName;
        self.tileTypes = tileTypes;
        self.tileSelections = tileSelections;#current possible tile selections
        self.viewTile = 0;self.selectedTile = -1;#what index of tileSelections is being viewed and being selected
        self.surface = surface;

class tileMap(object):
    def __init__(self, layerList, columns, rows, tileWidth=64, tileHeight=64, mapXOffset=0, mapYOffset=0):
        self.cols = columns;self.rows = rows;self.tTotal=self.cols*self.rows;
        self.tW = tileWidth;self.tH = tileHeight;#the width and height of the tiles
        self.mXOff = mapXOffset;self.mYOff = mapYOffset;#the pixel offset from the left top corner of the entire screen
        self.layerList = [];#The list that will hold all the mapLayers
        mw = self.cols*self.tW;mh = self.rows*self.tH;#the map width and height in pixels
        for layer in layerList:#go through all the layers in the given layer list and create mapLayers with layer data and add them to the maps own layer list
            self.layerList.append(mapLayer(layer.name, layer.tileTypes, layer.tileBased, [' ']*self.tTotal, pygame.Surface((mw,mh),pygame.SRCALPHA,32)));
        self.currentLayer = self.layerList[0];#Pointer to the current selected layer
        self.gridShow = True;
        self.gridSurface = pygame.Surface((mw,mh),pygame.SRCALPHA,32)
        self.gridSurface.convert_alpha();

    def drawTile(self, listPos, tileIdx=-1, layer=-1):
        '''Draws the image at the given column and row positions'''
        if layer == -1:
            layer = self.currentLayer;
        colRowPos = self.positionConverter(listPos);
        pygame.draw.rect(layer.surface, (0,0,0,0), (colRowPos[0]*self.tW, colRowPos[1]*self.tH, self.tW, self.tH),False);
        if tileIdx!=-1:#if there is no tileIdx given
            layer.surface.blit(layer.tileTypes[tileIdx][1],(colRowPos[0]*self.tW, colRowPos[1]*self.tH));

    def positionConverter(self, Pos):
        '''Converts given number into column and row positions'''
        return [Pos%self.cols, Pos//self.cols];

    def listPosConverter(self, Pos):
        if isinstance(Pos,int):
            return Pos;
        else:
            return int((Pos[0]-self.mXOff)/self.tW)+int((Pos[1]-self.mYOff)/self.tH)*self.cols

    def updateGrid(self):
        '''shows/not shows grid'''
        i = 0;
        while i < (self.tTotal):
            colRowPos = self.positionConverter(i);
            if self.gridShow:
                pygame.draw.rect(self.gridSurface, (255,255,255), (colRowPos[0]*self.tW, colRowPos[1]*self.tH, self.tW, self.tH),True);
            else:
                pygame.draw.rect(self.gridSurface, (0,0,0,0), (colRowPos[0]*self.tW, colRowPos[1]*self.tH, self.tW, self.tH),False);
            i+=1;
    
    def placeTile(self, Pos, tileIdx=-1, layer=-1):
        '''places the tile denoated by the value at given layer's tileTypes at given tileIdx''' 
        #print('meow')
        if layer == -1:
            layer = self.currentLayer;
        if layer.tileBased:
            listPos = self.listPosConverter(Pos);
            self.setTile(listPos, tileIdx, layer);
            self.drawTile(listPos,tileIdx,layer);
        else:
            n = nonTileBasedThing(layer.tileTypes[tileIdx][0] ,layer.tileTypes[tileIdx][1], (Pos[0]-self.tW/2-self.mXOff,Pos[1]-self.tH/2-self.mYOff));
            n.draw(layer.surface);
            layer.tileList.append(n);

    def deleteNonTileBasedThing(self, Pos, layer=-1):
        if layer == -1:
            layer = self.currentLayer;
        '''
        print(layer);
        print("meow");
        print(layer.tileList);
        '''
        idx = len(layer.tileList)-1;
        while idx >= 0:
        #for thing in layer.tileList:#((x2-x1).2+(y2-y1).2).0.5=d
            dist = (((Pos[0]-self.mXOff)-(layer.tileList[idx].pos[0]+32))**2+((Pos[1]-self.mYOff)-(layer.tileList[idx].pos[1]+32))**2)**0.5;
            if dist < self.tW/5:
                #thing.deleteMe = True;
                layer.tileList.remove(layer.tileList[idx]);
                break;
            idx -= 1;
        self.updateNonTileBasedThings();

    def updateNonTileBasedThings(self, layer=-1):
        if layer == -1:
            layer = self.currentLayer;
        layer.surface.fill((0,0,0,0));
        for thing in layer.tileList:
            thing.draw(layer.surface);
                
    def setTile(self, listPos, tileIdx=-1, layer=-1):
        '''sets the tile at given listPos in given layer's tileList at given tileIdx'''
        if layer == -1:
            layer = self.currentLayer;
        if tileIdx == -1:
            layer.tileList[listPos]=' ';
        else:
            layer.tileList[listPos]=layer.tileTypes[tileIdx][0];

    def getMapString(self):
        '''Converts the tiles into a map string'''
        s = "";
        for layer in self.layerList:
            s+="\nlayer " + str(layer.tileBased) + " " + layer.name + "\n";
            if layer.tileBased:
                i = 0;
                while i < (self.tTotal):
                    if (i)%self.cols == 0 and i != 0:
                        s += "\n"
                    s += layer.tileList[i]
                    i+=1;
            elif layer.tileBased != True:
                #need to collect some info
                #key(name):[[layerOrder,pos],[layerOrder,pos]];
                thingDict = {};
                j = 0;
                while j < len(layer.tileList):
                    if layer.tileList[j].imageName not in thingDict:
                        thingDict[layer.tileList[j].imageName] = [];
                    thingDict[layer.tileList[j].imageName].append([j,layer.tileList[j].pos]);
                    j+=1;
                for thing in thingDict:
                    s+=thing;
                    for j in thingDict[thing]:
                        s+=" "+str(int(j[0]))+","+str(int(j[1][0]))+","+str(int(j[1][1]));
                    s+="\n";
        print(s);
        return s;

    def updateTileMapFromMapList(self, lst, layer):
        '''this updates the tilelist form anouther list of chars like a map'''
        if layer.tileBased:
            i = 0;
            print(len(lst));
            while i < len(lst):
                if lst[i] == '\n':
                    continue;
                self.placeTile(i, getIdxFromList(layer.tileTypes, lst[i]), layer); 
                i+=1;
        else:
            layer.tileList = lst;
            self.updateNonTileBasedThings(layer);

    def loadMap(self, askForSave=True):
        '''Basic mapmaker loading functionality'''
        if askForSave == True:
            if util.ask("Save your work? (Yes/No)"):
                self.saveMap();
        fileName = util.askForFileName();
        if fileName != -1:
            loadedTileLists = util.loadTileLists(fileName);
            i = 0;
            while i < len(loadedTileLists):
                self.updateTileMapFromMapList(loadedTileLists[i],self.layerList[i]);
                i+=1;
        else:
            print("Canceling Load");
    
    def saveMap(self):
        '''Basic map saving functionallity'''
        fileName = input("Save level as (Without .lvl extention)(enter 'x' to cancel): ")
        if fileName == 'x':
            print("Save cancelled");
            return 0;
        fileName += ".lvl"
        filePath = "levels/" + fileName
        try:
            file = open(filePath, 'r');
            found = True;
            file.close();
        except:
            found = False;
        if found:
            answer = util.ask("Level already created.  Overight?: (Yes/No) ");
            if answer == True:
                found = False;
            else:
                print("Save canceled!");
        if found == False:    
            file = open(filePath, 'w')
            mapOutPut = "mapWidth " + str(self.cols) + "\nmapHeight " + str(self.rows) + "\n" + self.getMapString()
            file.write(mapOutPut);
            file.close();
            for layer in self.layerList:
                layer.tileListCatch = util.shallowCopy(layer.tileList);
            print(fileName+" saved");


class tileSelector(object):
    def __init__(self, layerList, tileWidth, tileHeight, selectorXOffset, selectorYOffset,  mapRows):
        self.tW = tileWidth;self.tH = tileHeight;
        self.tWD4 = self.tW>>2;self.tWD8 = self.tW>>3;
        self.tHD4 = self.tH>>2;self.tHD8 = self.tH>>3;
        self.selW = self.tW+self.tWD4;self.selH = self.tH+self.tHD4;
        self.sXOff = selectorXOffset;self.sYOff = selectorYOffset;#Offset form the top left corner of the entire screen
        self.sCols = 2; self.sRows = mapRows//(self.tH+self.tHD4);
        self.surfW = self.sCols*self.selW;self.surfH = self.sRows*self.selH;
        self.sTotal = self.sCols*self.sRows;
        self.layerList = [];#list of all the selector Layers
        for layer in layerList:
            self.layerList.append(selectorLayer(layer.name, layer.tileTypes,[-1]*self.sCols*self.sRows,pygame.Surface((self.surfW,self.surfH),0,32)))
        self.currentLayer = self.layerList[0];

    def select(self, Pos):
        '''Selects the tile at given position'''
        listPos = self.listPosConverter(Pos);
        if listPos >= len(self.currentLayer.tileTypes) or listPos < 0:
            self.currentLayer.selectedTile = -1;
        else:
            self.currentLayer.selectedTile=listPos;
        self.update();

    def positionConverter(self, Pos):
        '''Converts given list position into column and row positions'''
        Pos = Pos-self.currentLayer.viewTile;
        return [Pos%self.sCols, Pos//self.sCols];
    
    def listPosConverter(self, Pos):
        '''Converts given x and y or int postions/position into to the appropiate list position inside ofall the tile selections'''
        if isinstance(Pos, int):
            return self.currentLayer.viewTile+Pos;
        else:
            return self.currentLayer.viewTile+int((Pos[0]-self.sXOff)/self.selW)+int((Pos[1]-self.sYOff)/self.selH)*self.sCols;

    def drawSelector(self, Pos):
        '''draws the selector at the given x and y or int positions/position'''
        listPos = self.listPosConverter(Pos);
        colRowPos = self.positionConverter(listPos);
        backColor = (0,0,0)
        if listPos == self.currentLayer.selectedTile and listPos != -1:
            backColor = (0,115,0);
        pygame.draw.rect(self.currentLayer.surface,backColor,(colRowPos[0]*self.selW, colRowPos[1]*self.selH, self.selW, self.selH),False)
        if listPos >= len(self.currentLayer.tileTypes) or listPos < 0:
            pygame.draw.rect(self.currentLayer.surface,(30,30,30),(colRowPos[0]*self.selW+self.tWD8, colRowPos[1]*self.selH+self.tHD8, self.tW, self.tH),False)           
        else:
            tileImage = self.currentLayer.tileTypes[listPos][1];
            self.currentLayer.surface.blit(tileImage,(colRowPos[0]*self.selW+self.tWD8, colRowPos[1]*self.selH+self.tHD8));

    def update(self):
        '''Updates all the selector tiles'''
        i = 0;
        while i < self.sTotal:
            self.drawSelector(i);
            i+=1;

    def moveSelection(self, direction):
        '''Moves the top right viewed selector tile in a direction positive or negative based on sign of given direction value'''
        if direction < 0:
            self.currentLayer.viewTile-=self.sCols;
        else:
            self.currentLayer.viewTile+=self.sCols;
