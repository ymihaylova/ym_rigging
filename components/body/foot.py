from maya import cmds as mc
from ...common import attr
from ..base import BaseComponent

class FootComponent(BaseComponent):
    def __init__(self, side, footIkCtl):
        super(FootComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Setup foot roll with  Ball Straight and Toe Lift attributes exposed:
        rollAttr = attr.addAttr(footIkCtl, ln="roll", at="doubleAngle", k=1)
        toeLiftAttr = attr.addAttr(
            footIkCtl, ln="toesThreshold", at="doubleAngle", k=1, dv=0.5235988
        )
        ballStraightAttr = attr.addAttr(
            footIkCtl, ln="ballThreshold", at="doubleAngle", k=1, dv=1.047198
        )
        ikCtlChildren = mc.listRelatives(footIkCtl, c=1)
        ikCtlChildren.remove(footIkCtl + "Shape")
        ikCtlChildren = mc.group(ikCtlChildren, n="%s_footIkh_GRP" % side)
        # Banking attr exposed:
        bankAttr = attr.addAttr(footIkCtl, ln="Bank", at="float", k=1, min=-10, max=10)
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
