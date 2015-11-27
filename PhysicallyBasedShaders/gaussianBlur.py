#!/usr/bin/env python3
#1D Gaussian kernel
import math
import sys
import functools

r=float(3)
sigma=r/3.0
def g(i):
    tmp=float(-r+i); 
    tmp *= tmp
    tmp /= -2.0*sigma*sigma;  
    tmp = math.exp(tmp)
    tmp /= sigma * math.sqrt(2*3.14159265358979323)
    return tmp
A=[g(i) for i in range(int(2*r)+1)]
Asum = functools.reduce(lambda x,y: x+y,A,0)
Alen=len(A)
A=map(lambda x: x/Asum,A)
'''print("vec4 gaussblur%d(" % r)
print("         const in sampler2D tex,")
print("         const in vec2 tex_dist, ")
print("         const in vec2 texcoord,")
print("         const in vec2 deltas){")'''
print("precision highp float;");
print("uniform sampler2D image;");
print("uniform float ISize;")
print("uniform vec2 deltas;\n")
print("varying vec2 v_texcord;\n")
print("void main(){")
print("    vec4 color = vec4(0,0,0,0);")
m=-r
for q in A:
    print("    color +=",q,"* texture2D(image, v_texcord.st +",m,end=" ")
    print("* deltas * ISize);")
    m += 2.0*r/(Alen-1)
print("    gl_FragColor = color;")
print("}")
