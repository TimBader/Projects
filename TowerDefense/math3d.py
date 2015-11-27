# Lab2
# Tim Bader
# 1/13/14
from math import cos, sin, radians, atan2

def polar2rect2D(angle, magnitude):
    """Converts polar corndates with angle in radians to cartesian cordnates, Returns List: [x,y]"""
    x = cos(angle)*magnitude
    y = -sin(angle)*magnitude
    return [x,y];

def rect2polar2D(pos1, pos2):
    """Converts rectangular cordnates into polar cordnates with radians, Returns List: [angle, magnitude]"""
    pos1 = list(pos1)
    a = pos2[0] - pos1[0]
    pos2 = list(pos2)
    b = (pos2[1] - pos1[1])*-1
    m = (a**2+(-b)**2)**0.5
    d = atan2(b,a)
    
    return [d,m]

def dot(v1, v2):
    """Returns the dot product scalar from two vectors"""
    if isinstance(v1, VectorN) and isinstance(v2, VectorN):
        if len(v1) == len(v2):
            c = 0
            d = 0
            while c < len(v1):
                d += v1[c]*v2[c]
                c += 1
            return d
        else:
            raise TypeError("These Vectors do not have the same lenght");
    else:
        raise TypeError("One or two of these elements are not vectors");

def cross(v1, v2):
    """Return the cross product of two vectors as long as they have the same dimension"""
    if isinstance(v1, VectorN) and isinstance(v2, VectorN):
        if len(v1) == len(v2):   
            d = [];
            count = 0;
            dimGetA = 1;    #What dimention to take from v1
            dimGetB = 2;    #'' from v2
            while count < len(v1):
                if dimGetA > len(v1)-1:
                    dimGetA = 0;
                if dimGetB > len(v1)-1:
                    dimGetB = 0;
                d.append(v1[dimGetA]*v2[dimGetB]-v2[dimGetA]*v1[dimGetB])
                dimGetA += 1;
                dimGetB += 1;
                count += 1;
            newVec = VectorN(d);
            return newVec;
        else:
            raise TypeError("These Vectors do not have the same length");
    else:
        raise TypeError("One or two given elemnts are not a vector");
    

class VectorN(object):
    """This is a vector"""
    def __init__(self, other):
        self.mData = [];
        """"The dimentions could be in tuple, string, or a list format.  The value could also be anouther VectorN class object"""
        if hasattr(other, "__len__") and hasattr(other,"__getitem__"):
            self.mDim = len(other);
            for i in range(len(other)):
                self.mData.append(float(other[i]));
        else:
            try:
                self.mDim = int(other);
                i = 0;
                while i < self.mDim:
                    self.mData.append(float(0));
                    i += 1;
            except ValueError:
                raise ValueError("This is an inapporpriate varible type")

    def __str__(self):
        """This will return --> '<Vector(Dimention): mData[0], mData[1], ...>'"""
        s = "<Vector" + str(self.mDim) + ": "
        s1 = str()
        i = 0
        while i < self.mDim:
            if i != 0:
                s1 += ", "   
            s1 += str(self.mData[i])
            i += 1
        s += s1
        s += ">"
        return s

    def __len__(self):
        """This will return the dimention of the vector"""
        return self.mDim

    def __getitem__(self, pos):
        """This will return the value at the given position"""
        return self.mData[pos]

    def __setitem__(self, pos, value):
        """This will set the value at the given position"""
        self.mData[pos] = float(value)

    def __eq__(self, RHS):
        """This will test the two vectors to see if they have equal dimentions and if they have the same values at the same positions"""
        if isinstance(RHS, VectorN):
            if self.mDim == RHS.mDim:
                return self.mData == RHS.mData 
            else:
                return False
        else:
            return False

    def __neg__(self):
        """This Negates the given Vector"""
        d = []
        for i in self.mData:
            d.append(i*(-1))
        newVec = VectorN(d)
        return newVec

    def __mul__(self, RHS):
        """This will multiply the given vector by a scalar that is on the right"""
        if isinstance(RHS, int) or isinstance(RHS, float):
            d = [];
            for i in self.mData:
                d.append(i*RHS);
            newVec = VectorN(d);
            return newVec;
        else:
            raise TypeError("This needs a scalar.  Int or Float");
        
    def __rmul__(self, LHS):
        """This will multiply the given vector by a scalar that is on the left"""
        if isinstance(LHS, int) or isinstance(LHS, float):
            d = [];
            for i in self.mData:
                d.append(i*LHS);
            newVec = VectorN(d);
            return newVec;
        else:
            raise TypeError("This needs a scalar.  Int or Float");
    
    def __truediv__(self, RHS):
        """This will return a new vector which is divided by the scalar"""
        if isinstance(RHS, int) or isinstance(RHS, float) or RHS != 0:
            div = 1/RHS
            newVec = self*div
            return newVec
        else:
            raise TypeError("This needs a scalar.  Int or Float");

    def __add__(self, RHS):
        """This adds two given vectors"""
        if isinstance(RHS, VectorN) and self.mDim == RHS.mDim:
            d = [];
            i = 0;
            while i < self.mDim:
                d.append(self.mData[i]+RHS.mData[i]);
                i += 1
                newVec = VectorN(d);
            return newVec;
        else:
            raise TypeError("Add needs to be a VectorN and have the same dimention")
        
    def __sub__(self, RHS):
        """This subtracts two given vectors"""
        if isinstance(RHS, VectorN) and self.mDim == RHS.mDim:
            d = [];
            i = 0;
            while i < self.mDim:
                d.append(self.mData[i]-RHS.mData[i]);
                i += 1
                newVec = VectorN(d);
            return newVec;
        else:
            raise TypeError("Add needs to be a VectorN and have the same dimention")

    
    def copy(self):
        """This will return a copyable vector from the vector being copied"""
        newVec = VectorN(self.mData)
        return newVec

    def toIntTuple(self):
        """This will make a new mData list with truncated values returned in a tuple format"""
        t = [];
        for i in self.mData:
            t.append(int(i));
        t = tuple(t);   
        return t

    def isZero(self):
        """This will see if this vector is a Zero Vector"""
        for i in self.mData:
            if i != float(0):
                return False
        return True

    def magnitude(self):
        """This gets the magnitude of the given vector"""
        #Components
        comp = 0
        #Magnitude
        for i in self.mData:
            comp += i**2
        magn = comp**0.5
        return magn

    def normalized_copy(self):
        """This returns a normalized version of this vector"""
        if self.isZero:
            raise ZeroDivisionError("The current vector is a Zero Vector");
        d = []
        for i in self.mData:
            d.append(i/magn);
        newVec = VectorN(d);
        return newVec;

        
if __name__== "__main__":

    '''
    v = VectorN(3) 
    print(v.isZero())                   # True 
    w = VectorN((1, -2, 3)) 
    print(w.isZero())                   # False 
    z = -w # Same as z = w.__neg__() to python 
    print(z)                            # <Vector3: -1.0, 2.0, -3.0> 
    print(z * 5)                        # <Vector3: -5.0, 10.0, -15.0> 
    # This is print(z.__mul__(5)) to python 
    print(5 * z)                        # <Vector3: -5.0, 10.0, -15.0> 
    # 5.__mul__(z) fails, so python calls 
    # z.__rmul__(5) 
    # print(v * w) # ERROR!
    print(z / 2)                        # <Vector3: -0.5, 1.0, -1.5> 
    # This is print(z.__truediv__(2)) to python 
    #print(2 / z) # ERROR! 
    #print(z / w) # ERROR! 
    print(z.magnitude())                # 3.74165738677 
    print(w.magnitude())                # 3.74165738677. Interesting property: |-v| = |v| 
    #print(z + 2) # ERROR! 
    #print(z + VectorN(2)) # ERROR! 
    u = VectorN((3, 3, 3)) 
    print(z + u)                        # <Vector3: 2.0, 5.0, 0.0> 
    print(z - u)                        # <Vector3: -4.0, -1.0, -6.0> 
    print(z.normalized_copy())          # <Vector3: -0.2673, 0.5345, -0.802> 
    print(dot(u, z))                    # -6.0 
    print(cross(u, z))                  # <Vector3: -15.0, 6.0, 9.0>
    '''

    # FRONT or BEHIND, RIGHT of, LEFT of
    """
    V = VectorN((5, 0, 0))
    D = VectorN((0, 0, 0))
    C = cross(V, D)
    print(C)
    if C[2] > 0:
        print("Point D is to the RIGHT of point V")
    if C[2] == 0:
        print("Point D is in FRONT or BEHIND of or point V")
    if C[2] < 0:
        print("Point D is to the LEFT of point V")
    """

    # Direction Gettin
    '''
    T = VectorN((5, 1))
    E = VectorN((1, 5))
    V = E - T
    print(V)
    Vn = V.normalized_copy()
    print(Vn)
    '''

    #Cross Product in 4D
    '''
    u = VectorN((3, 3, 3, 3))
    z = VectorN((-1, 2, -3, 1))
    print(cross(u, z))
    '''

    #Dot Test
    '''
    v = VectorN((1,2,3))
    w = v.copy()
    print(dot(v, w))
    '''

    #Add and Sub Test
    '''
    v = VectorN((1,2,3,4,5));
    w = v.copy()
    v += w
    print(v)
    v -= w
    print(v)
    '''

    #Div Test
    '''
    v = VectorN((1,2,3,5));
    print(v/0.5)
    '''

    #Mult Test
    '''
    v = VectorN((1,2,3,5));
    print(v*0.5)
    print(2*v)
    '''

    #Normalized Copy
    '''
    v = VectorN((6,8,345,33))
    print(v.normalized_copy())
    d = VectorN(5)
    print(d.normalized_copy())
    '''

    #Magnitude
    '''
    v = VectorN((6,8,345,33))
    print(v.magnitude())
    '''
    
    #Negating
    '''
    v = VectorN((3.5,-344,"67"))
    a = -v
    print(v)
    print(a)
    '''

    '''
    v = VectorN(5) 
    print(v) # <Vector5: 0.0, 0.0, 0.0, 0.0, 0.0> 
    w = VectorN((1.2, "3", 5)) 
    print(w) # <Vector3: 1.2, 3.0, 5.0> 
    z = w.copy() 
    z[0] = 9.9 
    z[-1] = "6" 
    print(z) # <Vector3: 9.9, 3.0, 6.0> 
    print(w) # <Vector3: 1.2, 3.0, 5.0> 
    print(z == w) # False 
    print(z == 9) # False 
    print(z == VectorN((9.9, "3", 6))) # True 
    print(z[0]) # 9.9 
    print(len(v)) # 5 
    print(w.toIntTuple()) # (1, 3, 5)
    ''' 

