import pygame
import xml.etree.ElementTree as ET
import os

#print(os.path.isfile("tiles/b.png"))

class TileMap(object):

        def __init__(self):
                pass;

        def initializeNewMap(self, fileName):
                if not isinstance(fileName, str):
                        raise TypeError("The given argument needs to be a string")
                if not os.path.isfile("levels/" + fileName + ".tmx"):
                        raise NameError("The given file does not exist in levels/ folder")
                self.level = fileName
                self.tree = ET.parse("levels/" + fileName + ".tmx")
                self.root = self.tree.getroot()

                # get info about map from the tmx file
                self.tilewidth = int(self.root.findall('tileset')[0].attrib['tilewidth'])
                self.tileheight = int(self.root.findall('tileset')[0].attrib['tileheight'])
                tileset_image = self.root.findall('tileset')[0].findall('image')[0].attrib['source']
                self.tilesetheight = int(self.root.findall('tileset')[0].findall('image')[0].attrib['height'])#192
                self.tilesetwidth = int(self.root.findall('tileset')[0].findall('image')[0].attrib['width'])#192

                i = 3 #to chop off the "../" part :)
                tileAddress = ''
                while i < len(tileset_image):
                        tileAddress += tileset_image[i]
                        i += 1

                print(tileAddress)
                self.tileset = pygame.image.load(tileAddress)

                self.tilemapWidth = int(self.root.attrib['width'])#10
                self.tilemapHeight = int(self.root.attrib['height'])

        def getGidLocationMap(self):
                col = 0 # Colum
                tile_row = []
                tilemap = []
                for tile in self.root.findall('layer')[0].findall('data')[0].findall('tile'):
                        t = int(tile.attrib['gid'])
                        #print(t, col)
                        tile_row.append(t)
                        if col >= self.tilemapWidth-1:
                                tilemap.append(tile_row)
                                tile_row = []
                                col = 0
                        else:
                                col += 1;
                return(tilemap)

        def getTileSurface(self):
                #rendering to image
                s = pygame.Surface((self.tilewidth * self.tilemapWidth, self.tileheight * self.tilemapHeight))

                tilemap = self.getGidLocationMap()

                y_count = 0
                for row in tilemap:
                        x_count = 0
                        for gid in row:
                                #print("Gid: " + str(gid))
                                a = (self.tilesetwidth//self.tilewidth)
                                b = gid
                                c = 1
                                while b > a:
                                        c += 1
                                        b -= a
                                x1 = (b*self.tilewidth)-self.tilewidth
                                y1 = (c*self.tileheight)-self.tileheight
                                rect = (x1, y1, self.tilewidth, self.tileheight) 
                                #print(rect)
                                image = self.tileset.subsurface(rect)
                                s.blit(image, (x_count * self.tilewidth, y_count * self.tileheight))
                                x_count += 1
                        y_count += 1
                #pygame.image.save(s, str(level) + "_Map.png")
                return(s)
