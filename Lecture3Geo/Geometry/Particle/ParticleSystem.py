#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman
from Emitter import *


ps=Emitter([0,0,0],10)


ri = prman.Ri() # create an instance of the RenderMan interface

ri.Option("rib", {"string asciistyle": "indented"})

for frame in range(0,500) :

	filename = "Particle.%03d.rib" %(frame)
	# this is the begining of the rib archive generation we can only
	# make RI calls after this function else we get a core dump
	ri.Begin(filename)
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("Particle.%03d.exr" %(frame), "file", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(720,575,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
	
	
	# now we start our world
	ri.WorldBegin()
	
	ri.Translate(0,0,5)
	ps.Draw(ri)	
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()
	ps.Update()