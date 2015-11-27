from math import atan2
def point_distance(x1, y1, x2, y2):
    """ Returns the exact distance between two points"""
    a = x1 - x2
    b = y1 - y2
    d = (a*a + b*b)**0.5
    return d

def point_distance_check(x1, y1, x2, y2):
    """ Returns the distance un-sqaure rooted for better speed"""
    a = x1 - x2
    b = y1 - y2
    d = a*a + b*b
    return d

def point_direction(x1, y1, x2, y2):
    a = x2 - x1
    b = (y2 - y1)*-1
    d = atan2(b,a)
    return d

#print(point_direction(375, 200, -332.5802, 373.1364)*180/3.14)
#print(point_direction(375, 200, -44.5992+375, -50+200)*180/3.14)
