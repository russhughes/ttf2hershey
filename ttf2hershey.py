#!/usr/bin/env python2.7

# Convert True Type Fonts (.ttf) to Hershey Fonts
# (c) Lingdong Huang 2018

# Info on Hershey Fonts:
# - https://en.wikipedia.org/wiki/Hershey_fonts
# - http://paulbourke.net/dataformats/hershey/

import sys
from truetype.truetype import *

def tohershey(text, font_path="ttf/ubuntu.ttf", kern=0, verbose=True):

    ttf = TrueTypeFont(font_path, verbose=verbose)
    outer = ttf.ttf.xMin, ttf.ttf.yMin, ttf.ttf.xMax, ttf.ttf.yMax
    cmax = (36-kern)*2
    umax = max(abs(outer[2]-outer[0]),
               abs(outer[3]-outer[1]),
               abs(outer[3]-ttf.baseline),
               abs(outer[1]-ttf.baseline)
               )
    scale = float(cmax)/umax
    result = ""

    x_xmin, _, x_xmax, _ = ttf.glyphData[ttf.chr2idx('x')]['rect']
    x_xcent = (x_xmin+x_xmax)/2.0

    max_width = 0
    max_height = 0

    for ch in text:
        # ch = text[i]
        index = ttf.chr2idx(ch)

        polylines, (xmin, ymin, xmax, ymax) = ttf.glyphData[index]['poly'], \
            ttf.glyphData[index]['rect']
        width = xmax - xmin
        height = ymax - ymin

        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

        xcent = xmin + width/2.0
        ycent = ymin + height/2.0

        if ch == " ":
            result += str(ord(ch)).rjust(5)+str(2).rjust(3)
            result += chr(int((x_xmin-x_xcent)/2.0*scale)+ord('R'))\
                + chr(int((x_xmax-x_xcent)/2.0*scale)+ord('R'))
            result += "\n"
            continue

        res = chr(int(round((xmin-xcent)*scale))+ord('R')-kern)\
            + chr(int(round((xmax-xcent)*scale))+ord('R')+kern)

        for i in range(len(polylines)):
            for _j in range(len(polylines[i])+1):
                j = _j % len(polylines[i])
                x, y = polylines[i][j]
                x = x-xcent
                y = -(y-ttf.baseline)
                xs = chr(int(round(x*scale))+ord('R'))
                ys = chr(int(round(y*scale))+ord('R'))
                res += xs+ys
            if i != len(polylines)-1:
                res += " R"
        result += str(ord(ch)).rjust(5)+str(len(res)//2).rjust(3)+res+"\n"
    return (result, round(max_width*scale), round(max_height*scale))

if __name__ == "__main__":

    input_path = sys.argv[1]
    characters = "".join([chr(i) for i in range(32, 128)])
    font, width, height = tohershey(characters, font_path=input_path, kern=2, verbose=False)

    print("# WIDTH = %d" % width)
    print("# HEIGHT = %d" % height)
    print("# FIRST = 32")
    print("# LAST = 127")

    print font
