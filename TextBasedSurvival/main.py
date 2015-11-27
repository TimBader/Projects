from random import randint
import itemReader

#[0]: Name and Pural Case, [1]: Other Names with Pural Cases, [2]: Description, [3]: Crafting Class, [4]: Actions
startItemList = itemReader.getStartItemList('items.txt')

#print(startItemList)
#0 = item, 1 = object
'''
startObjectList =  [[['Tree','Trees'],[['Arbor','Arbors']],'Its a fucking tree, nothing much else to talk about',[['Harvesting', 'Swing Axe', 'Axe',[['Fallen Tree', 1, 1],['Stick', 20, 0]]]] ],
                    [['Fallen Tree','Fallen Trees'],0,'Its a fucking fallen tree, nothing much else to talk about',[['Harvesting', 'Swing Axe', 'Axe',[['Sticks', 200, 0]]]] ],
                    [['Furnace', 'Furnaces'],0,'Burn baby burn',[['Constructing','PUT STUFF TOGETHER',0,[['Stone', 40]]]] ]
                    ]
#'''
startObjectList = itemReader.getStartObjectList('objects.txt')
#print(startObjectList)

'''
print('The next string of items is for testing!!!!')    
for i in startItemList:
    print('Item--> ' + str(i))
'''
#Actions[Crafting['Crafting',craftingDialogue,craftingClassReq,Recipe[],numberItCreates,createsAlso[]]

print('\n----\n-All the items in game: ')
for i in startItemList:
    print(i[0][0])
print('\n----\n\n-All the objects in game: ')
for i in startObjectList:
    print(i[0][0])
print('\n----\n')


sceneStartItemList = [ ['Stick', randint(5,10)], ['Flint', randint(15,25)], ['Feather', randint(150,250)] ]
#sceneStartList = []
sceneStartObjectList = [['Tree', 20],['Tall Grass', 59],['Stone Pile', 15]]
#sceneStartObjectList = [['Tree', 20]]
class inventoryItem(object):
    def __init__(self, ID, pos, number):
        self.id = ID
        self.pos = pos
        self.number = number

class Object(object):
    def __init__(self, ID, name, otherNames, description, Actions):
        self.id = ID
        self.name = name
        self.otherNames = 0
        if otherNames != 0:
            self.otherNames = []
            for name in otherNames:
                case = []
                for cases in name:
                    case.append(cases.lower())
                self.otherNames.append(case)
        self.description = description

        #Actions
        self.Actions = 0
        if Actions != 0:
            self.Actions = []
            for action in Actions:
                #Listing Actions
                self.Actions.append(action[0])
                if action[0] == 'Harvesting':
                    self.harvestDialogue = action[1]
                    self.harvestClassReq = action[2]
                    self.harvestDrops = action[3]
                if action[0] == 'Constructing':
                    self.constructDialogue = action[1]
                    self.constructClassReq = action[2]
                    self.constructRecipe = action[3]

class Item(object):
    def __init__(self, ID, name, otherNames, description, craftingClass, Actions):
        self.id = ID
        self.name = name
        self.otherNames = 0
        if otherNames != 0:
            self.otherNames = []
            for name in otherNames:
                case = []
                for cases in name:
                    case.append(cases.lower())
                self.otherNames.append(case)
        self.description = description
        self.craftingClass = craftingClass
                 
        #Actions
        self.Actions = 0
        if Actions != 0:
            self.Actions = []
            for action in Actions:
                #Listing Actions
                self.Actions.append(action[0])
                #Crafting
                if action[0] == 'Crafting':
                    self.craftDialogue = action[1]
                    self.craftClassReq = action[2]
                    self.craftRecipe = action[3]
                    self.craftNumber = action[4]
                    self.craftOthersList = action[5]

class player(object):
    def __init__(self):
        self.itemList = []
        self.objectList = []
        count = 0
        for stat in startItemList:
            self.itemList.append(Item(count,stat[0],stat[1],stat[2],stat[3],stat[4]))
            count += 1
        count = 0
        for stat in startObjectList:
            self.objectList.append(Object(count,stat[0],stat[1],stat[2],stat[3]))
            count += 1

        craftString = 'These items have crafting recipes: \n'
        for item in self.itemList:
            if item.Actions != 0:
                for action in item.Actions:
                    #Crafting
                    if action == 'Crafting':
                        craftString += item.name[0] + '\n'
                        item.craftRecipe = self.convert2IDRecipe(item.craftRecipe, self.itemList)
                        if item.craftOthersList != 0:
                            item.craftOthersList = self.convert2IDRecipe(item.craftOthersList, self.itemList)
        print(craftString)

        harvestString = 'These items have harvesting recipes: \n'
        constructString = 'These items have constructing recipes: \n'
        for obj in self.objectList:
            if obj.Actions != 0:
                for action in obj.Actions:
                    #Harvesting
                    if action == 'Harvesting':
                        harvestString += obj.name[0] + '\n'
                        obj.harvestDrops = self.convert2IDRecipe(obj.harvestDrops, self.objectList)
                    if action == 'Constructing':
                        constructString += obj.name[0] + '\n'                        
                        obj.constructRecipe = self.convert2IDRecipe(obj.constructRecipe, self.itemList)
        print(harvestString)
        print(constructString)
                        
        self.sceneItems = []
        for item in sceneStartItemList:
            self.give(self.nameToID(item[0], self.itemList), item[1], self.sceneItems)
        self.sceneObjects = []
        for obj in sceneStartObjectList:
            self.give(self.nameToID(obj[0], self.objectList), obj[1], self.sceneObjects)
        
        self.inventory = []

    def doAction(self, inp):
        inp = inp.lower()
        #print(str(inp))
        for t in ['i','inventory']:
            if inp == t:
                string = '[Inventory: '
                count = 0
                for item in self.inventory:
                    caseName = self.getCase(item.id, item.number, self.itemList)
                    string += caseName + ' x' + str(item.number)
                    #string += ' pos ' + str(item.pos)
                    if count < len(self.inventory)-1:
                        string += ', '
                    count += 1
                string += ' ]'
                print(string)
                return;
        #'''
        for t in ['give']:
            if inp == t:
                ID = self.getInputItem('What item? :')
                numReq = getIntInput('How Many? : ')
                self.give(ID, numReq, self.inventory);
                return;
        #'''
    
        for t in ['look around', 'l']:
            if inp == t:
                print('Looking around you find: ')
                string = '[Items Around: '
                count = 0
                for item in self.sceneItems:
                    caseName = self.getCase(item.id, item.number, self.itemList)
                    string += caseName + ' x' + str(item.number)
                    if count < len(self.sceneItems)-1:
                        string += ', '
                    count += 1
                string += ' ]'
                print(string)
                
                string = '[Objects Around: '
                count = 0
                for obj in self.sceneObjects:
                    caseName = self.getCase(obj.id, obj.number, self.objectList)
                    string += caseName + ' x' + str(obj.number)
                    if count < len(self.sceneObjects)-1:
                        string += ', '
                    count += 1
                string += ' ]'
                print(string)
                return;
            
        for t in ['gather', 'collect', 'pick up']:
            if inp == t:
                ID = self.getInputItem('What item do you want to ' + inp + '?: ', 0, self.itemList)
                numReq = getIntInput('How many?: ')
                if numReq > 0:
                    self.transferItem(ID, numReq, self.sceneItems, self.inventory, 'There are not any ' + self.itemList[ID].name[1] + ' around', 'There are not that many ' + self.itemList[ID].name[1] + ' around', 'I succesfully found ' + str(numReq) + ' ' + self.getCase(ID, numReq, self.itemList))
                return;

        for t in ['harvest']:
            if inp == t:
                ID = self.getInputItem('What object do you want to harvest?: ', 0, self.objectList)
                numReq = getIntInput('How many?: ')
                self.harvest(ID, numReq)
                return;
            
        for t in ['craft']:
            if inp == t:
                ID = self.getInputItem('What do you want to craft?: ', "I don't know how to craft something like that!", self.itemList)
                if ID != -1:
                    if self.itemList[ID].Actions != 0:
                        for action in self.itemList[ID].Actions:
                            if action == 'Crafting':
                                numReq = getIntInput('How many ' + self.itemList[ID].name[1] + ' do you want to craft?: ')
                                self.craft(ID, numReq)
                                return;
                    print("I don't know how to craft a " + self.itemList[ID].name[0] + "!")
                return;

        for t in ['construct']:
            if inp == t:
                ID = self.getInputItem('What do you want to construct?: ', "I don't know how to construct something like that!", self.objectList)
                if ID != -1:
                    if self.objectList[ID].Actions != 0:
                        for action in self.objectList[ID].Actions:
                            if action == 'Constructing':
                                self.construct(ID)
                                return;
                    print("I don't know how to construct a " + self.objectList[ID].name[0] + "!")
                return;

        for t in ['deconstruct']:
            if inp == t:
                ID = self.getInputItem('What do you want to deconstruct?: ', "I don't know how to deconstruct something like that!", self.objectList)
                if ID != -1:
                    if self.findInInventory(ID, self.sceneObjects):
                        if self.objectList[ID].Actions != 0:
                            for action in self.objectList[ID].Actions:
                                if action == 'Constructing':
                                    self.deconstruct(ID)
                                    return;
                    else:
                        print("There are not any " + self.objectList[ID].name[1] + "around")
                        return;
                    print("I don't know how to deconstruct a " + self.objectList[ID].name[0] + ", for I don't know how it is made!")
                return;                

        #'''
        for t in ['remove']:
            if inp == t:
                ID = self.getInputItem('What item? :', 0, self.itemList)
                numReq = getIntInput('How many?: ')
                self.remove(ID, numReq, self.inventory);
                return;
        #'''

        for t in ['drop']:
            if inp == t:    
                ID = self.getInputItem('What item? :', 0, self.itemList)
                numReq = getIntInput('How many?: ')
                self.transferItem(ID, numReq, self.inventory, self.sceneItems, "I don't even have " + self.itemList[ID].name[1] + " in my inventory", "I don't have that many " + self.itemList[ID].name[1] + " in my inventory", "I successfully dropped " + str(numReq) + " " + self.getCase(ID, numReq, self.itemList) + " on the ground")
                return;
                
        for t in ['inspect','describe']:
            if inp == t:
                typ = input('What type of thing do you want to inspect? (Object/Item): ')
                typ = typ.lower()
                for i in ('object','o'):
                    if typ == i:
                        typ = 1
                        ID = self.getInputItem('What object do you wish to inspect?: ', 0, self.objectList)
                for i in ('item','i'):
                    if typ == i:
                        typ = 0
                        ID = self.getInputItem('What item do you wish to inspect?: ', 0, self.itemList)
                if not isinstance(typ, int):
                    print('FUCK give me a FUCKING object or A FUCKING item as the input! DipSHit!')
                    return;
                self.inspect(ID, typ)
                return;
            
        print('I dont know how to do that!')
        return;

    def harvest(self, ID, num):
        hObj = self.objectList[ID]
        
        invObj = self.findInInventory(ID, self.sceneObjects)
        caseName = self.getCase(ID, num ,self.objectList)

        countAndName = str(num) + ' ' + caseName
        
        if invObj != -1:
            if invObj.number < num:
                print('I cannot find ' + countAndName + ' around')
                return;
            if hObj.harvestClassReq != 0:
                if self.checkForClass(hObj.harvestClassReq, "I don't have a " + hObj.harvestClassReq + " in my inventory") == -1:
                    return;
        else:
            print('There are no ' + hObj.name[1] + ' around')
            return;
    
        self.remove(ID, num, self.sceneObjects)
        dropAmount = len(hObj.harvestDrops)
        print(hObj.harvestDialogue)

        self.createList(hObj.harvestDrops, num, 'Harvesting')

    def give(self, ID, num, lst):
        '''ID of item or object to give, number to give, list to give it to'''
        item = self.findInInventory(ID, lst)
        if item == -1:     #if it is a new item in list, append the new inventoryItem
            lst.append(inventoryItem(ID,len(lst),num))
        else:       
            item.number += num

    def transferItem(self, ID, num, fromLst, toLst, noItemTxt='Dont have item', notEnoughtTxt='not enought', successTxt='successful'):
        item = self.findInInventory(ID, fromLst)
        if item != -1:
            caseName = self.getCase(ID, item.number, self.itemList)
            if item.number >= num:
                self.give(ID, num, toLst)
                self.remove(ID, num, fromLst)
                print(successTxt)
                return;
            else:
                print(notEnoughtTxt)
        else:
            print(noItemTxt)

    def craft(self, ID, makeNum): #This will be a bitch to correctly do
        cItem = self.itemList[ID]
        partNum = len(cItem.craftRecipe)

        caseName = self.getCase(ID, makeNum, self.itemList)
        countAndName = str(makeNum) + ' ' + caseName
        
        print('Crafting ' + countAndName + ' will require: ')
        self.printRecipe(cItem.craftRecipe, makeNum, self.itemList) #Printing required materials        

        if cItem.craftClassReq != 0:
            print('This recipe also requires you have a ' + cItem.craftClassReq + ' in your inventory')
        inp = input('Do you still want to make ' + countAndName + '? (Yes/No): ').lower()

        for t in ['n','no','nope']:
            if inp == t:
                return;

        if cItem.craftClassReq != 0:
            if self.checkForClass(cItem.craftClassReq, "I dont have a " + cItem.craftClassReq + " in my inventory") == -1:
                return;
                
        if self.checkForRecipe(cItem.craftRecipe, makeNum ,'I don\'t have the neccesary materials to craft ' + countAndName) == -1:
            return;
        else:              

            self.removeRecipe(cItem.craftRecipe ,makeNum)
            self.give(ID, cItem.craftNumber*makeNum, self.inventory)
            if self.itemList[ID].craftDialogue != 0:
                print(cItem.craftDialogue)
            if cItem.craftOthersList != 0:
                self.createList(cItem.craftOthersList, makeNum, 'Crafting')
            print('I succesfully crafted ' + countAndName)

    def createList(self, createLst, makeNum, createType):
        string = '\nWhile ' + createType + ' you also managed to produce'
        for thing in createLst:
            thingType = 0
            thingIDLst = self.itemList
            toList = self.sceneItems
            if len(createLst) > 2:
                if thing[2] == 1:
                    thingType = 1
                    thingIDLst = self.objectList
                    toList = self.sceneObjects
            caseName = self.getCase(thing[0], thing[1]*makeNum, thingIDLst)
            self.give(thing[0], thing[1]*makeNum, toList)
            string += ' ' + str(thing[1]*makeNum) + ' ' + caseName
        print(string + ' on the ground')              

    def construct(self, ID): #This will be a bitch to correctly do
        cObject = self.objectList[ID]
        partNum = len(cObject.constructRecipe)

        caseName = self.getCase(ID, 1, self.objectList)
        countAndName = '1 ' + caseName
        
        print('Constructing ' + countAndName + ' will require: ')
        self.printRecipe(cObject.constructRecipe, 1, self.itemList) #Printing required materials        

        if cObject.constructClassReq != 0:
            print('This recipe also requires you have a ' + cObject.constructClassReq + ' in your inventory')

        inp = input('Do you still want to make ' + countAndName + '? (Yes/No): ').lower()
        for t in ['n','no','nope']:
            if inp == t:
                return;

        if cObject.constructClassReq != 0:
            if self.checkForClass(cObject.constructClassReq, "I dont have a " + cObject.constructClassReq + " in my inventory") == -1:
                return;
                
        if self.checkForRecipe(cObject.constructRecipe, 1 ,'I don\'t have the neccesary materials to construct ' + countAndName) == -1:
            return;
        else:              
            self.removeRecipe(cObject.constructRecipe, 1)
            self.give(ID, 1, self.sceneObjects)
            if self.objectList[ID].constructDialogue != 0:
                print(cObject.constructDialogue)
            print('I succesfully crafted ' + countAndName)

    def deconstruct(self, ID):
        cObject = self.objectList[ID]
        partNum = len(cObject.constructRecipe)

        self.remove(ID, 1, self.sceneObjects)

        string = '\nWhile deconstructing the ' + cObject.name[0] + ', you mannage to salvage'
        for item in cObject.constructRecipe:
            caseName = self.getCase(item[0], item[1]//(4/3), self.itemList)
            self.give(item[0], item[1]//(4/3), self.inventory)
            string += ' ' + str(item[1]//(4/3)) + ' ' + caseName
        print(string)

    def remove(self, ID, num, lst):
        removed = 0 # if 1 then the remaining items in the list will loose one pos
        for item in lst:
            if removed:
                item.pos -= 1
                continue;
            if item.id == ID:
                if item.number <= num:
                    removed = 1
                    #print('CATZ')
                    if lst == self.sceneItems:
                        self.sceneItems = lst[:(item.pos)] + lst[(item.pos+1):]
                    elif lst == self.sceneObjects:
                        self.sceneObjects = lst[:(item.pos)] + lst[(item.pos+1):]
                    elif lst == self.inventory:
                        self.inventory = lst[:(item.pos)] + lst[(item.pos+1):]
    
                else:
                    item.number -= num

    def checkForRecipe(self, recipe, makeNum, failTxt):
        '''Returns -1 if failed.  This checks to see if all the items in the recipe are in the inventory'''
        partNum = len(recipe)
        for part in recipe:
            item = self.findInInventory(part[0], self.inventory)
            if item != -1:
                if item.number >= part[1]*makeNum:
                    partNum -= 1
        if partNum != 0:
            print(failTxt)
            return -1;

    def removeRecipe(self, recipe, makeNum): #Maybe i will keep this
        for part in recipe:
            item = self.findInInventory(part[0], self.inventory)
            self.remove(item.id, part[1]*makeNum, self.inventory)  

    def printRecipe(self, recipe, makeNum, IDlst):
        partNum = len(recipe)
        count = 1
        string = ''
        for part in recipe:
            partCase = self.getCase(part[0], part[1]*makeNum, IDlst)
            string += partCase + ' x' + str(part[1]*makeNum)
            if count != partNum:
                string += ', '
            count += 1
        print(string)

    def checkForClass(self, Class, failTxt=0):
        '''Returns -1 if class in the inventory was not found'''
        for item in self.inventory:
            if self.itemList[item.id].craftingClass == Class:
                return item;
        if failTxt != 0:
            print(failTxt)
            return -1;

    def getCase(self, ID, num, idLst):
        if num == 1:
            return idLst[ID].name[0];
        else:
            return idLst[ID].name[1];

    def inspect(self, ID, typ):
        if typ == 1:
            if self.findInInventory(ID, self.sceneObjects) != -1:
                print(self.objectList[ID].description)
            else:
                print('If there was a ' + self.objectList[ID].name[0] + ' around, I would be better able to inspect it')

        elif typ == 0:
            if self.findInInventory(ID, self.inventory) != -1 or self.findInInventory(ID, self.sceneItems) != -1:
                print(self.itemList[ID].description)
            else:
                print('If I had a ' + self.itemList[ID].name[0] + ' or it was around, I would be able to inspect it')
               

    def getInputItem(self, txt, txt2=0, idLst=0):
        '''Checks to see if inputed name matches that of an associated ID'''
        if idLst == 0:
            idLst = self.itemList
        #txt2 means if the first try is not met with success then abort saying txt2
        while True:
            inpt = input(txt)
            inpt = inpt.lower()
            ID = self.nameToID(inpt, idLst)
            if ID != -1: #if there is a ID associated with that name
                return ID;
            if isinstance(txt2,str): #if not met with succses first try
                print(txt2)
                return -1;
                break;

    def nameToID(self, name, idLst):
        for item in idLst:
            for case in item.name:
                if case.lower() == name.lower():
                    return item.id
            if item.otherNames != 0:
                for case in item.otherNames:
                    for otherName in case:
                        if otherName == name.lower():
                            return item.id
        return -1; #Return that it has failed to find a ID that matches that name

    def findInInventory(self, ID, lst):
        '''returns the item if it was found in inventory.  If not found then it returns -1'''
        for item in lst:
            if item.id == ID:
                return item;
        return -1;

    def convert2IDRecipe(self, recipe, idLst):
        newRecipe = []
        for part in recipe:
            newPart = []
            if len(part) > 2:
                if part[2] == 1:
                    newPart.append(self.nameToID(part[0], self.objectList))
                elif part[2] == 0:
                    newPart.append(self.nameToID(part[0], self.itemList))
            else:
                newPart.append(self.nameToID(part[0], idLst))
            newPart.append(part[1])
            if len(part) > 2:
                newPart.append(part[2])
            newRecipe.append(newPart)
        return newRecipe

def getIntInput(inputText):
    while True:
        inp = input(inputText)
        try:
            inp = int(inp)
            return inp
        except ValueError:
            print('Give me whole integer numbers')
            continue;    

Player = player()
            
#Main Loop
while True:
    inp = input('-\nActions Available: inventory, drop, look around, gather, construct/deconstruct, craft, inspect\n---> What should I do next?: ')
    if inp == 'Quit' or inp == 'quit':
        exit;
    else:
        Player.doAction(inp)
        
    
