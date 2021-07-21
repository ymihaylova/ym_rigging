from maya import cmds as mc
from maya.api import OpenMaya as om2


def addAttr(*args, **kwargs):
    mc.addAttr(*args, **kwargs)

    return args[0] + "." + kwargs["ln"]


def getPoleVectorPosition(rootPos, midPos, endPos):
    rootJntVector = om2.MVector(rootPos[0], rootPos[1], rootPos[2])
    midJntVector = om2.MVector(midPos[0], midPos[1], midPos[2])
    endJntVector = om2.MVector(endPos[0], endPos[1], endPos[2])

    rootToEnd = endJntVector - rootJntVector
    closestPoint = midJntVector - rootJntVector

    scaleValue = (rootToEnd * closestPoint) / (rootToEnd * rootToEnd)
    projectionVector = rootToEnd * scaleValue + rootJntVector

    rootToMidLen = (midJntVector - rootJntVector).length()
    midToEndLen = (endJntVector - midJntVector).length()
    totalLen = rootToMidLen + midToEndLen

    poleVectorPosition = (
        midJntVector - projectionVector
    ).normal() * totalLen + midJntVector

    return poleVectorPosition


def getIkhPoleVecPos(ikHandle):
    # Get joints influencing the IK handle and call poleVectorPos() on them
    jointList = mc.ikHandle(ikHandle, q=True, jointList=True)
    jointList.append(mc.listRelatives(jointList[-1], children=True, type="joint")[0])

    rootJntPos = mc.xform(jointList[0], q=1, ws=1, t=1)
    midJntPos = mc.xform(jointList[1], q=1, ws=1, t=1)
    endJntPos = mc.xform(jointList[2], q=1, ws=1, t=1)

    poleVectorPos = getPoleVectorPosition(rootJntPos, midJntPos, endJntPos)

    return poleVectorPos


def createFollicle(nurbsSurface, parameterU, parameterV=0.5):
    follicleShape = mc.createNode("follicle")
    follicleTransform = mc.listRelatives(follicleShape, p=1)[0]

    mc.connectAttr(nurbsSurface + ".worldSpace", follicleShape + ".inputSurface")
    mc.connectAttr(follicleShape + ".outTranslate", follicleTransform + ".translate")
    mc.connectAttr(follicleShape + ".outRotate", follicleTransform + ".rotate")

    mc.setAttr(follicleShape + ".parameterU", parameterU)
    mc.setAttr(follicleShape + ".parameterV", parameterV)

    return follicleTransform


def getVector(startPoint, endPoint):
    positionA = mc.xform(startPoint, q=1, t=1, ws=1)
    positionB = mc.xform(endPoint, q=1, t=1, ws=1)
    vecFromAToB = (om2.MVector(positionB) - om2.MVector(positionA)).normal()

    return vecFromAToB
