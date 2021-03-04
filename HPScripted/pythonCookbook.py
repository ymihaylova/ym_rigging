import maya.cmds as mc

def buttonFunction(args):
    mc.polyCube()

def showUI():
    if (mc.window("ymButtonExample", exists=True)):
        mc.deleteUI("ymButtonExample")
    myWin = mc.window("ymButtonExample", title="Button Example", widthHeight=(200, 200))
    mc.columnLayout()
    mc.button(label="Make Cube", command=buttonFunction)
    mc.showWindow(myWin)

showUI()