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


def extractTwist(twistingObject, staticParent, alignXwith="X"):
    # Create a transform, parent and 0 out under the object for which twist info is sought
    twistTransform = mc.createNode(
        "transform",
        n="%s%sTwistExtractionTransform_TRN" % (twistingObject[:-4], alignXwith),
    )
    mc.parent(twistTransform, twistingObject, r=1)
    # Rotate so as to align the X axis of the twist transform with the axis of
    # the object around which it twists, to ensure stable rotation:
    if alignXwith == "Y":
        mc.rotate(0, 0, 90, twistTransform)
    elif alignXwith == "Z":
        mc.rotate(0, -90, 0, twistTransform)
    twistTransformDuplicate = mc.duplicate(twistTransform)[0]
    twistTransformDuplicate = mc.rename(
        twistTransformDuplicate, twistTransformDuplicate.replace("_TRN1", "Parent_TRN")
    )
    # Parent a duplicate of the transform under an object that will be unafected
    # by any rotation of the twistingObject:
    mc.parent(twistTransformDuplicate, staticParent)
    # Multiply the matrix of the twist transform and the duplicate:
    multMatrix = mc.createNode(
        "multMatrix", n="%sinTheSpaceOfParent_MUM" % (twistTransform[:-4])
    )
    mc.connectAttr(twistTransform + ".worldMatrix[0]", multMatrix + ".matrixIn[0]")
    mc.connectAttr(
        twistTransformDuplicate + ".worldInverseMatrix[0]", multMatrix + ".matrixIn[1]"
    )
    # Decompose matrix node to get acces to the twist information obtained from
    # the MultMatrix
    decomposed = mc.createNode(
        "decomposeMatrix", n="%sDecomposed_DCM" % multMatrix[0:-4]
    )
    mc.connectAttr(multMatrix + ".matrixSum", decomposed + ".inputMatrix")
    # The value from the decomposed matrix is in Qaternion, needed in Euler
    qte = mc.createNode("quatToEuler", n="%s_QTE" % twistTransform[:-4])
    mc.connectAttr(decomposed + ".outputQuatX", qte + ".inputQuatX")
    mc.connectAttr(decomposed + ".outputQuatW", qte + ".inputQuatW")

    return qte + ".outputRotateX"

