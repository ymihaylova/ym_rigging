from maya import cmds as mc
from ...common import control
from ..base import BaseComponent


class EyebrowsComponent(BaseComponent):
    def __init__(self, browCurve, orientationLoc, parent="C_head_CTL"):
        super(EyebrowsComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Setup:
        browsCtlsGrp = mc.createNode("transform", n="C_eyebrows_GRP", p=parent)
        # At the moment this assumes that numCvs%2 = 1
        numCvs = mc.getAttr(browCurve + ".spans") + mc.getAttr(browCurve + ".degree")
        midCv = numCvs / 2
        cvOrderRanges = {"L": [0, midCv], "R": [numCvs - 1, midCv]}
        compoundCtlGuide = {"L": midCv / 2, "R": (midCv + 1 + numCvs) / 2}
        # Get CV order list:

        for s in "LR":
            # Compound control set up using a dummy cluster created at the halfway cv for each side of the curve:
            sideGrp = mc.createNode(
                "transform", n=s + "_eyebrowCtls_GRP", p=browsCtlsGrp
            )

            _, dummyCluster = mc.cluster(
                browCurve + ".cv[%s]" % str(compoundCtlGuide[s]), n=s + "_dummy",
            )
            eyebrowCtl, _, eyebrowGrp = control.buildControl(
                s,
                "eyebrowComponent",
                guide=dummyCluster,
                shapeCVs=control.shapes.EYEBROW_SHAPE_CVS,
                colour=18 if s == "L" else 20,
            )
            mc.move(0, 0, 3, eyebrowCtl + ".cv[*]", ws=1, r=1)
            mc.delete(mc.orientConstraint(orientationLoc, eyebrowGrp, mo=0))
            mc.parent(eyebrowGrp, sideGrp)
            mc.delete(dummyCluster)
            # TO DO: Come up with a better way to do this and remove the hardcoding here
            if s == "L":
                cvOrder = ["4:6", "3", "2", "0:1"]
            else:
                cvOrder = ["8:10", "11", "12", "13:14"]

            for counter, cvIds in enumerate(cvOrder):
                cvs = browCurve + ".cv[%s]" % cvIds
                _, clusterHandle = mc.cluster(
                    cvs, name=s + "_eyebrow%s_CLS" % str(counter).zfill(2)
                )
                if counter != len(cvOrder) - 1:
                    ctl, ofs, grp = control.buildControl(
                        s,
                        "eyebrow%s" % str(counter).zfill(2),
                        shapeCVs="sphere",
                        guide=clusterHandle,
                        colour=18 if s == "L" else 20,
                    )
                    mc.delete(mc.orientConstraint(orientationLoc, grp, mo=0))
                    mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
                    mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
                    mc.parent(clusterHandle, ctl)
                    mc.parent(grp, eyebrowCtl)
                    if counter == (len(cvOrder) - 2):
                        mc.pointConstraint(
                            eyebrowCtl, parent, ofs, mo=1, w=0.5,
                        )
                else:
                    mc.parent(clusterHandle, sideGrp)

        # Midbrow Ctl:
        _, clusterHandle = mc.cluster(
            browCurve + ".cv[%s]" % midCv, name="C_eyebrowMid_CLS"
        )
        ctl, ofs, grp = control.buildControl(
            "C", "eyebrowMid", shapeCVs="sphere", guide=clusterHandle
        )
        mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
        mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
        mc.parent(clusterHandle, ctl)
        mc.pointConstraint("L_eyebrow00_CTL", "R_eyebrow00_CTL", ofs, mo=1)
        mc.parent(grp, browsCtlsGrp)

        mc.setAttr(browCurve + ".inheritsTransform", 0)
        # Clean up:

        if not DEBUG_MODE:
            mc.hide(mc.ls("*eyebrow*CLS*"))
            mc.delete(orientationLoc)

        # # Store things that might be needed from outside
        self.browCurve = browCurve
        self.browCtlsGroup = browsCtlsGrp
