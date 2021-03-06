import maya.cmds as mc

# def buttonFunction(*args):
#     for arg in args:
#         print(arg) 
#     mc.polyCube()

# def showUI():
#     if (mc.window("ymButtonExample", exists=True)):
#         mc.deleteUI("ymButtonExample")
#     myWin = mc.window("ymButtonExample", title="Button Example", widthHeight=(200, 200))
#     mc.columnLayout()
#     mc.button(label="Make Cube", command=buttonFunction)
#     mc.showWindow(myWin)

# global sphereCountField
# global sphereRadiusField

# def anotherShowUI():
#     global sphereCountField
#     global sphereRadiusField

#     myWin = mc.window(title="Make Spheres", widthHeight=(300, 200))
#     mc.columnLayout()
#     sphereCountField = mc.intField(minValue=1)
#     sphereRadiusField=mc.floatField(minValue=0.5)
#     mc.button(label="Make Spheres", command=makeSpheres)
#     mc.showWindow(myWin)

# def makeSpheres(*args):
#     global sphereCountField
#     global sphereRadiusField

#     numSpheres = mc.intField(sphereCountField, q=1, value=1)
#     myRadius = mc.floatField(sphereRadiusField, q=1, value=1)
    
#     for i in range(numSpheres):
#         sphere=mc.polySphere(radius=myRadius)
#         mc.move((i*myRadius*2.2), 0, 0, sphere)

# anotherShowUI()

#Classes
# class SpheresClass:
#     def __init__(self):
#         self.win = mc.window(title="Make Spheres", widthHeight=(300,200))
#         mc.columnLayout()
#         self.numSpheres = mc.intField(minValue=1)
#         mc.button(label="Make Spheres", command=self.makeSpheres)
#         mc.showWindow(self.win)
    
#     def makeSpheres(self, *args):
#         number = mc.intField(self.numSpheres, q=1, value=1)
#         for i in range (0, number):
#             sphere=mc.polySphere()
#             mc.move(i*2.2, 0, 0, sphere)

# SpheresClass()

# #Nested Layouts:

# class NestedLayouts:
#     def __init__(self):
#         self.win = mc.window(title="Nested Layouts", widthHeight=(300,200))
#         mc. columnLayout()

#         mc.rowLayout(numberOfColumns=2)
#         mc.text(label="Input One: ")
#         self.inputOne = mc.intField()
#         mc.setParent("..")

#         mc.rowLayout(numberOfColumns=2)
#         mc.text(label="Input Two: ")
#         self.inputTwo = mc.intField()
#         mc.setParent("..")

#         mc.showWindow(self.win)

# NestedLayouts()

#Tab Example:

