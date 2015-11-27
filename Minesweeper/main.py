#Minesweeper
import pygame
from random import randint
from time import time

def flag(oPos):
    global interaction
    global hudOffset
    global flagCount
    if tileList[oPos][2] == 0 and interaction != 0:
        if tileList[oPos][3] == 0:
            flagCount += 1
            tS05 = tileSize*0.5
            tS025 = tileSize*0.25
            rtileSizeP05tileSize = r*tileSize+tS05
            ctileSizeP05tileSize = c*tileSize+tS05
            tS025PxO = tS025+xOffset
            tS025PhOPyO = tS025+hudOffset+yOffset
            pygame.draw.polygon(tileSurface, (0,0,255),((int(rtileSizeP05tileSize-tS025PxO),int(ctileSizeP05tileSize+tS025PhOPyO)),(int(rtileSizeP05tileSize+tS025PxO),int(ctileSizeP05tileSize+tS025PhOPyO)),(int(rtileSizeP05tileSize+xOffset),int(ctileSizeP05tileSize-(tS025)+hudOffset+yOffset))))
            tileList[oPos][3] = 1
        elif tileList[oPos][3] == 1:
            flagCount -= 1
            tileSizeM2 = tileSize-2
            pygame.draw.rect(tileSurface, (0,0,0), (int(r*tileSize+1+xOffset), int(c*tileSize+1+hudOffset+yOffset), tileSizeM2, tileSizeM2))
            tileList[oPos][3] = 0

def reveal(oPos,semiReveal=0):
    global remaining
    global interaction
    global gameTime
    global hudOffset
    global gameState
    global firstReveal
    if tileList[oPos][3] == 0 and interaction ==  1: #if not flagged and interaction is enabled
        if tileList[oPos][2] == 0: #if not already revealed
            remaining -= 1
            tileList[oPos][2] = 1
            if tileList[oPos][0] != 1: #if not a bomb
                drawNum(oPos)
                #print(oPos)
            else:
                if firstReveal == 1:
                    i = 0
                    tS05 = tileSize*0.5
                    tS05PxO = tS05+xOffset
                    tS05PhOPyO = tS05+hudOffset+yOffset
                    while i < tileNum:  #draw all leBombas
                        if tileList[i][0] == 1:
                            r = i % rowW
                            c = int(i / rowW)
                            pygame.draw.circle(tileSurface, (195,0,0), (int(r*tileSize+tS05PxO), int(c*tileSize+tS05PhOPyO)),int(tS05))
                        i += 1
                    remaining += 1
                    interaction = 0
                    gameState = -1

                elif tileList[oPos][0] == 1:
                    #print('meow')
                    tileList[oPos][0] = 0
                    tileList[oPos][2] = 0
                    while True:
                        rPos = randint(1,tileNum)-1
                        if tileList[rPos][0] == 0 and rPos != oPos:
                            break;
                    tileList[rPos][0] = 1
                    #Testing
                    '''
                    r = rPos % rowW
                    c = int(rPos / rowW)
                    pygame.draw.circle(tileSurface, (255,0,0), (int(r*tileSize+0.5*tileSize+xOffset), int(c*tileSize+0.5*tileSize+hudOffset+yOffset)),int(tileSize*0.5))
                    #'''

                    remaining += 1

                    addAround(rPos)
                    addAround(oPos,-1)
                    
                    reveal(oPos)
                    
            if tileList[oPos][1] == 0: #if number of mines around is = 0
                revealAround(oPos)

        elif tileList[oPos][1] != 0 and semiReveal == 0: #if already revealed
            #print('meow')
            flagC = checkAroundForFlags(oPos)
            if flagC == tileList[oPos][1]:
                revealAround(oPos,1)

        if remaining == 0 and semiReveal == 0: #if there are no more mines around
            interaction = 0
            gameState = 1
            #print("You WON!!!\nTime Completed (Seconds): " + str(gameTime) + "\nPress 'r' to restart\nPress 'c' to create a custom game")

    firstReveal = 1

def checkAround(oPos): #returns a list of values that indicate which tile around them is allowed to be used
    pList = []
    if oPos % rowW != 0:
        pList.append(oPos-1)
        if not oPos-rowW < 0:
            pList.append(oPos-rowW-1)
        if not oPos+rowW >= tileNum:
            pList.append(oPos+rowW-1)
    if (oPos+1) % rowW != 0:
        pList.append(oPos+1)
        if not oPos-rowW < 0:
            pList.append(oPos-rowW+1)
        if oPos+rowW < tileNum:
            pList.append(oPos+rowW+1)
    if not oPos-rowW < 0:
        pList.append(oPos-rowW)
    if oPos+rowW < tileNum:
        pList.append(oPos+rowW)
    return pList

def checkAroundForFlags(oPos):
    pList = checkAround(oPos)
    flagC = 0
    for i in pList:
        if tileList[i][3] == 1:
            flagC += 1
    return flagC

def addAround(oPos,inc=1):
    pList = checkAround(oPos)
    for i in pList:
        tileList[i][1] += inc

def revealAround(oPos,semiReveal=0):
    pList = checkAround(oPos)
    for i in pList:
        reveal(i,semiReveal)

def drawNum(tilePos):
    global hudOffset
    pos = [0,0,0,0,0,0,0,0,0]
    if tileList[tilePos][1] == 1:
        pos = [0,0,0,0,1,0,0,0,0]   #~[ , , 
        color = (0,0,255)           #   ,o, 
    if tileList[tilePos][1] == 2:   #   , , ]
        pos = [0,0,0,1,0,1,0,0,0]   #~[ , , 
        color = (0,255,0)           #  o, ,o
    if tileList[tilePos][1] == 3:   #   , , ]
        pos = [0,1,0,0,0,0,1,0,1]   #~[ ,o, 
        color = (0,255,255)         #   , , 
    if tileList[tilePos][1] == 4:   #  o, ,o]
        pos = [1,0,1,0,0,0,1,0,1]   #~[o, ,o
        color = (255,255,0)         #   , , 
    if tileList[tilePos][1] == 5:   #  o, ,o]
        pos = [1,0,1,0,1,0,1,0,1]   #~[o, ,o
        color = (255,0,255)         #   ,o, 
    if tileList[tilePos][1] == 6:   #  o, ,o]
        pos = [1,0,1,1,0,1,1,0,1]   #~[o, ,o
        color = (255,150,0)         #  o, ,o  
    if tileList[tilePos][1] == 7:   #  o, ,o]
        pos = [1,0,1,1,1,1,1,0,1]   #~[o, ,o
        color = (255,255,255)       #  o,o,o
    if tileList[tilePos][1] == 8:   #  o, ,o]
        pos = [1,1,1,1,0,1,1,1,1]   #~[o,o,o
        color = (255,0,0)           #  o, ,o
                                    #  o,o,o]
    r = tilePos % rowW
    c = int(tilePos / rowW)
    yPos = 0
    xPos = 0
    rtsP1PxO = r*tileSize+1+xOffset
    ctsP1PyOPhO = c*tileSize+1+yOffset+hudOffset
    tS01 = int(tileSize*0.1)
    interval = int(tileSize*0.25)
    topLcornerx = int(rtsP1PxO+interval)
    topLcornery = int(ctsP1PyOPhO+interval)
    pygame.draw.rect(tileSurface, (135,135,135), (int(rtsP1PxO), int(ctsP1PyOPhO), tileSize-2, tileSize-2))

    for i in pos:
        if xPos == 3:
            xPos = 0
            yPos += 1
        if i == 1:
            x = topLcornerx+interval*xPos
            y = topLcornery+interval*yPos
            pygame.draw.circle(tileSurface,color,(x,y),tS01)
        xPos += 1

def newGame(rowWidth=16,colHeight=16,minesNumber=40):
    #print('----------')
    global rowW
    global colH
    global minesNum
    global tileNum
    global remaining
    global tileList
    global windowH
    global windowW
    global window
    global tileSurface
    global interaction
    global gameTime
    global hudOffset
    global flagCount
    global xOffset
    global yOffset
    global timeS
    global gameState #-1 Lost, 0 GameOn, 1 GameWon
    global firstReveal
    global insult
    insult = randomInsult()
    firstReveal = 0
    timeS = time();
    gameState = 0
    gameTime = 0
    flagCount = 0
    interaction = 1
    rowW = rowWidth
    colH = colHeight
    tileNum = rowW*colH
    minesNum = minesNumber
    remaining = tileNum-minesNum
    windowW = tileSize*rowW
    windowH = tileSize*colH+hudOffset
    if windowW < 400:
        xOffset = (400-windowW)/2
        windowW = 400

    if windowH < 400+hudOffset:
        yOffset = ((400+hudOffset)-windowH)/2
        windowH = 400+hudOffset

    window = pygame.display.set_mode((windowW, windowH));

    tileSurface = pygame.Surface((windowW,windowH),0,32)

    # Creating the tileList and where all the mines spawn and adds proximity count to adjacent tiles when a mine is placed
    tileList = []
    i = 0
    while i < tileNum:  #initializing list
        tileList.append([0,0,0,0]) #[0] = mine, [1] = proximity count, [2] = revealed, [3] = flagged
        i += 1
    i = 0
    while i < minesNum:
        rTnum = randint(1,tileNum)-1
        if tileList[rTnum][0] == 1:
            #print('Catz are cat catz meow')
            continue;
        tileList[rTnum][0] = 1
        #Testing
        '''
        r = rTnum % rowW
        c = int(rTnum / rowW)
        pygame.draw.circle(tileSurface, (255,0,0), (int(r*tileSize+0.5*tileSize+xOffset), int(c*tileSize+0.5*tileSize+hudOffset+yOffset)),int(tileSize*0.5))
        '''

        addAround(rTnum)

        i += 1

    # drawing all the unchecked tiles to the tileSurface
    row = 0
    while row < colH:
        i = 0
        while i < rowW:
            pygame.draw.rect(tileSurface, (75,75,75),(i*tileSize+xOffset, row*tileSize+hudOffset+yOffset, tileSize, tileSize), 1)
            i += 1
        row += 1

def createCustom():
    print('')
    while True:
        r = input('Input number of colums (0<x<=30): ')
        try:
            int(r)
        except:
            continue;
        r = int(r)
        if r > 0 and r <= 30:
            break;
    while True:
        c = input('Input number of rows (0<x<=21): ')
        try:
            int(c)
        except:
            continue;
        c = int(c)
        if c > 0 and c <= 21:
            break;
    while True:
        limit = r*c-2
        m = input('Input number of mines (0<x<=' + str(limit) + '): ')
        try:
            int(m)
        except:
            continue;
        m = int(m)
        if m > 0 and m <= limit:
            break;
    #print('----------')
    newGame(int(r),int(c),int(m))

def randomInsult():
    l = ['pea-brain','bucket-face','pubescent boy','no-brains','Mama-mia lover', 'tree face']
    return l[randint(1,len(l))-1]

### Game Initialization

tileSize = 30
hudOffset = 48
xOffset = 0
yOffset = 0
newGame(20,16,40)#(20,16,40)

pygame.font.init()
GameFont = pygame.font.SysFont(None, 30)

timeS = time();
#Main Game Loop
while True:
    #Updates
    dtime = time()-timeS;
    timeS = time();

    evt = pygame.event.poll()
    if evt.type == pygame.QUIT:
        break;
    if evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_r:
            newGame(rowW,colH,minesNum)
            #print('----------')
        if evt.key == pygame.K_c:
            createCustom()
    if evt.type == pygame.MOUSEBUTTONDOWN:
        button = pygame.mouse.get_pressed()
        mpos = [evt.pos[0], evt.pos[1]]
        if mpos[0] >= xOffset and mpos[0] <= windowW-xOffset:             
            mpos[0] = (mpos[0]-xOffset)-(mpos[0]-xOffset)%tileSize
            mpos[1] = (mpos[1]-hudOffset-yOffset)-(mpos[1]-hudOffset-yOffset)%tileSize
            r = mpos[0]/tileSize
            c = mpos[1]/tileSize
            tilePos = int(c*rowW+r)
            if button[0] == 1 and tilePos >= 0 and tilePos < tileNum:
                #print(tilePos)
                reveal(tilePos)
            if button[2] == 1 and tilePos >= 0 and tilePos < tileNum:
                flag(tilePos)

    if interaction == 1:
        gameTime += dtime

    #Render
    window.fill((0,0,0));
    window.blit(tileSurface,(0,0))
    pygame.draw.rect(window,(50,50,50),(0,0,windowW,hudOffset))
    text = GameFont.render(str(round(gameTime)), True, (255, 255, 255))
    window.blit(text, (int(windowW/2-40), int(hudOffset/2-10)))
    text = GameFont.render(str(round(minesNum-flagCount)), True, (255, 255, 255))
    window.blit(text, (int(windowW/2+40), int(hudOffset/2-10)))
    if gameState != 0:
        text = GameFont.render('Press \'r\' to restart', True, (255, 255, 0))
        window.blit(text, (int(windowW/2-90), int(windowH/2+40)))
        if gameState == 1:
            text = GameFont.render('You won in ' + str(round(gameTime)) + ' seconds', True, (255, 255, 0))
            window.blit(text, (int(windowW/2-120), int(windowH/2)))
        if gameState == -1:
            text = GameFont.render('You set off a mine ' + insult + '.', True, (255, 255, 0))
            window.blit(text, (int(windowW/2-123), int(windowH/2)))

    pygame.display.flip();

pygame.quit();
    
