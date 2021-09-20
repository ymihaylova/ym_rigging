from maya import cmds as mc
from maya.api import OpenMaya as om2
from ...common import attr, control, skin, twist, vector
from ..base import BaseComponent

class EyesComponent(BaseComponent):
    def __init__(self):
        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        for side in "LR":
            # Eyeball controls and constraints:
            upperLidCRV = "%s_lidUpper_CRV" % side
            lowerLidCRV = "%s_lidLower_CRV" % side
            eyeJnt = "%s_eye_JNT" % side
            # Create a duplicate of the eye joint to use for skinning of the eyelid area:
            eyeScalingJnt = mc.duplicate(eyeJnt)[0]
            eyeScalingJnt = mc.rename(
                eyeScalingJnt, eyeScalingJnt.replace("_JNT1", "Scaling_JNT")
            )
            mc.setAttr(eyeScalingJnt + ".v", 0)
            skin.addToSkinJoints(eyeScalingJnt)
            # Pupil joint which will be controlled by an attribute on the eye rotation ctl:
            pupilJnt = mc.duplicate(eyeJnt)[0]
            mc.hide(pupilJnt)
            pupilJnt = mc.rename(pupilJnt, pupilJnt.replace("_JNT1", "PupilSize_JNT"))
            mc.parent(pupilJnt, eyeJnt)
            mc.move(2, pupilJnt, z=1, r=1)
            mc.setAttr(pupilJnt + ".radius", 0.5)
            eyeSkinning = mc.skinCluster(eyeJnt, "%s_ball_PLY" % side, tsb=1)[0]
            # Eye system ctl:
            eyeSystemCtl, _, eyeSystemGrp = control.buildControl(
                side,
                "eyeSystem",
                "%s_eye_JNT" % side,
                shapeCVs=control.shapes.SQUARE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.move(0, 0, 3, eyeSystemGrp, ws=1, r=1)  # Position at the iris
            mc.rotate(-90, 0, 0, eyeSystemCtl + "Shape*.cv[*]", ws=1, r=1)
            if side == "L":
                mc.move(2, 0, -1, eyeSystemCtl + "Shape*.cv[*]", ws=1, r=1)
            else:
                mc.move(-2, 0, -1, eyeSystemCtl + "Shape*.cv[*]", ws=1, r=1)

            mc.scale(2, 2, 2, eyeSystemCtl + "Shape*.cv[*]")
            mc.parent(eyeSystemGrp, "C_head_CTL")
            mc.parent(eyeJnt, eyeScalingJnt, eyeSystemCtl)

            # Extract twist of the eye in X(up/down), and Y(leftRight) in preparation for
            # plugging it into the lid controls for fleshy eyelids:
            eyeJointTwistInX = twist.extractTwist(eyeJnt, eyeSystemCtl)
            eyeJointTwistInY = twist.extractTwist(eyeJnt, eyeSystemCtl, alignXwith="Y")

            # Eyeball:
            # Rotation ctl:
            rotationCtl, rotationOfs, rotationGrp = control.buildControl(
                side,
                "eyeRotation",
                "%s_eye_JNT" % side,
                shapeCVs="sphere",
                colour=18 if side == "L" else 20,
            )
            mc.rotate(0, 90, 0, rotationCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.move(0, 0, 1, rotationCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.scale(2, 2, 2, rotationCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.parentConstraint(rotationCtl, eyeJnt)
            mc.parent(rotationGrp, eyeSystemCtl)
            # Parent the pupil joint under the rotation Ctl:
            mc.parent(pupilJnt, rotationCtl)
            pupilSizeAttr = attr.addAttr(
                rotationCtl, ln="pupilDilation", at="float", min=-1, max=1, dv=0, k=1
            )
            # Plug the output of the pupilSizeAttr into a MDL which in turn drives the scale of the pupil joint:
            pupilSizeMDL = mc.createNode(
                "multDoubleLinear", n="%s_eyePupilSize_MDV" % side
            )
            mc.setAttr(pupilSizeMDL + ".input1", 2)
            mc.connectAttr(pupilSizeAttr, pupilSizeMDL + ".input2")
            pupilSizeADL = mc.createNode(
                "addDoubleLinear", n="%s_eyePupilSize_ADL" % side
            )
            mc.setAttr(pupilSizeADL + ".input1", 1)
            mc.connectAttr(pupilSizeMDL + ".output", pupilSizeADL + ".input2")
            for v in "xy":
                mc.connectAttr(pupilSizeADL + ".output", pupilJnt + ".s%s" % v)

            attr.lockAndHide(rotationCtl, attrList=[".txyz", ".sxyz"])
            # Create a fleshiness exposed attribute on the eye rotation control
            # which dictates the weight given to the extracted eye joint twist
            # when it is fed to the lid joints rotation:
            fleshinessUpperAttr = attr.addAttr(
                rotationCtl,
                ln="fleshinessUpperLid",
                at="float",
                min=0,
                max=1,
                k=1,
                dv=0.3,
            )
            fleshinessLowerAttr = attr.addAttr(
                rotationCtl,
                ln="fleshinessLowerLid",
                at="float",
                min=0,
                max=1,
                k=1,
                dv=0.2,
            )
            # create a MDV node to turn the value negative for the right eye:
            if side == "R":
                fleshinessAttrNeg = mc.createNode(
                    "multiplyDivide", n="R_fleshinessNegated_MDV"
                )
                mc.connectAttr(fleshinessUpperAttr, fleshinessAttrNeg + ".input1X")
                mc.setAttr(fleshinessAttrNeg + ".input2X", -1)
                mc.connectAttr(fleshinessLowerAttr, fleshinessAttrNeg + ".input1Y")
                mc.setAttr(fleshinessAttrNeg + ".input2Y", -1)
            # Aim Eye control - one created for each side.
            # When building the left side a parent control is built used to move
            #  both aim controls simultaneously:
            if side == "L":
                aimMaskCtl, _, aimMaskGrp = control.buildControl(
                    side, "eyesBothAim", "L_eye_JNT", shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
                )
                mc.move(0, 20, aimMaskGrp, xz=1, ws=1)
                mc.rotate(90, aimMaskCtl + "Shape*.cv[*]", ws=1, r=1)
                mc.scale(4, 3, 3, aimMaskCtl + "Shape*.cv[*]", ws=1, r=1)
                mc.parent(aimMaskGrp, "C_head_CTL")
            # Create an aim control for each eye, parent it under the aim controls
            # mask and create an aim constraint between the eye control and the
            # rotation control's offset transform.
            aimCtl, _, aimGrp = control.buildControl(
                side, "eyeAim", "%s_eye_JNT" % side, colour=18 if side == "L" else 20,
            )
            mc.move(20, aimGrp, z=1, ws=1)
            mc.scale(2, 2, 2, aimCtl + "Shape*.cv[*]")
            mc.parent(aimGrp, aimMaskCtl)
            mc.aimConstraint(
                aimCtl,
                rotationOfs,
                wut="objectrotation",
                u=[0, 1, 0],
                aim=[0, 0, 1],
                wu=[0, 1, 0],
                wuo=aimCtl,
            )
            attr.lockAndHide(aimCtl, attrList=[".rxyz", ".sxyz", ".v"])
            attr.lockAndHide(aimMaskCtl, attrList=[".rxyz", ".sxyz", ".v"])

            # Eyelids:
            # Set correct orientation of the base eyelid joint using the vector going from 1st and Last CV on the lid for X
            # and the mid pont between the two cvs at 0.5 position of the upper and lower lid curves
            # Vectors constructed using points on the curves exctracted from the inner edge of the eyelid:
            numCVsLowerLidCrv = len(mc.ls(lowerLidCRV + ".cv[*]", fl=1))
            if side == "L":
                xVector = vector.getVector(
                    lowerLidCRV + ".cv[0]", lowerLidCRV + ".cv[%i]" % numCVsLowerLidCrv
                )
            else:
                xVector = vector.getVector(
                    lowerLidCRV + ".cv[%i]" % numCVsLowerLidCrv, lowerLidCRV + ".cv[0]"
                )
            innerCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.25, p=True, top=True)
            midCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.5, p=True, top=True)
            outerCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.75, p=True, top=True)
            innerCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.25, p=True, top=True)
            midCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.5, p=True, top=True)
            outerCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.75, p=True, top=True)

            upperLidGuideCVs = [innerCVUpper, midCVUpper, outerCVUpper]
            lowerLidGuideCVs = [innerCVLower, midCVLower, outerCVLower]
            # Calculate the txyz of the point halfway between the mid CVs of the upper and lower curve
            midwayPoint = []
            for upperCvT, lowerCvT in zip(midCVUpper, midCVLower):
                midwayPoint.append((upperCvT + lowerCvT) / 2)
            # Create and position an empty transform at the midway point to be used as an aim guide for the lid joints when shut.

            guideTransform = mc.createNode(
                "transform", name="%s_eyeAimGuide_TRN" % side
            )
            mc.move(midwayPoint[0], midwayPoint[1], midwayPoint[2], guideTransform)

            # Creating a base joint to serve as template for all eyelid Joints
            baseGuideJoint = mc.createNode("joint", name="%s_lidBase_JNT" % side)
            mc.delete(mc.parentConstraint(eyeJnt, baseGuideJoint, mo=0))
            # Eyelid joints will have tX going from right to left along xVector
            # as calculated above, and tZ aimed at the eyeAimGuide transform.
            mc.delete(
                mc.aimConstraint(
                    guideTransform,
                    baseGuideJoint,
                    wut="vector",
                    u=[1, 0, 0],
                    aim=[0, 0, 1],
                    wu=xVector,
                )
            )
            # Freeze the base joint's rotation and scale and parent under the eyeSystem control.
            mc.makeIdentity(baseGuideJoint, a=True)
            mc.parent(baseGuideJoint, eyeSystemCtl)
            # Get the angle between blink line and open eye:
            blinkLineVector = vector.getVector(baseGuideJoint, guideTransform)
            guideTransformOpenEye = mc.createNode(
                "transform", name="%s_eyeOpenAimGuide_TRN" % side
            )
            # The open eye transform is slightly higher in Y than the lid curve in the topology
            # to allow for a complete seal of the lids when skinning
            mc.move(
                midCVUpper[0],
                midCVUpper[1] + 0.05,
                midCVUpper[2],
                guideTransformOpenEye,
            )
            openLidVector = vector.getVector(baseGuideJoint, guideTransformOpenEye)
            # Angle between closed and open lid in radians:
            openLidAngle = om2.MVector.angle(blinkLineVector, openLidVector)
            openLidAngle = float(mc.convertUnit(openLidAngle, f="radian", t="degree"))

            # Lists of the lid base and bind joints respectively:
            (
                upperLidJoints,
                upperLidBindJoints,
                lowerLidJoints,
                lowerLidBindJoints,
                cornerBindJoints,
            ) = (
                [],
                [],
                [],
                [],
                [],
            )
            # Create an inner and outer corner lid joints and controls.
            for corner in ["Inner", "Outer"]:
                cornerGroup = mc.createNode(
                    "transform", name="%s_lid%sCornerSetup_GRP" % (side, corner)
                )
                mc.parent(cornerGroup, eyeSystemCtl, r=1)
                # Duplicate the base joint, create a new joint and parent it underneath,
                # then use the points at the beginning and the end of the
                # upper Lid Curve to position the Bind joint exactly at the
                # corners of the eye.
                cornerJnt = mc.duplicate(baseGuideJoint)[0]
                cornerJnt = mc.rename(
                    cornerJnt,
                    cornerJnt.replace("lidBase_JNT1", "lid%sCorner_JNT" % corner),
                )

                cornerBindJnt = mc.createNode(
                    "joint", name="%s_lid%sCornerBind_JNT" % (side, corner)
                )
                mc.parent(cornerBindJnt, cornerJnt, r=1)
                mc.parent(cornerJnt, cornerGroup)
                cornerBindJoints.append(cornerBindJnt)
                if corner == "Inner":
                    curveLocation = mc.pointOnCurve(upperLidCRV, pr=0, p=True, top=True)
                else:
                    curveLocation = mc.pointOnCurve(upperLidCRV, pr=1, p=True, top=True)
                mc.move(
                    curveLocation[0],
                    curveLocation[1],
                    curveLocation[2],
                    cornerBindJnt,
                    ws=1,
                )
                skin.addToSkinJoints(cornerBindJnt)
                # Create a control for the corner joint, where the translation drives the corner joint rotation.
                ctl, ofs, grp = control.buildControl(
                    side,
                    "lid%sCorner" % corner,
                    guide=cornerBindJnt,
                    shapeCVs=control.shapes.TRIANGLE_SHAPE_CVS,
                )
                if side == "L":
                    if corner == "Inner":
                        mc.rotate(0, 0, 90, ctl + ".cv[*]", os=1)
                    else:
                        mc.rotate(0, 0, -90, ctl + ".cv[*]", os=1)
                else:
                    if corner == "Inner":
                        mc.rotate(0, 0, -90, ctl + ".cv[*]", os=1)
                    else:
                        mc.rotate(0, 0, 90, ctl + ".cv[*]", os=1)

                mc.scale(0.5, 0.5, 0.5, ctl + ".cv[*]")
                mc.move(0, 0, 1, ctl + ".cv[*]", r=1)
                mc.parent(grp, cornerGroup)
                # NOTE: do i need this? # Get radius of eye joint to use for setting .tz of the bind joint:
                # tzOfEyeBindJoint = (mc.getAttr(eyeJnt + ".radius")) * 0.5
                # Take the translate Y and X of the corner controls and use it to drive the rotation in X of the corner joints:
                translateYtoRotateX = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyeLid%sCornerTranslateYtoRotateXJoint_ADA" % (side, corner),
                )
                mc.setAttr(translateYtoRotateX + ".inputA", -4)
                mc.connectAttr(ctl + ".ty", translateYtoRotateX + ".weightA")
                mc.connectAttr(translateYtoRotateX + ".output", cornerJnt + ".rx")
                translateXtoRotateY = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyeLid%sCornerTranslateXtoRotateYJoint_ADA" % (side, corner),
                )
                mc.setAttr(translateXtoRotateY + ".inputA", 4)
                mc.connectAttr(ctl + ".tx", translateXtoRotateY + ".weightA")
                mc.connectAttr(translateXtoRotateY + ".output", cornerJnt + ".ry")
            # Create three base and three bind lid joints for upper and lower respectively
            for lid in ["Upper", "Lower"]:
                if lid == "Upper":
                    cvs = upperLidGuideCVs
                    midCV = midCVUpper
                    openLidAngle = abs(openLidAngle) * -1
                    nodesInput = ".inputA"
                else:
                    cvs = lowerLidGuideCVs
                    midCV = midCVLower
                    openLidAngle = abs(openLidAngle)
                    nodesInput = ".inputB"

                lidBaseJoints, lidBindJoints = [], []

                # Create groups for lid controls and position them in the hierarchy:
                lidGroup = mc.createNode(
                    "transform", name="%s_lid%sSetup_GRP" % (side, lid)
                )
                mc.parent(lidGroup, eyeSystemCtl, r=1)

                # Get radius of eye joint to use for setting .tz of the bind joint:
                tzOfEyeBindJoint = (mc.getAttr(eyeJnt + ".radius")) * 0.5
                # Create three pairs of joints for the respective lid by duplicating
                # the base joint as created above. Position the bind joints at
                # the respective positions as extracted from the lid curves,
                # but keep the tZ of each = to the radius of the eye joint and
                # the base joints rotated so that the bind joints are at the
                # blink line
                for i in range(3):
                    duplicate = mc.duplicate(baseGuideJoint)[0]
                    duplicate = mc.rename(
                        duplicate,
                        duplicate.replace(
                            "lidBase_JNT1", "lid%s%s_JNT" % (lid, str(i).zfill(2))
                        ),
                    )
                    lidBaseJoints.append(duplicate)
                    lidBindJnt = mc.createNode(
                        "joint",
                        name="%s_lid%sBind%s_JNT" % (side, lid, str(i).zfill(2)),
                    )
                    mc.parent(lidBindJnt, duplicate, r=1)
                    mc.setAttr(lidBindJnt + ".tx", cvs[i][0])
                    # NOTE one of these must be useless:
                    mc.setAttr(lidBindJnt + ".tz", tzOfEyeBindJoint)
                    mc.move(
                        cvs[i][0], midwayPoint[1], cvs[i][2], lidBindJnt, ws=1,
                    )
                    mc.setAttr(lidBindJnt + ".tz", tzOfEyeBindJoint)
                    lidBindJoints.append(lidBindJnt)
                    skin.addToSkinJoints(lidBindJnt)

                    # Set to blink line
                    mc.setAttr(lidBindJnt + ".ty", 0)
                    mc.parent(duplicate, lidGroup)
                # Controls to drive the rotation of lid joints via translation:
                # Position the guide transform at the respective mid CV for each lid curve
                mc.move(midCV[0], midCV[1], midCV[2], guideTransformOpenEye)

                ctl, ofs, grp = control.buildControl(
                    side,
                    "lid%s" % lid,
                    guide=guideTransformOpenEye,
                    shapeCVs=control.shapes.TRIANGLE_SHAPE_CVS,
                    colour=18 if side == "L" else 20,
                )
                mc.parent(grp, lidGroup)
                if lid == "Lower":
                    mc.rotate(180, 0, 0, ctl + ".cv[*]")

                mc.scale(0.5, 0.5, 0.5, ctl + ".cv[*]")
                if side == "L":
                    mc.move(0, 0, 1, ctl + ".cv[*]", r=1)
                else:
                    mc.move(0, 0, -1, ctl + ".cv[*]", r=1)
                mc.delete(mc.orientConstraint(lidBindJoints[1], grp, mo=0))
                if side == "R":
                    mc.rotate(0, 180, 0, grp, r=1)
                # Create a Blink Attr on the upper lid control:
                if lid == "Upper":
                    blinkAttr = attr.addAttr(
                        ctl, ln="blink", at="float", min=0, max=10, k=1
                    )
                    blinkRatioNode = mc.createNode(
                        "multDoubleLinear", n="%s_blinkAttrRatio_MDL" % side
                    )
                    mc.setAttr(blinkRatioNode + ".input2", 0.1)
                    mc.connectAttr(blinkAttr, blinkRatioNode + ".input1")
                    # Nodes for the middle set of eye joints which calculate the
                    # angle between the mid joints as driven by ctl.ty, halve that
                    # in preparation for calculating the final rotation value as set
                    # by ctl.ty + the blink attribute for the respective upper and lower
                    # mid lid joints:
                    midJointsAngleBetween = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidMidJointsAngleBetweenFromTY_ADA" % side,
                    )
                    mc.setAttr(
                        midJointsAngleBetween + ".weightB", -1
                    )  # lower lid rotations are positive

                    midJointsAngleBetweenHalved = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidMidJointsAngleBetweenFromTYHalved_ADA" % side,
                    )
                    mc.connectAttr(
                        midJointsAngleBetween + ".output",
                        midJointsAngleBetweenHalved + ".inputA",
                    )
                    mc.setAttr(midJointsAngleBetweenHalved + ".weightA", 0.5)

                    midJointsAngleBetweenHalvedWithBlink = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidMidJointsAngleBetweenFromTYHalvedWithBlink_ADA" % side,
                    )
                    mc.connectAttr(
                        midJointsAngleBetweenHalved + ".output",
                        midJointsAngleBetweenHalvedWithBlink + ".inputA",
                    )
                    mc.connectAttr(
                        blinkRatioNode + ".output",
                        midJointsAngleBetweenHalvedWithBlink + ".weightA",
                    )

                    midJointsAngleBetweenHalvedWithBlinkNegated = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidMidJointsAngleBetweenFromTYHalvedWithBlinkNegated_ADA"
                        % side,
                    )
                    mc.connectAttr(
                        midJointsAngleBetweenHalvedWithBlink + ".output",
                        midJointsAngleBetweenHalvedWithBlinkNegated + ".inputA",
                    )
                    mc.setAttr(
                        midJointsAngleBetweenHalvedWithBlinkNegated + ".weightA", -1
                    )
                    # Angle between ADA nodes for the inner and outer pairs of joints:
                    lidInnerJointsAngleBetween = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidInnerJointsAngleBetweenFromtXY_ADA" % side,
                    )
                    mc.setAttr(lidInnerJointsAngleBetween + ".weightB", -1)
                    lidOuterJointsAngleBetween = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lidOuterJointsAngleBetweenFromtXY_ADA" % side,
                    )
                    mc.setAttr(lidOuterJointsAngleBetween + ".weightB", -1)

                # Fleshiness: Create ADA nodes to add the rotation of the eye to
                # the rotation of the lid joints:
                # The twist around the X axis to be combined with the control translation in Y
                # NOTE: The rotation around the Y axis can be directly plugged
                # into the input of the ADA used for remapping ctl X translation into rotation.
                twistExtractionCombinedWithY = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyelid%sFleshinessEyeRotationAndLidYTranslation_ADA"
                    % (side, lid),
                )
                mc.connectAttr(
                    eyeJointTwistInX, twistExtractionCombinedWithY + ".inputA"
                )
                if lid == "Upper":
                    mc.connectAttr(
                        fleshinessUpperAttr, twistExtractionCombinedWithY + ".weightA"
                    )
                else:
                    mc.connectAttr(
                        fleshinessLowerAttr, twistExtractionCombinedWithY + ".weightA"
                    )

                mc.setAttr(twistExtractionCombinedWithY + ".weightB", 1)

                # Create animblend Nodes that use the translate X and Y of the lid control to drive rotation:
                lidTranslateYtoRotation = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyelid%sTranslateYtoRotateJoint_ADA" % (side, lid),
                )
                mc.connectAttr(ctl + ".ty", lidTranslateYtoRotation + ".weightA")
                mc.setAttr(lidTranslateYtoRotation + ".inputA", -15)
                mc.setAttr(lidTranslateYtoRotation + ".inputB", openLidAngle)
                # Connect to the fleshiness node:
                mc.connectAttr(
                    lidTranslateYtoRotation + ".output",
                    twistExtractionCombinedWithY + ".inputB",
                )
                # conect to the node calculating the angle between mid joints:
                mc.connectAttr(
                    twistExtractionCombinedWithY + ".output",
                    midJointsAngleBetween + nodesInput,
                )

                lidTranslateXtoRotation = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyelid%sTranslateXtoRotateJoint_ADA" % (side, lid),
                )
                mc.connectAttr(ctl + ".tx", lidTranslateXtoRotation + ".weightA")
                if lid == "Upper":
                    mc.setAttr(lidTranslateXtoRotation + ".inputA", 5)
                    if side == "L":
                        mc.connectAttr(
                            fleshinessUpperAttr, lidTranslateXtoRotation + ".weightB"
                        )
                    else:
                        mc.connectAttr(
                            fleshinessAttrNeg + ".outputX",
                            lidTranslateXtoRotation + ".weightB",
                        )
                else:
                    mc.setAttr(lidTranslateXtoRotation + ".inputA", -5)
                    if side == "L":
                        mc.connectAttr(
                            fleshinessLowerAttr, lidTranslateXtoRotation + ".weightB"
                        )
                    else:
                        mc.connectAttr(
                            fleshinessAttrNeg + ".outputY",
                            lidTranslateXtoRotation + ".weightB",
                        )
                mc.connectAttr(eyeJointTwistInY, lidTranslateXtoRotation + ".inputB")

                # negating the tX driven rotation to account for inner/outer
                # joints of the lid to rotate in the oposite direction:

                lidTranslateXtoRotationNegated = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_eyelid%sTranslateXtoRotateJointNegated_ADA" % (side, lid),
                )
                mc.setAttr(lidTranslateXtoRotationNegated + ".weightA", -1)
                mc.connectAttr(
                    lidTranslateXtoRotation + ".output",
                    lidTranslateXtoRotationNegated + ".inputA",
                )

                # Mid final rotation taking in the ctl.ty rotation and the blinked value:
                midJointFinalRotation = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_lid%sMidJointFinalRotation_ADA" % (side, lid),
                )
                mc.connectAttr(
                    twistExtractionCombinedWithY + ".output",
                    midJointFinalRotation + ".inputA",
                )
                if lid == "Upper":
                    mc.connectAttr(
                        midJointsAngleBetweenHalvedWithBlinkNegated + ".output",
                        midJointFinalRotation + ".inputB",
                    )
                else:
                    mc.connectAttr(
                        midJointsAngleBetweenHalvedWithBlink + ".output",
                        midJointFinalRotation + ".inputB",
                    )
                # Getting the angle between the pairs of inner and outer lid
                # joints using the same method as the one used for the mid joints
                #
                for lidCornerJoint in ["Inner", "Outer"]:
                    if lid == "Upper":
                        finalRotationWBValue = -1
                        if lidCornerJoint == "Inner":
                            xyNodeInput = lidTranslateXtoRotation
                            angleBetweenNode = lidInnerJointsAngleBetween

                        elif lidCornerJoint == "Outer":
                            xyNodeInput = lidTranslateXtoRotationNegated
                            angleBetweenNode = lidOuterJointsAngleBetween

                        jointsAngleBetweenHalved = mc.createNode(
                            "animBlendNodeAdditiveDA",
                            n="%s_lid%sJointsAngleBetweenFromTYHalved_ADA"
                            % (side, lidCornerJoint),
                        )
                        mc.connectAttr(
                            angleBetweenNode + ".output",
                            jointsAngleBetweenHalved + ".inputA",
                        )
                        mc.setAttr(jointsAngleBetweenHalved + ".weightA", 0.5)

                        jointsAngleBetweenHalvedWithBlink = mc.createNode(
                            "animBlendNodeAdditiveDA",
                            n="%s_lid%sJointsAngleBetweenFromTYHalvedWithBlink_ADA"
                            % (side, lidCornerJoint),
                        )
                        mc.connectAttr(
                            jointsAngleBetweenHalved + ".output",
                            jointsAngleBetweenHalvedWithBlink + ".inputA",
                        )
                        mc.connectAttr(
                            blinkRatioNode + ".output",
                            jointsAngleBetweenHalvedWithBlink + ".weightA",
                        )
                    elif lid == "Lower":
                        finalRotationWBValue = 1
                        if lidCornerJoint == "Inner":
                            xyNodeInput = lidTranslateXtoRotationNegated
                            angleBetweenNode = lidInnerJointsAngleBetween
                        elif lidCornerJoint == "Outer":
                            xyNodeInput = lidTranslateXtoRotation
                            angleBetweenNode = lidOuterJointsAngleBetween

                    angleBetweenHalvedWithBlink = (
                        "%s_lid%sJointsAngleBetweenFromTYHalvedWithBlink_ADA"
                        % (side, lidCornerJoint)
                    )

                    lidTranslateXYtoRotateJoint = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lid%s%sTranslateXYtyRotateJoint_ADA"
                        % (side, lid, lidCornerJoint),
                    )
                    mc.connectAttr(
                        xyNodeInput + ".output", lidTranslateXYtoRotateJoint + ".inputA"
                    )
                    mc.connectAttr(
                        midJointFinalRotation + ".output",
                        lidTranslateXYtoRotateJoint + ".inputB",
                    )

                    # Connect to the side joints Angle between Node:
                    mc.connectAttr(
                        lidTranslateXYtoRotateJoint + ".output",
                        angleBetweenNode + nodesInput,
                    )

                    lidCornerJointFinalRotation = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lid%s%sJointFinalRotation_ADA"
                        % (side, lid, lidCornerJoint),
                    )
                    mc.setAttr(
                        lidCornerJointFinalRotation + ".weightB", finalRotationWBValue
                    )
                    mc.connectAttr(
                        angleBetweenHalvedWithBlink + ".output",
                        lidCornerJointFinalRotation + ".inputB",
                    )
                    mc.connectAttr(
                        lidTranslateXYtoRotateJoint + ".output",
                        lidCornerJointFinalRotation + ".inputA",
                    )

            # Clamp node for positive angle values to account for lid collision (clamps Values 0-180):
            lidJointsAnglePositiveClamp = mc.createNode(
                "clamp", n="%s_lidJointsAnglePositive_CLP" % side
            )
            lidJointsCollisionAngleHalved = mc.createNode(
                "multiplyDivide", n="%s_lidJointsCollisionAngleHalved_MDV" % side
            )
            for inpRGB, inpXYZ in zip("RGB", "XYZ"):
                mc.setAttr(lidJointsAnglePositiveClamp + ".min%s" % inpRGB, 0)
                mc.setAttr(lidJointsAnglePositiveClamp + ".max%s" % inpRGB, 180)
                mc.setAttr(lidJointsCollisionAngleHalved + ".input2%s" % inpXYZ, 0.5)
                mc.connectAttr(
                    lidJointsAnglePositiveClamp + ".output%s" % inpRGB,
                    lidJointsCollisionAngleHalved + ".input1%s" % inpXYZ,
                )
            # Create an ADA node calculating the final angle between each pair of lid joints after blink:
            for pair, inpRGB in zip(["Inner", "Mid", "Outer"], "RGB"):
                angleDifferenceAfterBlink = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_lid%sJointsAngleDifferenceAfterBlink_ADA" % (side, pair),
                )
                mc.setAttr(angleDifferenceAfterBlink + ".weightB", -1)
                mc.connectAttr(
                    "%s_lidUpper%sJointFinalRotation_ADA.output" % (side, pair),
                    angleDifferenceAfterBlink + ".inputA",
                )
                mc.connectAttr(
                    "%s_lidLower%sJointFinalRotation_ADA.output" % (side, pair),
                    angleDifferenceAfterBlink + ".inputB",
                )

                mc.connectAttr(
                    angleDifferenceAfterBlink + ".output",
                    lidJointsAnglePositiveClamp + ".input%s" % inpRGB,
                )
            # Create an ADA to calculate the ultimate rotation for each final joint
            # considering both the control driven value/ blinked value + the clamp:
            lidSidePairs = ["Inner", "Mid", "Outer"]
            for lid in ["Upper", "Lower"]:
                for pair, inpXYZ, i in zip(lidSidePairs, "XYZ", range(3)):
                    jointRotationWithCollision = mc.createNode(
                        "animBlendNodeAdditiveDA",
                        n="%s_lid%s0%sRotationAndCollision_ADA" % (side, lid, str(i)),
                    )
                    if lid == "Upper":
                        mc.setAttr(jointRotationWithCollision + ".inputA", -1)
                    else:
                        mc.setAttr(jointRotationWithCollision + ".inputA", 1)

                    mc.connectAttr(
                        lidJointsCollisionAngleHalved + ".output%s" % inpXYZ,
                        jointRotationWithCollision + ".weightA",
                    )
                    mc.connectAttr(
                        "%s_lid%s%sJointFinalRotation_ADA.output" % (side, lid, pair),
                        jointRotationWithCollision + ".inputB",
                    )
                    mc.connectAttr(
                        jointRotationWithCollision + ".output",
                        "%s_lid%s0%s_JNT.rx" % (side, lid, str(i)),
                    )
            if DEBUG_MODE == False:
                mc.delete(upperLidCRV)
                mc.delete(lowerLidCRV)
                mc.hide(eyeJnt)
                lidJnts = mc.ls("*lid*JNT")
                for jnt in lidJnts:
                    mc.hide(jnt)
                mc.delete(guideTransform)
                mc.delete(guideTransformOpenEye)
