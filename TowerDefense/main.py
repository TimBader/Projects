import pygame
import twoD_math
from random import randint
from time import time
from math import sin, cos, degrees ,radians
import math3d
import os
import tilemapper
import util

class TowerController(object):
    """ """
    def __init__(self):
        self.towerList = [];
        #Fire Order list, a list of all the types of firing orders
        self.FoList = ["First", "Last", "Weakest", "Strongest", "Closest"];
        #Some Default Test Towers
        #self.towerList.append(Tower(150, "First", [windowW//2, 200], (255,0,0), 0.4, 600, 10));
        #self.towerList.append(Tower(230, "First", [windowW//2-50, 300], (255,0,255), 0.4, 600, 10));
        #self.towerList.append(Tower(230, "First", [windowW//2+50, 300], (255,255,255), 0.4, 600, 10));
        #self.towerList.append(Tower(260, "First", [windowW//2, 340], (0,255,0), 0.4, 600, 10));
        #self.towerList.append(Tower(515, "First", [windowW//2, 630], (0,0,255), 0.4, 600, 10));

    def update(self, dtime, enemy_list):
        for i in self.towerList:
            i.update(dtime, enemy_list);

    def createTower(self, mouse_pos, towersList):
        global currentgold
        fire_rng=towersList[0]
        fire_ordr=towersList[1]
        tower_cost=towersList[2]
        tower_color=towersList[3]
        fire_rates=towersList[4]
        projectile_spd=towersList[5]
        tower_damage=towersList[6]
        baseImg=towersList[7]
        topImg=towersList[8]
        projectileImg=towersList[9]
        rFo = randint(0, len(self.FoList)-1)    #Random Fire Order for testing
        if currentgold >= tower_cost:
            self.towerList.append(Tower(fire_rng, fire_ordr, [mouse_pos[0], mouse_pos[1]], tower_color, fire_rates, projectile_spd, tower_damage, baseImg, topImg, projectileImg));
            currentgold -= tower_cost
            
    def render(self, surface):
        for i in self.towerList:
            i.render(surface);

class Tower(object):
    """ """
    def __init__(self, fire_range, fire_order, pos, color, firerate, projectileSpeed, projectileDamage, baseImg, topImg, projectileImg):
        self.targeting_list = [];
        self.fire_order = str(fire_order);
        self.pos = list(pos);
        self.color = tuple(color);
        self.range = fire_range;
        self.target = 0;    #The target position of self.targeting list
        self.range2 = self.range**2
        self.firerate = 0
        self.firerateMax = firerate
        self.projectileSpeed = projectileSpeed
        self.projectileList = []
        self.projectileDamage = projectileDamage
        self.imgBase = loadImage(baseImg)
        self.imgTop = loadImage(topImg)
        #self.imgBase = pygame.image.load('art/' + baseImg)
        #self.imgTop = pygame.image.load('art/' + topImg)
        self.imgProjectile = loadImage(projectileImg)
        #self.imgProjectile = pygame.image.load('art/' + projectileImg)
        self.imgTopRot = self.imgTop
        self.aimRotation = 0

    def update(self, dtime, enemy_list):
        '''Tower Updating'''
        self.checkforTargets(enemy_list)
        self.findTarget()
        if self.firerate > self.firerateMax:
            I = self.getInterceptionPoint(enemy_list)
            if I:
                self.projectileList.append(projectile([self.pos[0], self.pos[1]], self.projectileSpeed, twoD_math.point_direction(self.pos[0], self.pos[1], I[0], I[1]), 5, self.color, I, self.projectileDamage, self.imgProjectile))
                self.firerate = 0
                self.aimRotation = degrees(twoD_math.point_direction(self.pos[0], self.pos[1], I[0], I[1]))
                self.imgTopRot = rotateImage(self.imgTop, self.aimRotation)
        self.updateProjectiles(dtime, enemy_list)
        self.firerate += dtime
        
    def checkforTargets(self, enemy_list):
        '''Checks to see what enemy is inside of its range'''
        tList = [];
        count = 0
        for i in enemy_list: #Grabbs information from enemies within range and putts usefull information in a list, the targetable list
            # self.targeting_list = [ [0] = Name, [1] = Health, [2] = Xpos, [3] = Ypos, [4] = distance**2, [5] = position in enemy_list, [6] = distance travaled, [7] = Movement Vector]
            if twoD_math.point_distance_check(self.pos[0], self.pos[1], i.pos[0], i.pos[1]) <= self.range2:
                tList.append([i.name, i.health, i.pos[0], i.pos[1], twoD_math.point_distance_check(self.pos[0], self.pos[1], i.pos[0], i.pos[1]), count, i.DistTrav, i.movVec]);
                self.targeting_list = tList;
            else:
                self.targeting_list = tList;
            count += 1
            
    def getInterceptionPoint(self, enemy_list):
        '''Finds the point in which to shoot at to hit the target'''
        # Shooting at enemies and target leading
        if len(self.targeting_list) > 0 and len(enemy_list) > 0: # Targeting Actions and how they target
            E = math3d.VectorN((self.targeting_list[self.target][2],self.targeting_list[self.target][3]))
            T = math3d.VectorN(self.pos)
            Ev = math3d.VectorN(self.targeting_list[self.target][7])
            Tv = math3d.VectorN((0,0))
            S = self.projectileSpeed
            Q = E - T
            Qv = Ev - Tv
            Qv = math3d.VectorN((Qv[0],Qv[1]*-1))
            vS = math3d.dot(Qv, Qv)
            if vS < 0.0001:
                iT = 0
            else:
                a = vS - S*S
                if abs(a) < 0.001:
                    t = (-1*math3d.dot(Q,Q))/(2*math3d.dot(Q, Qv))
                    iT = max(t, 0)
                else:
                    b = 2*math3d.dot(Q, Qv)
                    c = math3d.dot(Q, Q)
                    det = b*b-4*a*c
                    if det > 0:
                        t1 = (-b+det**.5)/(2*a)
                        t2 = (-b-det**.5)/(2*a)
                        if t1 > 0:
                            if t2 > 0:
                                iT = min(t1, t2)
                            else:
                                iT = t1
                        else:
                            iT  = max(t2, 0)
                    elif det < 0:
                        iT = 0
                    else:
                        iT = max(-b/(2*a), 0) 
            if iT != 0:
                I = E + iT*Qv
                return I

    def updateProjectiles(self, dtime, enemy_list):
        '''Updates all the projectiles the tower has shot'''
        # Controlling projectiles
        count = 0
        for i in self.projectileList:
            i.update(dtime)
            for ii in enemy_list:
                if twoD_math.point_distance_check(i.pos[0], i.pos[1], ii.pos[0], ii.pos[1]) < i.radius**2+ii.radius**2:
                    ii.health -= i.damage
                    self.projectileList = util.listPop(self.projectileList, count)
            if i.time >= 2:
                self.projectileList = util.listPop(self.projectileList, count)
            count += 1

    def findTarget(self):
        '''Figures out who to target'''
        if len(self.targeting_list) > 0: # Targeting Actions and how they target
            count = 0
            if self.target > len(self.targeting_list)-1:
                self.target = 0
            elif self.fire_order == "First":  #Targets the enemy who has traveled the most distance - Wont work right if enemy back tracks
                for i in self.targeting_list:
                    if i[6] > self.targeting_list[self.target][6]:
                        self.target = count
                    count += 1;
            elif self.fire_order == "Last": #"" But the one who has traveled the least amount of distance
                for i in self.targeting_list:
                    if i[6] < self.targeting_list[self.target][6]:
                        self.target = count
                    count += 1;
            elif self.fire_order == "Closest":
                for i in self.targeting_list:
                    if i[4] < self.targeting_list[self.target][4]:
                        self.target = count
                    count += 1;
            elif self.fire_order == "Weakest":
                for i in self.targeting_list:
                    if i[1] < self.targeting_list[self.target][1]:
                        self.target = count
                    count += 1;
            elif self.fire_order == "Strongest":
                for i in self.targeting_list:
                    if i[1] > self.targeting_list[self.target][1]:
                        self.target = count
                    count += 1;
        else:
            self.target = 0
    
    def render(self, surface):
        #pygame.draw.polygon(surface, self.color, ((int(self.pos[0]), int(self.pos[1])),(int(self.pos[0]+32), int(self.pos[1]+32)),(int(self.pos[0]+8), int(self.pos[1]+8)),(int(self.pos[0]-8), int(self.pos[1]+8))));
        blitImage(self.imgBase, self.pos, surface)
        blitImage(self.imgTopRot, self.pos, surface)
        #surface.blit(self.imgBase, (int(self.pos[0]-16), int(self.pos[1]-16))) ##-*
        #imgWd2 = self.imgTopRot.get_width()/2
        #imgHd2 = self.imgTopRot.get_height()/2
        #surface.blit(self.imgTopRot, (int(self.pos[0]-imgWd2), int(self.pos[1]-imgHd2))) ##-*
        #pygame.draw.rect(surface, self.color, (int(self.pos[0]-14), int(self.pos[1]-14), 28, 28))
        #pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.range, True);
        #Draw crossair for testing
        '''
        if len(self.targeting_list) > 0:
                pygame.draw.circle(surface, self.color, (int(self.targeting_list[self.target][2]), int(self.targeting_list[self.target][3])), 20, True)
                pygame.draw.line(surface, self.color, (int(self.targeting_list[self.target][2]-20), int(self.targeting_list[self.target][3])), (int(self.targeting_list[self.target][2]+20), int(self.targeting_list[self.target][3])),1);
                pygame.draw.line(surface, self.color, (int(self.targeting_list[self.target][2]), int(self.targeting_list[self.target][3]-20)), (int(self.targeting_list[self.target][2]), int(self.targeting_list[self.target][3]+20)),1);
        '''
        for i in self.projectileList:
            i.render(surface)
        
class Enemy(object):
    """ """
    def __init__(self, name, unitType, health, speed, direction, start_pos, color, worth, imageName):
        self.name = str(name);
        self.healthMax = health
        self.health = self.healthMax
        self.speed = speed;
        self.direction = direction;
        self.pos = list(start_pos);
        self.color = tuple(color);
        self.Cosx = cos(radians(self.direction))
        self.Siny = sin(radians(self.direction))
        self.movVec = [self.Cosx*self.speed, self.Siny*self.speed]
        self.unitType = unitType
        self.DistTrav = 0
        self.radius = 10
        self.dtilecolstatus = 0
        # 0 = havenot collided with direction tile, 1 = collided and awaiting direction change, 2 = still colliding but already had direction changed
        self.dtilecoldist = 0
        self.dtilecoldir = 0
        self.worth = worth
        self.dtilecolnum = 0
        self.image = loadImage(imageName)
        self.imageRot = rotateImage(self.image, self.direction)
        
    def update(self, dtime):
        self.pos[0] += self.movVec[0]*dtime;
        self.pos[1] -= self.movVec[1]*dtime;
        self.DistTrav += self.speed*dtime
        if self.dtilecolstatus == 1:
            self.dtilecoldist -= dtime*self.speed
            if self.dtilecoldist <= 0:
                self.dtilecolstatus = 2
                self.direction = self.dtilecoldir
                self.Cosx = cos(radians(self.direction))
                self.Siny = sin(radians(self.direction))
                self.movVec = [self.Cosx*self.speed, self.Siny*self.speed]
                self.imageRot = rotateImage(self.image, self.direction)
                

    def render(self, surface):
        if self.health > 0:
            blitImage(self.imageRot, self.pos, surface)
            #pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius); 
            pygame.draw.rect(surface, (255, 0, 0), (int(self.pos[0]-10), int(self.pos[1]-20), 20, 5))
            pygame.draw.rect(surface, (0, 255, 0), (int(self.pos[0]-10), int(self.pos[1]-20), 20/self.healthMax*self.health, 5))

class AIController(object):
    """ """
    def __init__(self, unitList, dirtilelist, Round):
        self.spawn_rate = 0
        self.enemy_list = []
        self.spawn_count = 0
        self.spawn_rateMax = 0.5
        self.unitList = unitList
        self.thresholdMax = 10
        self.threshold = 0
        self.Round = Round
        self.spawnList = []
        self.dirtilelist = dirtilelist
        self.SpawnLocation = []

    def update(self, dtime):
        self.spawn_rate += dtime
        self.createSpawnList()
        self.updateEnemies(dtime)
        self.spawnEnemies(dtime)
        
    def updateEnemies(self, dtime):
        '''Updates enemies duh'''
        global currentgold, lives
        count = 0
        for i in self.enemy_list:
            i.update(dtime)
            if i.pos[0] > windowW+64 or i.pos[0] < 0-64 or i.pos[1] > windowH+64 or i.pos[1] < 0-64:
                self.enemy_list = util.listPop(self.enemy_list, count)
                lives -= 1
            if i.health <= 0:
                self.enemy_list = util.listPop(self.enemy_list, count)
                currentgold += i.worth
            count += 1
            self.checkDtileCollision(i)

    def checkDtileCollision(self, i):
        '''Checks for collision adgainst for the enemy adgainst the direction tiles'''
        i.dtilecolnum = 0
        for ii in self.dirtilelist:
            if i.pos[0] >= ii[0][0]-30 and i.pos[0] <= ii[0][0]+30 and i.pos[1] >= ii[0][1]-30 and i.pos[1] <= ii[0][1]+30:
                if i.dtilecolstatus == 0:
                    i.dtilecolstatus = 1
                    i.dtilecoldist = twoD_math.point_distance(i.pos[0], i.pos[1], ii[0][0], ii[0][1])
                    if len(ii[1]) > 1: #to see if the direction tile has multiple directions
                        randomdirList = []  #create a list to store what directions could be chosen
                        for Dir in ii[1]:
                            if abs(Dir-i.direction) != 180: #to see if the current direction is opposite of what the enemy is going
                                randomdirList.append(Dir)   #if passes add it to the list
                        #print(i.direction,randomdirList) #testing code (it solved many problems :D)
                        i.dtilecoldir = randomdirList[randint(0,len(randomdirList)-1)] #choose random direction for the enemy from the random direciton list
                    else:
                        i.dtilecoldir = ii[1][0] #if the direction list is only one number
            elif i.dtilecolstatus == 2:
                i.dtilecolnum += 1
                if i.dtilecolnum == len(self.dirtilelist):#if all the dirtiles are not colliding and the enemy is in status 2, set status to 0
                    i.dtilecolstatus = 0;
                    i.dtilecolnum = 0
        
    def createSpawnList(self):
        '''Create a new SpawnList if now enemies exist anywhere and there is no spawn list'''
        if len(self.enemy_list) <= 0 and self.threshold <= 0 and len(self.spawnList) <= 0:
            self.Round += 1
            self.thresholdMax *= 1.25
            self.threshold = int(self.thresholdMax)
            while self.threshold > 0:
                a = randint(0, len(self.unitList)-1);
                if self.threshold - self.unitList[a][1] < 0 or self.Round < self.unitList[a][2]:  #Check to see if their is some threshold left, if you can spawn it
                    continue;
                self.spawnList.append(self.unitList[a]);
                self.threshold -= self.unitList[a][1];
                
    def spawnEnemies(self, dtime):
        '''Spawns enemies'''
        if self.spawn_rate >= self.spawn_rateMax and len(self.spawnList) > 0:
            randSpawn = randint(0, len(self.SpawnLocation)-1)
            enemy = Enemy("Enemy: " + str(self.spawn_count), self.spawnList[0][0],self.spawnList[0][3], self.spawnList[0][4], self.SpawnLocation[randSpawn][1], [self.SpawnLocation[randSpawn][0][0], self.SpawnLocation[randSpawn][0][1]], self.spawnList[0][5], self.spawnList[0][6], self.spawnList[0][7])
            self.enemy_list.append(enemy)
            self.spawnList = util.listPop(self.spawnList, 0);
            self.spawn_rate = 0;
            self.spawn_rateMax = self.Round*-1/50 + 0.5 #Lol y = mx + b :P
            self.spawn_count += 1*dtime;

    def render(self, surface):
        for i in self.enemy_list:
            i.render(surface)

        #drawing direction tiles
        '''
        for i in self.dirtilelist:
            scale = 22
            scale2 = 12
            pygame.draw.rect(surface, (255, 255, 255), (i[0][0]-32, i[0][1]-32, 64, 64), 1)
            for ii in i[1]:
                pygame.draw.line(surface, (255, 255, 255), (i[0][0] + cos(radians(ii))*scale, i[0][1] - sin(radians(ii))*scale), (i[0][0] + cos(radians(ii-180))*scale, i[0][1] - sin(radians(ii-180))*scale))
                pygame.draw.line(surface, (255, 255, 255), (i[0][0] + cos(radians(ii))*scale, i[0][1] - sin(radians(ii))*scale), (i[0][0] + cos(radians(ii+30))*scale2, i[0][1] - sin(radians(ii+30))*scale2))
                pygame.draw.line(surface, (255, 255, 255), (i[0][0] + cos(radians(ii))*scale, i[0][1] - sin(radians(ii))*scale), (i[0][0] + cos(radians(ii-30))*scale2, i[0][1] - sin(radians(ii-30))*scale2))
        '''

class projectile(object):
    """ """
    def __init__(self, startPos, speed, direction, radius, color, I, damage, image):
        self.pos = startPos
        self.speed = speed
        self.direction = direction
        self.Cosx = cos(self.direction)
        self.Siny = -sin(self.direction)
        self.radius = radius
        self.color = color
        self.time = 0
        self.I = I
        self.damage = damage
        self.img = image
        #self.img = pygame.image.load('art/' + str(imageName))
        self.imgRot = rotateImage(image, degrees(direction))

    def update(self, dtime):
        self.pos[0] += self.speed*self.Cosx*dtime
        self.pos[1] += self.speed*self.Siny*dtime
        self.time += dtime

    def render(self, surface):
        blitImage(self.imgRot, self.pos, surface)
        #pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        #pygame.draw.circle(surface, self.color, (int(self.I[0]), int(self.I[1])), 3)

def loadImage(imageName):
    try:
        image = pygame.image.load('art/' + imageName)
    except:
        image = 0
    return image

def rotateImage(image, angle):
    '''Returns a new surface rotated at the given angle (degrees) if the image is an image.  Returns 0 if not an image'''
    if image != 0:
        image = pygame.transform.rotate(image, angle)
    return image

def blitImage(image, pos ,surface):
    if image != 0:
        imgWd2 = image.get_width()/2
        imgHd2 = image.get_height()/2
        surface.blit(image, (int(pos[0]-imgWd2), int(pos[1]-imgHd2)))

def loadMap(LevelMap):
    global TileLocation
    global background
    global window
    TMap = tilemapper.TileMap()
    TMap.initializeNewMap(LevelMap)
    TileLocation = TMap.getGidLocationMap()
    background_img = TMap.getTileSurface()
    backgroundSize = background_img.get_size()
    background = pygame.Surface(backgroundSize, 0, 32)
    background.blit(background_img, (0, 0))
    window = pygame.display.set_mode(backgroundSize)
    window.blit(background, (0, 0))

def loadNewMap(LevelMap):
    global windowW, windowH, currentgold, lives, timeS, TowerC, Round, AIController_obj, unitList, dirtilelist, TileLocation, TMapStartTileKey, dirtilelist
    loadMap(LevelMap)
    dirtilelist = []
    #[ [0] = Position [ [0][0] = x, [0][1] = y ], [1] = Direction in Degrees ] ]
    windowW = window.get_width()
    windowH = window.get_height()
    currentgold = 300
    lives = 50
    timeS = time()
    TowerC = TowerController();
    Round = 0
    AIController_obj = AIController(unitList, dirtilelist, Round);
    util.dtileSearch(AIController_obj, TileLocation, TMapDtileKey)
    util.spawntileSearch(AIController_obj, TileLocation, TMapStartTileKey)
    print("Loaded: " + str(LevelMap))

def findBelowTile(pos, tileList):
    x = (pos[0] - pos[0] % 64)/64
    y = (pos[1] - pos[1] % 64)/64
    #print(x, y)
    tile = tileList[int(y)][int(x)]
    #print(tile)
    return tile

pygame.font.init()
TestingFont = pygame.font.SysFont(None, 25)

######For Tileset.img v1.0#######
TMapDtileKey = {1:[0, 270], 3:[180, 270], 19:[90, 0], 21:[90, 180], 30:[0, 90, 180, 270]}
TMapStartTileKey = {16:0, 17:270, 25:180, 26:90}
       
timeS = time()

unitList = [ ["Basic", 1, 1, 50, 100, (255, 255, 0),10,'Enemy1.png'],\
             ["Scout", 3, 2, 15, 150, (255, 0, 255),11,'Enemy1.png'],\
             ["Heavy", 12, 4, 150, 50, (255, 0, 0),12,'Heavy.png'],\
             ["Dude", 10, 3, 120, 110, (0, 255, 255),13,'Berserker.png'],\
             ["Commander", 50, 5, 200, 90, (0, 255, 0),14,'Commander.png'] ];
#[ [0] = Name, [1] = Threshold Amount, [2] = Round Reqiurment, [3] = Health, [4] = Speed, [5] = TempColor, [6] = Worth, [7] = Image Name ]

dirtilelist = [ ] # Direction Tile List
#[ [0] = Position [ [0][0] = x, [0][1] = y ], [1] = Direction in Degrees ] ]

towersList=[[250, "First", 50, (255,0,0),0.4,600,5,'', 'IceTower.png', 'FireBall.png',[11]],\
            [600, "First", 120, (0,255,0),1,1400,25,'Base2.png', 'Cannon.png', 'CannonBall.png', [11, 4, 5, 6, 13, 14, 15, 22, 23, 24, 31, 32, 33, 40, 41, 42, 49, 50, 51, 53, 58, 59, 60, 61, 62, 67, 68, 69, 70, 71]],\
            [300, "First", 100, (255,255,0),.1,800,10,'Base1.png', 'BallistaTurret.png', 'Harpoon.png', [11]],\
            [200, "Last", 100, (255,0,255),0.05,100,5,'Base1.png', 'Cannon.png', 'Flame1.png',[11]]];
#[ [0] = fire_range, [1] = fire_order, [2] = cost, [3] = color, [4] = firerateMax, [5] = projectileSpeed, [6] = DMG, [7] = Base Image Name, [8] = Top Image Name, [9] = Projectile Img Name, [10] = Tile list of nums that can be placed on ]

#FPS Counter
avgFPS = 0
FPS = 0
sumFPS = 0
count = 0

timeDia = 1

Paused = False

loadNewMap("LevelEx1")

#print(AIController_obj.SpawnLocation)

while True:
    dtime = time()-timeS
    if Paused:
        dtime = 0
    timeS = time()

    dtime *= timeDia

    if lives <= 0:
        break;

    #Update
    evt = pygame.event.poll()
    if evt.type == pygame.QUIT:
        break;
    elif evt.type == pygame.KEYDOWN:
        '''
        mpos = pygame.mouse.get_pos()
        mpos = [mpos[0], mpos[1]]
        mpos[0] = mpos[0]-mpos[0]%64+32
        mpos[1] = mpos[1]-mpos[1]%64+32
        '''

        if evt.key == pygame.K_SPACE:
            timeDia *= 2
        if evt.key == pygame.K_LALT:
            timeDia /= 2
        if evt.key == pygame.K_RETURN:
            break;
        '''
        if evt.key == pygame.K_w:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[90]]);
        if evt.key == pygame.K_x:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[270]]);
        if evt.key == pygame.K_d:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[0]]);
        if evt.key == pygame.K_a:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[180]]);
        if evt.key == pygame.K_q:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[270,0]]);
        if evt.key == pygame.K_e:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[270, 180]]);
        if evt.key == pygame.K_c:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[90, 180]]);
        if evt.key == pygame.K_z:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[90, 0]]);
        if evt.key == pygame.K_s:
            AIController_obj.dirtilelist.append([[mpos[0],mpos[1]],[90, 45, 135, 225, 315, 0, 270, 180]]);
        '''
        tower = 0
        mpos = pygame.mouse.get_pos()
        mpos = [mpos[0], mpos[1]]
        mpos[0] = mpos[0]-mpos[0]%32+16
        mpos[1] = mpos[1]-mpos[1]%32+16
        if evt.key == pygame.K_1:
            tile = findBelowTile(mpos, TileLocation)
            tower = towersList[0]
        if evt.key == pygame.K_2:
            tile = findBelowTile(mpos, TileLocation)
            tower = towersList[1]
        if evt.key == pygame.K_3:
            tile = findBelowTile(mpos, TileLocation)
            tower = towersList[2]
        if evt.key == pygame.K_4:
            tile = findBelowTile(mpos, TileLocation)
            tower = towersList[3]
            
        if tower:
            for i in tower[10]:
                if i == tile:
                    place = 1
                    for t in TowerC.towerList:
                        #print(t.pos, mpos)
                        if t.pos == mpos:
                            #Yell at player and break
                            place = 0
                            break;
                    if place:
                        TowerC.createTower([mpos[0], mpos[1]], tower) #randint(0,len(towersList)-1)
                    break;
                else:
                    #Yell at player
                    continue
        if evt.key == pygame.K_ESCAPE:
            if Paused:
                Paused = False
            else:
                Paused = True
        if evt.key == pygame.K_m:
            randi = randint(0,2)
            if randi == 0:
                loadNewMap("LevelEx2")
            elif randi == 1:
                loadNewMap("LevelEx1")
            elif randi == 2:
                loadNewMap("LevelEx3")
                
    AIController_obj.update(dtime);
    TowerC.update(dtime, AIController_obj.enemy_list);

    if dtime != 0 and timeDia == 1: #FPS Tracking
        FPS = int(1/dtime*timeDia)
        sumFPS += FPS
        count += 1
        avgFPS = sumFPS//count

    #Render
    window.fill((0,0,0));

    window.blit(background, (0, 0))

    TowerC.render(window);

    AIController_obj.render(window);

    #Testing Font -- Faster than using the print function
    text = TestingFont.render("FPS: " + str(FPS), True, (255, 255, 255))
    window.blit(text, (10, 10))
    text = TestingFont.render("Average FPS: " + str(avgFPS), True, (255, 255, 255))
    window.blit(text, (10, 30))
    text = TestingFont.render("Round: " + str(AIController_obj.Round), True, (255, 255, 255))
    window.blit(text, (10, 50))
    text = TestingFont.render("Time: " + str(timeDia/1) + "x", True, (255, 255, 255))
    window.blit(text, (10, 70))
    text = TestingFont.render("$: " + str(currentgold), True, (255, 255, 255))
    window.blit(text, (10, 90))
    text = TestingFont.render("Lives: " + str(lives), True, (255, 255, 255))
    window.blit(text, (10, 110))

    pygame.display.flip();
    
pygame.quit();
