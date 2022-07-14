import numpy as np
import math
from pyciede2000 import ciede2000
import random
from functools import lru_cache
from copy import deepcopy
from random import Random
r = Random()

# Utils and palettes for different distinct colormaps for arbirtray n or finite and small n
# SO thread: https://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors


# 16 optimal palette taken from: http://alumni.media.mit.edu/~wad/color/palette.html
def optimalPalette():
    # RGB values of black, dark grey, red, blue, green, brown, purple, light grey, 
    # light green, light blue, cyan, orange, yellow, tan, pink, white
    return np.array([[0,0,0],
                    [87,87,87],
                    [173,35,35],
                    [42,75,215],
                    [29,105,20],
                    [129,74,25],
                    [129,38,192],
                    [160,160,160],
                    [129,197,122],
                    [157,175,255],
                    [41,208,208],
                    [255,146,51],
                    [255,238,51],
                    [233,222,187],
                    [255,205,243],
                    [255,255,255]])



# 20 color palette taken from Kenneth Kelly
def kellyPalette():
    # Hex values of the 20 colors
    return np.array(['FFFFB300',
                     'FF803E75',
                     'FFFF6800',
                     'FFA6BDD7',
                     'FFC10020',
                     'FFCEA262',
                     'FF817066',
                     'FF007D34',
                     'FFF6768E',
                     'FF00538A',
                     'FFFF7A5C',
                     'FF53377A',
                     'FFFF8E00',
                     'FFB32851',
                     'FFF4C800',
                     'FF7F180D',
                     'FF93AA00',
                     'FF593315',
                     'FFF13A13',
                     'FF232C16'])
          
# Naive Solution for color picking based on distance metric CIEDE2000
# Described here: https://en.wikipedia.org/wiki/Color_difference#CIEDE2000

def getDistinctColors(n, iterations=1000):
    colors = []
    
    # Create random colors
    for i in range(n):
        colors.append(list(np.random.choice(range(255),size=3)))
    
    colors_copy = deepcopy(colors)
    
    max_dist = -float('inf')
    for i in range(iterations):
        step = random.random() * 10
        for j, cc in enumerate(colors_copy):
            for k in range(len(cc)):
                m = random.random() * step
                c = cc[k]
                c += m - (step / 2.0)
                if c > 255:
                    c = 255
                if c < 0:
                    c = 0            
                colors[j][k] = int(c)
        
        current_dist = maximized_distance(colors) 
        if current_dist > max_dist:
            max_dist    = current_dist
            colors_copy = deepcopy(colors)
    
    return colors       

def getColorDistance(r1,g1,b1,r2,g2,b2):
    lab1 = convertRGBLab(r1 / 255.0, g1 / 255.0, b1 / 255.0)
    lab2 = convertRGBLab(r2 / 255.0, g2 / 255.0, b2 / 255.0)
    return ciede2000(lab1, lab2)['delta_E_00']

# Code from: https://gist.github.com/tatarize/a483db49993e6e0e994ad82ba3e2a22e
# Color conversion formula borrowed from:
# http://www.easyrgb.com/index.php?X=MATH&H=02#text2

@lru_cache(maxsize=0xFFF)
def convertRGBLab(var_R: float, var_G: float, var_B: float):
    """
    Convert RGB to Lab colors.
    :param var_R:
    :param var_G:
    :param var_B:
    :return:
    """
    x, y, z = convertRGBXYZ(var_R, var_G, var_B)
    return convertXYZLab(x, y, z)


def convertRGBXYZ(var_R: float, var_G: float, var_B: float):
    """
    Convert RGB to XYZ colors
    :param var_R:
    :param var_G:
    :param var_B:
    :return:
    """
    if var_R > 0.04045:
        var_R = math.pow(((var_R + 0.055) / 1.055), 2.4)

    else:
        var_R = var_R / 12.92
    if var_G > 0.04045:
        var_G = math.pow(((var_G + 0.055) / 1.055), 2.4)

    else:
        var_G = var_G / 12.92
    if var_B > 0.04045:
        var_B = math.pow(((var_B + 0.055) / 1.055), 2.4)
    else:
        var_B = var_B / 12.92
    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100  # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    return X, Y, Z


def convertXYZLab(X: float, Y: float, Z: float):
    """
    Convert xyz to lab colors.
    :param X:
    :param Y:
    :param Z:
    :return:
    """
    ref_X = 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    ref_Y = 100.000  # ref_Y = 100.000
    ref_Z = 108.883  # ref_Z = 108.883
    
    var_X = X / ref_X
    var_Y = Y / ref_Y
    var_Z = Z / ref_Z

    if var_X > 0.008856:
        var_X = math.pow(var_X, 1.0 / 3.0)
    else:
        var_X = (7.787 * var_X) + (16.0 / 116.0)
    if var_Y > 0.008856:
        var_Y = math.pow(var_Y, 1.0 / 3.0)
    else:
        var_Y = (7.787 * var_Y) + (16.0 / 116.0)
    if var_Z > 0.008856:
        var_Z = math.pow(var_Z, 1.0 / 3.0)
    else:
        var_Z = (7.787 * var_Z) + (16.0 / 116.0)
    CIE_L = (116 * var_Y) - 16
    CIE_a = 500 * (var_X - var_Y)
    CIE_b = 200 * (var_Y - var_Z)
    return CIE_L, CIE_a, CIE_b

def maximized_distance(colors):
    distances = []
    for j, q1 in enumerate(colors):
        for k, q2 in enumerate(colors):
            if j == k:
                continue
            distances.append(getColorDistance(*q1, *q2))
    if len(distances):
        return min(distances)
    else:
        return -float("inf")  

# RGB to HEX
def hexcolor(r,g,b):
    return "#%02X%02X%02X" % (int(round(r)), int(round(g)), int(round(b)))

# HEX to RGB
def rgbcolor(hexc):
    return tuple(int(hexc[i:i+2], 16) for i in (0, 2, 4))

# Get HEX colors from RGB colors array
def toHexColors(colors):
    c = []
    for cc in colors:
        c.append(hexcolor(*cc))
    return c

# Get RGB colors from HEX colors array
def toRGBColors(colors):
    c = []
    for cc in colors:
        c.append(rgbcolor(cc))
    return c                     

                     
                        
                     