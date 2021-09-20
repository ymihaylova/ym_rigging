from maya import cmds as mc

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

def blendShapeDriverFromTwist(twistValue, n="", angle=90, remapRange=(0, 1)):
    node = mc.createNode(
        "multiplyDivide", n=twistValue.split(".")[0].rsplit("_", 1)[0] + n + "_MDV"
    )
    mc.connectAttr(twistValue, node + ".input1X")
    mc.setAttr(node + ".input2X", angle)
    mc.setAttr(node + ".operation", 2)

    clamp = mc.createNode("clamp", n=node.replace("_MDV", "_CLP"))
    mc.setAttr(clamp + ".maxR", 1)
    mc.connectAttr(node + ".outputX", clamp + ".inputR")

    remap = mc.createNode("remapValue", n=node.replace("_MDV", "_RMV"))
    mc.setAttr(remap + ".inputMin", remapRange[0])
    mc.setAttr(remap + ".outputMax", remapRange[1])
    mc.connectAttr(clamp + ".outputR", remap + ".inputValue")

    return remap + ".outValue"

def jointWithHalfwayTwist(
    joint1,
    joint2,
    twistAxisJoint1,
    twistAxisJoint2,
    twistAxisHalfwayJoint,
    staticParent,
    side,
    name,
):
    """Takes two joints, calculates their twist in the given axis and applies half 
    of that to a third joint created and situated halfway between the two. 
    Returns the halfway joint."""
    DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

    joint1Twist = extractTwist(joint1, staticParent, alignXwith=twistAxisJoint1)
    joint2Twist = extractTwist(joint2, staticParent, alignXwith=twistAxisJoint2)

    halfwayRotationBlendNode = mc.createNode(
        "animBlendNodeAdditiveDA", n="%s_%sHalfwayRotationBlend_ADA" % (side, name)
    )
    mc.setAttr(halfwayRotationBlendNode + ".weightA", 0.5)
    mc.setAttr(halfwayRotationBlendNode + ".weightB", 0.5)

    mc.connectAttr(joint1Twist, halfwayRotationBlendNode + ".inputA")
    mc.connectAttr(joint2Twist, halfwayRotationBlendNode + ".inputB")

    # Halfway joint:
    halfwayJoint = mc.createNode("joint", n="%s_%s_JNT" % (side, name))
    mc.delete(mc.parentConstraint(joint1, joint2, halfwayJoint, mo=0))
    mc.parent(halfwayJoint, staticParent)
    mc.connectAttr(
        halfwayRotationBlendNode + ".output",
        halfwayJoint + ".rotate%s" % twistAxisHalfwayJoint,
    )

    if not DEBUG_MODE:
        mc.hide(halfwayJoint)

    return halfwayJoint, joint1Twist, joint2Twist
