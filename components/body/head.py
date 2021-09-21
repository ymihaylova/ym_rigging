from maya import cmds as mc
from ...common import attr, control, skin, space
from ..base import BaseComponent


class HeadComponent(BaseComponent):
    def __init__(self, jointChain, jointChainTwist):
        super(HeadComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Create and position Neck Ctl, insert in the hierarchy
        neckBaseCtl, _, neckBaseGrp = control.buildControl("C", "neck", jointChain[0])
        mc.move(0, 0, 1, neckBaseCtl + ".cv[*]", r=1)
        mc.rotate(0, 90, 0, neckBaseCtl + ".cv[*]", r=1)
        mc.scale(6, 6, 6, neckBaseCtl + ".cv[*]")
        mc.parent(neckBaseGrp, "C_chest_CTL")
        mc.parent(jointChain[0], jointChainTwist[0], neckBaseCtl)
        # Add to skinnable joints:
        skin.addToSkinJoints(jointChainTwist[1])
        for joint in jointChain[:-1]:
            skin.addToSkinJoints(joint)
        # Head joint:
        headJnt = mc.duplicate(jointChain[-1], n="C_head_JNT")[0]
        skin.addToSkinJoints(headJnt)
        mc.parent(headJnt, w=1)
        mc.setAttr(headJnt + ".jointOrientX", 0)
        mc.setAttr(headJnt + ".jointOrientY", 0)
        mc.setAttr(headJnt + ".jointOrientZ", 0)
        headCtl, _, headGrp = control.buildControl(
            "C", "head", headJnt, shapeCVs=control.shapes.SQUARE_SHAPE_CVS
        )
        mc.scale(15, 15, 15, headCtl + ".cv[*]")
        mc.parent(headJnt, headCtl)
        mc.parent(headGrp, neckBaseCtl)
        mc.setAttr(headJnt + ".ty", 0.001)
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
                n="C_neck%sIndividualStretch_MDV" % str(jointChain.index(jnt)).zfill(2),
            )
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(
                stretchFactor + ".output.outputX", jointStretch + ".input2.input2X"
            )
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
        # Stretch jointChainTwist:
        jointStretch = mc.createNode(
            "multiplyDivide", n="C_neckWithTwist01IndividualStretch_MDV"
        )
        mc.setAttr(
            jointStretch + ".input1.input1X", mc.getAttr(jointChainTwist[-1] + ".tx")
        )
        mc.connectAttr(
            stretchFactor + ".output.outputX", jointStretch + ".input2.input2X"
        )
        mc.connectAttr(jointStretch + ".output.outputX", jointChainTwist[-1] + ".tx")
        # Orient to parent/world
        space.orientToParent(neckBaseCtl, "C_head_CTL", "C_head_GRP")
        if not DEBUG_MODE:
            attr.lockAndHide(headCtl, attrList=[".sxyz"])
            attr.lockAndHide(neckBaseCtl, attrList=[".sxyz"])
            mc.setAttr(headJnt + ".v", 0)
            mc.setAttr(jointChain[0] + ".v", 0)
            mc.setAttr(jointChainTwist[0] + ".v", 0)
