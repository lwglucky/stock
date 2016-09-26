#! /usr/bin/env python

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()

from  OpenGL.GL import *
from  OpenGL.arrays import vbo
from  OpenGLContext.arrays import *
from  OpenGL.GL import shaders
from  LoadObj import  ObjLoader

from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

import common


# v = ny.array(glGetFloatv(GL_MODELVIEW_MATRIX), ny.float32)
#     p = ny.array(glGetFloatv(GL_PROJECTION_MATRIX), ny.float32)
#     m = ny.array([[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0],[eye[0],0,eye[2],1]],ny.float32)
#     #print m
#     glUniformMatrix4fv(shaderall.updateProgram.pMatrix,1,GL_FALSE,p)
#     glUniformMatrix4fv(shaderall.updateProgram.vMatrix,1,GL_FALSE,v)
#     glUniformMatrix4fv(shaderall.updateProgram.mMatrix,1,GL_FALSE,m)

VSOURCE = """ #version 330 core
            layout (location = 0) in vec3 position;
            layout (location = 1) in vec3 normal;
 //           layout (location = 2) in vec3 color;
            uniform mat4 model;
            uniform mat4 m_view;
            uniform mat4 projection;

            out vec3 Normal;
            out vec3 Position;

            void main() {
                  gl_Position = vec4(position, 1.0f);
                gl_Position =  projection * m_view * model * vec4(position, 1.0f);
                Normal =   mat3(transpose(inverse(model))) * normal;
                Position = vec3(model * vec4(position, 1.0f));
            }""";

FSORUCE = """#version 330 core
            out vec4 color;

            in vec3 Normal;
            in vec3 Position;

            uniform vec3 lightPos;
            uniform vec3 cameraPos;

            void main() {
                float ambientStrength = 0.1f;
                vec3 lightColor = vec3(1,1,1);
                vec3 ambient = ambientStrength * lightColor;

                vec3 objcolor = vec3(1,1,1);

                vec3 lightPosv = vec3(0,1,-1);
                lightPosv = lightPos;
                vec3 cameraPosv = cameraPos ;//vec3(0,0,-1);

                vec3 norm = normalize(Normal);
                vec3 lightDir = normalize(lightPosv - Position);
                float diff = max(dot(norm, lightDir), 0.0);
                vec3 diffuse = diff * lightColor;

                float specularStrength = 0.5f;
                vec3 viewDir = normalize(cameraPosv - Position);
                vec3 reflectDir = reflect(-lightDir, norm);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
                vec3 specular =  specularStrength * spec * lightColor;

                vec3 result = (  ambient + diffuse + specular ) * objcolor;
                color = vec4(result, 1.0f) ;

     //           color = vec4(ambient, 1.0f);
           //     color = vec4(ourColor, 1.0f);
            }"""

class  TestContext  (  BaseContext ):
    """Creates a simple vertex shader..."""

    def OnInit(self):
        self.camera = common.camera()
        self.camera.move(0.0, 1.3, -3.0)
        self.camera.setthree(True)
        self.camera.length = 3
        sh_vertex = shaders.compileShader(  VSOURCE , GL_VERTEX_SHADER)
        sh_fragment = shaders.compileShader(FSORUCE,  GL_FRAGMENT_SHADER)
        try:
            self.prog = shaders.compileProgram(sh_vertex, sh_fragment)
        except  (GLError, RuntimeError) as err:
            print ('Example of shader compile error', err)

        data = ObjLoader().LoadObj("buddha.dat");
        self.buddhavbo = vbo.VBO(data)
        self.buddhavbo_len = len(self.buddhavbo)
        self.buddhavbo_len = self.buddhavbo_len / 2*3
        print ("VBO count:" , self.buddhavbo_len)

 #       self.ViewPort(800,800);

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(800) / float(800), 1.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 1.0, -3.0, 0 , 0 , 0 , 0.0, 1.0, 0.0)

        self.viewmatrix = np.array(glGetFloatv(GL_MODELVIEW_MATRIX), np.float32)
        self.projectmatrix = np.array(glGetFloatv(GL_PROJECTION_MATRIX), np.float32)
        self.modelmatrix = np.array([[1, 0, 0, 0],[0, 1, 0, 0], [0, 0, 1, 0],[0,0,0,1]],np.float32)

        self.lightpos =  np.array([0,0,-5])
        self.campos =  np.array([0.0, 0.0, -1.0])

        self.addEventHandler("keypress", name="r", function=self.OnCamChange)
        self.addEventHandler("keypress", name="f", function=self.OnLightChange)

        # print "view matrix:"
        # print  self.viewmatrix
        # print "project matrix"
        # print self.projectmatrix

        # for attribute in ('position', 'normal',):
        #     location = glGetAttribLocation(self.shader, attribute)
        #     if location in (None, -1):
        #         print 'Warning, no attribute: %s' % (attribute)
        #     setattr(self, attribute + '_loc', location)
        # self.vbo = vbo.VBO(array(
        #         [[0, 1, 0, 0, 1, 0], [-1, -1, 0, 1, 1, 0], [1, -1, 0, 0, 1, 1], [2, -1, 0, 1, 0, 0],
        #          [4, -1, 0, 0, 1, 0], [4, 1, 0, 0, 0, 1], [2, -1, 0, 1, 0, 0], [4, 1, 0, 0, 0, 1],
        #          [2, 1, 0, 0, 1, 1], ], 'f'))
        # self.UNIFORM_LOCATIONS = {'end_fog': glGetUniformLocation(self.shader, 'end_fog'),
        #                           'fog_color': glGetUniformLocation(self.shader, 'fog_color'), }

    def OnCamChange(self, event):
        self.campos[2] = self.campos[1]-0.01
        print ( self.campos)

    def OnLightChange(self, event):
        self.lightpos[2] = self.lightpos[1] - 0.01
        print (self.lightpos)

    def Render(self, mode):
        """Render the geometry for the scene."""
  #      shaders.glUseProgram(self.shader)
        BaseContext.Render( self, mode )
        glUseProgram(self.prog)

        # print      (glGetUniformLocation(self.prog, "lightPos") , ':' , self.lightpos)
        # print      (glGetUniformLocation(self.prog, "cameraPos"),  ':' ,self.campos)
        glUniform3fv(glGetUniformLocation(self.prog, "lightPos"), 1,  self.lightpos)
        glUniform3fv(glGetUniformLocation(self.prog, "cameraPos"), 1,  self.campos)

        # print    (  glGetUniformLocation(self.prog, "m_view"), glGetUniformLocation(self.prog, "projection") , glGetUniformLocation(self.prog, "model"))
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "m_view"), 1, GL_FALSE, self.viewmatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "projection"), 1, GL_FALSE, self.projectmatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "model"), 1, GL_FALSE, self.modelmatrix)




        # glUniform1f(self.UNIFORM_LOCATIONS['end_fog'], 15)
        # glUniform4f(self.UNIFORM_LOCATIONS['fog_color'], 1, 1, 1, 1)
        glClearColor(0.3 , 0.0 , 0.0 , 1.0 );
        try:
            self.buddhavbo.bind()
            try:
                glEnableVertexAttribArray(0)
                glEnableVertexAttribArray(1)
                stride = 6 * 4
                glVertexAttribPointer(0, 3, GL_FLOAT, False, stride, self.buddhavbo)
                glVertexAttribPointer(1, 3, GL_FLOAT, False, stride, self.buddhavbo + stride/2)
                glDrawArrays(GL_TRIANGLES, 0,self.buddhavbo_len  )  #
            finally:
                self.buddhavbo.unbind()
                glDisableVertexAttribArray(0)
                glDisableVertexAttribArray(1)
        finally:
            shaders.glUseProgram( 0 )

if __name__ == "__main__":
    TestContext.ContextMainLoop()