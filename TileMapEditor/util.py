import pygame;
import classes;

def shallowCopy(Lst):
    '''Does a shallow copy of the given list'''
    returnList = [];
    for i in Lst:
        returnList.append(i);
    return returnList;

def ask(txt, positiveValueList=["yes","y","yep"], lowerCase=True):
    '''This willl ask the user the given question,
       will return True if user input matches something inside of given positiveValue list,
       will not convert user input into lowerCase form if told not to'''
    inp = input(txt);
    if lowerCase:
        inp = inp.lower();
    for i in positiveValueList:
        if inp == i:
            return True;
    return False;

def askForFileName():
    "If no file is given, ask the user for file's name"
    fileName = input("Load level (Without .lvl extention)(enter 'x' to cancel): ");
    if fileName == 'x':
        return -1;
    return fileName
'''
def loadTileLists(fileName):
    This will load the tile lists from the given level name
    try:
        file = open("levels/" + fileName + ".lvl", 'r');
    except:
        raise IOError(fileName + ".lvl has some problems loading in");
    layerTileLists = [];
    mapW = 0;mapH = 0;
    listLineStall = 0;
    for line in file:
        #print(line)
        if listLineStall == 0:
            lineSplit = line.split();
            if len(lineSplit) > 1:
                #print(lineSplit);
                if lineSplit[0]=="mapWidth":
                    mapW=int(lineSplit[1]);
                elif lineSplit[0]=="mapHeight":
                    mapH=int(lineSplit[1]);
                elif lineSplit[0]=="layer":
                    if lineSplit[1] == "True":
                        listLineStall = mapH;
                        currentTileList = [];
        else:
            for char in line:
                if char == '\n':
                    break;
                currentTileList.append(char);
            listLineStall-=1;
            if listLineStall == 0:
                layerTileLists.append(currentTileList);
            
    file.close();
    print("File done loading");    
    return layerTileLists; 
'''
def loadTileLists(fileName):
    '''This will load the tile lists from the given level name'''
    try:
        file = open("levels/" + fileName + ".lvl", 'r');
    except:
        raise IOError(fileName + ".lvl has some problems loading in");
    layerTileLists = [];
    currentLayerName = "";
    tmpList = [];
    layerType = -1;
    for line in file:
        lineSplit = line.split();
        #print("ls: "+str(lineSplit)+'\ntL: '+str(tmpList));
        if len(lineSplit) > 1:
            if lineSplit[0]=="layer":
                if layerType != -1:
                    #print(tmpList);
                    if layerType == 0:
                        layerTileLists.append(currentTileList);
                        #print("\n");print(currentTileList);print("\n");
                    elif layerType == 1:
                        i = 0;l = 0;
                        for j in tmpList:
                            if int(j[0]) > l:
                                l = int(j[0]);
                        while i <= l:
                            for j in tmpList:
                                if int(j[0]) == i:
                                    img = pygame.image.load("art/" + currentLayerName + "/" + j[1]);
                                    c = classes.nonTileBasedThing(j[1],img,[int(j[2]),int(j[3])]);
                                    currentTileList.append(c);
                                    tmpList.remove(j);
                                    break;
                            i+=1;
                        #print(currentTileList);
                        layerTileLists.append(currentTileList);
                if lineSplit[1] == "True":
                    layerType = 0;
                else:
                    layerType = 1;
                currentLayerName = lineSplit[2];
                currentTileList = [];
                tmpList = [];
            else:
                if layerType == 0:
                    for char in line:
                        if char == '\n':
                            break;
                        currentTileList.append(char);
                elif layerType == 1:
                    #print(str(lineSplit)+"\n");
                    idx = 1;
                    while idx < len(lineSplit):
                        elementSplit = lineSplit[idx].split(',');
                        tmpList.append([elementSplit[0],lineSplit[0],elementSplit[1],elementSplit[2]]);
                        #print('tttl: ' + str(tmpList))
                        idx+=1;
        elif layerType == 0:
            for char in line:
                if char == '\n':
                    break;
                currentTileList.append(char);
    if layerType == 0:
        layerTileLists.append(currentTileList);
        #print("\n");print(currentTileList);print("\n");
    elif layerType == 1:
        i = 0;l = 0;
        for j in tmpList:
            if int(j[0]) > l:
                l = int(j[0]);
        while i <= l:
            for j in tmpList:
                if int(j[0]) == i:
                    img = pygame.image.load("art/" + currentLayerName + "/" + j[1]);
                    c = classes.nonTileBasedThing(j[1],img,[int(j[2]),int(j[3])]);
                    currentTileList.append(c);
                    tmpList.remove(j);
                    break;
            i+=1;
        #print(currentTileList);
        layerTileLists.append(currentTileList);
        
    for i in layerTileLists:
        print('\n');print(i);print('\n');
    return layerTileLists;                     
        
                    
def getImageFromASCIIValue(char, tileBank):
    '''This will get the image that is tied to the ascii value in the bank
       returns -1 if it is char'''
    if char == ' ':
        return -1;
    else:
        for i in tileBank:
            if i[0] == char:
                return i[1];
    raise IOError("Ahh something really fucked up, Your tileBank doesnt contain the acii value given");

def shallowCopy(lst):
    '''Creates a shallow copy of given list'''
    r = [];
    for i in lst:
        r.append(i);
    return r;

def deleteSimularItems(staticList,changingList):
    '''This will delete the simular items from the given changingList if it exists in the given staticList'''
    for i in staticList:
        for j in changingList:
            if i == j:
                changingList.remove(j);
                break;
    return changingList;
