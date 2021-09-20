from maya import cmds as mc
from maya.api import OpenMaya as om2

def getVector(startPoint, endPoint):
    positionA = mc.xform(startPoint, q=1, t=1, ws=1)
    positionB = mc.xform(endPoint, q=1, t=1, ws=1)
    vecFromAToB = (om2.MVector(positionB) - om2.MVector(positionA)).normal()

    return vecFromAToB
