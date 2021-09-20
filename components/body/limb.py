from maya import cmds as mc
from ...common import attr, control, poleVector, space, twist, skin, ribbon
from ..base import BaseComponent

PARAM_U_ARMS = [
    0.001,
    0.034,
    0.0687,
    0.12,
    0.22,
    0.2592135,
    0.32,
    0.42,
    0.5,
    0.58,
    0.721,
    0.8335,
    0.9,
]

PARAM_U_LEGS = [
    0.001,
    0.0222,
    0.042,
    0.0688,
    0.108,
    0.17,
    0.212,
    0.258,
    0.315,
    0.399,
    0.45,
    0.5,
    0.55,
    0.61,
    0.75,
    0.85,
    0.89,
]

class LimbComponent(BaseComponent):
    def __init__(self, side, name, parent, skinJointsMessageAttr):
        super(LimbComponent, self).__init__()
        self.limbType = "limb"
        self.side = side
        self.name = name
        self.parent = parent

    def buildLimb(self, side, name, parent, skinJointsMessageAttr):
        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        blendChain = mc.ls("%s_%s??_JNT" % (side, name))
        fkCtlsList = []
        fkCtlsOfsList = []
        fkCtlsGrpList = []
        prevFkCtl, prevFkCtlGrp = None, None
        ikHandle, ikCtl, ikCtlGrp, ikBaseCtl = None, None, None, None

        for jntId in range(len(blendChain) - 1):
            if self.limbType == "arm" and jntId == 0:
                fkCtl, fkCtlOfs, fkCtlGrp = control.buildControl(
                    side,
                    "%s%sFk" % (name, str(jntId).zfill(2)),
                    blendChain[jntId],
                    shapeCVs=control.shapes.L_CLAVICLE_SHAPE_CVS,
                    shapeKnots=control.shapes.KNOTS,
                    colour=18 if side == "L" else 20,
                )
            else:
                fkCtl, fkCtlOfs, fkCtlGrp = control.buildControl(
                    side,
                    "%s%sFk" % (name, str(jntId).zfill(2)),
                    blendChain[jntId],
                    colour=18 if side == "L" else 20,
                )
            if prevFkCtlGrp is None:
                mc.parent(fkCtlGrp, parent)
            else:
                mc.parent(fkCtlGrp, prevFkCtl)

            fkCtlsList.append(fkCtl)
            fkCtlsOfsList.append(fkCtlOfs)
            fkCtlsGrpList.append(fkCtlGrp)
            prevFkCtl, prevFkCtlGrp = fkCtl, fkCtlGrp
            # Adjust positioning of controls for the leg:
        if self.limbType == "leg":
            for ctl in fkCtlsList:
                mc.scale(6, 6, 6, ctl + ".cv[*]")

                if ctl != fkCtlsList[-1]:  # omit rotating the toe FK control CVs
                    mc.rotate(90, 0, 0, ctl + ".cv[*]", ws=1)

                if ctl == fkCtlsList[0]:  # move the hip FK control CVs for visual clarity
                    mc.move(0, -8, 0, ctl + ".cv[*]", ws=1, r=1)
            space.orientToParent(parent, fkCtlsList[0], fkCtlsGrpList[0])
        if self.limbType == "arm":
            mc.scale(1.5, 1.5, 1.5, fkCtlsList[0] + ".cv[*]")
            if side == "L":
                mc.move(8, 8, -2, fkCtlsList[0] + ".cv[*]", ws=1, r=1)
            else:
                mc.rotate(-180, 0, 0, fkCtlsList[0] + ".cv[*]", os=1, r=1)
                mc.move(-8, 8, -2, fkCtlsList[0] + ".cv[*]", ws=1, r=1)

            for fkCtl in fkCtlsList[1:]:
                mc.scale(6, 6, 6, fkCtl + ".cv[*]")
                mc.rotate(0, 90, 0, fkCtl + ".cv[*]", r=1)

                if fkCtl == fkCtlsList[1]:
                    if side == "L":
                        mc.move(3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                    else:
                        mc.move(-3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
            # Expose ability to change limb joints' orientation
            space.orientToParent(fkCtlsList[0], fkCtlsList[1], fkCtlsGrpList[1])
        # Create IK copy of the blend chain
        ikChain = mc.duplicate("%s_%s00_JNT" % (side, name), renameChildren=1)
        renamedIkChain = []
        for jnt in ikChain:
            renamedIkChain.append(mc.rename(jnt, jnt.replace("_JNT", "Ik_JNT")[:-1]))

        ikChain = renamedIkChain

        limbGrp = mc.group(blendChain[0], ikChain[0])
        limbGrp = mc.rename(limbGrp, "%s_%s_GRP" % (side, name))
        mc.parent(fkCtlsList[0][0:-4] + "_GRP", limbGrp)
        mc.parent(limbGrp, parent)

        # Create IK ctl and handle for the leg:
        if self.limbType == "leg":
            ikBaseCtl, _, ikBaseCtlGrp = control.buildControl(
                side,
                "%s00Ik" % name,
                "%s_%s00Ik_JNT" % (side, name),
                shapeCVs=control.shapes.SQUARE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.parent(ikBaseCtlGrp, parent)
            mc.scale(6, 6, 6, ikBaseCtl + ".cv[*]")
            mc.rotate(0, 0, 90, ikBaseCtl + ".cv[*]", ws=1)
            mc.move(0, -8, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
            ikCtl, _, ikCtlGrp = control.buildControl(
                side,
                "%s02Ik" % name,
                "%s_%s02Ik_JNT" % (side, name),
                shapeCVs=control.shapes.SQUARE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.scale(6, 6, 6, ikCtl + ".cv[*]")
            mc.parent(ikChain[0], ikBaseCtl)
            # Create a spaceSwitch for the leg Ik ctl:
            space.createSpaces(ikCtl, spaces=["C_top_CTL", "C_root_CTL", "C_hips_CTL"])
            # Create IK handle and parent to IK control:
            ikHandle, _ = mc.ikHandle(
                sj="%s_%s00Ik_JNT" % (side, name),
                ee="%s_%s02Ik_JNT" % (side, name), sol="ikRPsolver"
            )
            ikHandle = mc.rename(ikHandle, "%s_%s02_IKH" % (side, name))
            mc.parent(ikHandle, ikCtl)
            mc.hide(ikHandle)
        # Create IK ctl and handle for the arm:
        if self.limbType == "arm":
            ikBaseCtl, _, ikBaseCtlGrp = control.buildControl(
                side,
                "%s01Ik" % name,
                "%s_%s01Ik_JNT" % (side, name),
                shapeCVs=control.shapes.SQUARE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.parent(ikBaseCtlGrp, fkCtlsList[0])
            mc.parent(ikChain[0], ikBaseCtl)
            mc.scale(6, 6, 6, ikBaseCtl + ".cv[*]")
            mc.rotate(0, 0, 90, ikBaseCtl + ".cv[*]", r=1)
            if side == "L":
                mc.move(3, 0, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
            else:
                mc.move(-3, 0, 0, ikBaseCtl + ".cv[*]", ws=1, r=1)
            ikCtl, _, ikCtlGrp = control.buildControl(
                side,
                "%s03Ik" % name,
                "%s_%s03Ik_JNT" % (side, name),
                shapeCVs=control.shapes.SQUARE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.scale(6, 6, 6, ikCtl + ".cv[*]")
            mc.rotate(0, 0, 90, ikCtl + ".cv[*]", r=1)
            # Create a space swith to root, hip, chest, head, clavicle:
            space.createSpaces(
                ikCtl,
                spaces=[
                    "C_top_CTL",
                    "C_root_CTL",
                    "C_hips_CTL",
                    "C_chest_CTL",
                    "C_head_CTL",
                    "%s_%s00Fk_CTL" % (side, name),
                ],
            )
            # Create IK handle and parent to IK control:
            ikHandle, _ = mc.ikHandle(
                sj="%s_%s01Ik_JNT" % (side, name), ee="%s_%s03Ik_JNT" % (side, name), sol="ikRPsolver"
            )
            ikHandle = mc.rename(ikHandle, "%s_%s03_IKH" % (side, name))
            mc.parent(ikHandle, ikCtl)
            mc.hide(ikHandle)

        # Connect a message attr to the Harry Ctl for all skin joints:
        if self.limbType == "leg":
            for joint in blendChain:
                skin.addToSkinJoints(joint)
        else:
            for joint in blendChain[:-1]:
                skin.addToSkinJoints(joint)

        if not DEBUG_MODE:
            mc.hide(blendChain, ikChain)
            for ctl in fkCtlsList:
                attr.lockAndHide(fkCtl, [".txyz", ".sxyz"])
            attr.lockAndHide(ikBaseCtl, [".rxyz", ".sxyz"])
            attr.lockAndHide(ikCtl, [".sxyz"])

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

    def limbStretch(self, side, name, startEnd, startControl, endControl, conditional=1):
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

    def blendChainConstraints(self, limb, driven, skipTranslate, *args, **kwargs):
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

    def orientConstrainIkEndJoint(self, driven, driver):
        # Orient constrain the end joint of an Ik chain to the Ik CTL:
        constraintNode = mc.orientConstraint(driver, driven, mo=0)
        return constraintNode

    def blendTranslations(self, name, blendJoint, ikJoint):
        ikJointTranslate = ikJoint + ".translateX"
        staticLen = mc.getAttr(ikJointTranslate)
        blendTranslationsNode = mc.createNode("blendTwoAttr", n=name)
        mc.connectAttr(ikJointTranslate, blendTranslationsNode + ".input[0]")
        mc.setAttr(blendTranslationsNode + ".input[1]", staticLen)
        mc.connectAttr(blendTranslationsNode + ".output", blendJoint + ".translateX")

        return blendTranslationsNode


    def createConnectIkFkSwitch(self,
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
        ikFkSwitchCtl, ikFkSwitchOfs, ikFkSwitchGrp = control.buildControl(
            side, "%sIkFkSwitch" % name, parentJoint, shapeCVs=control.shapes.SWITCH_SHAPE_CVS
        )
        if self.limbType == "arm":
            mc.move(0, 10, -10, ikFkSwitchGrp, r=1, ws=1)
            mc.rotate(90, 0, 0, ikFkSwitchGrp, ws=1, r=1)
        else:
            mc.rotate(90, 0, 90, ikFkSwitchGrp, r=1, ws=1)
            if side == "L":
                mc.move(15, 10, 0, ikFkSwitchGrp, ws=1, r=1)
            else:
                mc.move(-15, 10, 0, ikFkSwitchGrp, ws=1, r=1)

        mc.pointConstraint(parentJoint, ikFkSwitchGrp, mo=1)
        mc.setAttr(ikFkSwitchGrp + ".inheritsTransform", 0)
        # Create the switch attribute, where 0=IK and 1=FK
        ikFkSwitchAttr = attr.addAttr(
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
        # Clean up:
        mc.setAttr(ikFkSwitchCtl + ".tx", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".ty", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".tz", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".rx", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".ry", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".rz", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".sx", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".sy", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".sz", lock=True, k=False, channelBox=False)
        mc.setAttr(ikFkSwitchCtl + ".v", lock=True, k=False, channelBox=False)

        return reversalNodeIkFk + ".output1D", ikFkSwitchAttr

    def buildBendyLimbs(self, side, limb, elbowKneeBendSharpness=2, wristAnkleBendSharpness=3):
        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Create guide joints for the midway controls for ribbons
        upperJoint, lowerJoint = None, None
        if limb == "arm":
            jointPairs = ["1", "2", "3"]
        else:
            jointPairs = ["0", "1", "2"]

        upperJoint = mc.duplicate(
            "%s_%s0%s_JNT" % (side, limb, jointPairs[1]), po=1, n="%s_upperArm_JNT" % side
        )[0]
        lowerJoint = mc.duplicate(
            "%s_%s0%s_JNT" % (side, limb, jointPairs[2]), po=1, n="%s_lowerArm_JNT" % side
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

        upperCtl, upperOfs, upperCtlGrp = control.buildControl(
            side,
            "%sUpper" % limb,
            upperJoint,
            shapeCVs=control.shapes.RIBBON_SHAPE_CVS,
            shapeKnots=control.shapes.KNOTS,
            colour=18 if side == "L" else 20,
        )
        lowerCtl, lowerOfs, lowerCtlGrp = control.buildControl(
            side,
            "%sLower" % limb,
            lowerJoint,
            shapeCVs=control.shapes.RIBBON_SHAPE_CVS,
            shapeKnots=control.shapes.KNOTS,
            colour=18 if side == "L" else 20,
        )
        if not DEBUG_MODE:
            attr.lockAndHide(upperCtl, [".rxyz", ".sxyz"])
            attr.lockAndHide(lowerCtl, [".rxyz", ".sxyz"])

        mc.parent(upperCtlGrp, lowerCtlGrp, "ctls_GRP")

        # Point and Orient contstrain the bend controls so that they travel with
        # the stretched limb and maintain the orientation of the control higher up
        # in the chain. NOTE:Plugged into the group as opposed to the offset due to the
        # half twist function calculation already affecting the offset later on:
        mc.orientConstraint("%s_%s0%s_JNT" % (side, limb, jointPairs[0]), upperCtlGrp)
        mc.orientConstraint("%s_%s0%s_JNT" % (side, limb, jointPairs[1]), lowerCtlGrp)

        mc.pointConstraint(
            "%s_%s0%s_JNT" % (side, limb, jointPairs[0]),
            "%s_%s0%s_JNT" % (side, limb, jointPairs[1]),
            upperCtlGrp,
            mo=1,
            w=0.5,
        )
        mc.pointConstraint(
            "%s_%s0%s_JNT" % (side, limb, jointPairs[1]),
            "%s_%s0%s_JNT" % (side, limb, jointPairs[2]),
            lowerCtlGrp,
            mo=1,
            w=0.5,
        )

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

        positionOrder = []
        extractedPointLocations = []
        # Extract joint xyz world space location
        for jnt in jointChain:
            loc = mc.spaceLocator()
            mc.parent(loc, jnt, r=1)
            positionOrder.append(mc.pointPosition(loc, w=1))
            mc.delete(loc)
        for locId in range(len(positionOrder)):
            if locId == 2:
                for i in range(elbowKneeBendSharpness):
                    extractedPointLocations.append(positionOrder[locId])
            elif locId == 4:
                for i in range(wristAnkleBendSharpness):
                    extractedPointLocations.append(positionOrder[locId])

            else:
                extractedPointLocations.append(positionOrder[locId])

        # Clean up:
        mc.delete(upperJoint)
        mc.delete(lowerJoint)

        # Create guide curve and clusters and parent them under the appropriate controls:

        baseCurve = mc.curve(
            n="%s_%sNURBS_CRV" % (side, limb), d=3, p=extractedPointLocations
        )
        firstCurve, secondCurve = None, None
        curveClusters = []
        ctlsList = [
            "%s_%s00Fk_CTL" % (side, self.name),
            "%s_%sUpper_CTL" % (side, self.name),
            "%s_%s01Fk_CTL" % (side, self.name),
            "%s_%sLower_CTL" % (side, self.name),
            "%s_%s02Fk_CTL" % (side, self.name),
            "%s_%s03Fk_CTL" % (side, self.name),
        ]

        # Variation in CV order depending on knee or elbow/ wrist and ankle bend sharpness:
        cvOrder = []
        dummyClusterCVs = None
        if elbowKneeBendSharpness == 2:
            if wristAnkleBendSharpness == 2:
                cvOrder = ["0", "1", "2:3", "4", "5:6", "7"]
                dummyClusterCVs = "5:7"
            elif wristAnkleBendSharpness == 3:
                cvOrder = ["0", "1", "2:3", "4", "5:7", "8"]
                dummyClusterCVs = "5:8"
        elif elbowKneeBendSharpness == 3:
            if wristAnkleBendSharpness == 2:
                cvOrder = ["0", "1", "2:4", "5", "6:7", "8"]
                dummyClusterCVs = "6:8"
            elif wristAnkleBendSharpness == 3:
                cvOrder = ["0", "1", "2:4", "5", "6:8", "9"]
                dummyClusterCVs = "6:9"

        for counter, cvIDs in enumerate(cvOrder):
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
            firstCurve,
            secondCurve,
            d=1,
            u=1,
            rn=0,
            rsn=True,
            ch=0,
            n="%s_%sSurface_NRB" % (side, limb),
            po=0,
        )[0]
        mc.delete(firstCurve, secondCurve, baseCurve)

        # Variation in CV order depending on knee or elbow/ wrist and ankle bend sharpness:
        cvOrder = []
        dummyClusterCVs = None
        if elbowKneeBendSharpness == 2:
            if wristAnkleBendSharpness == 2:
                cvOrder = ["0", "1", "2:3", "4", "5:6", "7"]
                dummyClusterCVs = "5:7"
            elif wristAnkleBendSharpness == 3:
                cvOrder = ["0", "1", "2:3", "4", "5:7", "8"]
                dummyClusterCVs = "5:8"
        elif elbowKneeBendSharpness == 3:
            if wristAnkleBendSharpness == 2:
                cvOrder = ["0", "1", "2:4", "5", "6:7", "8"]
                dummyClusterCVs = "6:8"
            elif wristAnkleBendSharpness == 3:
                cvOrder = ["0", "1", "2:4", "5", "6:8", "9"]
                dummyClusterCVs = "6:9"

        # Rotate wrist NURBS CVs:
        if limb == "arm":
            dummyTransform = mc.createNode("transform", parent="%s_%s03_JNT" % (side, self.name))
            _, dummyCluster = mc.cluster(nurbsSfs + ".cv[%s][0:1]" % dummyClusterCVs)
            mc.parent(dummyCluster, dummyTransform)
            mc.rotate(90, 0, 0, dummyTransform)
            mc.delete(nurbsSfs, ch=1)
        mc.parent(nurbsSfs, "rig_GRP")

        # Cluster and parent to correct joint/ctl:
        clusterParents = None
        if limb == "arm":
            clusterParents = [
                "%s_%s01_JNT" % (side, self.name),
                "%s_%sUpper_CTL" % (side, self.name),
                "%s_%s02_JNT" % (side, self.name),
                "%s_%sLower_CTL" % (side, self.name),
                "%s_%s03_JNT" % (side, self.name),
                "%s_%s04_JNT" % (side, self.name),
            ]
        else:
            clusterParents = [
                "%s_%s00_JNT" % (side, self.name),
                "%s_%sUpper_CTL" % (side, self.name),
                "%s_%s01_JNT" % (side, self.name),
                "%s_%sLower_CTL" % (side, self.name),
                "%s_%s02_JNT" % (side, self.name),
                "%s_%s03_JNT" % (side, self.name),
            ]
        for counter, cvIDs in enumerate(cvOrder):
            cvs = nurbsSfs + ".cv[%s][0:1]" % cvIDs

            _, clusterHandle = mc.cluster(
                cvs, name="%s_%sNURBS%s_CLS" % (side, limb, str(counter).zfill(2))
            )
            curveClusters.append(clusterHandle)
            clusterGroup = mc.createNode(
                "transform", n="%s_%s%sCLS_GRP" % (side, limb, str(counter).zfill(2))
            )
            mc.delete(mc.parentConstraint(clusterHandle, clusterGroup, mo=0))
            mc.parent(clusterHandle, clusterGroup)
            mc.parent(clusterGroup, clusterParents[counter])
            if DEBUG_MODE == False:
                mc.setAttr(clusterHandle + ".visibility", 0)

        # Create bind joints at the relevant parameters for each limb:
        if limb == "arm":
            paramUList = PARAM_U_ARMS
        else:
            paramUList = PARAM_U_LEGS
        limbBindJoints = ribbon.createBindJoints(
            side,
            limb,
            nurbsSfs,
            numFollicles=len(paramUList),
            createJoints=True,
            paramUList=paramUList,
        )
        for joint in limbBindJoints:
            skin.addToSkinJoints(joint)
        self.limbHalfTwist(side, limb)

        if DEBUG_MODE == False:
            mc.setAttr(nurbsSfs + ".v", 0)

    def limbHalfTwist(self, side, limb):
        if limb == "arm":
            jointPairs = [
                ["%s_%s01_JNT" % (side, self.name), "%s_%s02_JNT" % (side, self.name)],
                ["%s_%s02_JNT" % (side, self.name), "%s_%s03_JNT" % (side, self.name)],
            ]
            alignWithValues = ["X", "X"]
        else:
            jointPairs = [
                ["%s_%s00_JNT" % (side, self.name), "%s_%s01_JNT" % (side, self.name)],
                ["%s_%s01_JNT" % (side, self.name), "%s_%s02_JNT" % (side, self.name)],
            ]
            alignWithValues = ["X", "Y"]

        for jointPair, alignWithValue in zip(jointPairs, alignWithValues):
            twistingJoint = jointPair[1]
            staticParent = jointPair[0]
            if limb == "leg" and jointPair == jointPairs[1]:
                halfValue = -0.5
            else:
                halfValue = 0.5
            endJointTwist = twist.extractTwist(twistingJoint, staticParent, alignWithValue)
            # Plug this value of rotation into an ADA to half the rotation value:
            halfRotation = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_%sJointHalvedTwist_ADA" % (side, twistingJoint[2:-4]),
            )
            mc.connectAttr(endJointTwist, halfRotation + ".inputA")
            mc.setAttr(halfRotation + ".weightA", halfValue)
            if jointPair == jointPairs[0]:
                mc.connectAttr(halfRotation + ".output", "%s_%sUpper_OFS.rx" % (side, limb))
            else:
                mc.connectAttr(halfRotation + ".output", "%s_%sLower_OFS.rx" % (side, limb))

    def shoulderHalfTwist(self, side, name):
        """Calculates the twist in Z for each shouled (arm01) JNT and plugs a halved
        value into the armNURBS00_CLS to negate some of the intersection when raising
        the arm"""

        extractedTwistShoulder = twist.extractTwist(
            "%s_arm01_JNT" % (side), "%s_arm00_JNT" % (side), alignXwith="Z"
        )
        clusterParentNodeOrientated = mc.createNode(
            "transform", n="%s_%sOrientated_TRN" % (side, name)
        )
        mc.parent(clusterParentNodeOrientated, "%s_arm01_JNT" % (side), r=1)
        mc.parent("%s_arm00CLS_GRP" % (side), clusterParentNodeOrientated)
        # Plug this value of rotation into an ADA to half the rotation value:
        halfRotation = mc.createNode(
            "animBlendNodeAdditiveDA", n="%s_%s_ADA" % (side, name),
        )
        mc.connectAttr(extractedTwistShoulder, halfRotation + ".inputA")
        mc.setAttr(halfRotation + ".weightA", -0.5)
        mc.connectAttr(halfRotation + ".output", clusterParentNodeOrientated + ".rotateZ")

class LegComponent(LimbComponent):
    def __init__(self, side, name, parent, skinJointsMessageAttr):
        super(LegComponent, self).__init__(side, name, parent, skinJointsMessageAttr)
        self.limbType = "leg"

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Build IK chain and FK ctls
        (blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain,
         footIkCtl, footIkCtlGrp, footIkHandle, ikBaseCtl) = self.buildLimb(
             side, name, parent, skinJointsMessageAttr)

        # Build Pole Vector control and create pole vector constraint to leg02IK:
        kneePoleVectorCtl, kneePoleVectorGrp = poleVector.buildPoleVectorControl(
            side, "kneePoleVector", "%s_%s01Ik_JNT" % (side, name), footIkHandle)

        space.createSpaces(
            kneePoleVectorCtl, spaces=["C_top_CTL", "C_root_CTL", "C_hips_CTL", footIkCtl])

        ikCtlsGrp = mc.group(
            kneePoleVectorGrp, footIkCtlGrp, n="%s_%sIkCtls_GRP" % (side, name), w=1)
        mc.parent(ikCtlsGrp, "ctls_GRP")

        # Make limb stretchable:
        self.limbStretch(side, name, ikChain[:-2], ikBaseCtl, footIkCtl)

        # Create parent constraints for the blend chain, and a blend translations
        # node for the end joint:
        blendChainParentConstraints = self.blendChainConstraints(
            name, blendChain[:-1], 2, ikChain[:-1], fkCtlsList, mo=0)

        self.orientConstrainIkEndJoint("%s_%s02Ik_JNT" % (side, name), "%s_%s02Ik_CTL" % (side, name))
        blendTranslationsNode = self.blendTranslations(
            "%s_%s02_BTA" % (side, name), "%s_%s02_JNT" % (side, name), "%s_%s02Ik_JNT" % (side, name))

        # Create and position IK/FK Switch
        self.createConnectIkFkSwitch(
            side,
            name,
            "%s_%s02_JNT" % (side, name),
            blendChainParentConstraints,
            blendTranslationsNode,
            ikCtlsGrp,
            ikBaseCtl,
            fkCtlsGrpList)

        # Temporary place for the halfwayHipJoint creation:
        if side == "R":
            halfwayHipJoint, leftTwist, rightTwist = twist.jointWithHalfwayTwist(
                "L_%s00_JNT" % (name),
                "R_%s00_JNT" % (name),
                twistAxisJoint1="Y",
                twistAxisJoint2="Y",
                twistAxisHalfwayJoint="Y",
                staticParent=parent,
                side="C",
                name="halfwayLeg00",
            )

            skin.addToSkinJoints(halfwayHipJoint)

            # Drive leg up corrective BS:
            twist.blendShapeDriverFromTwist(leftTwist, angle=-90, remapRange=(0.32, 0.87))
            twist.blendShapeDriverFromTwist(rightTwist, angle=-90, remapRange=(0.32, 0.87))

        self.buildBendyLimbs(side, name)

        # Clean up:
        if not DEBUG_MODE:
            attr.lockAndHide(kneePoleVectorCtl, [".rxyz"])

        # Store things that might be needed from outside
        self.ikCtl = footIkCtl

class ArmComponent(LimbComponent):
    def __init__(self, side, name, parent, skinJointsMessageAttr):
        super(ArmComponent, self).__init__(side, name, parent, skinJointsMessageAttr)
        self.limbType = "arm"

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Build IK chain and FK ctls
        (blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain,
         wristIkCtl, wristIkCtlGrp, wristIkHandle, ikBaseCtl) = self.buildLimb(
             side, name, parent, skinJointsMessageAttr)

        # Elbow pole vector:
        elbowPoleVectorCtl, elbowPoleVectorGrp = poleVector.buildPoleVectorControl(
            side, "elbowPoleVector", "%s_%s02Ik_JNT" % (side, name), wristIkHandle
        )

        # Create spaces (same as wristIk + wristIK ctl):
        space.createSpaces(
            elbowPoleVectorCtl,
            spaces=[
                "C_top_CTL",
                "C_root_CTL",
                "C_hips_CTL",
                "C_chest_CTL",
                "C_head_CTL",
                "%s_%s00Fk_CTL" % (side, name),
                wristIkCtl,
            ],
        )

        # Place Ik ctls in hierarchy withing the CTLs group:
        ikCtlsGrp = mc.group(
            elbowPoleVectorGrp, wristIkCtlGrp, n="%s_%sIkCtls_GRP" % (side, name), w=1
        )
        mc.parent(ikCtlsGrp, "ctls_GRP")

        # Make limb stretchable:
        self.limbStretch(side, name, ikChain[1:-1], ikBaseCtl, wristIkCtl)

        # Parent constraints on the arm blend chain:
        blendChainParentConstraints = self.blendChainConstraints(
            name, blendChain[:-1], 3, ikChain[:-1], fkCtlsList, mo=0
        )

        self.orientConstrainIkEndJoint("%s_%s03Ik_JNT" % (side, name), "%s_%s03Ik_CTL" % (side, name))

        blendTranslationsNode = self.blendTranslations(
            "%s_%s03_BTA" % (side, name), "%s_%s03_JNT" % (side, name), "%s_%s03Ik_JNT" % (side, name)
        )

        # Create and position IK/FK Switch
        self.createConnectIkFkSwitch(
            side,
            name,
            "%s_%s03_JNT" % (side, name),
            blendChainParentConstraints,
            blendTranslationsNode,
            ikCtlsGrp,
            ikBaseCtl,
            fkCtlsGrpList[1:],
        )

        self.buildBendyLimbs(side, name)

        # Negate the arm00_JNT twist in Z by 0.5 and plug that directly into the
        # arm00 cluster to deal with some of the intersecting that occurs when
        # raising the arm:
        self.shoulderHalfTwist(side, "halfTwistInShoulder")

        # Clean up:
        if not DEBUG_MODE:
            attr.lockAndHide(elbowPoleVectorCtl, [".rxyz"])
