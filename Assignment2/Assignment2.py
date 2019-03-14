# -*- coding: utf-8 -*-
"""
 Created on Wed 06 Mar 2019 18:31:56
 @Author: Harsh Sharma
 @Email: contact@hsharma.xyz
 
 Description
"""

import vtk

# 1. Read CT dataset using vtkDICOMImageReader class.
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("CT")
reader.Update()
print("CT Data Loaded.")
# ---------------------------------------------------------

# 2. Create a colour transfer function using the following values.
colorTransfer = vtk.vtkColorTransferFunction()
colorTransfer.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorTransfer.AddRGBPoint(-77, 0.5, 0.2, 0.1)
colorTransfer.AddRGBPoint(94, 0.9, 0.6, 0.3)
colorTransfer.AddRGBPoint(179, 1.0, 0.9, 0.9)
colorTransfer.AddRGBPoint(260, 0.6, 0.0, 0.0)
colorTransfer.AddRGBPoint(3071, 0.8, 0.7, 1.0)
print("Colour transfer function created.")
# ---------------------------------------------------------

# 3. Create a opacity transfer function using the following values.
opacityTransfer = vtk.vtkPiecewiseFunction()
opacityTransfer.AddPoint(-3024, 0.0)
opacityTransfer.AddPoint(-77, 0.0)
opacityTransfer.AddPoint(180, 0.2)
opacityTransfer.AddPoint(260, 0.4)
opacityTransfer.AddPoint(3071, 0.8)
print("Opacity transfer function created.")
# ---------------------------------------------------------

# 4. Create viewports as shown below and render the CT dataset 
# using direct volume rendering approach in viewport 1.
ctMapper = vtk.vtkSmartVolumeMapper()
ctMapper.SetInputConnection(reader.GetOutputPort())

# Add the opacity and colour transfer functions defined above
ctProp = vtk.vtkVolumeProperty()
ctProp.SetScalarOpacity(opacityTransfer)
ctProp.SetColor(colorTransfer)
ctProp.ShadeOn()

# Define a volume actor
ctVolume = vtk.vtkVolume()
volRen = vtk.vtkRenderer()

# Set volume actor properties
ctVolume.SetMapper(ctMapper)
ctVolume.SetProperty(ctProp)

volRen.AddVolume(ctVolume)
print("Volume rendering done.")

# ---------------------------------------------------------
# 5. In viewport 2, display the iso-surface extracted at intensity 
# value 300 using marching cubes algorithm. 

iso = vtk.vtkMarchingCubes()
iso.SetInputConnection(reader.GetOutputPort())
iso.ComputeGradientsOn()
iso.ComputeScalarsOff()
# print (iso.GetValue(0))
iso.SetValue(0, 300)

# Polydata mapper for the iso-surface
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(iso.GetOutputPort())
isoMapper.ScalarVisibilityOff()

# Actor for the iso surface
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(1.,1.,1.)

## renderer and render window
isoRen = vtk.vtkRenderer()
## add the actors to the renderer
isoRen.AddActor(isoActor)
print("ISO surface extracted.")
# ---------------------------------------------------------

# 6. Create a combo rederer
comboRen = vtk.vtkRenderer()

# Reuse actor and volume
comboRen.AddActor(isoActor)
comboRen.AddVolume(ctVolume)
# ---------------------------------------------------------

print("Creating render window")
# Create a render window with three viewports
xmins=[0,0.33,0.66]
xmaxs=[0.33,0.66,1]
ymins=[0,0,0]
ymaxs=[1,1,1]

mainWindow = vtk.vtkRenderWindow()
windInteract = vtk.vtkRenderWindowInteractor()
mainWindow.SetSize(1300,600)
windInteract.SetRenderWindow(mainWindow)

# SetActiveCameras to the ActiveCamera of the first renderer
# This allows the visualization to be viewed from same angel in all three viewports
isoRen.SetActiveCamera(volRen.GetActiveCamera());
comboRen.SetActiveCamera(isoRen.GetActiveCamera());
volRen.ResetCamera()

# Add the renderes to main window
mainWindow.AddRenderer(volRen)
mainWindow.AddRenderer(isoRen)
mainWindow.AddRenderer(comboRen)

# Set the location
volRen.SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0])
isoRen.SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1])
comboRen.SetViewport(xmins[2],ymins[2],xmaxs[2],ymaxs[2])

mainWindow.Render()

wind2Im = vtk.vtkWindowToImageFilter()
wind2Im.SetInput(mainWindow)
wind2Im.Update()

# Save the output
writer = vtk.vtkJPEGWriter()
writer.SetInputConnection(wind2Im.GetOutputPort())
writer.SetFileName('assignment2_sharma_harsh.jpg')
writer.Write()


windInteract.Initialize()
windInteract.Start()













