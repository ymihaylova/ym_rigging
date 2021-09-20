from maya import cmds as mc
from ...common import control
from ..base import BaseComponent

class EyebrowsComponent(BaseComponent):
    def __init__(self):
        super(EyebrowsComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Setup:
        browCurve = "C_eyebrows_CRV"
        orientationLoc = "C_eyebrowOrientation_LTR"
        leftBrowCtlsGrp = mc.createNode(
            "transform", n="L_eyebrowCtls_GRP", p="C_head_CTL"
        )
        rightBrowCtlsGrp = mc.createNode(
            "transform", n="R_eyebrowCtls_GRP", p="C_head_CTL"
        )
        # Build clusters and controls for eyebrow curve:
        cvOrderLeft = ["4:6", "3", "2", "0:1"]
        midwayCv = "7"
        cvOrderRight = ["8:10", "11", "12", "13:14"]
        # Left eyebrow:
        # Left eyebrow primary layer control set up:
        _, clusterHandle = mc.cluster(
            browCurve + ".cv[3]", name="L_eyebrowComponent_CLS"
        )
        leftEyebrowCtl, _, leftEyebrowGrp = control.buildControl(
            "L",
            "eyebrowComponent",
            guide=clusterHandle,
            shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
            colour=18,
        )
        mc.delete(mc.orientConstraint(orientationLoc, leftEyebrowGrp, mo=0))
        mc.parent(leftEyebrowGrp, leftBrowCtlsGrp)
        mc.rotate(90, 0, 0, leftEyebrowCtl + ".cv[*]", ws=0, r=1)
        mc.move(-0.5, -0.5, 3, leftEyebrowCtl + ".cv[*]", ws=0, r=1)
        mc.scale(2, 1, 1, leftEyebrowCtl + ".cv[*]")
        mc.delete(clusterHandle)
        # Left eyebrow secondary layer controls:
        for counter, cvIds in enumerate(cvOrderLeft):
            cvs = browCurve + ".cv[%s]" % cvIds
            _, clusterHandle = mc.cluster(
                cvs, name="L_eyebrow%s_CLS" % str(counter).zfill(2)
            )
            if cvIds != "0:1":
                ctl, _, grp = control.buildControl(
                    "L",
                    "eyebrow%s" % str(counter).zfill(2),
                    shapeCVs="sphere",
                    guide=clusterHandle,
                    colour=18,
                )
                mc.delete(mc.orientConstraint(orientationLoc, grp, mo=0))
                mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
                mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
                mc.parent(clusterHandle, ctl)
                mc.parent(grp, leftEyebrowCtl)
                mc.hide(clusterHandle)
            else:
                mc.parent(clusterHandle, leftBrowCtlsGrp)
                mc.hide(clusterHandle)
        # Right eyebrow:
        # Right eyebrow primary layer control set up:
        _, clusterHandle = mc.cluster(
            browCurve + ".cv[11]", name="R_eyebrowComponent_CLS"
        )
        rightEyebrowCtl, _, rightEyebrowGrp = control.buildControl(
            "R",
            "eyebrowComponent",
            guide=clusterHandle,
            shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
            colour=20,
        )
        mc.delete(mc.orientConstraint(orientationLoc, rightEyebrowGrp, mo=0))
        mc.parent(rightEyebrowGrp, rightBrowCtlsGrp)
        mc.rotate(90, 0, 0, rightEyebrowCtl + ".cv[*]", ws=0, r=1)
        mc.move(0.5, -0.5, 3, rightEyebrowCtl + ".cv[*]", ws=0, r=1)
        mc.scale(2, 1, 1, rightEyebrowCtl + ".cv[*]")
        mc.delete(clusterHandle)

        for counter, cvIds in enumerate(cvOrderRight):
            cvs = browCurve + ".cv[%s]" % cvIds
            _, clusterHandle = mc.cluster(
                cvs, name="R_eyebrow%s_CLS" % str(counter).zfill(2)
            )
            if cvIds != "13:14":
                ctl, _, grp = control.buildControl(
                    "R",
                    "eyebrow%s" % str(counter).zfill(2),
                    shapeCVs="sphere",
                    guide=clusterHandle,
                    colour=20,
                )
                mc.delete(mc.orientConstraint(orientationLoc, grp, mo=0))
                mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
                mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
                mc.parent(clusterHandle, ctl)
                mc.parent(grp, rightEyebrowCtl)
                mc.hide(clusterHandle)
            else:
                mc.parent(clusterHandle, rightBrowCtlsGrp)
                mc.hide(clusterHandle)

        # Midbrow Ctl:
        _, clusterHandle = mc.cluster(
            browCurve + ".cv[%s]" % midwayCv, name="C_eyebrowMid_CLS"
        )
        ctl, ofs, grp = control.buildControl(
            "C", "eyebrowMid", shapeCVs="sphere", guide=clusterHandle
        )
        mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
        mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
        mc.parent(clusterHandle, ctl)
        mc.pointConstraint("L_eyebrow00_CTL", "R_eyebrow00_CTL", ofs, mo=1)
        mc.parent(grp, "C_head_CTL")
        mc.hide(clusterHandle)

        mc.setAttr(browCurve + ".inheritsTransform", 0)
        mc.setAttr(browCurve + ".tx", 0)
        mc.setAttr(browCurve + ".ty", 0)
        mc.setAttr(browCurve + ".tz", 0)

        # Point constrain the end secondary layer control to the eyebrow
        # compound joint and the head control for more pleasing behaviour when
        # brow is lowered:
        for side in "LR":
            mc.pointConstraint(
                "%s_eyebrowComponent_CTL" % side,
                "C_head_CTL",
                "%s_eyebrow02_OFS" % side,
                mo=1,
                w=0.5,
            )

        if not DEBUG_MODE:
            mc.hide(browCurve)
            mc.delete(orientationLoc)

        # Store things that might be needed from outside
        self.browCurve = browCurve
