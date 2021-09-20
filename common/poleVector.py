from maya import cmds as mc
from maya.api import OpenMaya as om2
from . import control

def getPoleVectorPosition(rootPos, midPos, endPos):
    # NOTE: maybe move this to common.vector
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

def buildPoleVectorControl(side, name, guideJoint, ikHandle):
    """Builds a pole vector control, positions it along a vector using the 
    getIKhPoleVecPos function and creates a pole vector constraint to the passed joint.
    Returns the created control"""
    poleVectorCtl, _, poleVectorGrp = control.buildControl(
        side,
        name,
        guideJoint,
        shapeCVs=control.shapes.DIAMOND_SHAPE_CVS,
        colour=18 if side == "L" else 20,
    )
    poleVectorPos = getIkhPoleVecPos(ikHandle)
    mc.scale(4, 4, 4, poleVectorCtl + ".cv[*]")
    mc.move(
        poleVectorPos.x, poleVectorPos.y, poleVectorPos.z, poleVectorGrp,
    )
    mc.poleVectorConstraint(poleVectorCtl, ikHandle)

    return poleVectorCtl, poleVectorGrp
