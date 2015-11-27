from math import radians, cos, sin

def listPop(List, Count):
    newList = List[:Count] + List[Count+1:]
    return newList

# finding where direction tiles should be placed
def dtileSearch(Controller_Obj, TileList, dtileKey):
    y_count = 0
    for a in TileList:
        x_count = 0
        for b in a:
            x = x_count*64
            y = y_count*64
            for c in dtileKey:
                if c == b:
                    Controller_Obj.dirtilelist.append([[x+32,y+32], dtileKey[c]]);
            x_count += 1
        y_count += 1

def spawntileSearch(Controller_Obj, TileList, spawntileKey):
    y_count = 0
    for a in TileList:
        x_count = 0
        for b in a:
            x = x_count*64
            y = y_count*64
            for c in spawntileKey:
                if c == b:
                    Controller_Obj.SpawnLocation.append([[x+32+cos(radians(spawntileKey[c]-180))*64,y+32-sin(radians(spawntileKey[c]-180))*64], spawntileKey[c]]);
            x_count += 1
        y_count += 1

