import vtk
from vtk.util.colors import brown_ochre, tomato, banana

# 1. Read input file
fohe = vtk.vtkBYUReader()
fohe.SetGeometryFileName("fohe.g")

# Create Mapper of FOHE
foheMapper = vtk.vtkPolyDataMapper()
foheMapper.SetInputConnection(fohe.GetOutputPort())

# Get and store center and normals
foheCenter = foheMapper.GetCenter()

foheNormals = vtk.vtkPolyDataNormals()
foheNormals.SetInputConnection(fohe.GetOutputPort())

# 2. Create plane with origin as center of FOHE data and set normal
fohePlane = vtk.vtkPlane()
fohePlane.SetOrigin(foheCenter)
fohePlane.SetNormal(0.866, 0.0, -0.5) # Set the normal vector to [0.866, 0.0, -0.5]T

# 3. Create a clipper to clip the object/data
foheClipper = vtk.vtkClipPolyData()
foheClipper.SetInputConnection(foheNormals.GetOutputPort())
foheClipper.SetClipFunction(fohePlane) #Setting the plane to clip the data.
foheClipper.GenerateClipScalarsOn() #Interpolate output scalar values
foheClipper.GenerateClippedOutputOn() #Generate clipped out data
foheClipper.SetValue(0) #Clipping value of the implicit function set to 0.

foheClipMapper = vtk.vtkPolyDataMapper()
foheClipMapper.SetInputConnection(foheClipper.GetOutputPort())
foheClipMapper.ScalarVisibilityOff()
backProp = vtk.vtkProperty()
backProp.SetDiffuseColor(tomato)

# Create clip actor
foheClipActor = vtk.vtkActor()
foheClipActor.SetMapper(foheClipMapper)
foheClipActor.GetProperty().SetColor(brown_ochre) # Set clipped data colour
foheClipActor.SetBackfaceProperty(backProp)

# 4. Show the intersection area between the plane and polygonal data.

# VTK Cutter to display intersection area
foheCutEdges = vtk.vtkCutter()
foheCutEdges.SetInputConnection(foheNormals.GetOutputPort())
foheCutEdges.SetCutFunction(fohePlane)
foheCutEdges.GenerateCutScalarsOn()
foheCutEdges.SetValue(0, 0)

foheCutStrips = vtk.vtkStripper()
foheCutStrips.SetInputConnection(foheCutEdges.GetOutputPort())
foheCutStrips.Update()
foheCutPoly = vtk.vtkPolyData()
foheCutPoly.SetPoints(foheCutStrips.GetOutput().GetPoints()) # Get points from strips
foheCutPoly.SetPolys(foheCutStrips.GetOutput().GetLines()) # Create polygonal data to be displayed

# Create Triangle Filter
foheCutTriangles = vtk.vtkTriangleFilter()
foheCutTriangles.SetInputData(foheCutPoly)
foheCutMapper = vtk.vtkPolyDataMapper()
foheCutMapper.SetInputData(foheCutPoly)
foheCutMapper.SetInputConnection(foheCutTriangles.GetOutputPort())
foheCutActor = vtk.vtkActor()
foheCutActor.SetMapper(foheCutMapper)
foheCutActor.GetProperty().SetColor(banana)

# Create mapper and actor for remaining data
foheRestMapper = vtk.vtkPolyDataMapper()
foheRestMapper.SetInputData(foheClipper.GetClippedOutput())
foheRestMapper.ScalarVisibilityOff()
foheRestActor = vtk.vtkActor()
foheRestActor.SetMapper(foheRestMapper)
foheRestActor.GetProperty().SetRepresentationToWireframe()


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


# Add actors to viewports
renTL.AddActor(foheClipActor)
renBL.AddActor(foheCutActor)
renTR.AddActor(foheRestActor)

renBR.AddActor(foheClipActor)
renBR.AddActor(foheCutActor)
renBR.AddActor(foheRestActor)


# SetActiveCameras to the ActiveCamera of the first renderer
# This allows the visualization to be viewed from same angel in all four viewports
renTR.SetActiveCamera(renTL.GetActiveCamera());
renBR.SetActiveCamera(renTL.GetActiveCamera());
renBL.SetActiveCamera(renTL.GetActiveCamera());
renTL.ResetCamera()


# Render the window with all the reprsentations
rw.Render()
rw.SetWindowName('MM 802 - Assignment 3 - Harsh Sharma') # Set the windows name

# Writing the rendered scene to JPEG
win2Im = vtk.vtkWindowToImageFilter()
win2Im.SetInput(rw) 
win2Im.ReadFrontBufferOff()
win2Im.Update()

imWriter = vtk.vtkJPEGWriter() # Create a jpeg file writer
imWriter.SetFileName('assignment3_sharma_harsh.jpg') # output jpeg filename.
imWriter.SetInputConnection(win2Im.GetOutputPort()) # Get render window scene
imWriter.Write()


iren.Start()
