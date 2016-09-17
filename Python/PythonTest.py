

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from Image import *
import common
import sys
import shaderProg
import loadtexture
import numpy as ny
import particle
window = 0
sph = common.sphere(16,16,0.3)
camera = common.camera()
plane = common.plane(101,101,0.1,0.1)
#the shaderall,colorMap,hightMap Should be placed after gl init,otherwise all 0
shaderall = None
tf = None
ps = None
colorMap = 0 
hightMap = 0 
def InitGL(width,height):
    glClearColor(0.1,0.1,0.5,0.1)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    camera.move(0.0,1.3,0.0)   
    camera.setthree(True)
    camera.length = 3
    global shaderall
    shaderall = shaderProg.allshader() 
    global tf
    tf = common.transformFeedback(shaderall.tfProgram)
    global ps
    ps = particle.particleSystem(5000)
    global colorMap 
    global hightMap    
    colorMap = loadtexture.Texture.loadmap("ground2.bmp")
    #hight map for cpu to gpu
    hightMap = loadtexture.Texture.loadmap("hight.gif")
    #create terrain use cpu
    hightimage = loadtexture.Texture.loadterrain("hight.gif")
    image = open("ground2.bmp").convert("RGBA")
    plane.setHeight(hightimage)
def DrawGLScene():    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)   
    glMatrixMode(GL_MODELVIEW)     
    camera.setLookat()
    #texture set
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, colorMap) 
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, hightMap)     
    #plane
    glUseProgram(shaderall.planeProgram)
    glUniform1i(shaderall.planeProgram.tex0, 0) 
    plane.draw() 
    glUseProgram(0)
    #sphare
    eyeLoc = camera.origin
    uv = eyeLoc[0] / plane.xl + 0.5,eyeLoc[2] / plane.yl + 0.5
    glUseProgram(shaderall.updateProgram)    
    glUniform1f(shaderall.updateProgram.xl, plane.xl)  
    glUniform1f(shaderall.updateProgram.yl, plane.yl) 
    #CPU compute height
    #glUniform1f(shaderall.updateProgram.height,
    #plane.getHeight(eyeLoc[0],eyeLoc[2]))
    glUniform1f(shaderall.updateProgram.sphereRadius, sph.radius)
    glUniform1i(shaderall.updateProgram.tex0, 1) 
    #print uv
    glUniform2f(shaderall.updateProgram.xz,eyeLoc[0],eyeLoc[2]) 
    #print "eye:",eyeLoc,eyeLoc[0],eyeLoc[2]
    getMVP(eyeLoc)
    sph.draw(shaderall.updateProgram.pos)   
    glUseProgram(0)  

    glUseProgram(shaderall.particleProgram)
    glUniform1i(shaderall.particleProgram.plane, 1) 
    glUniform2f(shaderall.particleProgram.planeSacle,plane.xl,plane.yl)     
    glUniform3f(shaderall.particleProgram.sphere,eyeLoc[0],sph.radius,eyeLoc[2]) 
    ps.render(shaderall.particleProgram)
    glUseProgram(0)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

    glBegin(GL_LINES)
    glColor(1.0,0.0,0.0)
    glVertex3f(-plane.xl / 2.0, 1.0, -plane.yl / 2.0)
    glVertex3f(100.0, 1.0, -plane.yl / 2.0)
    glColor(0.0,1.0,0.0)
    glVertex3f(-plane.xl / 2.0, 1.0, -plane.yl / 2.0)
    glVertex3f(-plane.xl / 2.0, 1.0, 100.0)

    glColor(1.0,0.0,0.0)
    glVertex3f(0.0, 0.0,0.0)
    glVertex3f(100.0, 0.0, 0.0)
    glColor(0.0,1.0,0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 100.0)
    glEnd()
    
    glutSwapBuffers()

def getMVP(eye):
    v = ny.array(glGetFloatv(GL_MODELVIEW_MATRIX), ny.float32)
    p = ny.array(glGetFloatv(GL_PROJECTION_MATRIX), ny.float32)
    m = ny.array([[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0],[eye[0],0,eye[2],1]],ny.float32)
    #print m
    glUniformMatrix4fv(shaderall.updateProgram.pMatrix,1,GL_FALSE,p)
    glUniformMatrix4fv(shaderall.updateProgram.vMatrix,1,GL_FALSE,v)
    glUniformMatrix4fv(shaderall.updateProgram.mMatrix,1,GL_FALSE,m) 
    #glgetfloat
def mouseButton(button, mode, x, y):	
	if button == GLUT_RIGHT_BUTTON:
		camera.mouselocation = [x,y]

def ReSizeGLScene(Width, Height): 
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #glOrtho(-5, 5, -5, 5,0.0,20)
    glMatrixMode(GL_MODELVIEW)
    
def main():
    global window
    #glutInit(sys.argv)
    glutInit([])
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640,480)    
    glutInitWindowPosition(800,600)
    window = glutCreateWindow("opengl")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutMouseFunc(mouseButton)
    glutMotionFunc(camera.mouse)
    glutKeyboardFunc(camera.keypress)
    glutSpecialFunc(camera.keypress)
    InitGL(640, 480)
    glutMainLoop()

main()
