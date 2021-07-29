from maya import cmds as mc
from maya.api import OpenMaya as om2
from ym_rigging.general import ctl_shapes as cs
from ym_rigging.general import general as gen
from ym_rigging.general import parameters as prm

reload(cs)
reload(gen)
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
            lockAndHide(headCtl, ".sxyz")
            lockAndHide(neckBaseCtl, ".sxyz")
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
        lipsOrientAttr = gen.addAttr(
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
                    influenceAttr = gen.addAttr(
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
                follicle = gen.createFollicle(surface, parameterU=u, parameterV=v)
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
                shapeCVs="sphere",
                colour=18 if side == "L" else 20,
            )
            mc.move(0, 0, 3, eyeSystemGrp, ws=1, r=1)
            mc.move(0, 0, 1, eyeSystemCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.parent(eyeSystemGrp, "C_head_CTL")
            mc.parent(eyeJnt, eyeSystemCtl)
            # Rotation ctl:
            rotationCtl, rotationOfs, rotationGrp = buildControl(
                side,
                "eyeRotation",
                "%s_eye_JNT" % side,
                shapeCVs="sphere",
                colour=18 if side == "L" else 20,
            )
            mc.move(0, 0, 4, rotationCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.scale(2, 2, 2, rotationCtl + "Shape*.cv[*]", ws=1, r=1)
            mc.parentConstraint(rotationCtl, eyeJnt)
            mc.scaleConstraint(rotationCtl, eyeJnt)
            lockAndHide(rotationCtl, attrList=".txyz")
            lockAndHide(rotationCtl, attrList=".sxyz")
            # Aim ctl:
            aimCtl, _, aimGrp = buildControl(
                side,
                "eyeAim",
                "%s_eye_JNT" % side,
                shapeCVs=cs.DIAMOND_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.move(0, 0, 15, aimGrp, ws=1, r=1)
            mc.aimConstraint(
                aimCtl,
                rotationOfs,
                wut="objectrotation",
                u=[0, 1, 0],
                aim=[0, 0, 1],
                wu=[0, 1, 0],
                wuo=aimCtl,
            )
            mc.parent(aimGrp, eyeSystemCtl)
            mc.parent(rotationGrp, eyeSystemCtl)
            # Eyelids:
            # Set correct orientation of the base eyelid joint using the vector going from 1st and Last CV on the lid for X
            # and the mid pont between the two cvs at 0.5 position of the upper and lower lid curves
            xVector = gen.getVector(lowerLidCRV + ".cv[0]", lowerLidCRV + ".cv[-1]")
            innerCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.25, p=True, top=True)
            midCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.5, p=True, top=True)
            outerCVUpper = mc.pointOnCurve(upperLidCRV, pr=0.75, p=True, top=True)
            innerCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.25, p=True, top=True)
            midCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.5, p=True, top=True)
            outerCVLower = mc.pointOnCurve(lowerLidCRV, pr=0.75, p=True, top=True)
            midwayPoint = [
                (midCVUpper[0] + midCVLower[0]) / 2,
                (midCVUpper[1] + midCVLower[1]) / 2,
                (midCVUpper[2] + midCVLower[2]) / 2,
            ]
            guideTransform = mc.createNode(
                "transform", name="%s_eyeAimGuide_TRN" % side
            )
            mc.move(midwayPoint[0], midwayPoint[1], midwayPoint[2], guideTransform)
            # Creating a base joint to serve as template for all eyelid Joints
            baseGuideJoint = mc.createNode("joint", name="%s_lidBase_JNT" % side)
            mc.delete(mc.parentConstraint(eyeJnt, baseGuideJoint, mo=0))
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
            # mc.delete(guideTransform)
            mc.makeIdentity(baseGuideJoint, a=True)
            mc.parent(baseGuideJoint, eyeJnt)
            # Create three base and three bind lid joints for upper and lower respectively
            upperLidJoints, upperLidBindJoints, lowerLidJoints, lowerLidBindJoints = (
                [],
                [],
                [],
                [],
            )
            upperCVs = [innerCVUpper, midCVUpper, outerCVUpper]
            lowerCVs = [innerCVLower, midCVLower, outerCVLower]
            # Create groups for lid controls and position them in the hierarchy:
            upperLidGroup = mc.createNode(
                "transform", name="%s_lidUpperSetup_GRP" % side
            )
            mc.parent(upperLidGroup, eyeSystemCtl, r=1)
            lowerLidGroup = mc.createNode(
                "transform", name="%s_lidLowerSetup_GRP" % side
            )
            mc.parent(lowerLidGroup, eyeSystemCtl, r=1)
            innerLidCornerGroup = mc.createNode(
                "transform", name="%s_lidInnerCornerSetup_GRP" % side
            )
            mc.parent(innerLidCornerGroup, eyeSystemCtl, r=1)
            outerLidCornerGroup = mc.createNode(
                "transform", name="%s_lidInnerCornerSetup_GRP" % side
            )
            mc.parent(outerLidCornerGroup, eyeSystemCtl, r=1)
            # Inner and Outer corner joints:
            cornerJoints = []
            innerLidCornerJnt = mc.duplicate(baseGuideJoint)[0]
            innerLidCornerJnt = mc.rename(
                innerLidCornerJnt,
                innerLidCornerJnt.replace("lidBase_JNT1", "lidInnerCorner_JNT"),
            )

            innerLidCornerBindJnt = mc.createNode(
                "joint", name="%s_lidInnerCornerBind_JNT" % side
            )
            mc.parent(innerLidCornerBindJnt, innerLidCornerJnt, r=1)
            curveLocation = mc.pointOnCurve(upperLidCRV, pr=0, p=True, top=True)
            cornerJoints.append(innerLidCornerBindJnt)
            mc.move(
                curveLocation[0],
                curveLocation[1],
                curveLocation[2],
                innerLidCornerBindJnt,
                ws=1,
            )
            outerLidCornerJnt = mc.duplicate(baseGuideJoint)[0]
            outerLidCornerJnt = mc.rename(
                outerLidCornerJnt,
                outerLidCornerJnt.replace("lidBase_JNT1", "lidOuterCorner_JNT"),
            )

            outerLidCornerBindJnt = mc.createNode(
                "joint", name="%s_lidOuterCornerBind_JNT" % side
            )
            mc.parent(outerLidCornerBindJnt, outerLidCornerJnt, r=1)
            curveLocation = mc.pointOnCurve(upperLidCRV, pr=1, p=True, top=True)
            mc.move(
                curveLocation[0],
                curveLocation[1],
                curveLocation[2],
                outerLidCornerBindJnt,
                ws=1,
            )
            cornerJoints.append(outerLidCornerBindJnt)
            for joint in cornerJoints:
                ctl, ofs, grp = buildControl(
                    side,
                    "%s" % joint[2:-8],
                    guide=joint,
                    shapeCVs=cs.TRIANGLE_SHAPE_CVS,
                )
                mc.rotate(90, 0, 0, ctl + ".cv[*]", ws=1)
                mc.scale(0.5, 0.5, 0.5, ctl + ".cv[*]")
                mc.move(0, 0, 1, ctl + ".cv[*]", r=1)
                mc.parent(grp, eyeSystemCtl)
            # Get radius of eye joint to use for setting .tz of the bind joint:
            tzOfEyeBindJoint = (mc.getAttr(eyeJnt + ".radius")) * 0.5
            print(tzOfEyeBindJoint)
            for i in range(3):
                # Upper lid joints and controls
                upperDuplicate = mc.duplicate(baseGuideJoint)[0]
                upperDuplicate = mc.rename(
                    upperDuplicate,
                    upperDuplicate.replace(
                        "lidBase_JNT1", "lidUpper%s_JNT" % str(i).zfill(2)
                    ),
                )
                upperLidJoints.append(upperDuplicate)
                upperLidBindJnt = mc.createNode(
                    "joint", name="%s_lidUpperBind%s_JNT" % (side, str(i).zfill(2))
                )
                mc.parent(upperLidBindJnt, upperDuplicate, r=1)
                mc.setAttr(upperLidBindJnt + ".tx", upperCVs[i][0])
                mc.setAttr(upperLidBindJnt + ".tz", tzOfEyeBindJoint)
                mc.move(
                    upperCVs[i][0],
                    midwayPoint[1],
                    upperCVs[i][2],
                    upperLidBindJnt,
                    ws=1,
                )
                print(upperCVs[i][0])
                mc.setAttr(upperLidBindJnt + ".tz", tzOfEyeBindJoint)
                upperLidBindJoints.append(upperLidBindJnt)
                addToSkinJoints(upperLidBindJnt)

                # Set to blink line
                mc.setAttr(upperLidBindJnt + ".ty", 0)
                mc.parent(upperDuplicate, upperLidGroup)
                # Conrol
                # lidUpperControl, lidUpperOfs, lidUpperGrp = buildControl(side, "lidUpper%s" % str(i).zfill(2), guide=upperDuplicate, shapeCVs=cs.TRIANGLE_SHAPE_CVS, colour=18 if side == "L" else 20)
                # mc.parent(lidUpperGrp, upperLidCtlsGroup)
                # mc.rotate(90, 0, 0, lidUpperControl + ".cv[*]")
                # mc.scale(0.5, 0.5, 0.5,  lidUpperControl + ".cv[*]")
                # mc.move(mc.getAttr(upperLidBindJnt +".tx"), mc.getAttr(upperLidBindJnt +".ty"), mc.getAttr(upperLidBindJnt +".tz") + 1,  lidUpperControl + ".cv[*]", r=1)
                # Lower lid joints and controls
                lowerDuplicate = mc.duplicate(baseGuideJoint)[0]
                lowerDuplicate = mc.rename(
                    lowerDuplicate,
                    lowerDuplicate.replace(
                        "lidBase_JNT1", "lidLower%s_JNT" % str(i).zfill(2)
                    ),
                )
                lowerLidJoints.append(lowerDuplicate)
                lowerLidBindJnt = mc.createNode(
                    "joint", name="%s_lidLowerBind%s_JNT" % (side, str(i).zfill(2))
                )
                mc.parent(lowerLidBindJnt, lowerDuplicate, r=1)
                mc.move(
                    lowerCVs[i][0],
                    midwayPoint[1],
                    lowerCVs[i][2],
                    lowerLidBindJnt,
                    ws=1,
                )
                print(lowerCVs[i][0])
                mc.setAttr(lowerLidBindJnt + ".tz", tzOfEyeBindJoint)
                mc.setAttr(lowerLidBindJnt + ".ty", 0)
                # Set to blink line
                lowerLidBindJoints.append(lowerLidBindJnt)
                addToSkinJoints(lowerLidBindJnt)
                mc.parent(lowerDuplicate, lowerLidGroup)
                # Control:
                # lidLowerControl, lidLowerOfs, lidLowerGrp = buildControl(side, "lidLower%s" % str(i).zfill(2), guide=lowerDuplicate, shapeCVs=cs.TRIANGLE_SHAPE_CVS, colour=18 if side == "L" else 20)
                # mc.parent(lidLowerGrp, lowerLidCtlsGroup)
                # mc.rotate(90, 0, 180, lidLowerControl + ".cv[*]")
                # mc.scale(0.5, 0.5, 0.5,  lidLowerControl + ".cv[*]")
                # mc.move(mc.getAttr(lowerLidBindJnt +".tx"), mc.getAttr(lowerLidBindJnt +".ty"), mc.getAttr(lowerLidBindJnt +".tz") + 1,  lidLowerControl + ".cv[*]", r=1)
            # Get the angle between blink line and open eye:
            blinkLineVector = gen.getVector(baseGuideJoint, guideTransform)
            guideTransformOpenEye = mc.createNode(
                "transform", name="%s_eyeOpenAimGuide_TRN" % side
            )
            mc.move(
                midCVUpper[0],
                midCVUpper[1] + 0.05,
                midCVUpper[2],
                guideTransformOpenEye,
            )
            openLidVector = gen.getVector(baseGuideJoint, guideTransformOpenEye)
            # Angle between closed and open lid in radians:
            openLidAngle = om2.MVector.angle(blinkLineVector, openLidVector)
            openLidAngle = float(mc.convertUnit(openLidAngle, f="radian", t="degree"))
            # Controls for upper and lower lids:
            lidUpperControl, lidUpperOfs, lidUpperGrp = buildControl(
                side,
                "lidUpper",
                guide=guideTransformOpenEye,
                shapeCVs=cs.TRIANGLE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.parent(lidUpperGrp, upperLidGroup)
            mc.rotate(90, 0, 0, lidUpperControl + ".cv[*]")
            mc.scale(0.5, 0.5, 0.5, lidUpperControl + ".cv[*]")
            mc.move(0, 0, 1, lidUpperGrp, r=1)
            mc.delete(mc.orientConstraint(upperLidBindJoints[1], lidUpperGrp, mo=0))
            # Move the guide transform:
            mc.move(midCVLower[0], midCVLower[1], midCVLower[2], guideTransformOpenEye)
            # Lower lid control:
            lidLowerControl, lidLowerOfs, lidLowerGrp = buildControl(
                side,
                "lidLower",
                guide=guideTransformOpenEye,
                shapeCVs=cs.TRIANGLE_SHAPE_CVS,
                colour=18 if side == "L" else 20,
            )
            mc.parent(lidLowerGrp, lowerLidGroup)
            mc.rotate(90, 0, 180, lidLowerControl + ".cv[*]")
            mc.scale(0.5, 0.5, 0.5, lidLowerControl + ".cv[*]")
            mc.move(0, 0, 1, lidLowerControl + ".cv[*]", r=1)
            mc.delete(mc.orientConstraint(lowerLidBindJoints[1], lidLowerGrp, mo=0))
            # Create a blink attr:
            blinkAttr = gen.addAttr(
                lidUpperControl, ln="blink", at="float", min=0, max=10, k=1
            )
            blinkRatioNode = mc.createNode(
                "multDoubleLinear", n="%s_blinkAttrRatio_MDL" % side
            )
            mc.connectAttr(blinkAttr, blinkRatioNode + ".input1")
            mc.setAttr(blinkRatioNode + ".input2", 0.10)
            # Eye set up connection:
            # Open/close
            # Upper Lid
            translateYAnimBlendUpper = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidUpperTranslateYtoRotateJoint_ADA" % side,
            )
            mc.connectAttr(
                lidUpperControl + ".ty", translateYAnimBlendUpper + ".weightA"
            )
            mc.setAttr(translateYAnimBlendUpper + ".inputA", -15)
            mc.setAttr(translateYAnimBlendUpper + ".inputB", openLidAngle * -1)
            # Lower Lid:
            translateYAnimBlendLower = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidLowerTranslateYtoRotateJoint_ADA" % side,
            )
            mc.connectAttr(
                lidLowerControl + ".ty", translateYAnimBlendLower + ".weightA"
            )
            mc.setAttr(translateYAnimBlendLower + ".inputA", -15)
            mc.setAttr(translateYAnimBlendLower + ".inputB", openLidAngle)

            # left/right
            # Upper Lid:
            combineXandYTranslateUpper = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidUpperTranslateXYtoRotateJoint_ADA" % side,
            )
            translateXAnimBlendUpper = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidUpperTranslateXtoRotateJoint_ADA" % side,
            )
            mc.connectAttr(
                lidUpperControl + ".tx", translateXAnimBlendUpper + ".weightA"
            )
            mc.setAttr(translateXAnimBlendUpper + ".inputA", 5)
            mc.connectAttr(
                translateXAnimBlendUpper + ".output",
                combineXandYTranslateUpper + ".inputA",
            )
            # mc.connectAttr(
            #     translateYAnimBlendUpper + ".output",
            #     combineXandYTranslateUpper + ".inputB",
            # )
            negatedcombineXandYTranslateUpper = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidUpperTranslateXYtoRotateJointNegative_ADA" % side,
            )
            mc.connectAttr(
                translateXAnimBlendUpper + ".output",
                negatedcombineXandYTranslateUpper + ".inputA",
            )
            # mc.connectAttr(
            #     translateYAnimBlendUpper + ".output",
            #     negatedcombineXandYTranslateUpper + ".inputB",
            # )
            mc.setAttr(negatedcombineXandYTranslateUpper + ".weightA", -1)
            # Lower lid:
            combineXandYTranslateLowerNegated = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidLowerTranslateXYtoRotateJointNegated_ADA" % side,
            )
            mc.setAttr(combineXandYTranslateLowerNegated + ".weightA", -1)
            translateXAnimBlendLower = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidLowerTranslateXtoRotateJoint_ADA" % side,
            )
            mc.connectAttr(
                lidLowerControl + ".tx", translateXAnimBlendLower + ".weightA"
            )
            mc.setAttr(translateXAnimBlendLower + ".inputA", 5)
            mc.connectAttr(
                translateXAnimBlendLower + ".output",
                combineXandYTranslateLowerNegated + ".inputA",
            )
            # mc.connectAttr(
            #     translateYAnimBlendLower + ".output",
            #     combineXandYTranslateLowerNegated + ".inputB",
            # )
            combineXandYTranslateLower = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidLowerTranslateXYtoRotateJoint_ADA" % side,
            )
            mc.connectAttr(
                translateXAnimBlendLower + ".output",
                combineXandYTranslateLower + ".inputA",
            )
            # mc.connectAttr(
            #     translateYAnimBlendLower + ".output",
            #     combineXandYTranslateLower + ".inputB",
            # )
            # mc.setAttr(combineXandYTranslateLower + ".weightA", -1)
            # Collision Setup (subtraction is from Upper):
            # Create ADA nodes that calcutale the angle between upper and lower joint
            innerJointsCollisonAngle = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidInnerJointsCollisionAngle_ADA" % side,
            )
            mc.connectAttr(
                combineXandYTranslateUpper + ".output",
                innerJointsCollisonAngle + ".inputA",
            )
            mc.connectAttr(
                combineXandYTranslateLower + ".output",
                innerJointsCollisonAngle + ".inputB",
            )
            mc.setAttr(innerJointsCollisonAngle + ".weightB", -1)
            midJointsCollisonAngle = mc.createNode(
                "animBlendNodeAdditiveDA", n="%s_lidMidJointsCollisionAngle_ADA" % side
            )
            mc.connectAttr(
                translateYAnimBlendUpper + ".output", midJointsCollisonAngle + ".inputA"
            )
            mc.connectAttr(
                translateYAnimBlendLower + ".output", midJointsCollisonAngle + ".inputB"
            )
            mc.setAttr(midJointsCollisonAngle + ".weightB", -1)
            outerJointsCollisonAngle = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidOuterJointsCollisionAngle_ADA" % side,
            )
            mc.connectAttr(
                combineXandYTranslateLowerNegated + ".output",
                outerJointsCollisonAngle + ".inputB",
            )
            mc.connectAttr(
                negatedcombineXandYTranslateUpper + ".output",
                outerJointsCollisonAngle + ".inputA",
            )
            mc.setAttr(outerJointsCollisonAngle + ".weightB", -1)
            # Set up and connect the blink attribute:
            # Mid Joint:
            midJointsCollisonAngleHalved = mc.createNode(
                "animBlendNodeAdditiveDA", n="%s_lidMidJointsAngleHalved_ADA" % side
            )
            mc.connectAttr(
                midJointsCollisonAngle + ".output",
                midJointsCollisonAngleHalved + ".inputA",
            )
            mc.setAttr(midJointsCollisonAngleHalved + ".weightA", 0.5)
            blinkRotationMidJoint = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidMidJointAngleWithBlinkAccountedFor_ADA" % side,
            )
            mc.connectAttr(
                midJointsCollisonAngleHalved + ".output",
                blinkRotationMidJoint + ".inputA",
            )
            mc.connectAttr(
                blinkRatioNode + ".output", blinkRotationMidJoint + ".weightA"
            )
            blinkRotationMidJointNegated = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidMidJointAngleWithBlinkAccountedForNegated_ADA" % side,
            )
            mc.connectAttr(
                blinkRotationMidJoint + ".output",
                blinkRotationMidJointNegated + ".inputA",
            )
            mc.setAttr(blinkRotationMidJointNegated + ".weightA", -1)
            midUpperJointFinalRotation = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidUpperMidJointFinalRotation_ADA" % side,
            )
            mc.connectAttr(
                translateYAnimBlendUpper + ".output",
                midUpperJointFinalRotation + ".inputA",
            )
            mc.connectAttr(
                blinkRotationMidJointNegated + ".output",
                midUpperJointFinalRotation + ".inputB",
            )
            midLowerJointFinalRotation = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidLowerMidJointFinalRotation_ADA" % side,
            )
            mc.connectAttr(
                translateYAnimBlendLower + ".output",
                midLowerJointFinalRotation + ".inputA",
            )
            mc.connectAttr(
                blinkRotationMidJoint + ".output",
                midLowerJointFinalRotation + ".inputB",
            )
            differenceAfterTheBlink = mc.createNode(
                "animBlendNodeAdditiveDA",
                n="%s_lidMidJointsAngleDifferenceAfterBlink_ADA" % side,
            )
            mc.connectAttr(
                midUpperJointFinalRotation + ".output",
                differenceAfterTheBlink + ".inputA",
            )
            mc.connectAttr(
                midLowerJointFinalRotation + ".output",
                differenceAfterTheBlink + ".inputB",
            )
            mc.setAttr(differenceAfterTheBlink + ".weightB", -1)
            # Replace the direct translate Y connection into the inner/outer joints translateXY to rotate with the blink accounted for rotation ADA node:
            # Upper side joints:
            mc.connectAttr(
                midUpperJointFinalRotation + ".output",
                negatedcombineXandYTranslateUpper + ".inputB",
            )
            mc.connectAttr(
                midUpperJointFinalRotation + ".output",
                combineXandYTranslateUpper + ".inputB",
            )
            mc.connectAttr(
                midLowerJointFinalRotation + ".output",
                combineXandYTranslateLowerNegated + ".inputB",
            )
            mc.connectAttr(
                midLowerJointFinalRotation + ".output",
                combineXandYTranslateLower + ".inputB",
            )

            # Clamp positive values for the collision angle(when lid is open the angle is negative):
            anglePositiveClamp = mc.createNode(
                "clamp", n="%s_lidJointsAnglePositive_CLP" % side
            )
            mc.setAttr(anglePositiveClamp + ".maxR", 180)
            mc.setAttr(anglePositiveClamp + ".maxG", 180)
            mc.setAttr(anglePositiveClamp + ".maxB", 180)
            mc.connectAttr(
                innerJointsCollisonAngle + ".output", anglePositiveClamp + ".inputR"
            )
            mc.connectAttr(
                differenceAfterTheBlink + ".output", anglePositiveClamp + ".inputG"
            )
            mc.connectAttr(
                outerJointsCollisonAngle + ".output", anglePositiveClamp + ".inputB"
            )
            # Divide the collision angle to simulate resistance:
            divideCollisonAngle = mc.createNode(
                "multiplyDivide", n="%s_lidJointCollisonAngleHalved_MDV" % side
            )
            mc.setAttr(divideCollisonAngle + ".operation", 1)
            mc.connectAttr(
                anglePositiveClamp + ".outputR", divideCollisonAngle + ".input1X"
            )
            mc.connectAttr(
                anglePositiveClamp + ".outputG", divideCollisonAngle + ".input1Y"
            )
            mc.connectAttr(
                anglePositiveClamp + ".outputB", divideCollisonAngle + ".input1Z"
            )
            mc.setAttr(divideCollisonAngle + ".input2X", 0.5)
            mc.setAttr(divideCollisonAngle + ".input2Y", 0.5)
            mc.setAttr(divideCollisonAngle + ".input2Z", 0.5)
            # Create final AnimBlend nodes to combine the rotation from the control and the collison angle:
            upperNodes = [
                combineXandYTranslateUpper + ".output",
                midUpperJointFinalRotation + ".output",
                negatedcombineXandYTranslateUpper + ".output",
            ]
            lowerNodes = [
                combineXandYTranslateLower + ".output",
                midLowerJointFinalRotation + ".output",
                combineXandYTranslateLowerNegated + ".output",
            ]
            angleMDVOutputs = [
                divideCollisonAngle + ".outputX",
                divideCollisonAngle + ".outputY",
                divideCollisonAngle + ".outputZ",
            ]
            for jointU, jointL, i in zip(upperLidJoints, lowerLidJoints, range(3)):
                print(upperNodes[i], lowerNodes[i], angleMDVOutputs[i])
                lidJointRotationWithCollisionUpper = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_lidUpperJointXRotationWithCollision%s_ADA"
                    % (side, str(i).zfill(2)),
                )
                lidJointRotationWithCollisionLower = mc.createNode(
                    "animBlendNodeAdditiveDA",
                    n="%s_lidLowerJointXRotationWithCollision%s_ADA"
                    % (side, str(i).zfill(2)),
                )
                # For upper joints
                mc.connectAttr(
                    angleMDVOutputs[i], lidJointRotationWithCollisionUpper + ".weightA"
                )
                mc.connectAttr(
                    upperNodes[i], lidJointRotationWithCollisionUpper + ".inputB"
                )
                mc.setAttr(lidJointRotationWithCollisionUpper + ".inputA", -1)
                mc.connectAttr(
                    lidJointRotationWithCollisionUpper + ".output", jointU + ".rx"
                )
                # For lower joints:
                mc.connectAttr(
                    angleMDVOutputs[i], lidJointRotationWithCollisionLower + ".weightA"
                )
                mc.connectAttr(
                    lowerNodes[i], lidJointRotationWithCollisionLower + ".inputB"
                )
                mc.setAttr(lidJointRotationWithCollisionLower + ".inputA", 1)
                mc.connectAttr(
                    lidJointRotationWithCollisionLower + ".output", jointL + ".rx"
                )


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
                    lockAndHide(ctl, ".txyz")
                    lockAndHide(ctl, ".sxyz")
                for jntChain in fingerJointChains:
                    mc.setAttr(jntChain[0] + ".v", 0)


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
            lockAndHide(fkCtl, ".txyz")
            lockAndHide(fkCtl, ".sxyz")
        lockAndHide(ikBaseCtl, ".rxyz")
        lockAndHide(ikBaseCtl, ".sxyz")
        lockAndHide(ikCtl, ".sxyz")

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
        lockAndHide(upperCtl, ".rxyz")
        lockAndHide(upperCtl, ".sxyz")
        lockAndHide(lowerCtl, ".rxyz")
        lockAndHide(lowerCtl, ".sxyz")

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
        follicle = gen.createFollicle(nurbsSfs, parameterU=paramU, parameterV=0.5)
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
    if attrList == ".txyz":
        attrList = [".tx", ".ty", ".tz"]
    elif attrList == ".rxyz":
        attrList = [".rx", ".ry", ".rz"]
    elif attrList == ".sxyz":
        attrList = [".sx", ".sy", ".sz"]
    for attr in attrList:
        mc.setAttr(node + attr, lock=True, k=False, channelBox=False)


def main():
    # Create a new file and import model and guides
    mc.file(new=1, force=1)
    mc.file(
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_body.ma", i=1
    )
    mc.file(
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_guides.0002.ma",
        i=1,
    )

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
    neck = HeadComponent(mc.ls("C_neck??_JNT"), mc.ls("C_neckWithTwist??_JNT"))
    mouth = FaceComponent()

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
        # Clean up:
        if not DEBUG_MODE:
            lockAndHide(kneePoleVectorCtl, ".rxyz")

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
            fkCtlsGrpList[1:],
        )
        # Build Hand structure and controls:
        hand = HandComponent(side)
        buildBendyLimbs(side, "arm")
        # Clean up:
        if not DEBUG_MODE:
            lockAndHide(elbowPoleVectorCtl, ".rxyz")

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
        "body_skin_weights_01.xml",
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
    referenceGeoAttr = gen.addAttr(
        harryCtl, ln="referenceGeo", at="long", min=0, max=1, dv=1, k=1
    )
    mc.connectAttr(referenceGeoAttr, "C_geometry_GRP.overrideEnabled")
    mc.setAttr("C_geometry_GRP.overrideDisplayType", 2)
    # Spine curve and root in hierarchy
    mc.parent("C_root_GRP", harryCtl)
    mc.parent("C_spine_CRV", harryCtl)
    mc.setAttr("C_spine_CRV.inheritsTransform", 0)
    mc.viewFit("L_lidUpper_CRV")


main()
