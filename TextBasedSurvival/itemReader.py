#itemReader

#[['Wooden Handle', 'Wooden Handles'], 0,"Its a comfortable-to-hold carved wooden handle", 'Material', [ ['Crafting', 'You spend some time wittleing away at the stick until you create a confortable wooden handle', 'Knife', [['Stick', 1]], 1, [['Wood Shaving', 1]] ] ]],
# [ ['Crafting', 'You spend some time wittleing away at the stick until you create a confortable wooden handle', 'Knife', [['Stick', 1]], 1, [['Wood Shaving', 1]] ] ]

def getStartItemList(fileName):
    file = open(fileName, 'r')
    itemList = []
    item = [[0,0],0,0,0,0]
    craft = ['Crafting',0,0,0,0,0]
    otherNameCount = 0
    craftRecipeAmount = 0
    craftItem = [0,0]
    craftRecipeLst = []
    craftOtherAmount = 0
    craftOtherLst = []
    #Not the same ^^ for below
    otherName = [0,0]
    otherNameLst = []
    newItem = 0
    newCraft = 0
    craftForItem = 0
    for line in file:
        #Skipping Lines
        if line[0] == '/' and line[1] == '/':
            continue;
        if line[0] == '-':
            if line[1] == 'i':
                newItem = 1
                continue;
            if line[1] == 'c':
                newCraft = 1
                continue;
            if line[1] == 'd':
                if newItem:
                    newItem = 0
                    itemList.append(item)
                    item = [[0,0],0,0,0,0]
                if newCraft:
                    newCraft = 0
                    #print(itemList)
                    for i in itemList:
                        if i[0][0] == craftForItem or i[0][1] == craftForItem:
                            if i[4] == 0:
                                i[4] = [craft]
                                #print('buckets')
                                #print(i[4])
                            else:
                                i[4].append(craft)
                            break;
                    craft = ['Crafting',0,0,0,0,0]

        if newCraft == 1:
            l = seperateLine(line)
            stat = l[0]
            statValue = l[1]

            l = something(craftRecipeAmount, 'elementName', 'elementNumRq', stat, statValue, 1, 0, craftItem, craftRecipeLst, craft, 3)
            craftRecipeAmount = l[0]
            craftItem = l[1]
            craftRecipeLst = l[2]
            craft = l[3]

            l = something(craftOtherAmount, 'craftOtherName', 'craftOtherNum', stat, statValue, 1, 0, craftItem, craftOtherLst, craft, 5)
            craftOtherAmount = l[0]
            craftItem = l[1]
            craftOtherLst = l[2]
            craft = l[3]          
    
            if stat == 'craftForItem':
                craftForItem = statValue
            if stat == 'craftDialogue':
                craft[1] = statValue
            if stat == 'craftClassReq':
                craft[2] = statValue
            if stat == 'recipeElementAmount':
                craftRecipeAmount = 2*int(statValue)
            if stat == 'recipeCreateAmount':
                craft[4] = int(statValue)
            if stat == 'craftOtherAmount':
                craftOtherAmount = 2*int(statValue)
            
        if newItem == 1:
            l = seperateLine(line)
            stat = l[0]
            statValue = l[1]

            l = something(otherNameCount, 'otherName', 'otherNamePuralCase', stat, statValue, 0, 1, otherName, otherNameLst, item, 1)
            otherNameCount = l[0]
            otherName = l[1]
            otherNameLst = l[2]
            item = l[3]

            if stat == 'itemName':
                item[0][0] = statValue
            if stat == 'itemPuralCase':
                item[0][1] = statValue
            elif item[0][0] != 0 and item[0][1] == 0:
                item[0][1] = item[0][0]
            if stat == 'otherNameCount':
                otherNameCount = 2*int(statValue)
            if stat == 'itemDescription':
                item[2] = statValue
            if stat == 'itemClass':
                item[3] = statValue
    file.close()
    return itemList;

def getStartObjectList(fileName):
    file = open(fileName, 'r')
    objectList = []
    objectStats = [[0,0],0,0,0]
    #Not the same ^^ for below
    otherNameCount = 0
    otherName = [0,0]
    otherNameLst = []
    newObject = 0
    harvest = ['Harvesting',0,0,0]
    otherNameCount = 0
    harvestDropAmount = 0
    harvestItem = [0,0]
    harvestDropLst = []
    construct = ['Constructing',0,0,0]
    constructElementAmount = 0
    constructItem = [0,0]
    constructItemLst = []
    craftOtherAmount = 0
    craftOtherLst = []
    #Not the same ^^ for below
    newConstruct = 0
    newHarvest = 0
    harvestForItem = 0
    constructForItem = 0
    for line in file:
        #Skipping Lines
        if line[0] == '/' and line[1] == '/':
            continue;
        if line[0] == '-':
            if line[1] == 'o':
                newObject = 1
                continue;
            if line[1] == 'h':
                newHarvest = 1
                continue;
            if line[1] == 'c':
                newConstruct = 1
                continue;
            if line[1] == 'd':
                if newObject:
                    newObject = 0
                    objectList.append(objectStats)
                    objectStats = [[0,0],0,0,0]
                if newHarvest:
                    newHarvest = 0
                    for i in objectList:
                        if i[0][0] == harvestForItem or i[0][1] == harvestForItem:
                            if i[3] == 0:
                                i[3] = [harvest]
                            else:
                                i[3].append(harvest)
                            break;
                    harvest = ['Harvesting',0,0,0]
                if newConstruct:
                    newConstruct = 0
                    for i in objectList:
                        if i[0][0] == constructForItem or i[0][1] == constructForItem:
                            if i[3] == 0:
                                i[3] = [construct]
                            else:
                                i[3].append(construct)
                            break;
                    construct = ['Constructing',0,0,0]
            
        if newObject == 1:
            l = seperateLine(line)
            stat = l[0]
            statValue = l[1]

            l = something(otherNameCount, 'otherName', 'otherNamePural', stat, statValue, 0, 1, otherName, otherNameLst, objectStats, 1)
            otherNameCount = l[0]
            otherName = l[1]
            otherNameLst = l[2]
            objectStats = l[3]

            if stat == 'objectName':
                objectStats[0][0] = statValue
            if stat == 'objectPuralCase':
                objectStats[0][1] = statValue
            elif objectStats[0][0] != 0 and objectStats[0][1] == 0:
                objectStats[0][1] = objectStats[0][0]
            if stat == 'otherNameAmount':
                otherNameCount = 2*int(statValue)
            if stat == 'objectDescription':
                objectStats[2] = statValue

        if newHarvest == 1:
            l = seperateLine(line)
            stat = l[0]
            statValue = l[1]

            l = something(harvestDropAmount, 'harvestName', 'harvestNum', stat, statValue, 1, 0, harvestItem, harvestDropLst, harvest, 3)
            harvestDropAmount = l[0]
            harvestItem = l[1]
            harvestDropLst = l[2]
            harvest = l[3]      
    
            if stat == 'objectFor':
                harvestForItem = statValue
            if stat == 'harvestDialogue':
                harvest[1] = statValue
            if stat == 'harvestClassReq':
                harvest[2] = statValue
            if stat == 'harvestDropsAmount':
                harvestDropAmount = 2*int(statValue)

        if newConstruct == 1:
            l = seperateLine(line)
            stat = l[0]
            statValue = l[1]

            l = something(constructElementAmount, 'constructName', 'constructNum', stat, statValue, 1, 0, constructItem, constructItemLst, construct, 3)
            constructElementAmount = l[0]
            constructItem = l[1]
            constructItemLst = l[2]
            construct = l[3]   

            if stat == 'objectFor':
                constructForItem = statValue
            if stat == 'constructDialogue':
                construct[1] = statValue
            if stat == 'constructClassReq':
                construct[2] = statValue
            if stat == 'constructElementAmount':
                constructElementAmount = 2*int(statValue)



    file.close()
    for obj in objectList:
        if obj[3] != 0:
            if obj[3][0][0] == 'Harvesting' or obj[3][0][0] == 'Constructing':
                for item in obj[3][0][3]:
                    found = 0
                    for o in objectList:
                        if o[0][0] == item[0] and len(item) < 3:
                            found = 1
                    if found == 0:
                        item.append(0)
                    else: #This assumes that if the name is not a objects then it must be a item's name
                        item.append(1)
                            
    return objectList;


def seperateLine(line):                
    stat = ''
    statValue = ''
    val = 0
    valueStart = 0
    skip = 0
    for letter in line:
        if skip:
            skip = 0
            continue;
        if letter == '\n':
            skip = 1
            continue;
        if val == 0:
            if letter == ':':
                val = 1;
                continue;
            else:
                stat += letter
        if val == 1:
            if letter == ' ' and valueStart == 0:
                continue;
            else:
                valueStart = 1
                statValue += letter
    return [stat, statValue]

def something(count, txt1, txt2, stat, statValue, sndRq, snd0IntOr1Str, lst, mainLst, mainmainLst, mainmainPos):    
    if count >= 0:
        count -= 1
        if stat == txt1:
            if sndRq == 0:
                lst[0] = statValue
            elif lst[0] != 0: #if second spot not required then makes lst[1] = lst[0]
                count -= 1
                lst[1] = lst[0]
            else:
                lst[0] = statValue
        elif stat == txt2:
            lst[1] = statValue
        elif sndRq == 0:
            if lst[0] != 0:
                lst[1] = lst[0]
        if lst[0] != 0 and lst[1] != 0:
            if snd0IntOr1Str == 0:
                lst[1] = int(lst[1])
            mainLst.append(lst)
            lst = [0,0]
        if count == 0:
            mainmainLst[mainmainPos] = mainLst
            mainLst = []
    return [count, lst, mainLst, mainmainLst]

