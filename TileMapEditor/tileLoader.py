#Minesweeper
import pygame
import util
from random import randint
from time import time
from os import listdir
from os import walk

def findAllFiles(path=""):
    f = [];
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames);
        break;
    return f;

def getBankedData(file, getASCII=True, printMe=False):
    '''Returns a list containing a list of all the names and a coresponding list of ascii character representations'''
    if getASCII:
        nameCatch = [];asciiCatch = [];
        for line in file:
            lineSplitted = line.split()
            if (len(lineSplitted) != 2):
                raise ImportError("Yo! The file is messed up!");
            if (len(lineSplitted[1]) != 1):
                raise ImportError("YO! Something is wrong with how the file is layed out, delete the bank file and create a new one");
            nameCatch.append(lineSplitted[0])
            asciiCatch.append(lineSplitted[1])
            if printMe:
                print(lineSplitted[0] + " " + lineSplitted[1])
        return [nameCatch, asciiCatch];
    else:
        nameCatch = [];
        for line in file:
            lineSplitted = line.split();
            nameCatch.append(lineSplitted[0]);
            if printMe:
                print(lineSplitted[0]);
        return [nameCatch];

'''
def changeMaps(path, removeList, layerName, printMe=False):
    if printMe:
        print("Re-edititing maps")
    levels = findAllFiles(path);
    for levelName in levels:
        levelFile = open(path+levelName, "r")
        writeOut = "";
        changed = False;
        mapWidth = 0;mapHeight = 0;
        lineStall = 0;
        for line in levelFile:
            if lineStall > 0:
                for char in line:
                    deleteMe = False;
                    for i in removeList:
                        if char == i:
                            changed = True;
                            deleteMe = True;
                            break;
                    if deleteMe:
                        writeOut+=" ";
                    else:
                        writeOut+=char;
                lineStall-=1;
            else:
                writeOut += line;
                lineSplited = line.split();
                if len(lineSplited) > 1:
                    if lineSplited[0] == "mapHeight":
                        mapHeight = lineSplited[1];
                    elif lineSplited[0] == "layer":
                        if lineSplited[2] == layerName:
                            lineStall = int(mapHeight);
        if changed == True:
            if printMe:
                print(levelName + " has been changed");
                print(writeOut);
            levelFile.close();
            levelFile = open(path+levelName, "w")
            levelFile.seek(0);
            levelFile.truncate();
            levelFile.write(writeOut);
        levelFile.close();
'''

'''
def writeOutBank(fileNames, writeOutFile, nameCatch, asciiCatch, printMe=False):
    if printMe:
        print("\n")
    writeOut = "";
    for i in fileNames:
        found = 0;
        ii = 0;
        while ii < len(nameCatch):
            if i == nameCatch[ii]:
                found = 1;
                writeOut += nameCatch[ii] + " " + asciiCatch[ii] + "\n"
            ii+=1;
        if found == 0:
            if printMe:
                print("Creating ascii representation for " + i)
            c = 33;
            while c < 126:
                #print(c)
                gotOne = 0;
                for cc in asciiCatch:
                    if cc == chr(c):
                        gotOne = 1;
                        break;
                if gotOne == 0:
                    asciiCatch.append(chr(c));  #So this ascii charactor doesnt get picked again
                    writeOut += i + " " + chr(c) + "\n";
                    break;
                c += 1;
                if c == 125:
                    raise IOError("Yo! U ran out of applicable spots for")

    if printMe:
        print("\nThis stuff if being written out:");
        print(writeOut)
        print("Hurray! Things done did right!");
    writeOutFile.seek(0)
    writeOutFile.truncate();
    writeOutFile.write(writeOut);
'''

def changeMaps(layerName, removedItems, tileBased=True,printMe=False):
    if printMe:
        print("Re-edititing maps")
    levels = findAllFiles("levels/");
    for levelName in levels:
        levelFile = open("levels/"+levelName, "r")
        editing = False;#is it editing currently
        writeOut = "";
        for line in levelFile:
            lineSplit = line.split();
            if editing:
                if len(lineSplit) > 0:
                    if lineSplit[0] == "layer":
                        editing = False;
                        writeOut += line;
                        continue;
                if tileBased:
                    for char in line:
                        found = False;
                        for item in removedItems:
                            if char == item:
                                found = True;
                                writeOut += " ";
                                break;
                        if found == False:
                            writeOut += char;
                else:
                    if len(lineSplit)>0:
                        found = False;
                        for item in removedItems:
                            if lineSplit[0] == item:
                                #possibly remove item from list for preformance
                                found = True;
                                break;
                        if found == False:
                            writeOut += line;
                
            elif len(lineSplit) > 0:
                if lineSplit[0] == "layer":
                    if lineSplit[2] == layerName:
                        editing = True;
                writeOut += line;
            else:
                writeOut += line;
        print(writeOut);
        levelFile.close();
        levelFile = open("levels/"+levelName, "w")
        levelFile.seek(0);
        levelFile.truncate();
        levelFile.write(writeOut);
        levelFile.close();

                            
                    
                            

def checkBankForUpdate(bankName, foundData, tileBased=True, printMe=False):
    '''checks the bank with the given bank name to see if anything from the given list, found data, has been added or removed'''    
    #images = findAllFiles("art/"+fileName+"/");
    bankFile = open(bankName+".txt","r+");
    if tileBased:
        bankedData = getBankedData(bankFile);
        bankedNames = bankedData[0];bankedASCIIs = bankedData[1];
        addedNames = util.shallowCopy(foundData);#Figure out what has been added
        addedNames = util.deleteSimularItems(bankedNames, addedNames);
        removedNames = util.shallowCopy(bankedNames);#Figure out what has been removed
        removedNames = util.deleteSimularItems(foundData, removedNames);
        removedASCIIs = []
        for i in removedNames:
            if printMe:
                print(i + " has been removed, removing ascii representation from pool")
            removedASCIIs.append(bankedASCIIs.pop(bankedNames.index(i)));#Removes it from the other an adds it to the removed list
            bankedNames.pop(bankedNames.index(i));
        if len(removedASCIIs) > 0:
            print("TILEBASED:"+str(removedASCIIs));
            changeMaps(bankName,removedASCIIs);
        asciiCatch = getNewASCIIs(addedNames, bankedASCIIs, printMe);
        for name in addedNames:
            bankedNames.append(name);
        writeOutBank(bankFile, bankedNames, bankedASCIIs, printMe);
        #bankedNames = util.deleteSimularItems(removedNames, bankedNames);
        #writeOutBank(foundData, bankFile, bankedNames, bankedASCIIs)
    else:
        bankedNames = getBankedData(bankFile, False)[0];
        print("\n")
        print(bankedNames)
        print("\n")
        addedNames = util.shallowCopy(foundData);
        addedNames = util.deleteSimularItems(bankedNames, addedNames);
        removedNames = util.shallowCopy(bankedNames);
        removedNames = util.deleteSimularItems(foundData, removedNames);
        bankedNames = util.deleteSimularItems(removedNames, bankedNames);
        for name in addedNames:
            bankedNames.append(name);
        if len(removedNames) > 0:
            print("NON TILEBASED: "+str(removedNames));
            changeMaps(bankName, removedNames, False)
        writeOutBank(bankFile, bankedNames, -1, printMe);
    bankFile.close();

def writeOutBank(writeOutFile, nameCatch, asciiCatch=-1, printMe=False):
    idx = 0;writeOut = "";
    while idx < len(nameCatch):
        writeOut +=  nameCatch[idx];
        if asciiCatch != -1:
            writeOut += " " + asciiCatch[idx];
        writeOut += "\n";
        idx+=1;
    if printMe:
        print("\nThis stuff if being written out:");
        print(writeOut)
        print("Hurray! Things done did right!");
    writeOutFile.seek(0)
    writeOutFile.truncate();
    writeOutFile.write(writeOut);

def getNewASCIIs(newNames, asciiCatch, printMe=False):
    for name in newNames:
        if printMe:
            print("Creating ascii representation for " + name)
        c = 33;
        while c < 126:
            #print(c)
            found = 0;
            for cc in asciiCatch:
                if cc == chr(c):
                    found = 1;
                    break;
            if found == 0:
                asciiCatch.append(chr(c));  #So this ascii charactor doesnt get picked again
                break;
            c += 1;
            if c == 125:
                raise IOError("Yo! U ran out of applicable spots for new items")
    return asciiCatch;

'''
def writeOutBank(writeOutFile, nameCatch, asciiCatch=-1, printMe=False):
    if printMe:
        print("\n")
    writeOut = "";
    idx = 0;
    for i in nameCatch:
        writeOut += i;
        +"\n";
    if printMe:
        print("\nThis stuff if being written out:");
        print(writeOut)
        print("Hurray! Things done did right!");
    writeOutFile.seek(0)
    writeOutFile.truncate();
    writeOutFile.write(writeOut);
'''





            
