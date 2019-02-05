# -*- coding: utf-8 -*-
"""
 Created on Tue 04 Feb 2019 16:14:19
 @Author: Harsh Sharma
 @Email: contact@hsharma.xyz


 MM 804 GRAPHICS AND ANIMATION - Assigment 1
 Render 3d object using VTK in following representation
 1) Wireframe
 2) With texture
 3) Surface
 4) With textire and shading

 Refer Assignment1.pdf for more details 
"""

import vtk

# Define the object, texture and output file names
objectFileName = 'apple_obj.obj'
jpegFileName = 'apple_texture.jpg'
outputFileName = 'assignment1_sharma_harsh.jpg'


# Initialize render window
iren_list = []
rw = vtk.vtkRenderWindow()
rw.SetSize(1300, 950) #Set render window size.
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(rw)


# Locations of the viewports
xmins=[0,.5,0,.5]
xmaxs=[0.5,1,0.5,1]
ymins=[0,0,.5,.5]
ymaxs=[0.5,0.5,1,1]

# Intialize view ports and set location
# Bottom left
renBL = vtk.vtkRenderer()
rw.AddRenderer(renBL)
renBL.SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0])

# Bottom right
renBR = vtk.vtkRenderer()
rw.AddRenderer(renBR)
renBR.SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1])

# Top left
renTL = vtk.vtkRenderer()
rw.AddRenderer(renTL)
renTL.SetViewport(xmins[2],ymins[2],xmaxs[2],ymaxs[2])

# Top right
renTR = vtk.vtkRenderer()
rw.AddRenderer(renTR)
renTR.SetViewport(xmins[3],ymins[3],xmaxs[3],ymaxs[3])


# Define light properties
light = vtk.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, 100, 100)
light.SetFocalPoint(0,0,0)
light.SetIntensity(0.7)



# Read the object from file 
appleObject = vtk.vtkOBJReader()
appleObject.SetFileName(objectFileName)

# Read the texture from file
textureObject = vtk.vtkJPEGReader()
textureObject.SetFileName(jpegFileName)
texture = vtk.vtkTexture()
texture.SetInputConnection(textureObject.GetOutputPort())

# Initialize the mapper for non-textured rendering
objectMapperPlain = vtk.vtkPolyDataMapper()
objectMapperPlain.SetInputConnection(appleObject.GetOutputPort())

# Initialize the mapper for rendering with texture
objectMapperTexture = vtk.vtkPolyDataMapper()
objectMapperTexture.SetInputConnection(appleObject.GetOutputPort())


# Create actor for surface rendering
objectActor_Surface=vtk.vtkActor()
objectActor_Surface.SetMapper(objectMapperPlain)
objectActor_Surface.GetProperty().SetRepresentationToSurface()

# Create actor for wireframe rendering
objectActor_wireframe=vtk.vtkActor()
objectActor_wireframe.SetMapper(objectMapperPlain)
objectActor_wireframe.GetProperty().SetRepresentationToWireframe()

# Create actor for rendering with only texture
objectActor_texture=vtk.vtkActor()
objectActor_texture.SetMapper(objectMapperTexture)
objectActor_texture.SetTexture(texture)

# Create actor for rendering with texture and shading
objectActor_shading=vtk.vtkActor()
objectActor_shading.SetMapper(objectMapperTexture)
objectActor_shading.SetTexture(texture)

#Compute normals for phong shading
normal = vtk.vtkPolyDataNormals()
normal.SetInputConnection(appleObject.GetOutputPort())

#Set actor properties for phong shading
properties = objectActor_shading.GetProperty()
properties.SetInterpolationToPhong()
properties.ShadingOn()
properties.SetDiffuse(0.8) 
properties.SetAmbient(0.15)
properties.SetSpecular(0.9) 
properties.SetSpecularPower(100.0)


# Set caption texts and properties

txtTL = vtk.vtkTextActor() # Text actor for top left view port
txtTL.SetInput('''View Port 1
Representation – Wireframe
(No shading or texture)''') # Set the caption text
txtpropTL=txtTL.GetTextProperty()
txtpropTL.SetFontSize(18) # Set the font size
txtTL.SetPosition(100,50) # position in lower left corner of view port

txtTR = vtk.vtkTextActor() # Text actor for top right view port
txtTR.SetInput('''View Port 2
Surface with texture map
(No shading)''') # Set the caption text
txtpropTR=txtTR.GetTextProperty()
txtpropTR.SetFontSize(18) # Set the font size
txtTR.SetPosition(100,50) # position in lower left corner of view port

txtBL = vtk.vtkTextActor() # Text actor for bottom left view port
txtBL.SetInput('''View Port 3
Representation – Surface
(No shading or texture)''') # Set the caption text
txtpropBL=txtBL.GetTextProperty()
txtpropBL.SetFontSize(18) # Set the font size
txtBL.SetPosition(100,50) # position in lower left corner of view port

txtBR = vtk.vtkTextActor() # Text actor for bottom right view port
txtBR.SetInput('''View Port 4
Surface with texture map
and Phong shading''') # Set the caption text
txtpropBR=txtBR.GetTextProperty()
txtpropBR.SetFontSize(18) # Set the font size
txtBR.SetPosition(100,50) # position in lower left corner of view port

 
# Add surface actor to rendering viewport
renBL.AddActor(objectActor_Surface)
renBL.AddActor(txtBL)

# Add wireframe actor to rendering viewport
renTL.AddActor(objectActor_wireframe)
renTL.AddActor(txtTL)

# Add texture actor to rendering viewport
renTR.AddActor(objectActor_texture)
renTR.AddActor(txtTR)

# Add texture+shading actor to rendering viewport
renBR.AddActor(objectActor_shading)
renBR.AddLight(light) # Add light to the viewport scene.
renBR.AddActor(txtBR)

# Render the window with all the reprsentations
rw.Render()
rw.SetWindowName('MM 802 - Assignment 1') # Set the windows name

# Writing the rendered scene to JPEG
win2Im = vtk.vtkWindowToImageFilter()
win2Im.SetInput(rw) 
win2Im.ReadFrontBufferOff()
win2Im.Update()

imWriter = vtk.vtkJPEGWriter() # Create a jpeg file writer
imWriter.SetFileName(outputFileName) # output jpeg filename.
imWriter.SetInputConnection(win2Im.GetOutputPort()) # Get render window scene
imWriter.Write()


iren.Start()

