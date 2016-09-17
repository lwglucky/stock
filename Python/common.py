#common.py
import math
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import OpenGL.GLUT as glut
import numpy as ny
#Python Imaging Library (PIL)
class common:
    bCreate = False

#sphere
class sphere(common):
    def __init__(this,rigns,segments,radius):
        this.rigns = rigns
        this.segments = segments
        this.radius = radius
    def createVAO(this):
        vdata = []
        vindex = []
        for y in range(this.rigns):
            phi = (float(y) / (this.rigns - 1)) * math.pi
            for x in range(this.segments):
                theta = (float(x) / float(this.segments - 1)) * 2 * math.pi
                vdata.append(math.sin(phi) * math.cos(theta))
                vdata.append(math.cos(phi))
                vdata.append(math.sin(phi) * math.sin(theta))
                vdata.append(this.radius * math.sin(phi) * math.cos(theta))
                vdata.append(this.radius * math.cos(phi))
                #print "sphere height:",this.radius * math.cos(phi)
                vdata.append(this.radius * math.sin(phi) * math.sin(theta))
                #print this.radius * math.cos(phi)
        for y in range(this.rigns - 1):
            for x in range(this.segments - 1):
                vindex.append((y + 0) * this.segments + x)
                vindex.append((y + 1) * this.segments + x)
                vindex.append((y + 1) * this.segments + x + 1)
                vindex.append((y + 1) * this.segments + x + 1)
                vindex.append((y + 0) * this.segments + x + 1)
                vindex.append((y + 0) * this.segments + x)
        #this.vboID = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER,this.vboID)
        #glBufferData (GL_ARRAY_BUFFER, len(vdata)*4, vdata, GL_STATIC_DRAW)
        #this.eboID = glGenBuffers(1)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,this.eboID)
        #glBufferData (GL_ELEMENT_ARRAY_BUFFER, len(vIndex)*4, vIndex,
        #GL_STATIC_DRAW)
        this.vbo = vbo.VBO(ny.array(vdata,'f'))
        this.ebo = vbo.VBO(ny.array(vindex,'H'),target = GL_ELEMENT_ARRAY_BUFFER)
        this.vboLength = this.segments * this.rigns
        this.eboLength = len(vindex)
        this.bCreate = True
    def drawShader(this,vi,ni,ei):
        if this.bCreate == False:
            this.createVAO()
        #glBindBuffer(GL_ARRAY_BUFFER,this.vboID)
        #glVertexAttribPointer(vi,3,GL_FLOAT,False,24,0)
        #glEnableVertexAttribArray(vi)
        #glVertexAttribPointer(ni,3,GL_FLOAT,False,24,12)
        #glEnableVertexAttribArray(ni)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,this.eboID)
        #glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_INT,0)
        this.vbo.bind()
    def draw(this,pi):
        if this.bCreate == False:
            this.createVAO()
        #glBindBuffer(GL_ARRAY_BUFFER,this.vboID)
        #glInterleavedArrays(GL_N3F_V3F,0,None)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,this.eboID)
        #glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_INT,None)
        this.vbo.bind()  
        glEnableVertexAttribArray(pi)  
        glVertexAttribPointer(pi,3,GL_FLOAT,False,24,this.vbo+12)        
        this.ebo.bind()
        glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_SHORT,None) 
        this.vbo.unbind()
        this.ebo.unbind()       
        glDisableVertexAttribArray(pi)
class plane(common):
    def __init__(this,xres,yres,xscale,yscale):
        this.xr,this.yr,this.xc,this.yc = xres,yres,xscale,yscale
        this.xl,this.yl = (this.xr - 1) * this.xc,(this.yr - 1) * this.yc
        this.createVAO()
    def createVAO(this):
        helfx = (this.xr - 1) * this.xc * 0.5
        helfy = (this.yr - 1) * this.yc * 0.5
        print helfx,helfy
        vdata = []
        vindex = []
        for y in range(this.yr):
            for x in range(this.xr):
                #uv
                vdata.append(float(x) / float(this.xr - 1))
                vdata.append(float(y) / float(this.yr - 1))
                #position x,y,z
                vdata.append(this.xc * float(x) - helfx)
                vdata.append(0.)
                vdata.append(this.yc * float(y) - helfy)
        for y in range(this.yr - 1):
            for x in range(this.xr - 1):
                vindex.append((y + 0) * this.xr + x)
                vindex.append((y + 1) * this.xr + x)
                vindex.append((y + 0) * this.xr + x + 1)
                vindex.append((y + 0) * this.xr + x + 1)
                vindex.append((y + 1) * this.xr + x)
                vindex.append((y + 1) * this.xr + x + 1)
        print len(vdata),len(vindex)
        this.data = vdata
        this.idata = vindex
        print len(this.data)
    def draw(this):
        if this.bCreate == False:            
            this.vbo = vbo.VBO(ny.array(this.data,'f'))
            this.ebo = vbo.VBO(ny.array(this.idata,'H'),target = GL_ELEMENT_ARRAY_BUFFER)
            this.eboLength = len(this.idata)
            this.bCreate = True
            #this.createVAO()
        this.vbo.bind()
        glInterleavedArrays(GL_T2F_V3F,0,None)
        this.ebo.bind()
        glDrawElements(GL_TRIANGLES,this.eboLength,GL_UNSIGNED_SHORT,None)  
    def setHeight(this,image):
        ix = image.size[0] 
        iy = image.size[1] 
        this.heightImage = image
        print ix,iy
        #print "xr,yr",this.xr,this.yr
        lerp = lambda a,b,d:a * d + b * (1.0 - d)  
        fade = lambda t : t * t * (3.0 - 2.0 * t)  #t*t*t*(t*(t*6.0-15.0)+10.0)
        for y in range(this.yr):
            for x in range(this.xr):  
                # y index location in this.data
                #if x != 0 or y != 0:
                    #continue
                index = 5 * (this.xr * y + x) + 3
                #print index
                fx = float(x) / float(this.xr - 1) * float(ix - 1)
                fy = float(y) / float(this.yr - 1) * float(iy - 1)
                #print float(x) / float(this.xr - 1),fx,float(y) /
                #float(this.yr - 1),fy
                xl,xr,yu,yd = int(math.floor(fx)),int(math.ceil(fx)),int(math.floor(fy)),int(math.ceil(fy))
                dx,dy = fade(fx - xl),fade(fy - yu)  
                #print "loc:",xl,xr,yu,yd,dx,dy
                #left up,right up,left down,right down
                lu,ru,ld,rd = image.im[ix * yu + xl],image.im[ix * yu + xr],image.im[ix * yd + xl],image.im[ix * yd + xr] 
                #print ix * yu + xl,lu,ru,ld,rd
                hight = lerp(lerp(lu,ru,dx),lerp(ld,rd,dx),dy)
                this.data[index] = hight / 255.0
                #print "setHeight:",hight / 255.0
    def getHeight(this,x,y):
        image = this.heightImage
        ix = image.size[0] 
        iy = image.size[1] 
        lerp = lambda a,b,d:a * d + b * (1.0 - d) 
        fade = lambda t : t * t * (3.0 - 2.0 * t)  #t*t*t*(t*(t*6.0-15.0)+10.0)
        #fx,fy
        fx = (float(x) / float(this.xl) + 0.5) * float(ix - 1)
        fy = (float(y) / float(this.xl) + 0.5) * float(iy - 1)
        #print "vv:",fx,fy
        #print float(x) / float(this.xr - 1),fx,float(y) / float(this.yr -
        #1),fy
        xl,xr,yu,yd = int(math.floor(fx)),int(math.ceil(fx)),int(math.floor(fy)),int(math.ceil(fy))
        dx,dy = fade(fx - xl),fade(fy - yu)  
        #print "loc:",xl,xr,yu,yd,dx,dy
        #left up,right up,left down,right down
        lu,ru,ld,rd = image.im[ix * yu + xl],image.im[ix * yu + xr],image.im[ix * yd + xl],image.im[ix * yd + xr] 
        #print ix * yu + xl,lu,ru,ld,rd
        hight = lerp(lerp(lu,ru,dx),lerp(ld,rd,dx),dy) / 255.0
        #print hight
        return hight
#
class camera:
    origin = [0.0,0.0,0.0]
    length = 1.
    yangle = 0.
    zangle = 0.
    __bthree = False
    def __init__(this):
        this.mouselocation = [0.0,0.0]
        this.offest = 0.03
        this.zangle = 0. if not this.__bthree else math.pi
    def setthree(this,value):
        this.__bthree = value
        this.zangle = this.zangle + math.pi
        this.yangle = - this.yangle          
    def eye(this):
        return this.origin if not this.__bthree else this.direction()
    def target(this):
        return this.origin if this.__bthree else this.direction()
    def direction(this):
        if this.zangle > math.pi * 2.0 :
            this.zangle < - this.zangle - math.pi * 2.0
        elif this.zangle < 0. :
            this.zangle < - this.zangle + math.pi * 2.0
        len = 1. if not this.__bthree else this.length if this.length != 0. else 1.        
        xy = math.cos(this.yangle) * len
        x = this.origin[0] + xy * math.sin(this.zangle)
        y = this.origin[1] + len * math.sin(this.yangle)
        z = this.origin[2] + xy * math.cos(this.zangle)        
        return [x,y,z]
    def move(this,x,y,z):
        sinz,cosz = math.sin(this.zangle),math.cos(this.zangle)        
        xstep,zstep = x * cosz + z * sinz,z * cosz - x * sinz
        if this.__bthree : 
            xstep = -xstep
            zstep = -zstep
        this.origin = [this.origin[0] + xstep,this.origin[1] + y,this.origin[2] + zstep]        
    def rotate(this,z,y):
        this.zangle,this.yangle = this.zangle - z,this.yangle + y if not this.__bthree else -y
    def setLookat(this):
        ve,vt = this.eye(),this.target()        
        glLoadIdentity()
        gluLookAt(ve[0],ve[1],ve[2],vt[0],vt[1],vt[2],0.0,1.0,0.0)                
    def keypress(this,key, x, y):
        if key in ('e', 'E'):
            this.move(0.,0.,1 * this.offest)
        if key in ('f', 'F'):
            this.move(-1 * this.offest,0.,0.)
        if key in ('s', 'S'):
            this.move(1 * this.offest,0.,0.)
        if key in ('d', 'D'):
            this.move(0.,0.,-1 * this.offest)
        if key in ('w', 'W'):
            this.move(0.,1 * this.offest,0.)
        if key in ('r', 'R'):
            this.move(0.,-1 * this.offest,0.)
        if key in ('v', 'V'):
            #this.__bthree = not this.__bthree
            this.setthree(not this.__bthree)
        if key == GLUT_KEY_UP:
            this.offest = this.offest + 0.1
        if key == GLUT_KEY_DOWN:
            this.offest = this.offest - 0.1
    def mouse(this,x,y):  
        rx = (x - this.mouselocation[0]) * this.offest * 0.1
        ry = (y - this.mouselocation[1]) * this.offest * -0.1
        this.rotate(rx,ry)
        #print x,y
        this.mouselocation = [x,y]

class transformFeedback(common):
    def __init__(this,pro):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        data1 = [1.0] * 5
        this.vbo = vbo.VBO(ny.array(data,'f'))
        this.tbo = vbo.VBO(ny.array(data1,'f'))
        glUseProgram(pro)
        pi = pro.invalue
        #this.vbo = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER, this.vbo)
        #output data
        this.tbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, this.tbo)
        glBufferData(GL_ARRAY_BUFFER, 40, None, GL_STATIC_DRAW)
        #input data 
        this.vbo.bind()
        glEnableVertexAttribArray(pi)
        #in pyopengl,the glVertexAttribPointer last two params must not be 0,0
        glVertexAttribPointer(pi,1,GL_FLOAT,False,4*1,this.vbo) 
        glEnable(GL_RASTERIZER_DISCARD)
        glBindBufferBase(GL_TRANSFORM_FEEDBACK_BUFFER, 0, this.tbo)
        glBeginTransformFeedback(GL_POINTS)
        glDrawArrays(GL_POINTS, 0, 5)
        glEndTransformFeedback()
        glDisable(GL_RASTERIZER_DISCARD)
        glDisableVertexAttribArray(pi)
        glFlush()

        glBindBuffer(GL_ARRAY_BUFFER, this.tbo)
        buffer = (ctypes.c_float * 10)()
        #get buffer pointer
        point = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_float)) 
        glGetBufferSubData(GL_ARRAY_BUFFER, 0, 10 * 4,point)        
        #convert pointer to array
        array = ny.ctypeslib.as_array(point,(10,))
        print "tf",array

        bf = glMapBuffer(GL_TRANSFORM_FEEDBACK_BUFFER,GL_READ_WRITE)
        pointv = ctypes.cast(bf, ctypes.POINTER(ctypes.c_float))
        arrayv = ny.ctypeslib.as_array(pointv,(5,))
        print "tfv",arrayv
        glUnmapBuffer(GL_ARRAY_BUFFER) 

        