from maya import cmds as mc
from ym_rigging import components
from ym_rigging.common import attr, control, weights, ribbon, skin, blendShape, twist

MODEL_FILE = (
    "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_body_textured.ma"
)
GUIDES_FILE = (
    "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes\hp_guides_withSnS.ma"
)
DEBUG_MODE = False


def main():
    # Create a new file and import model and guides
    mc.file(new=1, force=1)
    mc.file(MODEL_FILE, i=1)
    mc.file(GUIDES_FILE, i=1)

    # Housekeeping setup:q
    topCtl, _, _ = control.buildControl(
        "C", "top", shapeCVs=control.shapes.SQUARE_SHAPE_CVS
    )
    mc.scale(15, 15, 15, topCtl + ".cv[*]")
    topCtlSkinJoints = attr.addAttr(topCtl, ln="skinJoints", at="message")
    ctlsGrp = mc.group(em=1)
    ctlsGrp = mc.rename(ctlsGrp, "ctls_GRP")
    rigGrp = mc.group(em=1)
    rigGrp = mc.rename(rigGrp, "rig_GRP")

    # In order to be able to access DEBUG_MODE from everywhere,
    # we store it on the top control
    attr.addAttr(topCtl, ln="debugMode", at="bool", dv=DEBUG_MODE)
    mc.setAttr(topCtl + ".debugMode", k=0, cb=0)

    # Build spine
    spine = components.body.spine(mc.ls("C_spine??_JNT"), "C_spine_CRV")

    # Build head
    head = components.body.head(mc.ls("C_neck??_JNT"), mc.ls("C_neckWithTwist??_JNT"))

    for side in "LR":
        # Build leg FK ctls. IK chain, Handle and Ctls
        leg = components.body.leg(side, "leg", "C_hips_CTL", topCtlSkinJoints)

        # Foot
        foot = components.body.foot(side, leg.ikCtl)

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
        weights.loadDeformerWeights(
            "%s_sock_skinWeights.xml" % side,
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
            deformer=skinClusterSock,
        )
        mc.skinCluster(skinClusterSock, e=1, forceNormalizeWeights=True)
        weights.loadDeformerWeights(
            "%s_shoe_skinWeights.xml" % side,
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
            deformer=skinClusterShoe,
        )
        mc.skinCluster(skinClusterShoe, e=1, forceNormalizeWeights=True)

        # Build arm FK ctls. IK chain, Handle and Ctls
        arm = components.body.arm(side, "arm", "C_chest_CTL", topCtlSkinJoints)

        # Hand
        # TODO: Make it so the args for this component are not hardcoded, but
        # taken in as arguments similar to the spine, head and limb components
        hand = components.body.hand(side)

    # Face
    # Eyebrows
    # TODO: Make it so the args for this component are not hardcoded, but
    # taken in as arguments similar to the spine, head and limb components
    eyebrows = components.face.eyebrows()

    # Create wire deformers for C_body_PLY and for the eyebrow proxies:
    bodyWireDefNode, _ = mc.wire("C_body_PLY", w=eyebrows.browCurve, dds=(0, 4.01))
    mc.setAttr(bodyWireDefNode + ".rotation", 0.2)
    weights.loadDeformerWeights(
        "HP_body_wireWeights.xml",
        path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\scenes",
        deformer=bodyWireDefNode,
    )
    browsWireDefNode = mc.wire(
        "C_eyebrowsProxy_PLY", w=eyebrows.browCurve, dds=(0, 50)
    )[0]
    mc.setAttr(browsWireDefNode + ".rotation", 0.5)
    mc.parentConstraint("C_head_CTL", "C_eyebrowsProxy_PLY", mo=1)

    # Clean up:
    mc.parent(mc.ls(eyebrows.browCurve + "*", typ="transform"), "C_head_CTL")

    # Eyes
    # TODO: Make it so the args for this component are not hardcoded, but
    # taken in as arguments similar to the spine, head and limb components
    eyes = components.face.eyes()

    # Mouth
    # Lips and jaw
    # TODO: Make it so the args for this component are not hardcoded, but
    # taken in as arguments similar to the spine, head and limb components
    mouth = components.face.mouth()

    # Mouth blendshapes drivers
    for side in "LR":
        ctl, ofs, grp = control.buildControl(
            side,
            "blendShape",
            guide="%s_lipCorner_CTL" % side,
            shapeCVs=control.shapes.BLEND_SHAPES_CVS,
        )
        mc.rotate(0, 0, 0, grp, ws=1)
        if side == "L":
            pass
            # mc.move(5, grp, x=1)
        else:
            # mc.move(-5, grp, x=1)
            mc.scale(-1, grp, x=1)
        mc.rotate(90, ctl + ".cv[*]", x=1)
        mc.move(2, grp, z=1, r=1)
        mc.scale(0.25, 0.25, 0.25, ctl + ".cv[*]")
        mc.parent(grp, "C_head_CTL")

        # create an MDV node to normalize the x/y values to 0to1 which I can use to drive blend shapes:
        normalize0to1 = mc.createNode(
            "multiplyDivide", n="%s_blendShapesXYZNormalise0to1_MDV" % side
        )
        mc.setAttr(normalize0to1 + ".operation", 2)
        # MDV to turn the negative values into positive to drive the narrow and frown
        negateNormalized = mc.createNode(
            "multiplyDivide", n="%s_blendShapesNegatedValues_MDV" % side
        )
        clampPositive = mc.createNode(
            "clamp", n="%s_blendShapesPositiveValues_CLP" % side
        )
        clampNegative = mc.createNode(
            "clamp", n="%s_blendShapesNegativeValues_CLP" % side
        )

        for i, j in zip("XYZ", "RGB"):
            if i == "X":
                mc.setAttr(normalize0to1 + ".input2%s" % i, 1.793)
            elif i == "Y":
                mc.setAttr(normalize0to1 + ".input2%s" % i, 2.8)
            mc.setAttr(negateNormalized + ".input2%s" % i, -1)
            for clamp in (clampPositive, clampNegative):
                mc.setAttr(clamp + ".min%s" % j, 0)
                mc.setAttr(clamp + ".max%s" % j, 1)
        # Connect the CTL movement to the normalisation MDVs
        mc.connectAttr(ctl + ".t", normalize0to1 + ".input1")
        mc.connectAttr(normalize0to1 + ".output", negateNormalized + ".input1")

        # Connect the positive normalised values to clamp:
        mc.connectAttr(normalize0to1 + ".output", clampPositive + ".input")
        mc.connectAttr(negateNormalized + ".output", clampNegative + ".input")

    # Tongue
    # create an on/off attribute that controls the visibility of controls for the
    # tongue and teeth from the jaw control:
    visibilityAttr = attr.addAttr(
        "C_jaw_CTL",
        ln="mouthCtlsVisibility",
        sn="mcv",
        at="long",
        min=0,
        max=1,
        dv=1,
        k=1,
    )
    tongue = components.face.tongue(
        "C", "tongue", mc.ls("C_tongue??_JNT"), "C_jaw_CTL", visibilityAttr
    )

    # Create and load body skin weights
    # We need it before we can create the double ribbon setups
    # since they will use the body skinning as a base
    skinJoints = mc.listConnections("C_top_CTL.skinJoints")

    body = "C_body_PLY"
    skinCluster = mc.skinCluster(skinJoints, body, n=body[:-4] + "_SCD", tsb=1)[0]
    mc.setAttr(skinCluster + ".skinningMethod", 2)

    weights.loadDeformerWeights(
        "body_skin_weights_06.xml",
        path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\sourceimages",
        deformer=skinCluster,
    )
    mc.skinCluster(skinCluster, e=1, forceNormalizeWeights=True)

    # Teeth
    # TODO: Make it so the args for this component are not hardcoded, but
    # taken in as arguments similar to the spine, head and limb components
    teeth = components.face.teeth()

    # Clothes rig
    clothesGroup = mc.createNode("transform", n="C_clothes_GRP")
    mc.parent(clothesGroup, topCtl, r=1)
    jumper = "C_jumper_PLY"
    jumperBindJoints = ribbon.doubleRibbonSetup(
        "C",
        "jumper",
        clothesGroup,
        "C_jumperUpper_CRV",
        "C_jumperLower_CRV",
        baseNumFollicles=12,
        secondNumFollicles=20,
        copySkinWeightsFrom="C_body_PLY",
    )

    for side in "LR":
        pointConstraintJoint = "%s_arm03_JNT" % side
        orientConstraintJoint = "%s_armBind09_JNT" % side
        bindJoint = mc.createNode(
            "joint", n=pointConstraintJoint.replace("03_JNT", "jumperSleeveBind_JNT")
        )
        mc.hide(bindJoint)
        mc.parent(bindJoint, "%s_arm_GRP" % side)

        mc.pointConstraint(pointConstraintJoint, bindJoint, mo=0)
        mc.orientConstraint(orientConstraintJoint, bindJoint, mo=0)

        jumperBindJoints += ribbon.doubleRibbonSetup(
            side,
            "jumperSleeve",
            clothesGroup,
            "%s_sleeveUpper_CRV" % side,
            "%s_sleeveLower_CRV" % side,
            baseNumFollicles=6,
            secondNumFollicles=12,
            bindToJoints=bindJoint,
        )

    # driving blend shapes for the shirt collar with the twist in neck:
    neckJointTwistInZ = twist.extractTwist(
        "C_neck00_JNT", "C_chest_CTL", alignXwith="Z"
    )
    neckJointTwistInY = twist.extractTwist(
        "C_neck00_JNT", "C_chest_CTL", alignXwith="Y"
    )

    twist.blendShapeDriverFromTwist(
        neckJointTwistInZ, n="Positive", angle=23.5, remapRange=(0.2, 1)
    )
    twist.blendShapeDriverFromTwist(
        neckJointTwistInZ, n="Negative", angle=-23.5, remapRange=(0.2, 1)
    )
    twist.blendShapeDriverFromTwist(
        neckJointTwistInY, n="Positive", angle=21.4, remapRange=(0.25, 1)
    )
    twist.blendShapeDriverFromTwist(
        neckJointTwistInY, n="Negative", angle=-21.4, remapRange=(0.2, 1)
    )

    # Create and load blendshapes
    blendShapeDef = blendShape.loadBlendShapes(
        "C_body_PLY",
        "HP_blendShapes.shp",
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\shapes",
    )
    mc.setAttr(blendShapeDef + ".C_bodyShrink", 1)

    for side in "LR":
        # Connect the clamped values to the blend shapes:
        mc.connectAttr(
            side + "_blendShapesPositiveValues_CLP" + ".outputR",
            blendShapeDef + ".%s_wide" % side,
        )
        mc.connectAttr(
            side + "_blendShapesPositiveValues_CLP" + ".outputG",
            blendShapeDef + ".%s_smile" % side,
        )
        mc.connectAttr(
            side + "_blendShapesNegativeValues_CLP" + ".outputR",
            blendShapeDef + ".%s_narrow" % side,
        )
        mc.connectAttr(
            side + "_blendShapesNegativeValues_CLP" + ".outputG",
            blendShapeDef + ".%s_frown" % side,
        )

    # Jaw opening controlling the jaw open corrective:
    jawOpen0to16 = mc.createNode(
        "animBlendNodeAdditiveDA", n="C_jawCorrectiveNormalize0to1_ADA"
    )
    jawOpenClamp = mc.createNode("clamp", n="C_jawOpenBlendShape_CLP")
    mc.setAttr(jawOpenClamp + ".minR", 0)
    mc.setAttr(jawOpenClamp + ".maxR", 1)
    # Extract the twist in Z for the Jaw Control:
    jawTwistZ = twist.extractTwist("C_jaw_CTL", "C_head_CTL", alignXwith="Z")
    mc.connectAttr(jawTwistZ, jawOpen0to16 + ".inputA")
    mc.setAttr(jawOpen0to16 + ".weightA", -0.066)
    mc.connectAttr(jawOpen0to16 + ".output", jawOpenClamp + ".inputR")
    mc.connectAttr(jawOpenClamp + ".outputR", blendShapeDef + ".C_jawOpenCorrective")

    # Head rotation in X controlling the neck corrective:
    head0to45 = mc.createNode(
        "animBlendNodeAdditiveDA", n="C_neckCorrectiveFromHeadTwistNormalize0to1_ADA"
    )
    neckClamp = mc.createNode("clamp", n="C_neckBlendShape_CLP")
    mc.setAttr(neckClamp + ".minR", 0)
    mc.setAttr(neckClamp + ".maxR", 1)
    # Extract the twist in X for the head Control:
    headTwistX = twist.extractTwist("C_head_CTL", "C_neck_CTL", alignXwith="X")
    mc.connectAttr(headTwistX, head0to45 + ".inputA")
    mc.setAttr(head0to45 + ".weightA", -0.022)
    mc.connectAttr(head0to45 + ".output", neckClamp + ".inputR")
    # mc.connectAttr(neckClamp + ".outputR", blendShapeDef + ".C_neck")

    # Jumper bottom blend shape creation and connection
    jumperBlendShape = mc.blendShape(
        ["L_jumperSurfaceLegUp", "R_jumperSurfaceLegUp"],
        "C_jumperSurface_NRB",
        n="C_jumperSurfaceBase_BLS",
    )[0]
    for s in "LR":
        mc.delete("%s_jumperSurfaceLegUp")

    for s in "LR":
        mc.connectAttr(
            s + "_leg00YTwistExtractionTransform_RMV.outValue",
            jumperBlendShape + "." + s + "_jumperSurfaceLegUp",
        )

    # Shirt automated blend shapes for moving the neck:
    # Twist in Z responsible for side to side movement, and twist in Y for back and forth
    shirtBlendShapeDef = blendShape.loadBlendShapes(
        "C_shirt_PLY",
        "hp_shirt_blendshapes.shp",
        "C:\Users\Yana\Documents\maya\projectFolder\HPScripted\shapes",
    )

    for s, d, v in zip("LR", ["Forward", "Back"], ["Negative", "Positive"]):
        mc.connectAttr(
            "C_neck00ZTwistExtractionTransform%s_RMV.outValue" % v,
            shirtBlendShapeDef + "." + s + "_neckSide",
        )
        mc.connectAttr(
            "C_neck00YTwistExtractionTransform%s_RMV.outValue" % v,
            shirtBlendShapeDef + ".C_neck" + d,
        )

    # Clothes skinning
    for ply in ["pants", "jumper", "tie", "shirt"]:
        if ply == "jumper":
            bindJoints = skinJoints + jumperBindJoints
        else:
            bindJoints = skinJoints

        clothingSkinCluster = mc.skinCluster(
            bindJoints, "C_%s_PLY" % ply, n="C_%s_SC" % ply, tsb=1
        )[0]

        weights.loadDeformerWeights(
            "%s_skin_weights.xml" % ply,
            path="C:\Users\Yana\Documents\maya\projectFolder\HPScripted\sourceimages",
            deformer=clothingSkinCluster,
        )
        mc.skinCluster(clothingSkinCluster, e=1, forceNormalizeWeights=True)

    # Skin gums, teeth, tongue:
    mc.skinCluster("C_head_JNT", "C_upperTeeth_PLY", tsb=1)
    mc.skinCluster("C_head_JNT", "C_upperGums_PLY", tsb=1)
    mc.skinCluster("C_jaw00_JNT", "C_lowerTeeth_PLY", tsb=1)
    mc.skinCluster("C_jaw00_JNT", "C_lowerGums_PLY", tsb=1)
    mc.skinCluster(
        "C_tongue00_JNT",
        "C_tongue01_JNT",
        "C_tongue02_JNT",
        "C_tongue03_JNT",
        "C_tongue_PLY",
        fnw=1,
        tsb=1,
    )

    # Constrain eyebrows
    mc.parentConstraint("C_head_CTL", "C_hairAndEyebrowsProxy_PLY", mo=1)

    # Ensure deformation order
    mc.reorderDeformers(
        "C_jumperBaseSurface_SC", "C_jumperSurfaceBase_BLS", "C_jumperSurface_NRB"
    )
    mc.reorderDeformers("wire1", "C_body_SCD", "C_body_PLY")
    mc.reorderDeformers("C_body_SCD", "C_body_BLS", "C_body_PLY")

    # Housekeeping:
    groups = mc.ls("*GRP")
    offsets = mc.ls("*OFS")
    if DEBUG_MODE == False:
        for grp in groups:
            attr.lockAndHide(grp)
        for ofs in offsets:
            attr.lockAndHide(ofs)

    # Geometry in hierarchy
    mc.setAttr("C_geometry_GRP.inheritsTransform", 0)
    mc.parent("C_geometry_GRP", topCtl)
    # Make geometry unselectble:
    referenceGeoAttr = attr.addAttr(
        topCtl, ln="referenceGeo", at="long", min=0, max=1, dv=1, k=1
    )
    mc.connectAttr(referenceGeoAttr, "C_geometry_GRP.overrideEnabled")
    mc.setAttr("C_geometry_GRP.overrideDisplayType", 2)
    # Spine curve and root in hierarchy
    mc.viewFit("C_head_CTL")


main()
