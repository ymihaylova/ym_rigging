from maya import cmds as mc
from maya.api import OpenMaya as om2
from ym_rigging.general import ctl_shapes as cs
from ym_rigging.general import general as vs
from ym_rigging.general import parameters as prm

reload(cs)
reload(vs)
reload(prm)

DEBUG_MODE = False


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
            addToSkinJoints(jnt)
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
        addToSkinJoints("C_hips_JNT")
        addToSkinJoints("C_chest_JNT")
        if DEBUG_MODE == False:
            mc.hide(jointChain)


class HeadComponent:
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
        orientToParent("C_chest_CTL", "C_head_CTL", "C_head_GRP")

        if not DEBUG_MODE:
            lockAndHide(headCtl, attrList=[".sxyz"])
            lockAndHide(neckBaseCtl, attrList=[".sxyz"])
            mc.setAttr(headJnt + ".v", 0)
            mc.setAttr(jointChain[0] + ".v", 0)
            mc.setAttr(jointChainTwist[0] + ".v", 0)


class FaceComponent:
    def __init__(self):
        self.buildLips()
        self.buildEyebrows()
        self.buildEyes()

    def buildLips(self):
        # Hierarchy:
        lipsCtlsGrp = mc.createNode("transform", n="C_lipControls_GRP", p="C_head_CTL")
        lips = mc.createNode("transform", n="C_lips_GRP", p="C_head_CTL")
        mc.parent(lipsCtlsGrp, lips)
        # Create a jaw joint ctl, position it in the hierarchy:
        jawJnt = "C_jaw00_JNT"
        jawCtl, _, jawGrp = buildControl(
            "C", "jaw", jawJnt, shapeCVs=cs.L_CLAVICLE_SHAPE_CVS, shapeKnots=cs.KNOTS
        )
        mc.scale(1.5, 1.5, 1.5, jawCtl + ".cv[*]")
        mc.rotate(0, 0, -72.7, jawCtl + ".cv[*]", os=1, fo=1)
        mc.move(0, -12, 15, jawCtl + ".cv[*]", r=1, ws=1)
        mc.parent(jawJnt, jawCtl)
        mc.parent(jawGrp, "C_head_CTL")
        addToSkinJoints(jawJnt)
        # Nurbs surfaces - creating clusters:
        upperLip = "C_lipUpperSfs_NURBS"
        lowerLip = "C_lipLowerSfs_NURBS"
        upperCurve = "C_lipUpper_CRV"
        lowerCurve = "C_lipLower_CRV"
        lipSurfaces = [upperLip, lowerLip]
        lipCurves = [upperCurve, lowerCurve]
        upperLipClusters, lowerLipClusters = [], []
        # Grouping:
        upperLipGrp = mc.group(upperLip, upperCurve, n="C_lipLower_GRP")
        lowerLipGrp = mc.group(lowerLip, lowerCurve, n="C_lipUpper_GRP")
        mc.parent(upperLipGrp, lowerLipGrp, "rig_GRP")
        lipsOrientAttr = vs.addAttr(
            "C_head_CTL",
            ln="lipsOrientationInfluence",
            at="float",
            min=0,
            max=1,
            dv=0.3,
            k=1,
        )
        # Lip corner compound controls:
        # Right corner
        _, dummyCluster = mc.cluster(upperLip + ".cv[0][0:3]")
        leftLipCtl, leftLipOfs, leftLipGrp = buildControl(
            "L",
            "lipCorner",
            guide=dummyCluster,
            shapeCVs=cs.RECTANGLE_SHAPE_CVS,
            colour=18,
        )
        mc.delete(dummyCluster)
        # Left corner:
        _, dummyCluster = mc.cluster(upperLip + ".cv[14][0:3]")
        rightLipCtl, rightLipOfs, rightLipGrp = buildControl(
            "R",
            "lipCorner",
            guide=dummyCluster,
            shapeCVs=cs.RECTANGLE_SHAPE_CVS,
            colour=18,
        )
        mc.delete(dummyCluster)
        for ctl in [rightLipCtl, leftLipCtl]:
            shape = ctl + ".cv[*]"
            mc.rotate(90, 0, 90, shape, ws=1, r=1)
            mc.move(0, 0, 2, shape, ws=1, r=1)
        for grp in [rightLipGrp, leftLipGrp]:
            mc.delete(
                mc.orientConstraint(
                    "C_lipLowerOrientation_LOC", "C_lipUpperOrientation_LOC", grp, mo=0
                )
            )
            mc.parent(grp, lipsCtlsGrp)
        for ofs in [leftLipOfs, rightLipOfs]:
            mc.parentConstraint("C_head_CTL", jawJnt, ofs, mo=1)

        # Lips bind controls set up:
        for surface, curve in zip(lipSurfaces, lipCurves):
            # Create controls, parent constraints and clusters
            if surface == upperLip:
                lipClusters = upperLipClusters
                name = "lipUpper"
                influenceValues = [0.5, 0.3, 0.06, 0.01, 0, 0.01, 0.06, 0.3, 0.5]
                orientationLoc = "C_lipUpperOrientation_LOC"
            else:
                lipClusters = lowerLipClusters
                name = "lipLower"
                orientationLoc = "C_lipLowerOrientation_LOC"
                influenceValues = [0.5, 0.7, 0.94, 0.99, 1, 0.99, 0.94, 0.7, 0.5]
            # Create large lip control:
            _, dummyCluster = mc.cluster(surface + ".cv[5][0:3]")
            largeLipCtl, _, largeLipGrp = buildControl(
                "C",
                name + "Compound",
                guide=dummyCluster,
                shapeCVs=cs.RECTANGLE_SHAPE_CVS,
                colour=20,
            )
            mc.delete(mc.orientConstraint(orientationLoc, largeLipGrp, mo=0))
            mc.rotate(90, 0, 0, largeLipCtl + ".cv[*]", ws=0, r=1)
            if surface == lowerLip:
                mc.parent(largeLipGrp, jawCtl)
                mc.move(0, -1.5, 2, largeLipCtl + ".cv[*]", ws=0, r=1)
            else:
                mc.parent(largeLipGrp, lipsCtlsGrp)
                mc.move(0, 0.5, 2, largeLipCtl + ".cv[*]", ws=0, r=1)
            # mc.scale(2, 1, 1, largeLipCtl + ".cv[*]")
            mc.delete(dummyCluster)

            for rowId in range(1, 10):
                cvs = surface + ".cv[%s][0:3]" % rowId
                if rowId == 1:
                    cvs = surface + ".cv[0:1][0:3]"
                    _, clusterHandle = mc.cluster(
                        cvs, name="C_%s%s_CLS" % (name, str(rowId - 1).zfill(2))
                    )
                elif rowId == 9:
                    cvs = surface + ".cv[9:10][0:3]"
                    _, clusterHandle = mc.cluster(
                        cvs, name="C_%s%s_CLS" % (name, str(rowId - 1).zfill(2))
                    )

                else:
                    _, clusterHandle = mc.cluster(
                        cvs, name="C_%s%s_CLS" % (name, str(rowId - 1).zfill(2))
                    )

                lipClusters.append(clusterHandle)
                if DEBUG_MODE == False:
                    mc.setAttr(clusterHandle + ".v", 0)
                # Build a control per cluster:
                # keep to 1 ctl per corner:

                if surface == lowerLip and rowId == 1:
                    control = "C_lipUpper00_CTL"
                elif surface == lowerLip and rowId == 9:
                    control = "C_lipUpper08_CTL"
                else:
                    control, ofs, grp = buildControl(
                        "C",
                        "%s%s" % (name, str(rowId - 1).zfill(2)),
                        shapeCVs="sphere",
                        guide=clusterHandle,
                    )
                    mc.scale(0.2, 0.2, 0.2, control + "Shape*.cv[*]")
                    influenceAttr = vs.addAttr(
                        control, ln="jawInfluence", at="float", min=0, max=1, k=1
                    )
                    mc.setAttr(influenceAttr, influenceValues[rowId - 1])

                    if control not in ["C_lipUpper00_CTL", "C_lipUpper08_CTL"]:
                        if surface == upperLip:
                            mc.move(0, 0.5, 1, control + "Shape*.cv[*]", ws=1, r=1)
                        else:
                            mc.move(0, -0.4, 1, control + "Shape*.cv[*]", ws=1, r=1)
                    else:
                        mc.move(0, 0, 1, control + "Shape*.cv[*]", ws=1, r=1)
                    # Constrain each control to jaw and head joints and provide control over the influence.

                    mc.delete(mc.orientConstraint(orientationLoc, grp, mo=0))
                    if control in ["C_lipUpper00_CTL", "C_lipUpper08_CTL"]:
                        if control == "C_lipUpper00_CTL":
                            mc.parent(grp, leftLipCtl)
                        else:
                            mc.parent(grp, rightLipCtl)

                    else:
                        if control in ["C_%s07_CTL" % name, "C_%s01_CTL" % name]:
                            if control == "C_%s01_CTL" % name:
                                mc.parent(grp, leftLipCtl)
                                parCon = mc.parentConstraint(
                                    largeLipCtl, leftLipCtl, ofs, mo=1
                                )[0]
                            else:
                                mc.parent(grp, rightLipCtl)
                                parCon = mc.parentConstraint(
                                    largeLipCtl, rightLipCtl, ofs, mo=1
                                )[0]

                        else:
                            if surface == upperLip:
                                parCon = mc.parentConstraint(
                                    largeLipCtl, "C_jaw00_JNT", ofs, mo=1
                                )[0]
                            else:
                                parCon = mc.parentConstraint(
                                    "C_head_CTL", largeLipCtl, ofs, mo=1
                                )[0]

                        mc.connectAttr(influenceAttr, parCon + ".w1")
                        reverse = mc.createNode(
                            "reverse",
                            n="C_%s%sParConReverseInfluence_RV"
                            % (name, str(rowId - 1).zfill(2)),
                        )
                        mc.connectAttr(parCon + ".w1", reverse + ".inputX")
                        mc.connectAttr(reverse + ".outputX", parCon + ".w0")
                    if rowId not in [1, 2, 8, 9]:
                        mc.parent(grp, largeLipCtl)

                mc.parent(clusterHandle, control)
            # Create follicles per CV for each surface:
            curveCVs = mc.ls(curve + ".cv[0:]", fl=True)
            slList = om2.MSelectionList().add(surface)
            mfnSurface = om2.MFnNurbsSurface(slList.getDagPath(0))

            # Duplicate group:
            duplicatesGrp = mc.createNode(
                "transform", n="C_%sBindJntDuplicates_GRP" % name, p=lips
            )
            for cv in curveCVs:
                position = mc.pointPosition(cv)
                pt, u, v = mfnSurface.closestPoint(om2.MPoint(position))
                follicle = vs.createFollicle(surface, parameterU=u, parameterV=v)
                follicle = mc.rename(
                    follicle,
                    "C_%sBind%s_FLC" % (name, str(curveCVs.index(cv)).zfill(2)),
                )

                bindJoint = mc.createNode(
                    "joint",
                    n="C_%sBind%s_JNT" % (name, str(curveCVs.index(cv)).zfill(2)),
                )
                mc.parent(bindJoint, follicle, r=1)
                if surface == upperLip:
                    mc.parent(follicle, upperLipGrp)
                else:
                    mc.parent(follicle, lowerLipGrp)
                # Create a duplicate fpr each bind joint to manage orientation when moving lips:
                duplicate = mc.duplicate(bindJoint)[0]
                duplicate = mc.rename(
                    duplicate, duplicate.replace("_JNT1", "Dupilicate_JNT")
                )
                mc.hide(duplicate)
                mc.parent(duplicate, duplicatesGrp)
                orientCon = mc.orientConstraint(duplicate, follicle, bindJoint, mo=0)[0]
                mc.setAttr(orientCon + ".interpType", 2)
                mc.connectAttr(lipsOrientAttr, orientCon + ".w1")
                reverse = mc.createNode(
                    "reverse", n="C_%sOrientConReverseInfluence_RV" % (bindJoint[2:-4]),
                )
                mc.connectAttr(orientCon + ".w1", reverse + ".inputX")
                mc.connectAttr(reverse + ".outputX", orientCon + ".w0")
                # Set up for skinning:
                addToSkinJoints(bindJoint)

        # Clean Up:
        if DEBUG_MODE == False:
            mc.setAttr("rig_GRP.v", 0)
            mc.setAttr(jawJnt + ".v", 0)
            mc.delete("C_lipUpperOrientation_LOC")
            mc.delete("C_lipLowerOrientation_LOC")

    def buildEyebrows(self):
        # Setup:
        browCurve = "C_eyebrows_CRV"
        brows = "C_eyebrowsProxy_PLY"
        body = "C_body_PLY"
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
        leftEyebrowCtl, _, leftEyebrowGrp = buildControl(
            "L",
            "eyebrowComponent",
            guide=clusterHandle,
            shapeCVs=cs.RECTANGLE_SHAPE_CVS,
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
                ctl, _, grp = buildControl(
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
        rightEyebrowCtl, _, rightEyebrowGrp = buildControl(
            "R",
            "eyebrowComponent",
            guide=clusterHandle,
            shapeCVs=cs.RECTANGLE_SHAPE_CVS,
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
                ctl, _, grp = buildControl(
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
        ctl, ofs, grp = buildControl(
            "C", "eyebrowMid", shapeCVs="sphere", guide=clusterHandle
        )
        mc.scale(0.2, 0.2, 0.2, ctl + "Shape*.cv[*]")
        mc.move(0, 0, 1, ctl + "Shape*.cv[*]", ws=1, r=1)
        mc.parent(clusterHandle, ctl)
        mc.pointConstraint("L_eyebrow00_CTL", "R_eyebrow00_CTL", ofs, mo=1)
        mc.parent(grp, "C_head_CTL")
        mc.hide(clusterHandle)

        # Create wire deformers for C_body_PLY and for the eyebrow proxies:
        bodyWireDefNode, _ = mc.wire(body, w=browCurve, dds=(0, 4.01))
        mc.setAttr(bodyWireDefNode + ".rotation", 0.2)
        mc.deformerWeights(
            "HP_body_wireWeights.xml",
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
            deformer=bodyWireDefNode,
            im=1,
            method="index",
        )
        browsWireDefNode = mc.wire(brows, w=browCurve, dds=(0, 50))[0]
        mc.setAttr(browsWireDefNode + ".rotation", 0.5)
        # Clean up:
        mc.parent(
            browCurve, browCurve + "BaseWire", browCurve + "BaseWire1", "C_head_CTL"
        )
        mc.setAttr(browCurve + ".inheritsTransform", 0)
        mc.setAttr(browCurve + ".tx", 0)
        mc.setAttr(browCurve + ".ty", 0)
        mc.setAttr(browCurve + ".tz", 0)

        mc.parentConstraint("C_head_CTL", brows, mo=1)

        if not DEBUG_MODE:
            mc.hide(browCurve)
            mc.delete(orientationLoc)

    def buildEyes(self):
        for side in "LR":
            # Eyeball controls and constraints:
            upperLidCRV = "%s_lidUpper_CRV" % side
            lowerLidCRV = "%s_lidLower_CRV" % side
            eyeJnt = "%s_eye_JNT" % side
            eyeSkinning = mc.skinCluster(eyeJnt, "%s_ball_PLY" % side, tsb=1)[0]
            # Eye system ctl:
            eyeSystemCtl, _, eyeSystemGrp = buildControl(
                side,
                "eyeSystem",
                "%s_eye_JNT" % side,
                shapeCVs=cs.SQUARE_SHAPE_CVS,
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
            mc.parent(eyeJnt, eyeSystemCtl)
            # Extract twist of the eye in X(up/down), and Y(leftRight) in preparation for
            # plugging it into the lid controls for fleshy eyelids:
            eyeJointTwistInX = vs.extractTwist(eyeJnt, eyeSystemCtl)
            eyeJointTwistInY = vs.extractTwist(eyeJnt, eyeSystemCtl, alignXwith="Y")

            # Eyeball:
            # Rotation ctl:
            rotationCtl, rotationOfs, rotationGrp = buildControl(
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
            lockAndHide(rotationCtl, attrList=[".txyz", ".sxyz"])
            # Create a fleshiness exposed attribute on the eye rotation control
            # which dictates the weight given to the extracted eye joint twist
            # when it is fed to the lid joints rotation:
            fleshinessAttr = vs.addAttr(
                rotationCtl, ln="fleshiness", at="float", min=0, max=1, k=1, dv=0.3
            )
            # create a MDV node to turn the value negative for the right eye:
            if side == "R":
                fleshinessAttrNeg = mc.createNode(
                    "multDoubleLinear", n="R_fleshinessNegated_MDV"
                )
                mc.connectAttr(fleshinessAttr, fleshinessAttrNeg + ".input1")
                mc.setAttr(fleshinessAttrNeg + ".input2", -1)
            # Aim Eye control - one created for each side.
            # When building the left side a parent control is built used to move
            #  both aim controls simultaneously:
            if side == "L":
                aimMaskCtl, _, aimMaskGrp = buildControl(
                    side, "eyesBothAim", "L_eye_JNT", shapeCVs=cs.RECTANGLE_SHAPE_CVS,
                )
                mc.move(0, 20, aimMaskGrp, xz=1, ws=1)
                mc.rotate(90, aimMaskCtl + "Shape*.cv[*]", ws=1, r=1)
                mc.scale(4, 3, 3, aimMaskCtl + "Shape*.cv[*]", ws=1, r=1)
                mc.parent(aimMaskGrp, eyeSystemCtl)
            # Create an aim control for each eye, parent it under the aim controls
            # mask and create an aim constraint between the eye control and the
            # rotation control's offset transform.
            aimCtl, _, aimGrp = buildControl(
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
            lockAndHide(aimCtl, attrList=[".rxyz", ".sxyz", ".v"])
            lockAndHide(aimMaskCtl, attrList=[".rxyz", ".sxyz", ".v"])

            # Eyelids:
            # Set correct orientation of the base eyelid joint using the vector going from 1st and Last CV on the lid for X
            # and the mid pont between the two cvs at 0.5 position of the upper and lower lid curves
            # Vectors constructed using points on the curves exctracted from the inner edge of the eyelid:
            xVector = vs.getVector(lowerLidCRV + ".cv[0]", lowerLidCRV + ".cv[-1]")
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
            blinkLineVector = vs.getVector(baseGuideJoint, guideTransform)
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
            openLidVector = vs.getVector(baseGuideJoint, guideTransformOpenEye)
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
                addToSkinJoints(cornerBindJnt)
                # Create a control for the corner joint, where the translation drives the corner joint rotation.
                ctl, ofs, grp = buildControl(
                    side,
                    "lid%sCorner" % corner,
                    guide=cornerBindJnt,
                    shapeCVs=cs.TRIANGLE_SHAPE_CVS,
                )
                if side == "L":
                    if corner == "Inner":
                        mc.rotate(0, 0, -35, ctl + ".cv[*]", os=1)
                    else:
                        mc.rotate(0, 0, 35, ctl + ".cv[*]", os=1)
                else:
                    if corner == "Inner":
                        mc.rotate(0, 0, 35, ctl + ".cv[*]", os=1)
                    else:
                        mc.rotate(0, 0, -35, ctl + ".cv[*]", os=1)

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
                    addToSkinJoints(lidBindJnt)

                    # Set to blink line
                    mc.setAttr(lidBindJnt + ".ty", 0)
                    mc.parent(duplicate, lidGroup)
                # Controls to drive the rotation of lid joints via translation:
                # Position the guide transform at the respective mid CV for each lid curve
                mc.move(midCV[0], midCV[1], midCV[2], guideTransformOpenEye)

                ctl, ofs, grp = buildControl(
                    side,
                    "lid%s" % lid,
                    guide=guideTransformOpenEye,
                    shapeCVs=cs.TRIANGLE_SHAPE_CVS,
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
                    blinkAttr = vs.addAttr(
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
                mc.connectAttr(
                    fleshinessAttr, twistExtractionCombinedWithY + ".weightA"
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
                else:
                    mc.setAttr(lidTranslateXtoRotation + ".inputA", -5)
                mc.connectAttr(eyeJointTwistInY, lidTranslateXtoRotation + ".inputB")
                if side == "L":
                    mc.connectAttr(fleshinessAttr, lidTranslateXtoRotation + ".weightB")
                else:
                    mc.connectAttr(
                        fleshinessAttrNeg + ".output",
                        lidTranslateXtoRotation + ".weightB",
                    )
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
            # Clean up:
            if not DEBUG_MODE:
                for ctl in ctlsList:
                    lockAndHide(ctl, attrList=[".txyz", ".sxyz"])

                for jntChain in fingerJointChains:
                    mc.setAttr(jntChain[0] + ".v", 0)


def curlStretch(side, name, ctlsOfsList):
    # Create and position control:
    curlCtl, _, curlCtllGrp = buildControl(side, name, ctlsOfsList[0])
    mc.move(0, 5, 0, curlCtl + ".cv[*]", r=1)
    mc.rotate(0, 90, 0, curlCtl + ".cv[*]", ws=1, r=1)
    mc.parent(curlCtllGrp, "%s_handBase_TRN" % side)
    # Create attribute and connect it to joints:
    curlAttr = vs.addAttr(curlCtl, ln="curl", at="float", min=-10, max=10, k=1)
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


def buildControl(
    side, name, guide=None, shapeCVs=[], shapeKnots=None, degree=1, colour=17
):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    elif shapeCVs == "locator":
        control = mc.spaceLocator()[0]
    elif shapeCVs == "sphere":
        control = mc.circle(constructionHistory=0)[0]
        shape2 = mc.circle(constructionHistory=0)[0]
        shape3 = mc.circle(constructionHistory=0)[0]
        mc.parent(shape2[:-1] + "Shape2", control, s=1, r=1)
        mc.parent(shape3[:-1] + "Shape3", control, s=1, r=1)
        mc.rotate(0, 90, 0, control[:-1] + "Shape1.cv[*]", ws=1)
        mc.rotate(90, 0, 0, control[:-1] + "Shape2.cv[*]", ws=1)
        mc.delete(shape2, shape3)
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
        if jntId == 0:
            fkCtl, fkCtlOfs, fkCtlGrp = buildControl(
                side,
                "%s%sFk" % (name, str(jntId).zfill(2)),
                blendChain[jntId],
                shapeCVs=cs.L_CLAVICLE_SHAPE_CVS,
                shapeKnots=cs.KNOTS,
                colour=18 if side == "L" else 20,
            )
        else:

            fkCtl, fkCtlOfs, fkCtlGrp = buildControl(
                side,
                "%s%sFk" % (name, str(jntId).zfill(2)),
                blendChain[jntId],
                colour=18 if side == "L" else 20,
            )
        # Clean up attribute visibility:
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
        orientToParent(fkCtlsList[0], fkCtlsList[1], fkCtlsGrpList[1])
    # Create IK copy of the blend chain
    ikChain = mc.duplicate("%s_%s00_JNT" % (side, name), renameChildren=1)
    renamedIkChain = []
    for jnt in ikChain:
        renamedIkChain.append(mc.rename(jnt, jnt.replace("_JNT", "Ik_JNT")[:-1]))

    ikChain = renamedIkChain

    limbGrp = mc.group(blendChain[0], ikChain[0])
    limbGrp = mc.rename(limbGrp, "%s_%s_GRP" % (side, name))
    mc.parent(limbGrp, fkCtlsList[0])

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
        mc.parent(ikBaseCtlGrp, fkCtlsList[0])
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
        for ctl in fkCtlsList:
            lockAndHide(fkCtl, [".txyz", ".sxyz"])
        lockAndHide(ikBaseCtl, [".rxyz", ".sxyz"])
        lockAndHide(ikCtl, [".sxyz"])

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
    ikFkSwitchAttr = vs.addAttr(
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


def footRollSetup(side, footIkCtl):
    # Setup foot roll with  Ball Straight and Toe Lift attributes exposed:
    rollAttr = vs.addAttr(footIkCtl, ln="roll", at="doubleAngle", k=1)
    toeLiftAttr = vs.addAttr(
        footIkCtl, ln="toeLift", at="doubleAngle", k=1, dv=0.5235988
    )
    ballStraightAttr = vs.addAttr(
        footIkCtl, ln="ballStraight", at="doubleAngle", k=1, dv=1.047198
    )
    ikCtlChildren = mc.listRelatives(footIkCtl, c=1)
    ikCtlChildren.remove(footIkCtl + "Shape")
    ikCtlChildren = mc.group(ikCtlChildren, n="%s_footIkh_GRP" % side)
    # Banking attr exposed:
    bankAttr = vs.addAttr(footIkCtl, ln="Bank", at="float", k=1, min=-10, max=10)
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
    jointMessageAttr = vs.addAttr(joint, ln="skinJoint", at="message")
    mc.connectAttr(skinJointsMessageAttr, jointMessageAttr)


def orientToParent(parentCtl, drivenCtl, drivenGrp, worldControl="C_harry_CTL"):
    # Create an attribute for the control
    orientAttr = vs.addAttr(
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


def buildBendyLimbs(side, limb, elbowKneeBendSharpness=2, wristAnkleBendSharpness=3):
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
    if not DEBUG_MODE:
        lockAndHide(upperCtl, [".rxyz", ".sxyz"])
        lockAndHide(lowerCtl, [".rxyz", ".sxyz"])

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
        n="%s_%sSurfase_NRB" % (side, limb),
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
        dummyTransform = mc.createNode("transform", parent="%s_arm03_JNT" % side)
        _, dummyCluster = mc.cluster(nurbsSfs + ".cv[%s][0:1]" % dummyClusterCVs)
        mc.parent(dummyCluster, dummyTransform)
        mc.rotate(90, 0, 0, dummyTransform)
        mc.delete(nurbsSfs, ch=1)
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
    for counter, cvIDs in enumerate(cvOrder):
        cvs = nurbsSfs + ".cv[%s][0:1]" % cvIDs

        _, clusterHandle = mc.cluster(
            cvs, name="%s_%sNURBS%s_CLS" % (side, limb, str(counter).zfill(2))
        )
        curveClusters.append(clusterHandle)
        mc.parent(clusterHandle, clusterParents[counter])
        if DEBUG_MODE == False:
            mc.setAttr(clusterHandle + ".visibility", 0)

    createBindJoints(side, limb, nurbsSfs)

    if DEBUG_MODE == False:
        mc.setAttr(nurbsSfs + ".v", 0)


def createBindJoints(side, limb, nurbsSfs):
    grp = mc.createNode("transform", n="%s_%sBindFlcJoint_GRP" % (side, limb))
    lockAndHide(grp)

    mc.parent(grp, "rig_GRP")
    paramUList = []
    follicle = None
    folliclesList = []
    if limb == "arm":
        paramUList = prm.PARAM_U_ARMS
    else:
        paramUList = prm.PARAM_U_LEGS

    for paramU in paramUList:
        follicle = vs.createFollicle(nurbsSfs, parameterU=paramU, parameterV=0.5)
        follicle = mc.rename(
            follicle,
            "%s_%sBind%s_FLC" % (side, limb, str(paramUList.index(paramU)).zfill(2)),
        )
        folliclesList.append(follicle)
        mc.parent(follicle, grp)

        bindJoint = mc.createNode(
            "joint",
            name="%s_%sBind%s_JNT"
            % (side, limb, str(paramUList.index(paramU)).zfill(2)),
        )
        mc.parent(bindJoint, follicle, r=1)
        addToSkinJoints(bindJoint)
        if DEBUG_MODE == False:
            mc.setAttr(bindJoint + ".v", 0)
            mc.setAttr(follicle + ".v", 0)


def lockAndHide(
    node, attrList=[".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"]
):
    attrList = attrList
    if ".txyz" in attrList:
        attrList.remove(".txyz")
        attrList.append(".tx")
        attrList.append(".ty")
        attrList.append(".tz")

    if ".rxyz" in attrList:
        attrList.remove(".rxyz")
        attrList.append(".rx")
        attrList.append(".ry")
        attrList.append(".rz")
    if ".sxyz" in attrList:
        attrList.remove(".sxyz")
        attrList.append(".sx")
        attrList.append(".sy")
        attrList.append(".sz")
    for attr in attrList:
        mc.setAttr(node + attr, lock=True, k=False, channelBox=False)


def main():
    # Create a new file and import model and guides
    mc.file(new=1, force=1)
    mc.file(
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_body.ma", i=1
    )
    mc.file(
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_guides.ma",
        i=1,
    )

    # Housekeeping setup:q
    harryCtl, _, _ = buildControl("C", "harry", shapeCVs=cs.SQUARE_SHAPE_CVS)
    mc.scale(15, 15, 15, harryCtl + ".cv[*]")
    harryCtlSkinJoints = vs.addAttr(harryCtl, ln="skinJoints", at="message")
    ctlsGrp = mc.group(em=1)
    ctlsGrp = mc.rename(ctlsGrp, "ctls_GRP")
    rigGrp = mc.group(em=1)
    rigGrp = mc.rename(rigGrp, "rig_GRP")

    # Build spine
    spine = SpineComponent(mc.ls("C_spine??_JNT"), "C_spine_CRV")
    head = HeadComponent(mc.ls("C_neck??_JNT"), mc.ls("C_neckWithTwist??_JNT"))
    face = FaceComponent()

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
        kneePoleVectorPos = vs.getIkhPoleVecPos(footIkHandle)
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
        # Clean up:
        if not DEBUG_MODE:
            lockAndHide(kneePoleVectorCtl, [".rxyz"])

        # Skin and import weights for shoes and socks
        sockSkinJoints = [
            "%s_legBind12_JNT" % side,
            "%s_legBind13_JNT" % side,
            "%s_legBind14_JNT" % side,
            "%s_legBind16_JNT" % side,
            "%s_leg03_JNT" % side,
        ]
        shoeSkinJoints = ["%s_legBind16_JNT" % side, "%s_leg03_JNT" % side]
        sock = "%s_shoeSock_PLY" % side
        shoe = "%s_shoe_PLY" % side
        skinClusterSock = mc.skinCluster(sockSkinJoints, sock, tsb=1)[0]
        skinClusterShoe = mc.skinCluster(shoeSkinJoints, shoe, tsb=1)[0]
        mc.deformerWeights(
            "%s_sock_skinWeights.xml" % side,
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
            deformer=skinClusterSock,
            im=1,
            method="index",
        )
        # mc.skinCluster(skinClusterSock, e=1, forceNormalizeWeights=True)
        mc.deformerWeights(
            "%s_shoe_skinWeights.xml" % side,
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
            deformer=skinClusterShoe,
            im=1,
            method="index",
        )
        mc.skinCluster(skinClusterShoe, e=1, forceNormalizeWeights=True)

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
        elbowPoleVectorPos = vs.getIkhPoleVecPos(wristIkHandle)
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
            fkCtlsGrpList[1:],
        )
        # Build Hand structure and controls:
        hand = HandComponent(side)
        buildBendyLimbs(side, "arm")
        # Clean up:
        if not DEBUG_MODE:
            lockAndHide(elbowPoleVectorCtl, [".rxyz"])

    # Housekeeping:
    groups = mc.ls("*GRP")
    offsets = mc.ls("*OFS")
    if DEBUG_MODE == False:
        for grp in groups:
            lockAndHide(grp)
        for ofs in offsets:
            lockAndHide(ofs)
    # Basic skin geometry:
    skinJoints = mc.listConnections("C_harry_CTL.skinJoints")
    body = "C_body_PLY"
    skinCluster = mc.skinCluster(skinJoints, body, tsb=1)[0]
    mc.setAttr(skinCluster + ".skinningMethod", 2)
    # Ensuring deformers are in the correct order:
    mc.reorderDeformers("wire1", skinCluster, body)

    mc.deformerWeights(
        "body_skin_weights_02.xml",
        path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\sourceimages",
        deformer=skinCluster,
        im=1,
        method="index",
    )
    mc.skinCluster(skinCluster, e=1, forceNormalizeWeights=True)
    # Skin gums, teeth, tongue:
    mc.skinCluster("C_head_JNT", "C_upperTeeth_PLY", tsb=1)
    mc.skinCluster("C_head_JNT", "C_upperGums_PLY", tsb=1)
    mc.skinCluster("C_jaw00_JNT", "C_lowerTeeth_PLY", tsb=1)
    mc.skinCluster("C_jaw00_JNT", "C_lowerGums_PLY", tsb=1)
    mc.skinCluster("C_jaw00_JNT", "C_tongue_PLY", tsb=1)

    # Geometry in hierarchy
    mc.setAttr("C_geometry_GRP.inheritsTransform", 0)
    mc.parent("C_geometry_GRP", harryCtl)
    # Make geometry unselectble:
    referenceGeoAttr = vs.addAttr(
        harryCtl, ln="referenceGeo", at="long", min=0, max=1, dv=1, k=1
    )
    mc.connectAttr(referenceGeoAttr, "C_geometry_GRP.overrideEnabled")
    mc.setAttr("C_geometry_GRP.overrideDisplayType", 2)
    # Spine curve and root in hierarchy
    mc.parent("C_root_GRP", harryCtl)
    mc.parent("C_spine_CRV", harryCtl)
    mc.setAttr("C_spine_CRV.inheritsTransform", 0)
    mc.viewFit("C_head_CTL")


main()
