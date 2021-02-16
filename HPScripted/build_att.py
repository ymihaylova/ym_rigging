from maya import cmds as mc
from maya import OpenMaya as om
# from maya import ctl_shapes as cs

DEBUG_MODE = True
DIAMOND_SHAPE_CVS = [[-1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [1.0, 0.0, 0.0],
                     [0.0, -1.0, 0.0],
                     [-1.0, 0.0, 0.0],
                     [0.0, 0.0, -1.0],
                     [1.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0],
                     [-1.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0],
                     [0.0, 1.0, 0.0],
                     [0.0, 0.0, -1.0],
                     [0.0, -1.0, 0.0],
                     [0.0, 0.0, 1.0]]
                     
SQUARE_SHAPE_CVS = [[-1.0, 0.0, -1.0],
                    [-1.0, 0.0, 1.0],
                    [1.0, 0.0, 1.0],
                    [1.0, 0.0, -1.0],
                    [-1.0, 0.0, -1.0]]



def buildControl(side, name, guide=None, shapeCVs=[], colour=17, offset = []):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    else:
        control = mc.curve(p=shapeCVs, degree=1)
    offset = mc.group(control)
    group = mc.group(offset)

        # NOTE: Check whether name exists and handle it if it does
    control = mc.rename(control, "%s_%s_CTL" % (side, name))
    offset = mc.rename(offset, "%s_%s_OFS" % (side, name))
    group = mc.rename(group, "%s_%s_GRP" % (side, name))

    # #snap to guide
    mc.delete(mc.parentConstraint(guide, group, maintainOffset=0))
    # if offset != []:
    #     mc.move(offset[0], offset[1], offset[2], group, relative=True)

    # Set colour
    mc.setAttr(control + ".overrideEnabled", 1)
    mc.setAttr(control + ".overrideColor", colour)

    return control, offset, group

def getPoleVectorPosition(rootPos, midPos, endPos):

    rootJntVector = om.MVector(rootPos[0], rootPos[1], rootPos[2])
    midJntVector = om.MVector(midPos[0], midPos[1], midPos[2])
    endJntVector = om.MVector(endPos[0], endPos[1], endPos[2])

    rootToEnd = (endJntVector - rootJntVector)
    closestPoint = (midJntVector - rootJntVector)

    scaleValue = (rootToEnd * closestPoint) / (rootToEnd * rootToEnd)

    projectionVector = rootToEnd * scaleValue + rootJntVector

    rootToMidLen = (midJntVector - rootJntVector).length()
    midToEndLen = (endJntVector - midJntVector).length()
    totalLen = rootToMidLen + midToEndLen

    poleVectorPosition = (midJntVector - projectionVector).normal() * \
                    (totalLen * 0.5) + midJntVector
    
    return poleVectorPosition

def getIkhPoleVecPos(ikHandle):

    # List the joint chain IK Handle affects and 
    jointList = mc.ikHandle(ikHandle, q=True, jointList=True)
    jointList.append(mc.listRelatives(jointList[-1], children=True, type="joint")[0])

    rootJntPos = mc.xform(jointList[0], q=1, ws=1, t=1)
    midJntPos = mc.xform(jointList[1], q=1, ws=1, t=1)
    endJntPos = mc.xform(jointList[2], q=1, ws=1, t=1)

    poleVectorPos = getPoleVectorPosition(rootJntPos, midJntPos, endJntPos)

    return poleVectorPos


def main():

    #Create a new file and import model and guides 
    mc.file(new=1, force=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_body.ma", i=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_guides.ma", i=1)


    #create and rename IK copies of joints

    #build FK ctls. IK chain, Handle and Ctls
    fkCtlsList = []
    ikCtlsList = []

    # legBindChain = mc.ls("L_leg??Bind_JNT")[0]
    # # legBindChain.append(mc.listRelatives("L_leg00Bind_JNT", ad=1))
    # print(legBindChain)

    for side in "LR":
        # Build FK controls
        legBindChain = mc.ls("%s_leg??Bind_JNT" % side)
        prevFkCtl = []

        for jnt in range(len(legBindChain)-1):
            fkCtl = buildControl(side, "leg%s" % str(jnt).zfill(2) , legBindChain[jnt], 
                colour=17 if side == "L" else 19)

            mc.scale(6,6,6,fkCtl[0] + ".cv[*]")

            if jnt != (len(legBindChain)-2): # omit rotating the toe FK control CVs 
                mc.rotate(90,0,0,fkCtl[0] + ".cv[*]", ws=1)

            if jnt == 0: # move the hip FK control CVs for visual clarity
                mc.move(0, -8, 0, fkCtl[0] + ".cv[*]", ws=1, r=1)

            if prevFkCtl != []:
                mc.parent(fkCtl[2], prevFkCtl[0])

            fkCtlsList.append(fkCtl)
            prevFkCtl = fkCtl 
        
        # Create IK copy of the leg chain
        ikChain = mc.duplicate("%s_leg00Bind_JNT" % side, renameChildren = 1)
        renamedIkChain = []
        for jnt in ikChain:
            renamedIkChain.append(mc.rename(jnt, jnt.replace("Bind_JNT1", "Ik_JNT")))
        
        ikChain = renamedIkChain

        # Build IK foot control:
        footIkCtl = buildControl(side, "leg02IK", "%s_leg02Ik_JNT" % side, 
                shapeCVs=SQUARE_SHAPE_CVS, colour=18 if side=="L" else 20)
        mc.scale(6,6,6, footIkCtl[0] + ".cv[*]")

        # Create IK handle and parent to IK control:
        footIkHandle, _ = mc.ikHandle(sj="%s_leg00Ik_JNT" % side, ee="%s_leg02Ik_JNT" % side, sol="ikRPsolver")
        footIkHandle = mc.rename(footIkHandle, "%s_leg02_IKH" % side)
        mc.parent(footIkHandle, footIkCtl[0])

        # Build Pole Vector control and create pole vector constraint to leg02IK:
        kneePoleVectorCtl = buildControl(side, "kneePoleVector", "%s_leg01Ik_JNT" 
                        % side, shapeCVs=DIAMOND_SHAPE_CVS, colour=18 if side=="L"
                        else 20)
        
        kneePoleVectorPos = getIkhPoleVecPos(footIkHandle)
        mc.scale(4,4,4, kneePoleVectorCtl[0] + ".cv[*]")
        mc.move(kneePoleVectorPos.x, kneePoleVectorPos.y, kneePoleVectorPos.z, 
                        kneePoleVectorCtl)
        mc.poleVectorConstraint(kneePoleVectorCtl, footIkHandle)


        




# if limb == "arm":
#                 mc.parent(ikChain[1], w = True)
#                 mc.delete(ikChain.pop(-1), ikChain.pop(0))    

 

main()