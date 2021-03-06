#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman



def Scene(ri) :
	ri.AttributeBegin()
	random.seed(25)

	face=[-0.1,-1,-3, 0.1,-1,-3,-0.1,-1,3, 0.1,-1,3]
	plank=-5.0
	while (plank <=5.0) :
		ri.TransformBegin()
		ri.Color([random.uniform(0.35,0.4),random.uniform(0.1,0.025),0])
		c0=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		c1=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		ri.Surface("wood",{"Ks":[0.1],"point c0":c0,"point c1":c1,"float grain":random.randint(2,20)})
		ri.Translate(plank,0,0)
		ri.Patch("bilinear",{'P':face})
		ri.TransformEnd()
		plank=plank+0.206
	ri.AttributeEnd()
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Color([1,1,1])
	ri.Translate( 0,-1.0,0)
	ri.Rotate(-90,1,0,0)
	ri.Rotate(36,0,0,1)
	ri.Scale(0.4,0.4,0.4)
	ri.Surface("plastic")
	ri.Geometry("teapot")
	ri.AttributeEnd()
	ri.TransformEnd()
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})


filename = "AnimSpot.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin(filename)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
ri.Declare("Light1" ,"string")
ri.Declare("Ambient" ,"string")

frame=1
Lightx=-3.0
while Lightx<3.0 :
	ri.FrameBegin(frame)
	# now we add the display element using the usual elements
	# FILENAME DISPLAY Type Output format
	ri.Display("SpotLight.%03d.exr" %(frame), "file", "rgba")
	# Specify PAL resolution 1:1 pixel Aspect ratio
	ri.Format(720,575,1)
	# now set the projection to perspective
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
	
	
	
	# now we start our world
	ri.WorldBegin()
	
	#spot directly above
	ri.LightSource( "spotlight", {ri.HANDLEID:"Light1",
					"from" : [0,2,4], 
					"to" :[Lightx,0,4 ],
					"intensity" : [5],
					"coneangle" : [0.3],
					"conedeltaangle" : [0.01]})
	
	
	#ri.LightSource ("ambientlight",{ri.HANDLEID: "Ambient","intensity" :[0.05]}) 
	
	
	ri.Translate(0,0,4)
	ri.Illuminate("Light1",1)
	#ri.Illuminate("Ambient",1)
	
	Scene(ri)
	
	
	ri.WorldEnd()
	ri.FrameEnd()
	frame+=1
	Lightx+=0.2
	# and finally end the rib file
ri.End()
