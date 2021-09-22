#! /usr/bin/env python3

import sys
import os.path
import argparse
import subprocess
from copy import deepcopy

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input', metavar='fname', type=str)
parser.add_argument('--occlude', metavar='fname', type=str,default="")

args = parser.parse_args()

#  --occlude 30-29:42.43,28:38
# For slides 30-29  we want to exclude layers 42 and 43 and for slide 28 we want to exclude 38


def parseOcclude(hides):
    occludes={}
    if not hides: return occludes
    the_list = hides.split(",")
    for sp in  the_list:
        layers,not_wanted = sp.split(":")
        the_layers=layers.split("-")
        if len(the_layers)==1:  the_layers=the_layers+the_layers
        l1,l2 = the_layers
        notw=not_wanted.split(".")
        for l in range(int(l1),int(l2)+1):
            for n in notw:
                curr = occludes.get(l,[])
                curr.append(int(n))
                occludes[l]=curr
    return occludes


occludes = parseOcclude(args.occlude)
    

#	0)	Color pseudo-object.
#	1)	Ellipse which is a generalization of circle.
#	2)	Polyline which includes polygon and box.
#	3)	Spline which includes
#	4)	Text.
#	5)	Arc.
#6)	Compound object which is composed of one or more objects


depth_field = { '0':-1, '1':6, '2':6, '3':6, '4':3, '5':6 }

def getDepth(fname):
    depths = set([])
    max_x=max_y=0
    print(fname)
    for line in open(fname):
        if len(line)==0 or line[0]=="#" or line[0]=="	": continue
        if line[0] in [" ","\t",chr(9)]:
            data = line.strip().split()
            print(data)
            if obj_type=="2" and len(data)%2 == 1: continue
            for i in range(0,len(data),2):
                max_x=max(float(data[i]),max_x)
                max_y=max(float(data[i+1]),max_y)
                min_x=min(float(data[i]),max_x)
                min_y=min(float(data[i+1]),max_y)
            continue
        fields = line.split()
        if len(fields)<=7: continue
        obj_type = fields[0]
        if obj_type=='4':
             data = line.strip().split()
             max_x=max(float(data[11]),max_x)
             max_y=max(float(data[12]),max_y)
             min_x=min(float(data[11]),max_x)
             min_y=min(float(data[12]),max_y)
        curr_depth = fields[depth_field[obj_type]]
        if curr_depth=='-1': print (line)
        depths.add(curr_depth)
    depths=sorted(list(depths))
    return depths

def getHeader(f):
      header=f.readline()
      header = header+f.readline() # Portrait/Landscape
      header = header+f.readline() # where
      header = header+f.readline() # metric?
      f.readline() # pagetype
      header = header + "A4\n"
      header = header + f.readline() # mag
      f.readline() # multiple/single
      header = header + "Single\n"
      header = header + f.readline() # trans colour
      header = header + f.readline() # coord system
      return header

def getObject(f,buffer):
    obj = buffer if buffer else f.readline()
    fields = obj.split()
    obj_type = fields[0]
    curr_depth = fields[depth_field[obj_type]]
    for line in f:
        if line[0] not in [0,chr(9)]:
            buffer = line
            break
        obj=obj+line
    else:
        return None, None, None
    return curr_depth, obj, buffer
    
def outputLayers(layers,fname):
    base, ext = os.path.splitext(fname)
    with open(fname) as f:
        header=getHeader(f)
        out = [open("base.%d.fig"%layer[l],"w") for l in layers]
        buffer = ""
        for g in out:
            g.write(header)
        while True:
            depth,obj,buffer = getObject(f,buffer)
            if depth is None: break
            this_layer = layer[depth]
            if depth=="-1":
                for g in out: g.write(obj)
            else:
                for l in range(0,this_layer+1):
                    out[l].write(obj)
        for g in out: g.close()

depths  = getDepth(args.input)
layer = {}

base, ext = os.path.splitext(args.input)
curr_depths=[]
depths.reverse()
print(occludes)
for i, d in enumerate(depths):
    pdf = "%s-%d.pdf"%(base,i)
    curr_depths.append(d)
    curr_hides = occludes.get(int(d),[])
    the_depths = [t for t in curr_depths if int(t) not in curr_hides]
    print(d,the_depths,curr_hides)
    subprocess.run("fig2dev -L pdf -B '2500 3000 0 0'  -D +%s %s %s"%(",".join(the_depths),args.input,pdf),shell=True)
    
