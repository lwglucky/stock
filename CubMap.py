#! /usr/bin/env python

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()

from  OpenGL.GL import *
from  OpenGL.arrays import vbo
from  OpenGLContext.arrays import *
from  OpenGL.GL import shaders
from  LoadObj  import  ObjLoader

from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
import common

from Image import *


SKYBOX_VSOURCE = """ #version 330 core
                    layout (location = 0) in vec3 position;
                    out vec3 TexCoords;
                    uniform mat4 projection;
                    uniform mat4 view;
                    void main() {
                        gl_Position =   projection * view * vec4(position, 1.0);
                        TexCoords = position;
                    } """
SKYBOX_FSOURCE = """#version 330 core
                    in vec3 TexCoords;
                    out vec4 color;
                    uniform samplerCube skybox;
                    void main() {
                        color = texture(skybox, TexCoords);
                    }
                """

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
            }"""

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

class  CubMapContext  (  BaseContext ):
    """Creates a simple vertex shader..."""
    cubmaps = [ 'ft.JPG' ,'bk.JPG' , 'up.JPG' , 'dn.JPG' ,  'lf.JPG' , 'rt.JPG' ]
    # cubmaps = ['lf.JPG', 'lf.JPG', 'lf.JPG', 'lf.JPG', 'lf.JPG', 'lf.JPG']
    cubemapTexture = 0

    def LoadSkyBoxVBO(self):
        data = np.array (  [[-1.0,  1.0, -1.0],  [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0],\
                            [ 1.0, -1.0, -1.0],  [ 1.0,  1.0, -1.0], [-1.0,  1.0, -1.0], \
                            [-1.0, -1.0, 1.0],   [-1.0, -1.0, -1.0],  [-1.0, 1.0, -1.0],\
                            [-1.0, 1.0, -1.0],  [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], \
                            [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0],\
                            [1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [1.0, -1.0, -1.0], \
                            [-1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0],\
                            [1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [-1.0, -1.0, 1.0], \
                            [-1.0, 1.0, -1.0], [1.0, 1.0, -1.0], [1.0, 1.0, 1.0],\
                            [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], \
                            [-1.0, -1.0, -1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, -1.0],\
                            [1.0, -1.0, -1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0]] \
                            , np.float32)
        return data , len(data)

    def loadCubemap(self , names):
        # global texture
        id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, id)  # 2d texture (x and y size)
        for (name, i) in zip(names, np.arange(len(names))):
            image = open(name)
            image = image.transpose(FLIP_TOP_BOTTOM)
            ix , iy = image.size[0] , image.size[1]
            print type(image)
            image = image.tostring("raw", "RGBX", 0, -1)
            # Create Texture
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X+i, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
        return id

    def LoadShader(self , vsource , fsource):
        sh_vertex = shaders.compileShader(vsource, GL_VERTEX_SHADER)
        sh_fragment = shaders.compileShader(fsource, GL_FRAGMENT_SHADER)
        try:
            prog = shaders.compileProgram(sh_vertex, sh_fragment)
            return prog
        except  (GLError, RuntimeError) as err:
            print ('Example of shader compile error', err)
            return 0
        return 0

    def OnInit(self):
        self.camera = common.camera()
        self.camera.move(0.0, 1.3, -3.0)
        self.camera.setthree(True)
        self.camera.length = 3

        self.prog = self.LoadShader(VSOURCE,FSORUCE)
        self.skybox_prog = self.LoadShader(SKYBOX_VSOURCE,SKYBOX_FSOURCE)

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


        self.skybox_len = len(data)
        data , datalen  = self.LoadSkyBoxVBO()
        self.skyboxvbo = vbo.VBO(data)
        self.skybox_len = len(self.skyboxvbo)
        self.cubemapTexture = self.loadCubemap(self.cubmaps)

    def OnCamChange(self, event):
        self.campos[2] = self.campos[1]-0.01
        print ( self.campos)

    def OnLightChange(self, event):
        self.lightpos[2] = self.lightpos[1] - 0.01
        print (self.lightpos)

    def Render(self, mode):

        BaseContext.Render( self, mode )
        glClearColor(0.3, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#### skybox render
        glDepthMask(GL_FALSE)
        glUseProgram(self.skybox_prog)
        glUniformMatrix4fv(glGetUniformLocation(self.skybox_prog, "view"), 1, GL_FALSE, self.viewmatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.skybox_prog, "projection"), 1, GL_FALSE, self.projectmatrix)
        self.skyboxvbo.bind()
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 12, self.skyboxvbo)
        glActiveTexture(GL_TEXTURE0)
        glUniform1i(glGetUniformLocation(self.skybox_prog, "skybox"), 0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubemapTexture)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        self.skyboxvbo.unbind()
        glDisableVertexAttribArray(0)
        glDepthMask(GL_TRUE)

####scene render
        glUseProgram(self.prog)
        glUniform3fv(glGetUniformLocation(self.prog, "lightPos"), 1,  self.lightpos)
        glUniform3fv(glGetUniformLocation(self.prog, "cameraPos"), 1,  self.campos)
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "m_view"), 1, GL_FALSE, self.viewmatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "projection"), 1, GL_FALSE, self.projectmatrix)
        glUniformMatrix4fv(glGetUniformLocation(self.prog, "model"), 1, GL_FALSE, self.modelmatrix)
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
    CubMapContext.ContextMainLoop()