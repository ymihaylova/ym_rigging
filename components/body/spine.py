from maya import cmds as mc
from ...common import attr, control, skin
from ..base import BaseComponent

class SpineComponent(BaseComponent):
    def __init__(self, jointChain, curve):
        super(SpineComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")
        
        # Clusters and controls:
        spineCtls = []
        spineCtlsGrps = []
        names = ["hips", "spineMid", "chest"]
        shapes = [control.shapes.HIPS_SHAPE_CVS, control.shapes.SPINEMID_SHAPE_CVS, control.shapes.CHEST_SHAPE_CVS]
        hipFkCtl, hipFkGrp = [], []
        spineMidFkCtl, spineMidFkGrp = [], []
        # Root Ctl:
        rootCtl, _, rootGrp = control.buildControl(
            "C",
            "root",
            "C_spine00_JNT",
            shapeCVs=control.shapes.SPINEMID_SHAPE_CVS,
            shapeKnots=control.shapes.KNOTS,
        )
        mc.scale(1.5, 1.5, 1.5, rootCtl + ".cv[*]")
        mc.rotate(0, 0, 0, rootGrp, ws=1)

        for counter, cvIDs in enumerate(["0:1", "2", "3:4"]):
            cvs = curve + ".cv[%s]" % cvIDs

            _, clusterHandle = mc.cluster(
                cvs, name="C_spine%s_CLS" % str(counter).zfill(2)
            )
            ctl, _, group = control.buildControl(
                "C",
                names[counter],
                clusterHandle,
                shapeCVs=shapes[counter],
                shapeKnots=control.shapes.KNOTS,
                degree=3,
            )
            if counter != 1:
                # Create a "FK like" hip control
                if counter == 0:
                    hipFkCtl, _, hipFkGrp = control.buildControl(
                        "C",
                        "hipFk",
                        clusterHandle,
                        shapeCVs=control.shapes.SPINEFK_SHAPE_CVS,
                        shapeKnots=control.shapes.KNOTS,
                        colour=9,
                    )
                # Create a hips/chest joint, reposition to ctl location and parent:
                joint = mc.createNode("joint", name="C_%s_JNT" % names[counter])
                mc.delete(mc.parentConstraint(ctl, joint, mo=0))
                mc.parent(joint, ctl)
            if counter == 1:
                spineMidFkCtl, _, spineMidFkGrp = control.buildControl(
                    "C",
                    "spineMidFk",
                    clusterHandle,
                    shapeCVs=control.shapes.SPINEFK_SHAPE_CVS,
                    shapeKnots=control.shapes.KNOTS,
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
            skin.addToSkinJoints(jnt)
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
        # Housekeeping:
        skin.addToSkinJoints("C_hips_JNT")
        skin.addToSkinJoints("C_chest_JNT")
        if DEBUG_MODE == False:
            mc.hide(jointChain)

        mc.parent("C_root_GRP", "C_top_CTL")
        mc.parent("C_spine_CRV", "C_top_CTL")
        mc.setAttr("C_spine_CRV.inheritsTransform", 0)
        mc.hide("C_spine_CRV")
