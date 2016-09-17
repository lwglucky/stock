#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception



import sys

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.
        '''
  sys.exit()


def display():
   # clear all pixels
   glClear (GL_COLOR_BUFFER_BIT)

   # draw white polygon (rectangle) with corners at
   # (0.25, 0.25, 0.0) and (0.75, 0.75, 0.0)
   glColor3f (1.0, 1.0, 1.0)
   glBegin(GL_POLYGON)
   glVertex3f (0.25, 0.25, 0.0)
   glVertex3f (0.75, 0.25, 0.0)
   glVertex3f (0.75, 0.75, 0.0)
   glVertex3f (0.25, 0.75, 0.0)
   glEnd()

   # don't wait!
   # start processing buffered OpenGL routines
   glFlush ();

def init():
   # select clearing color
   glClearColor (0.0, 0.0, 0.0, 0.0)

   # initialize viewing values
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)

#  Declare initial window size, position, and display mode
#  (single buffer and RGBA).  Open window with "hello"
#  in its title bar.  Call initialization routines.
#  Register callback function to display graphics.
#  Enter main loop and process events.

if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("hello")
    init()
    glutDisplayFunc(display)
    glutMainLoop()
