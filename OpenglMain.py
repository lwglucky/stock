#!/usr/bin/env python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

import sys
import common

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.vertex_shader import *

from OpenGL.GL import shaders
from ctypes import *
from OpenGL.GL.shaders import ShaderProgram

sph = common.sphere(16,16,1)
camera = common.camera()
plane = common.plane(12,12,1.,1.)


def InitGL(width, height):
    glClearColor(0.1, 0.1, 0.5, 0.1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glClearDepth(1.0)
#    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    camera.move(0.0, 3.0, -15)


def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    camera.setLookat()
    plane.draw()
    glTranslatef(-1.5, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glEnd()
    glTranslatef(3.0, 0.0, 0.0)
    sph.draw()
    glutSwapBuffers()

def InitShaders():
    global sP
    sP = ShaderProgram()
    sP.addShader(GL_VERTEX_SHADER_ARB, "v.vert")
    sP.addShader(GL_FRAGMENT_SHADER_ARB, "f.frag")
    sP.linkShaders()
    sP.enable()
    glUniform1fARB(sP.indexOfUniformVariable("Amplitude"), 0.3)
    glUniform3fvARB(sP.indexOfUniformVariable("LightPosition"), 1,   (0.0, 0.0, 3.0))
    glUniform3fvARB(sP.indexOfUniformVariable("BrickColor"), 1,   (1.0, 0.3, 0.2))
    glUniform3fvARB(sP.indexOfUniformVariable("MortarColor"), 1, (0.85, 0.86, 0.84))
    glUniform2fvARB(sP.indexOfUniformVariable("BrickSize"), 1,  (0.3, 0.15))
    glUniform2fvARB(sP.indexOfUniformVariable("BrickPct"), 1, \
                    (0.9, 0.85))

def mouseButton(button, mode, x, y):
    if button == GLUT_RIGHT_BUTTON:
        camera.mouselocation = [x, y]


def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 400)
    glutInitWindowPosition(40, 40)
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


if __name__ == '__main__':
    main()
