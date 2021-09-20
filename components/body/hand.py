from maya import cmds as mc
from ...common import attr, control, skin
from ..base import BaseComponent


class HandComponent(BaseComponent):
    def __init__(self, side):
        super(HandComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

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
                skin.addToSkinJoints(jnt)
                if jntChain == thumbJoints:
                    ctl, ctlOfs, ctlGrp = control.buildControl(
                        side, jnt[2:-4], jnt, colour=18 if side == "L" else 20,
                    )
                elif jntChain == pinkyJoints:
                    ctl, ctlOfs, ctlGrp = control.buildControl(
                        side, jnt[2:-4], jnt, colour=18 if side == "L" else 20,
                    )
                else:
                    ctl, ctlOfs, ctlGrp = control.buildControl(
                        side, jnt[2:-4], jnt, colour=18 if side == "L" else 20,
                    )
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
            # Clean up:
            if not DEBUG_MODE:
                for ctl in ctlsList:
                    attr.lockAndHide(ctl, attrList=[".txyz", ".sxyz"])

                for jntChain in fingerJointChains:
                    mc.setAttr(jntChain[0] + ".v", 0)


def curlStretch(side, name, ctlsOfsList):
    # Create and position control:
    curlCtl, _, curlCtllGrp = control.buildControl(
        side, name, ctlsOfsList[0], colour=18 if side == "L" else 20
    )
    mc.move(0, 5, 0, curlCtl + ".cv[*]", r=1)
    mc.rotate(0, 90, 0, curlCtl + ".cv[*]", ws=1, r=1)
    mc.parent(curlCtllGrp, "%s_handBase_TRN" % side)
    # Create attribute and connect it to joints:
    curlAttr = attr.addAttr(curlCtl, ln="curl", at="float", min=-10, max=10, k=1)
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

    mc.setAttr(curlCtl + ".tx", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".ty", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".tz", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".rx", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".ry", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".rz", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".sx", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".sy", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".sz", lock=True, k=False, channelBox=False)
    mc.setAttr(curlCtl + ".v", lock=True, k=False, channelBox=False)
