from maya import cmds as mc
from maya.api import OpenMaya as om2
from ym_rigging.general import ctl_shapes as cs
from ym_rigging.general import general as gen


DEBUG_MODE = True


class SpineComponent:
    def __init__(self, jointChain, curve):
        self.build(jointChain, curve)

    def build(self, jointChain, curve):
        # Clusters and controls:
        spineCtls = []
        spineCtlsGrps = []
        names = ["hips", "spineMid", "chest"]
        shapes = [cs.HIPS_SHAPE_CVS, cs.SPINEMID_SHAPE_CVS, cs.CHEST_SHAPE_CVS]
        hipFkCtl, hipFkGrp = [], []
        spineMidFkCtl, spineMidFkGrp = [], []
        # Root Ctl:
        rootCtl, _, rootGrp = buildControl(
            "C",
            "root",
            "C_spine00_JNT",
            shapeCVs=cs.SPINEMID_SHAPE_CVS,
            shapeKnots=cs.KNOTS,
        )
        mc.scale(1.5, 1.5, 1.5, rootCtl + ".cv[*]")
        mc.rotate(0, 0, 0, rootGrp, ws=1)

        for counter, cvIDs in enumerate(["0:1", "2", "3:4"]):
            cvs = curve + ".cv[%s]" % cvIDs

            _, clusterHandle = mc.cluster(
                cvs, name="C_spine%s_CLS" % str(counter).zfill(2)
            )
            ctl, _, group = buildControl(
                "C",
                names[counter],
                clusterHandle,
                shapeCVs=shapes[counter],
                shapeKnots=cs.KNOTS,
                degree=3,
            )
            if counter != 1:
                # Create a "FK like" hip control
                if counter == 0:
                    hipFkCtl, _, hipFkGrp = buildControl(
                        "C",
                        "hipFk",
                        clusterHandle,
                        shapeCVs=cs.SPINEFK_SHAPE_CVS,
                        shapeKnots=cs.KNOTS,
                        colour=9,
                    )
                # Create a hips/chest joint, reposition to ctl location and parent:
                joint = mc.createNode("joint", name="C_%s_JNT" % names[counter])
                mc.delete(mc.parentConstraint(ctl, joint, mo=0))
                mc.parent(joint, ctl)
            if counter == 1:
                spineMidFkCtl, _, spineMidFkGrp = buildControl(
                    "C",
                    "spineMidFk",
                    clusterHandle,
                    shapeCVs=cs.SPINEFK_SHAPE_CVS,
                    shapeKnots=cs.KNOTS,
                    colour=9,
                )

            spineCtls.append(ctl)
            spineCtlsGrps.append(group)
            # Parent cluster under ctl:
            mc.parent(clusterHandle, ctl)

            if not DEBUG_MODE:
                mc.hide(joint, clusterHandle)
        # Parenting Controls
        mc.parent(hipFkGrp, spineCtlsGrps[0], rootCtl)
        mc.parent(spineMidFkGrp, hipFkCtl)
        mc.parent(spineCtlsGrps[1:], spineMidFkCtl)
        mc.parent(jointChain[0], rootCtl)
        # Spine stretch setup
        # Claculating spine length
        spineLen = mc.createNode("curveInfo", n="C_spineLen_INF")
        mc.connectAttr(curve + "Shape.worldSpace", spineLen + ".inputCurve")
        staticSpineLen = mc.getAttr(spineLen + ".arcLength")
        # Calcualting stretch factor:
        stretchFactor = mc.createNode("multiplyDivide", n="C_spineStretchFactor_MDV")
        mc.connectAttr(spineLen + ".arcLength", stretchFactor + ".input1.input1X")
        mc.setAttr(stretchFactor + ".input2.input2X", staticSpineLen)
        mc.setAttr(stretchFactor + ".operation", 2)
        # Stretching Joints
        jointStretch = mc.createNode("multiplyDivide", n="C_spineJointStretch_MDV")
        mc.connectAttr(
            stretchFactor + ".output.outputX", jointStretch + ".input1.input1X"
        )
        mc.setAttr(jointStretch + ".input2.input2X", mc.getAttr("C_spine01_JNT.tx"))
        for jnt in jointChain:
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
        # Spline IK handle:
        splineIkh, _ = mc.ikHandle(
            sj="C_spine00_JNT",
            ee="C_spine04_JNT",
            solver="ikSplineSolver",
            createCurve=0,
            curve=curve,
        )
        splineIkh = mc.rename(splineIkh, "C_spine_IKH")
        mc.hide(splineIkh)
        mc.parent(splineIkh, rootCtl)

        # Advanced twist:
        mc.setAttr(splineIkh + ".dTwistControlEnable", 1)
        mc.setAttr(splineIkh + ".dWorldUpType", 4)
        mc.setAttr(splineIkh + ".dForwardAxis", 0)
        mc.setAttr(splineIkh + ".dWorldUpAxis", 0)
        mc.setAttr(splineIkh + ".dWorldUpVector", -1, 0, 0)
        mc.setAttr(splineIkh + ".dWorldUpVectorEnd", -1, 0, 0)
        mc.connectAttr(spineCtls[0] + ".worldMatrix", splineIkh + ".dWorldUpMatrix")
        mc.connectAttr(spineCtls[-1] + ".worldMatrix", splineIkh + ".dWorldUpMatrixEnd")


class NeckComponent:
    def __init__(self, jointChain, jointChainTwist):
        self.build(jointChain, jointChainTwist)

    def build(self, jointChain, jointChainTwist):
        # Create and position Neck Ctl, insert in the hierarchy
        neckBaseCtl, _, neckBaseGrp = buildControl("C", "neck", jointChain[0])
        mc.move(0, 0, 1, neckBaseCtl + ".cv[*]", r=1)
        mc.rotate(0, 90, 0, neckBaseCtl + ".cv[*]", r=1)
        mc.scale(6, 6, 6, neckBaseCtl + ".cv[*]")
        mc.parent(neckBaseGrp, "C_chest_CTL")
        mc.parent(jointChain[0], jointChainTwist[0], neckBaseCtl)
        # Add to skinnable joints:
        addToSkinJoints(jointChainTwist[1])
        for joint in jointChain[:-1]:
            addToSkinJoints(joint)
        # Head joint:
        headJnt = mc.duplicate(jointChain[-1], n="C_head_JNT")[0]
        addToSkinJoints(headJnt)
        mc.parent(headJnt, w=1)
        mc.setAttr(headJnt + ".jointOrientX", 0)
        mc.setAttr(headJnt + ".jointOrientY", 0)
        mc.setAttr(headJnt + ".jointOrientZ", 0)
        headCtl, _, headGrp = buildControl(
            "C", "head", headJnt, shapeCVs=cs.SQUARE_SHAPE_CVS
        )
        mc.scale(15, 15, 15, headCtl + ".cv[*]")
        mc.parent(headJnt, headCtl)
        mc.parent(headGrp, neckBaseCtl)
        # Aim constrain jointChain to chest and jointChainTwist to head:
        mc.aimConstraint(
            "C_head_CTL",
            jointChain[0],
            wut="objectrotation",
            u=[0, 1, 0],
            aim=[1, 0, 0],
            wu=[-1, 0, 0],
            wuo="C_chest_CTL",
        )
        mc.aimConstraint(
            "C_head_CTL",
            jointChainTwist[0],
            wut="objectrotation",
            u=[0, 1, 0],
            aim=[1, 0, 0],
            wu=[-1, 0, 0],
            wuo="C_head_CTL",
        )
        # Mid joint half twist:
        halfTwistNode = mc.createNode(
            "animBlendNodeAdditiveDA", n="C_neck01HalfTwist_ADA"
        )
        mc.connectAttr(jointChain[0] + ".rx", halfTwistNode + ".inputA")
        mc.connectAttr(jointChainTwist[0] + ".rx", halfTwistNode + ".inputB")
        mc.setAttr(halfTwistNode + ".weightA", 0.5)
        mc.setAttr(halfTwistNode + ".weightB", 0.5)
        mc.connectAttr(halfTwistNode + ".output", jointChain[1] + ".rx", f=1)
        # Stretch:
        length = mc.getAttr(jointChainTwist[-1] + ".tx")
        # Stretch factor:
        stretch = mc.createNode("distanceBetween", n="C_neckStretch_DB")
        mc.connectAttr(neckBaseCtl + ".worldMatrix", stretch + ".inMatrix1")
        mc.connectAttr(headCtl + ".worldMatrix", stretch + ".inMatrix2")
        stretchFactor = mc.createNode("multiplyDivide", n="%C_neckStretchFactor_MDV")
        mc.connectAttr(stretch + ".distance", stretchFactor + ".input1.input1X")
        mc.setAttr(stretchFactor + ".input2.input2X", length)
        mc.setAttr(stretchFactor + ".operation", 2)
        # Stretch jointChain joints
        for jnt in jointChain[1:]:
            jointStretch = mc.createNode(
                "multiplyDivide",
                n="C_Neck%sIndividualStretch_MDV" % str(jointChain.index(jnt)).zfill(2),
            )
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(
                stretchFactor + ".output.outputX", jointStretch + ".input2.input2X"
            )
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
        # Stretch jointChainTwist:
        jointStretch = mc.createNode(
            "multiplyDivide", n="C_NeckWithTwist01IndividualStretch_MDV"
        )
        mc.setAttr(
            jointStretch + ".input1.input1X", mc.getAttr(jointChainTwist[-1] + ".tx")
        )
        mc.connectAttr(
            stretchFactor + ".output.outputX", jointStretch + ".input2.input2X"
        )
        mc.connectAttr(jointStretch + ".output.outputX", jointChainTwist[-1] + ".tx")
        # Orient to parent/world
        orientToParent("C_chest_CTL", "C_head_CTL", "C_head_GRP")


class HandComponent:
    def __init__(self, side):
        self.buildControls(side)

    def buildControls(self, side):
        # Create hand base transform and get it parent constrained to arm03_JNT
        baseTransform = mc.createNode("transform", n="%s_handBase_TRN" % side)
        mc.parentConstraint("%s_arm03_JNT" % side, baseTransform, mo=0)
        mc.parent(baseTransform, "C_chest_CTL")
        # Parent finger joints to it:
        thumbJoints = mc.ls("%s_thumb??_JNT" % side)
        indexJoints = mc.ls("%s_index??_JNT" % side)
        midFingerJoints = mc.ls("%s_midFinger??_JNT" % side)
        ringFingerJoints = mc.ls("%s_ring??_JNT" % side)
        pinkyJoints = mc.ls("%s_pinky??_JNT" % side)
        fingerJointChains = [
            thumbJoints,
            indexJoints,
            midFingerJoints,
            ringFingerJoints,
            pinkyJoints,
        ]
        mc.parent(
            thumbJoints[0],
            indexJoints[0],
            midFingerJoints[0],
            ringFingerJoints[0],
            pinkyJoints[0],
            baseTransform,
        )
        # Build controls and constrain them:
        for jntChain in fingerJointChains:
            ctlsList = []
            ctlsOfsList = []
            ctlsGrpList = []
            prevCtl, prevCtlGrp = None, None
            for jnt in jntChain[:-1]:
                addToSkinJoints(jnt)
                if jntChain == thumbJoints:
                    ctl, ctlOfs, ctlGrp = buildControl(
                        side,
                        jnt[2:-4],
                        jnt,
                        shapeCVs=cs.THUMB_SHAPE_CVS,
                        shapeKnots=cs.KNOTS,
                        colour=18 if side == "L" else 20,
                    )
                elif jntChain == pinkyJoints:
                    ctl, ctlOfs, ctlGrp = buildControl(
                        side,
                        jnt[2:-4],
                        jnt,
                        shapeCVs=cs.PINKY_SHAPE_CVS,
                        shapeKnots=cs.KNOTS,
                        colour=18 if side == "L" else 20,
                    )
                else:
                    ctl, ctlOfs, ctlGrp = buildControl(
                        side,
                        jnt[2:-4],
                        jnt,
                        shapeCVs=cs.FINGERS_SHAPE_CVS,
                        shapeKnots=cs.KNOTS,
                        colour=18 if side == "L" else 20,
                    )
                if jnt == jntChain[-2]:
                    mc.scale(0.8, 0.8, 0.8, ctl + ".cv[*]")
                if side == "R":
                    mc.rotate(0, 180, 0, ctl + ".cv[*]")
                if prevCtlGrp != None:
                    mc.parent(ctlGrp, prevCtl)
                    mc.parentConstraint(ctl, jnt, mo=0)
                else:
                    mc.parent(ctlGrp, baseTransform)
                    mc.parent(jnt, ctl)

                ctlsList.append(ctl)
                ctlsOfsList.append(ctlOfs)
                ctlsGrpList.append(ctlGrp)
                prevCtl, prevCtlGrp = ctl, ctlGrp

            curlStretch(side, "%sCurl" % ctlsList[0][2:-4], ctlsOfsList)


def curlStretch(side, name, ctlsOfsList):
    # Create and position control:
    curlCtl, _, curlCtllGrp = buildControl(side, name, ctlsOfsList[0])
    mc.move(0, 5, 0, curlCtl + ".cv[*]", r=1)
    mc.rotate(0, 90, 0, curlCtl + ".cv[*]", ws=1, r=1)
    mc.parent(curlCtllGrp, "%s_handBase_TRN" % side)
    # Create attribute and connect it to joints:
    curlAttr = gen.addAttr(curlCtl, ln="curl", at="float", min=-10, max=10, k=1)
    positiveNegativeNode = mc.createNode(
        "condition", name="%s_%sPositiveOrNegative_CDT" % (side, name)
    )
    mc.connectAttr(curlAttr, positiveNegativeNode + ".firstTerm")
    mc.setAttr(positiveNegativeNode + ".colorIfFalseR", -1.5)
    mc.setAttr(positiveNegativeNode + ".colorIfTrueR", -8.5)
    mc.setAttr(positiveNegativeNode + ".operation", 2)
    curlAdditive = mc.createNode(
        "animBlendNodeAdditiveDA", name="%s_%s_ADA" % (side, name)
    )
    mc.connectAttr(positiveNegativeNode + ".outColorR", curlAdditive + ".weightA")
    mc.connectAttr(curlAttr, curlAdditive + ".inputA")
    for ctlOfs in ctlsOfsList[1:]:
        mc.connectAttr(curlAdditive + ".output", ctlOfs + ".rotateZ")


def buildControl(
    side, name, guide=None, shapeCVs=[], shapeKnots=None, degree=1, colour=17
):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    else:
        if not shapeKnots:
            control = mc.curve(p=shapeCVs, degree=degree)
        else:
            control = mc.curve(p=shapeCVs, knot=shapeKnots, periodic=1)
    offset = mc.group(control)
    group = mc.group(offset)
    # Temporary ugly fix:
    mc.xform(offset, ztp=1)
    mc.xform(group, ztp=1)

    # NOTE: Check whether name exists and handle it if it does
    control = mc.rename(control, "%s_%s_CTL" % (side, name))
    offset = mc.rename(offset, "%s_%s_OFS" % (side, name))
    group = mc.rename(group, "%s_%s_GRP" % (side, name))

    # #snap to guide
    if guide != None:
        mc.delete(mc.parentConstraint(guide, group, maintainOffset=0))
    # Set colour
    for ctlShape in mc.listRelatives(control, s=1):
        mc.setAttr(ctlShape + ".overrideEnabled", 1)
        mc.setAttr(ctlShape + ".overrideColor", colour)

    return control, offset, group


def buildLimb(side, name, parent, skinJointsMessageAttr):
    blendChain = mc.ls("%s_%s??_JNT" % (side, name))
    fkCtlsList = []
    fkCtlsOfsList = []
    fkCtlsGrpList = []
    prevFkCtl, prevFkCtlGrp = None, None
    ikHandle, ikCtl, ikCtlGrp, ikBaseCtl = None, None, None, None

    for jntId in range(len(blendChain) - 1):
        fkCtl, fkCtlOfs, fkCtlGrp = buildControl(
            side,
            "%s%sFk" % (name, str(jntId).zfill(2)),
            blendChain[jntId],
            colour=18 if side == "L" else 20,
        )

        if prevFkCtlGrp is not None:
            mc.parent(fkCtlGrp, prevFkCtl)
        else:
            mc.parent(fkCtlGrp, parent)

        fkCtlsList.append(fkCtl)
        fkCtlsOfsList.append(fkCtlOfs)
        fkCtlsGrpList.append(fkCtlGrp)
        prevFkCtl, prevFkCtlGrp = fkCtl, fkCtlGrp
        # Adjust positioning of controls for the leg:
    if name == "leg":
        for ctl in fkCtlsList:
            mc.scale(6, 6, 6, ctl + ".cv[*]")

            if ctl != fkCtlsList[-1]:  # omit rotating the toe FK control CVs
                mc.rotate(90, 0, 0, ctl + ".cv[*]", ws=1)

            if ctl == fkCtlsList[0]:  # move the hip FK control CVs for visual clarity
                mc.move(0, -8, 0, ctl + ".cv[*]", ws=1, r=1)
        orientToParent("C_hips_CTL", fkCtlsList[0], fkCtlsGrpList[0])
    if name == "arm":
        for fkCtl in fkCtlsList:
            mc.scale(6, 6, 6, fkCtl + ".cv[*]")
            mc.rotate(0, 90, 0, fkCtl + ".cv[*]", r=1)

            if (
                fkCtl == fkCtlsList[0]
            ):  # move the clavicle FK control CVs for visual clarity
                if side == "L":
                    mc.move(3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                else:
                    mc.move(-3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                mc.scale(1.5, 1.5, 1.5, fkCtl + ".cv[*]")
            if fkCtl == fkCtlsList[1]:
                if side == "L":
                    mc.move(3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                else:
                    mc.move(-3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
        # Expose ability to change limb joints' orientation
        orientToParent(fkCtlsList[0], fkCtlsList[1], fkCtlsGrpList[1])
    # Create IK copy of the blend chain
    ikChain = mc.duplicate("%s_%s00_JNT" % (side, name), renameChildren=1)
    renamedIkChain = []
    for jnt in ikChain:
        renamedIkChain.append(mc.rename(jnt, jnt.replace("_JNT", "Ik_JNT")[:-1]))

    ikChain = renamedIkChain

    limbGrp = mc.group(blendChain[0], ikChain[0])
    limbGrp = mc.rename(limbGrp, "%s_%s_GRP" % (side, name))
    mc.parent(limbGrp, parent)

    # Create IK ctl and handle for the leg:
    if name == "leg":
        ikBaseCtl, _, ikBaseCtlGrp = buildControl(
            side,
            "leg00Ik",
            "%s_leg00Ik_JNT" % side,
            shapeCVs=cs.SQUARE_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        mc.parent(ikBaseCtlGrp, parent)
        mc.scale(6, 6, 6, ikBaseCtl + ".cv[*]")
        mc.rotate(0, 0, 90, ikBaseCtl + ".cv[*]", ws=1)
        mc.move(0, -8, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
        ikCtl, _, ikCtlGrp = buildControl(
            side,
            "leg02Ik",
            "%s_leg02Ik_JNT" % side,
            shapeCVs=cs.SQUARE_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        mc.scale(6, 6, 6, ikCtl + ".cv[*]")
        mc.parent(ikChain[0], ikBaseCtl)
        # Create IK handle and parent to IK control:
        ikHandle, _ = mc.ikHandle(
            sj="%s_leg00Ik_JNT" % side, ee="%s_leg02Ik_JNT" % side, sol="ikRPsolver"
        )
        ikHandle = mc.rename(ikHandle, "%s_leg02_IKH" % side)
        mc.parent(ikHandle, ikCtl)
    # Create IK ctl and handle for the arm:
    if name == "arm":
        ikBaseCtl, _, ikBaseCtlGrp = buildControl(
            side,
            "arm01Ik",
            "%s_arm01Ik_JNT" % side,
            shapeCVs=cs.SQUARE_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        mc.parent(ikBaseCtlGrp, parent)
        mc.parent(ikChain[0], ikBaseCtl)
        mc.scale(6, 6, 6, ikBaseCtl + ".cv[*]")
        mc.rotate(0, 0, 90, ikBaseCtl + ".cv[*]", r=1)
        if side == "L":
            mc.move(3, 0, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
        else:
            mc.move(-3, 0, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
        ikCtl, _, ikCtlGrp = buildControl(
            side,
            "arm03Ik",
            "%s_arm03Ik_JNT" % side,
            shapeCVs=cs.SQUARE_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        mc.scale(6, 6, 6, ikCtl + ".cv[*]")
        mc.rotate(0, 0, 90, ikCtl + ".cv[*]", r=1)

        # Create IK handle and parent to IK control:
        ikHandle, _ = mc.ikHandle(
            sj="%s_arm01Ik_JNT" % side, ee="%s_arm03Ik_JNT" % side, sol="ikRPsolver"
        )
        ikHandle = mc.rename(ikHandle, "%s_arm03_IKH" % side)
        mc.parent(ikHandle, ikCtl)

    # Connect a message attr to the Harry Ctl for all skin joints:
    if name == "leg":
        for joint in blendChain:
            addToSkinJoints(joint)
    else:
        for joint in blendChain[:-1]:
            addToSkinJoints(joint)

    if not DEBUG_MODE:
        mc.hide(blendChain, ikChain)

    return (
        blendChain,
        fkCtlsList,
        fkCtlsOfsList,
        fkCtlsGrpList,
        ikChain,
        ikCtl,
        ikCtlGrp,
        ikHandle,
        ikBaseCtl,
    )


def limbStretch(side, name, startEnd, startControl, endControl, conditional=1):
    startPoint = mc.createNode("transform", n=startEnd[0][:-4] + "_TRN")
    mc.parent(startPoint, startControl, r=1)  # Parent to ikBaseCtl and snap location
    # Create a transform to locate end of stretchable chain
    endPoint = mc.createNode("transform", n=startEnd[-1][:-4] + "_TRN")
    mc.parent(endPoint, endControl, r=1)

    # Calculate actual length:
    length = 0
    for jnt in startEnd[1:]:
        length += mc.getAttr(jnt + ".tx")

    # Calculate stretch factor
    stretchDistance = mc.createNode(
        "distanceBetween", n="%s_%sStretched_DB" % (side, name)
    )
    mc.connectAttr(startPoint + ".worldMatrix", stretchDistance + ".inMatrix1")
    mc.connectAttr(endPoint + ".worldMatrix", stretchDistance + ".inMatrix2")
    stretchFactor = mc.createNode(
        "multiplyDivide", n="%s_%sStretchFactor_MDV" % (side, name)
    )
    mc.connectAttr(stretchDistance + ".distance", stretchFactor + ".input1.input1X")
    mc.setAttr(stretchFactor + ".input2.input2X", abs(length))
    mc.setAttr(stretchFactor + ".operation", 2)

    # If the stretch is unconditional - cause the limb to squish when distance
    if conditional == 0:
        jointStretchMDVsList = []
        for jnt in startEnd[1:]:
            jointStretch = mc.createNode(
                "multiplyDivide",
                n="%s_%s%sIndividualStretch_MDV"
                % (side, name, str(startEnd.index(jnt)).zfill(2)),
            )
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(
                stretchFactor + ".output.outputX", jointStretch + ".input2.input2X"
            )
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
            jointStretchMDVsList.append(jointStretch)

    else:
        isLimbStretched = mc.createNode(
            "condition", n="%s_%sIsStretched_CD" % (side, name)
        )
        mc.connectAttr(
            stretchFactor + ".output.outputX", isLimbStretched + ".firstTerm"
        )
        mc.connectAttr(
            stretchFactor + ".output.outputX",
            isLimbStretched + ".colorIfTrue.colorIfTrueR",
        )
        mc.setAttr(isLimbStretched + ".secondTerm", 1)
        mc.setAttr(isLimbStretched + ".operation", 2)

        jointStretchMDVsList = []
        for jnt in startEnd[1:]:
            jointStretch = mc.createNode(
                "multiplyDivide",
                n="%s_%s%sIndividualStretch_MDV"
                % (side, name, str(startEnd.index(jnt)).zfill(2)),
            )
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(
                isLimbStretched + ".outColorR", jointStretch + ".input2.input2X"
            )
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
            jointStretchMDVsList.append(jointStretch)


def blendChainConstraints(limb, driven, skipTranslate, *args, **kwargs):
    constraintsList = []
    for transforms in zip(driven, *args):
        if driven.index(transforms[0]) < skipTranslate:
            parCon = mc.parentConstraint(transforms[1:], transforms[0], **kwargs)[0]
        if driven.index(transforms[0]) >= skipTranslate:
            parCon = mc.parentConstraint(
                transforms[1:], transforms[0], st=["x", "y", "z"], **kwargs
            )[0]
        if parCon not in constraintsList:
            constraintsList.append(parCon)
    return constraintsList


def orientConstrainIkEndJoint(driven, driver):
    # Orient constrain the end joint of an Ik chain to the Ik CTL:
    constraintNode = mc.orientConstraint(driver, driven, mo=0)
    return constraintNode


def blendTranslations(name, blendJoint, ikJoint):

    ikJointTranslate = ikJoint + ".translateX"
    staticLen = mc.getAttr(ikJointTranslate)
    blendTranslationsNode = mc.createNode("blendTwoAttr", n=name)
    mc.connectAttr(ikJointTranslate, blendTranslationsNode + ".input[0]")
    mc.setAttr(blendTranslationsNode + ".input[1]", staticLen)
    mc.connectAttr(blendTranslationsNode + ".output", blendJoint + ".translateX")

    return blendTranslationsNode


def createConnectIkFkSwitch(
    side,
    name,
    parentJoint,
    blendChainParentConstraints,
    blendTranslationsNode,
    ikCtlsGrp,
    ikBaseCtl,
    fkControlsGroupsList,
):
    # Create and position IK/FK Switch
    ikFkSwitchCtl, ikFkSwitchOfs, ikFkSwitchGrp = buildControl(
        side, "%sIkFkSwitch" % name, parentJoint, shapeCVs=cs.SWITCH_SHAPE_CVS
    )
    if name == "arm":
        mc.move(0, 10, -10, ikFkSwitchGrp, r=1, ws=1)
        mc.rotate(90, 0, 0, ikFkSwitchGrp, ws=1, r=1)
    else:
        mc.rotate(90, 0, 90, ikFkSwitchGrp, r=1, ws=1)
        if side == "L":
            mc.move(15, 10, 0, ikFkSwitchGrp, ws=1, r=1)
        else:
            mc.move(-15, 10, 0, ikFkSwitchGrp, ws=1, r=1)

    mc.parentConstraint(parentJoint, ikFkSwitchGrp, sr=["x", "y", "z"], mo=1)
    # Create the switch attribute, where 0=IK and 1=FK
    ikFkSwitchAttr = gen.addAttr(
        ikFkSwitchCtl, at="float", k=1, ln="ikFkSwitch", max=1, min=0, dv=0
    )
    # Reverse IK FK switch attribute's value:
    reversalNodeIkFk = mc.createNode(
        "plusMinusAverage", n="%s_%sIkFkReversedValue_PMA" % (side, name)
    )
    mc.setAttr(reversalNodeIkFk + ".operation", 2)
    mc.setAttr(reversalNodeIkFk + ".input1D[0]", 1)
    mc.connectAttr(ikFkSwitchAttr, reversalNodeIkFk + ".input1D[1]")
    # Connect IK/Fk Switch to parent constraints:
    for parCon in blendChainParentConstraints:
        mc.connectAttr(ikFkSwitchAttr, parCon + ".w1")
        mc.connectAttr(reversalNodeIkFk + ".output1D", parCon + ".w0")
    # Connect IK/FK switch to the node blending the translations of the end joint:
    mc.connectAttr(ikFkSwitchAttr, blendTranslationsNode + ".attributesBlender")
    # Connect IK/FK Switch to control visibility:
    mc.connectAttr(reversalNodeIkFk + ".output1D", ikCtlsGrp + ".v")
    mc.connectAttr(reversalNodeIkFk + ".output1D", ikBaseCtl + ".v")
    for ctl in fkControlsGroupsList:
        mc.connectAttr(ikFkSwitchAttr, ctl + ".v")
    # Place switch in the hierarchy
    mc.parent(ikFkSwitchGrp, "%s_%s_GRP" % (side, name))

    return reversalNodeIkFk + ".output1D", ikFkSwitchAttr


def footRollSetup(side, footIkCtl):
    # Setup foot roll with  Ball Straight and Toe Lift attributes exposed:
    rollAttr = gen.addAttr(footIkCtl, ln="roll", at="doubleAngle", k=1)
    toeLiftAttr = gen.addAttr(
        footIkCtl, ln="toeLift", at="doubleAngle", k=1, dv=0.5235988
    )
    ballStraightAttr = gen.addAttr(
        footIkCtl, ln="ballStraight", at="doubleAngle", k=1, dv=1.047198
    )
    ikCtlChildren = mc.listRelatives(footIkCtl, c=1)
    ikCtlChildren.remove(footIkCtl + "Shape")
    ikCtlChildren = mc.group(ikCtlChildren, n="%s_footIkh_GRP" % side)
    # Banking attr exposed:
    bankAttr = gen.addAttr(footIkCtl, ln="Bank", at="float", k=1, min=-10, max=10)
    # Assigning names to pivots from the guides file
    bankOutLtr = "%s_footBankOut_LTR" % side
    bankInLtr = "%s_footBankIn_LTR" % side
    heelLtr = "%s_heel_LTR" % side
    ballFootLtr = "%s_ballFoot_LTR" % side
    toesLtr = "%s_toes_LTR" % side
    # Construct hierarchy:
    mc.parent(ikCtlChildren, ballFootLtr)
    mc.parent(ballFootLtr, toesLtr)
    mc.parent(toesLtr, heelLtr)
    mc.parent(heelLtr, bankInLtr)
    mc.parent(bankInLtr, bankOutLtr)
    mc.parent(bankOutLtr, footIkCtl)
    # IK handle:
    ballFootIkHandle, _ = mc.ikHandle(
        sj="%s_leg02Ik_JNT" % side,
        ee="%s_leg03Ik_JNT" % side,
        sol="ikSCsolver",
        n="%s_ballfoot_IKH" % side,
    )
    mc.parent(ballFootIkHandle, ballFootLtr)
    # Set up rotation nodes:

    ballFootClamp = mc.createNode("clamp", n="%s_ballOfFootRotationClamp_CL" % side)
    mc.connectAttr(rollAttr, ballFootClamp + ".input.inputR")
    mc.connectAttr(toeLiftAttr, ballFootClamp + ".max.maxR")
    ballFootReverseRemapValue = mc.createNode(
        "remapValue", n="%s_ballOfFootreverseRotation_RMV" % side
    )
    mc.connectAttr(ballStraightAttr, ballFootReverseRemapValue + ".inputMax")
    mc.connectAttr(toeLiftAttr, ballFootReverseRemapValue + ".inputMin")
    mc.connectAttr(toeLiftAttr, ballFootReverseRemapValue + ".outputMax")
    mc.connectAttr(rollAttr, ballFootReverseRemapValue + ".inputValue")
    ballFootRotationBlend = mc.createNode(
        "animBlendNodeAdditiveDA", n="%s_ballOfFootRotationBlend_ADA" % side
    )
    mc.connectAttr(ballFootClamp + ".outputR", ballFootRotationBlend + ".inputA")
    mc.connectAttr(
        ballFootReverseRemapValue + ".outValue", ballFootRotationBlend + ".inputB"
    )
    mc.setAttr(ballFootRotationBlend + ".weightB", -1)
    mc.connectAttr(ballFootRotationBlend + ".output", ballFootLtr + ".rotate.rotateX")
    negateXRotationBall = mc.createNode(
        "animBlendNodeAdditiveDA", n="%s_negateXRotationInBall_ADA" % side
    )
    mc.setAttr(negateXRotationBall + ".weightA", -1)
    mc.connectAttr(ballFootLtr + ".rotate.rotateX", negateXRotationBall + ".inputA")
    mc.connectAttr(negateXRotationBall + ".output", "%s_leg03Ik_JNT.rotateX" % side)

    toesRemapOutputMax = mc.createNode(
        "animBlendNodeAdditiveDA", n="%s_toeLiftRemapOutputMax_ADA" % side
    )
    mc.setAttr(toesRemapOutputMax + ".inputA", 180)
    mc.connectAttr(toeLiftAttr, toesRemapOutputMax + ".inputB")
    mc.setAttr(toesRemapOutputMax + ".weightB", -1)
    toesRotationRemap = mc.createNode("remapValue", n="%s_toesRotationRemap_RMV" % side)
    mc.connectAttr(rollAttr, toesRotationRemap + ".inputValue")
    mc.connectAttr(toeLiftAttr, toesRotationRemap + ".inputMin")
    mc.setAttr(toesRotationRemap + ".inputMax", 180)
    mc.setAttr(toesRotationRemap + ".outputMin", 0)
    mc.connectAttr(toesRemapOutputMax + ".output", toesRotationRemap + ".outputMax")
    mc.connectAttr(toesRotationRemap + ".outColorR", toesLtr + ".rx")

    heelRollClamp = mc.createNode("clamp", n="%s_heelRoll_CL" % side)
    mc.connectAttr(rollAttr, heelRollClamp + ".input.inputR")
    mc.setAttr(heelRollClamp + ".minR", -45)
    mc.setAttr(heelRollClamp + ".maxR", 0)
    mc.connectAttr(heelRollClamp + ".outputR", heelLtr + ".rx")

    # Set up banking:
    # Clamp
    bankingClamp = mc.createNode("clamp", n="%s_footBankingClamp_CL" % side)
    mc.connectAttr(bankAttr, bankingClamp + ".inputR")
    mc.setAttr(bankingClamp + ".maxR", 10)
    mc.connectAttr(bankAttr, bankingClamp + ".inputG")
    mc.setAttr(bankingClamp + ".minG", -10)
    # Animblend to Bank out:
    bankOutAnimBlend = mc.createNode(
        "animBlendNodeAdditiveDA", n="%s_bankOut_ADA" % side
    )
    mc.setAttr(bankOutAnimBlend + ".inputA", -10)
    mc.connectAttr(bankingClamp + ".outputR", bankOutAnimBlend + ".weightA")
    mc.connectAttr(bankOutAnimBlend + ".output", bankOutLtr + ".rz")
    # Animblend to Bank In:
    bankInAnimBlend = mc.createNode("animBlendNodeAdditiveDA", n="%s_bankIn_ADA" % side)
    mc.setAttr(bankInAnimBlend + ".inputA", -10)
    mc.connectAttr(bankingClamp + ".outputG", bankInAnimBlend + ".weightA")
    mc.connectAttr(bankInAnimBlend + ".output", bankInLtr + ".rz")

    # Housekeeping:
    if DEBUG_MODE == False:
        ltrSet = [bankOutLtr, bankInLtr, heelLtr, toesLtr, ballFootLtr]
        for ltr in ltrSet:
            mc.setAttr(ltr + ".v", 0)


def addToSkinJoints(joint, skinJointsMessageAttr="C_harry_CTL.skinJoints"):
    jointMessageAttr = gen.addAttr(joint, ln="skinJoint", at="message")
    mc.connectAttr(skinJointsMessageAttr, jointMessageAttr)


def orientToParent(parentCtl, drivenCtl, drivenGrp, worldControl="C_harry_CTL"):
    # Create an attribute for the control
    orientAttr = gen.addAttr(
        drivenCtl, at="float", ln="orientToParent", k=1, min=0, max=1
    )
    # create a zeroed out transform at the parent location
    if parentCtl[0] != "C":
        worldOrientedNode = mc.createNode(
            "transform", n=parentCtl[:-4] + "WorldOrientation_TRN"
        )
        mc.parent(worldOrientedNode, parentCtl, r=1)
        mc.rotate(0, 0, 0, worldOrientedNode, ws=1)
        # Orient constrain the drivenGroup:
        orientConstraintNode = mc.orientConstraint(
            worldControl, worldOrientedNode, drivenGrp, mo=1
        )[0]
    else:
        orientConstraintNode = mc.orientConstraint(
            worldControl, parentCtl, drivenGrp, mo=1
        )[0]
    # Connect the attr to the parentCtlConstraint
    mc.connectAttr(orientAttr, orientConstraintNode + ".w1")
    reverse = mc.createNode("reverse", n=drivenGrp[:-4] + "ReverseInfluence_RV")
    mc.connectAttr(orientConstraintNode + ".w1", reverse + ".inputX")
    mc.connectAttr(reverse + ".outputX", orientConstraintNode + ".w0")


def buildBendyLimbs(side, limb, bendSharpness=3):
    # Create guide joints for the midway controls for ribbons
    upperJoint, lowerJoint = None, None
    if limb == "arm":
        upperJoint = mc.duplicate(
            "%s_arm02_JNT" % side, po=1, n="%s_upperArm_JNT" % side
        )[0]
        lowerJoint = mc.duplicate(
            "%s_arm03_JNT" % side, po=1, n="%s_lowerArm_JNT" % side
        )[0]
    elif limb == "leg":
        upperJoint = mc.duplicate(
            "%s_leg01_JNT" % side, po=1, n="%s_upperLeg_JNT" % side
        )[0]
        lowerJoint = mc.duplicate(
            "%s_leg02_JNT" % side, po=1, n="%s_lowerLeg_JNT" % side
        )[0]
    xPosUpper = mc.getAttr(upperJoint + ".tx") * 0.5
    mc.setAttr(upperJoint + ".tx", xPosUpper)
    xPosLower = mc.getAttr(lowerJoint + ".tx") * 0.5
    mc.setAttr(lowerJoint + ".tx", xPosLower)
    halfwayJoints = [upperJoint, lowerJoint]
    # Zero out orientations and create controls:
    for jnt in halfwayJoints:
        mc.setAttr(jnt + ".jointOrientX", 0)
        mc.setAttr(jnt + ".jointOrientY", 0)
        mc.setAttr(jnt + ".jointOrientZ", 0)

    upperCtl, _, upperCtlGrp = buildControl(
        side,
        "%sUpper" % limb,
        upperJoint,
        shapeCVs=cs.RIBBON_SHAPE_CVS,
        shapeKnots=cs.KNOTS,
        colour=18 if side == "L" else 20,
    )
    lowerCtl, _, lowerCtlGrp = buildControl(
        side,
        "%sLower" % limb,
        lowerJoint,
        shapeCVs=cs.RIBBON_SHAPE_CVS,
        shapeKnots=cs.KNOTS,
        colour=18 if side == "L" else 20,
    )

    mc.parent(upperCtlGrp, lowerCtlGrp, "ctls_GRP")
    # Parent constrain
    if limb == "arm":
        mc.parentConstraint("%s_arm01_JNT" % side, upperCtlGrp, mo=1)
        mc.parentConstraint("%s_arm02_JNT" % side, lowerCtlGrp, mo=1)
    else:
        mc.parentConstraint("%s_leg00_JNT" % side, upperCtlGrp, mo=1)
        mc.parentConstraint("%s_leg01_JNT" % side, lowerCtlGrp, mo=1)
    jointChainReversed = mc.listRelatives(
        "%s_%s00_JNT" % (side, limb), ad=1, typ="joint"
    )
    jointChain = ["%s_%s00_JNT" % (side, limb)]
    for joint in reversed(jointChainReversed):
        jointChain.append(joint)
    if limb == "leg":
        jointChain = jointChain[:-1]
    else:
        jointChain = jointChain[1:]
    # Clean up
    # mc.delete(upperJoint)
    # mc.delete(lowerJoint)

    # def buildNurbsSurface(limb, upperCtl, lowerCtl):
    positionOrder = []
    extractedPointLocations = []
    # Extract joint xyz world space location
    for jnt in jointChain:
        loc = mc.spaceLocator()
        mc.parent(loc, jnt, r=1)
        positionOrder.append(mc.pointPosition(loc, w=1))
        mc.delete(loc)
    for locId in range(len(positionOrder)):
        if locId == 2 or locId == 4:
            for i in range(bendSharpness):
                extractedPointLocations.append(positionOrder[locId])
        else:
            extractedPointLocations.append(positionOrder[locId])
    # Create guide curve and clusters and parent them under the appropriate controls:
    baseCurve = mc.curve(
        n="%s_%sNURBS_CRV" % (side, limb), d=3, p=extractedPointLocations
    )
    firstCurve, secondCurve = None, None
    curveClusters = []
    ctlsList = []
    if limb == "arm":
        ctlsList = [
            "%s_arm01Fk_CTL" % side,
            "%s_armUpper_CTL" % side,
            "%s_arm02Fk_CTL" % side,
            "%s_armLower_CTL" % side,
            "%s_arm03Fk_CTL" % side,
            "%s_arm03Fk_CTL" % side,
        ]
    else:
        ctlsList = [
            "%s_leg00Fk_CTL" % side,
            "%s_legUpper_CTL" % side,
            "%s_leg01Fk_CTL" % side,
            "%s_legLower_CTL" % side,
            "%s_leg02Fk_CTL" % side,
            "%s_leg03Fk_CTL" % side,
        ]
    for counter, cvIDs in enumerate(["0", "1", "2:4", "5", "6:8", "9"]):
        cvs = baseCurve + ".cv[%s]" % cvIDs

        _, clusterHandle = mc.cluster(
            cvs, name="%s_%s%s_CLS" % (side, limb, str(counter).zfill(2))
        )
        curveClusters.append(clusterHandle)
        mc.parent(clusterHandle, ctlsList[counter])
    # Move curve in local space, create first curve
    for clsId in range(len(curveClusters)):
        if limb == "arm":
            mc.move(
                mc.getAttr(curveClusters[clsId] + ".ty") + 1,
                curveClusters[clsId],
                y=1,
                ls=1,
            )
        if limb == "leg":
            if clsId <= 3:
                mc.move(
                    mc.getAttr(curveClusters[clsId] + ".ty") + 1,
                    curveClusters[clsId],
                    y=1,
                    ls=1,
                )
            else:
                mc.move(
                    mc.getAttr(curveClusters[clsId] + ".tx") + 1,
                    curveClusters[clsId],
                    x=1,
                    ls=1,
                )

    firstCurve = mc.duplicate(baseCurve)
    # Move curve in local space to create second curve
    for clsId in range(len(curveClusters)):
        if limb == "arm":
            mc.move(
                mc.getAttr(curveClusters[clsId] + ".ty") - 2,
                curveClusters[clsId],
                y=1,
                ls=1,
            )
        if limb == "leg":
            if clsId <= 3:
                mc.move(
                    mc.getAttr(curveClusters[clsId] + ".ty") - 2,
                    curveClusters[clsId],
                    y=1,
                    ls=1,
                )
            else:
                mc.move(
                    mc.getAttr(curveClusters[clsId] + ".tx") - 2,
                    curveClusters[clsId],
                    x=1,
                    ls=1,
                )
    secondCurve = mc.duplicate(baseCurve)

    # Create NURBS surface
    nurbsSfs = mc.loft(
        firstCurve, secondCurve, d=1, ch=0, n="%s_%sNURBS_SFS" % (side, limb), po=0, rsn=1
    )[0]
    mc.delete(firstCurve, secondCurve, baseCurve)
    # Rotate wrist NURBS CVs:
    if limb == "arm":
        if side == "L":
            mc.rotate(
                90,
                0,
                0,
                nurbsSfs + ".cv[0:3][6:9]",
                os=1,
                fo=1,
                r=1,
                p=[52.490207, 94.25426, -7.880189],
            )
        else:
            mc.rotate(
                90,
                0,
                0,
                nurbsSfs + ".cv[0:3][6:9]",
                os=1,
                fo=1,
                r=1,
                p=[-52.490207, 94.25426, -7.880189],
            )
    mc.parent(nurbsSfs, "rig_GRP")

    # Cluster and parent to correct joint/ctl:
    clusterParents = None
    if limb == "arm":
        clusterParents = [
            "%s_arm01_JNT" % side,
            "%s_armUpper_CTL" % side,
            "%s_arm02_JNT" % side,
            "%s_armLower_CTL" % side,
            "%s_arm03_JNT" % side,
            "%s_arm04_JNT" % side,
        ]
    else:
        clusterParents = [
            "%s_leg00_JNT" % side,
            "%s_legUpper_CTL" % side,
            "%s_leg01_JNT" % side,
            "%s_legLower_CTL" % side,
            "%s_leg02_JNT" % side,
            "%s_leg03_JNT" % side,
        ]
    for counter, cvIDs in enumerate(["0", "1", "2:4", "5", "6:8", "9"]):
        cvs = nurbsSfs + ".cv[0:3][%s]" % cvIDs

        _, clusterHandle = mc.cluster(
            cvs, name="%s_%sNURBS%s_CLS" % (side, limb, str(counter).zfill(2))
        )
        curveClusters.append(clusterHandle)
        mc.parent(clusterHandle, clusterParents[counter])


def main():
    # Create a new file and import model and guides
    mc.file(new=1, force=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_body.ma", i=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_guides.ma", i=1)

    # Housekeeping setup:
    harryCtl, _, _ = buildControl("C", "harry", shapeCVs=cs.SQUARE_SHAPE_CVS)
    mc.scale(15, 15, 15, harryCtl + ".cv[*]")
    harryCtlSkinJoints = gen.addAttr(harryCtl, ln="skinJoints", at="message")
    ctlsGrp = mc.group(em=1)
    ctlsGrp = mc.rename(ctlsGrp, "ctls_GRP")
    rigGrp = mc.group(em=1)
    rigGrp = mc.rename(rigGrp, "rig_GRP")

    # Build spine
    spine = SpineComponent(mc.ls("C_spine??_JNT"), "C_spine_CRV")
    neck = NeckComponent(mc.ls("C_neck??_JNT"), mc.ls("C_neckWithTwist??_JNT"))

    # Build leg FK ctls. IK chain, Handle and Ctls
    for side in "LR":
        # Build IK chain and FK ctls
        (
            blendChain,
            fkCtlsList,
            fkCtlsOfsList,
            fkCtlsGrpList,
            ikChain,
            footIkCtl,
            footIkCtlGrp,
            footIkHandle,
            ikBaseCtl,
        ) = buildLimb(side, "leg", "C_hips_CTL", harryCtlSkinJoints)
        # Build Pole Vector control and create pole vector constraint to leg02IK:
        kneePoleVectorCtl, _, kneePoleVectorGrp = buildControl(
            side,
            "kneePoleVector",
            "%s_leg01Ik_JNT" % side,
            shapeCVs=cs.DIAMOND_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        kneePoleVectorPos = gen.getIkhPoleVecPos(footIkHandle)
        mc.scale(4, 4, 4, kneePoleVectorCtl + ".cv[*]")
        mc.move(
            kneePoleVectorPos.x,
            kneePoleVectorPos.y,
            kneePoleVectorPos.z,
            kneePoleVectorGrp,
        )
        mc.poleVectorConstraint(kneePoleVectorCtl, footIkHandle)

        ikCtlsGrp = mc.group(
            kneePoleVectorGrp, footIkCtlGrp, n="%s_legIkCtls_GRP" % side, w=1
        )
        mc.parent(ikCtlsGrp, ctlsGrp)

        # Make limb stretchable:
        limbStretch(side, "leg", ikChain[:-2], ikBaseCtl, footIkCtl)
        # Create parent constraints for the blend chain, and a blend translations
        # node for the end joint:
        blendChainParentConstraints = blendChainConstraints(
            "leg", blendChain[:-1], 2, ikChain[:-1], fkCtlsList, mo=0
        )
        orientConstrainIkEndJoint("%s_leg02Ik_JNT" % side, "%s_leg02Ik_CTL" % side)
        blendTranslationsNode = blendTranslations(
            "%s_leg02_BTA" % side, "%s_leg02_JNT" % side, "%s_leg02Ik_JNT" % side
        )
        # Create and position IK/FK Switch
        createConnectIkFkSwitch(
            side,
            "leg",
            "%s_leg02_JNT" % side,
            blendChainParentConstraints,
            blendTranslationsNode,
            ikCtlsGrp,
            ikBaseCtl,
            fkCtlsGrpList,
        )
        # Build foot roll:
        footRollSetup(side, footIkCtl)

        buildBendyLimbs(side, "leg")

    # Build arm FK ctls. IK chain, Handle and Ctls
    for side in "LR":
        # Build IK chain and FK ctls
        (
            blendChain,
            fkCtlsList,
            fkCtlsOfsList,
            fkCtlsGrpList,
            ikChain,
            wristIkCtl,
            wristIkCtlGrp,
            wristIkHandle,
            ikBaseCtl,
        ) = buildLimb(side, "arm", "C_chest_CTL", harryCtlSkinJoints)

        # Elbow pole vector:
        elbowPoleVectorCtl, _, elbowPoleVectorGrp = buildControl(
            side,
            "elbowPoleVector",
            "%s_arm02Ik_JNT" % side,
            shapeCVs=cs.DIAMOND_SHAPE_CVS,
            colour=18 if side == "L" else 20,
        )
        elbowPoleVectorPos = gen.getIkhPoleVecPos(wristIkHandle)
        mc.scale(4, 4, 4, elbowPoleVectorCtl + ".cv[*]")
        mc.move(
            elbowPoleVectorPos.x,
            elbowPoleVectorPos.y,
            elbowPoleVectorPos.z,
            elbowPoleVectorGrp,
        )
        mc.poleVectorConstraint(elbowPoleVectorCtl, wristIkHandle)
        # Place Ik ctls in hierarchy withing the CTLs group:
        ikCtlsGrp = mc.group(
            elbowPoleVectorGrp, wristIkCtlGrp, n="%s_armIkCtls_GRP" % side, w=1
        )
        mc.parent(ikCtlsGrp, ctlsGrp)
        # Make limb stretchable:
        limbStretch(side, "arm", ikChain[1:-1], ikBaseCtl, wristIkCtl)
        # Parent constraints on the arm blend chain:
        blendChainParentConstraints = blendChainConstraints(
            "arm", blendChain[:-1], 3, ikChain[:-1], fkCtlsList, mo=0
        )
        orientConstrainIkEndJoint("%s_arm03Ik_JNT" % side, "%s_arm03Ik_CTL" % side)
        blendTranslationsNode = blendTranslations(
            "%s_arm03_BTA" % side, "%s_arm03_JNT" % side, "%s_arm03Ik_JNT" % side
        )
        # Create and position IK/FK Switch
        createConnectIkFkSwitch(
            side,
            "arm",
            "%s_arm03_JNT" % side,
            blendChainParentConstraints,
            blendTranslationsNode,
            ikCtlsGrp,
            ikBaseCtl,
            fkCtlsGrpList,
        )
        # Build Hand structure and controls:
        hand = HandComponent(side)
        buildBendyLimbs(side, "arm")

    # Housekeeping:
    # Geometry in hierarchy
    mc.setAttr("C_geometry_GRP.inheritsTransform", 0)
    mc.parent("C_geometry_GRP", harryCtl)
    # Spine curve and root in hierarchy
    mc.parent("C_root_GRP", harryCtl)
    mc.parent("C_spine_CRV", harryCtl)
    mc.setAttr("C_spine_CRV.inheritsTransform", 0)
    mc.viewFit("C_geometry_GRP")


main()