from maya import cmds as mc
from maya.api import OpenMaya as om2
from ...common import attr, control, skin, ribbon
from ..base import BaseComponent

class MouthComponent(BaseComponent):
    def __init__(self):
        super(MouthComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # Hierarchy:
        lipsCtlsGrp = mc.createNode("transform", n="C_lipControls_GRP", p="C_head_CTL")
        lips = mc.createNode("transform", n="C_lips_GRP", p="C_head_CTL")
        mc.parent(lipsCtlsGrp, lips)
        # Create a jaw joint ctl, position it in the hierarchy:
        jawJnt = "C_jaw00_JNT"
        jawCtl, _, jawGrp = control.buildControl(
            "C", "jaw", jawJnt, shapeCVs=control.shapes.L_CLAVICLE_SHAPE_CVS, shapeKnots=control.shapes.KNOTS
        )
        mc.scale(0.8, 0.8, 0.8, jawCtl + ".cv[*]")
        mc.rotate(0, 0, -72.7, jawCtl + ".cv[*]", os=1, fo=1)
        mc.move(0, -9, 10, jawCtl + ".cv[*]", r=1, ws=1)
        mc.parent(jawJnt, jawCtl)
        mc.parent(jawGrp, "C_head_CTL")
        skin.addToSkinJoints(jawJnt)
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
        lipsOrientAttr = attr.addAttr(
            "C_head_CTL",
            ln="lipsOrientationInfluence",
            at="float",
            min=0,
            max=1,
            dv=0.3,
            k=1,
        )
        # Lip corner compound controls:
        lipCornerControlOrientGuide = "L_lipCornerOrient_LOC"
        mc.parent(lipCornerControlOrientGuide, "rig_GRP")
        # Left corner
        _, dummyCluster = mc.cluster(upperLip + ".cv[0][0:3]")
        leftLipCtl, leftLipOfs, leftLipGrp = control.buildControl(
            "L",
            "lipCorner",
            guide=dummyCluster,
            shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
            colour=18,
        )
        mc.delete(dummyCluster)
        mc.delete(mc.orientConstraint(lipCornerControlOrientGuide, leftLipGrp, mo=0))
        lipCornerControlOrientGuide = "R_lipCornerOrient_LOC"
        mc.parent(lipCornerControlOrientGuide, "rig_GRP")
        # Right corner:
        _, dummyCluster = mc.cluster(upperLip + ".cv[14][0:3]")
        rightLipCtl, rightLipOfs, rightLipGrp = control.buildControl(
            "R",
            "lipCorner",
            guide=dummyCluster,
            shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
            colour=18,
        )
        mc.delete(mc.orientConstraint(lipCornerControlOrientGuide, rightLipGrp, mo=0))
        mc.delete(dummyCluster)
        for ctl in [rightLipCtl, leftLipCtl]:
            shape = ctl + ".cv[*]"
            if ctl == rightLipCtl:
                mc.rotate(90, 0, -61.7, shape, ws=1, r=1)
            else:
                mc.rotate(90, 0, 61.7, shape, ws=1, r=1)

            mc.move(0, 0, 2, shape, ws=1, r=1)
        for grp in [rightLipGrp, leftLipGrp]:
            # mc.delete(
            #     mc.orientConstraint(
            #         "C_lipLowerOrientation_LOC", "C_lipUpperOrientation_LOC", grp, mo=0
            #     )
            # )
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
            largeLipCtl, _, largeLipGrp = control.buildControl(
                "C",
                name + "Compound",
                guide=dummyCluster,
                shapeCVs=control.shapes.RECTANGLE_SHAPE_CVS,
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
                    lipControl = "C_lipUpper00_CTL"
                elif surface == lowerLip and rowId == 9:
                    lipControl = "C_lipUpper08_CTL"
                else:
                    lipControl, ofs, grp = control.buildControl(
                        "C",
                        "%s%s" % (name, str(rowId - 1).zfill(2)),
                        shapeCVs="sphere",
                        guide=clusterHandle,
                    )
                    mc.scale(0.2, 0.2, 0.2, lipControl + "Shape*.cv[*]")
                    influenceAttr = attr.addAttr(
                        lipControl, ln="jawInfluence", at="float", min=0, max=1, k=1
                    )
                    mc.setAttr(influenceAttr, influenceValues[rowId - 1])

                    if lipControl not in ["C_lipUpper00_CTL", "C_lipUpper08_CTL"]:
                        if surface == upperLip:
                            mc.move(0, 0.5, 1, lipControl + "Shape*.cv[*]", ws=1, r=1)
                        else:
                            mc.move(0, -0.4, 1, lipControl + "Shape*.cv[*]", ws=1, r=1)
                    else:
                        mc.move(0, 0, 1, lipControl + "Shape*.cv[*]", ws=1, r=1)
                    # Constrain each control to jaw and head joints and provide control over the influence.

                    mc.delete(mc.orientConstraint(orientationLoc, grp, mo=0))
                    if lipControl in ["C_lipUpper00_CTL", "C_lipUpper08_CTL"]:
                        if lipControl == "C_lipUpper00_CTL":
                            mc.parent(grp, leftLipCtl)
                        else:
                            mc.parent(grp, rightLipCtl)

                    else:
                        if lipControl in ["C_%s07_CTL" % name, "C_%s01_CTL" % name]:
                            if lipControl == "C_%s01_CTL" % name:
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

                mc.parent(clusterHandle, lipControl)
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
                follicle = ribbon.createFollicle(surface, parameterU=u, parameterV=v)
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
                # Create a duplicate for each bind joint to manage orientation when moving lips:
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
                skin.addToSkinJoints(bindJoint)

        # Clean Up:
        if DEBUG_MODE == False:
            mc.setAttr("rig_GRP.v", 0)
            mc.setAttr(jawJnt + ".v", 0)
            mc.delete("C_lipUpperOrientation_LOC")
            mc.delete("C_lipLowerOrientation_LOC")
