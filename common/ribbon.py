from maya import cmds as mc
from . import attr, control


def createFollicle(nurbsSurface, parameterU, parameterV=0.5):
    follicleShape = mc.createNode("follicle")
    follicleTransform = mc.listRelatives(follicleShape, p=1)[0]

    mc.connectAttr(nurbsSurface + ".worldSpace", follicleShape + ".inputSurface")
    mc.connectAttr(follicleShape + ".outTranslate", follicleTransform + ".translate")
    mc.connectAttr(follicleShape + ".outRotate", follicleTransform + ".rotate")

    mc.setAttr(follicleShape + ".parameterU", parameterU)
    mc.setAttr(follicleShape + ".parameterV", parameterV)

    return follicleTransform


def doubleRibbonSetup(
    side,
    name,
    parentGroup,
    curveUpper,
    curveLower,
    baseNumFollicles,
    secondNumFollicles,
    copySkinWeightsFrom=None,
    bindToJoints=None,
):
    """Creates a two NURBS surfaces, the base one driven by the body skinning, 
    and the second one driven by bind joints attached to the base one. Returns 
    the bind joints fron the second NURBS in a list"""
    ctlsGrp = mc.createNode("transform", n="%s_%ssControls_GRP" % (side, name))
    mc.parent(ctlsGrp, parentGroup, r=1)
    mc.setAttr(ctlsGrp + ".inheritsTransform", 0)

    c1 = curveUpper
    c2 = curveLower
    nurbsSfsBase = mc.loft(
        c1,
        c2,
        d=1,
        u=1,
        rn=0,
        rsn=True,
        ch=0,
        n="%s_%sSurface_NRB" % (side, name),
        po=0,
    )[0]
    mc.delete(c1, c2)
    nurbsSfsSecond = mc.duplicate(nurbsSfsBase)[0]
    nurbsSfsSecond = mc.rename(
        nurbsSfsSecond, nurbsSfsSecond.replace("_NRB1", "Second_NRB")
    )
    baseSurfaceSkinJoints = createBindJoints(
        side=side,
        name=name + "Base",
        nurbsSfs=nurbsSfsBase,
        numFollicles=baseNumFollicles,
        createControls=True,
        createJoints=True,
        parentNode=ctlsGrp,
    )

    # create a skin cluster on the base surface and copy the skin weights from the body to it.
    if copySkinWeightsFrom != None:
        baseSurfaceSkinning = mc.skinCluster(
            mc.listConnections("C_top_CTL.skinJoints"),
            nurbsSfsBase,
            n="%s_%sBaseSurface_SC" % (side, name),
            tsb=1,
        )[0]

        mc.skinCluster(baseSurfaceSkinning, e=1, forceNormalizeWeights=True)
        mc.select(copySkinWeightsFrom, nurbsSfsBase + ".cv[*]")
        mc.CopySkinWeights()
    else:
        baseSurfaceSkinning = mc.skinCluster(
            bindToJoints, nurbsSfsBase, n="%s_%sBaseSurface_SC" % (side, name), tsb=1
        )[0]

    mc.skinCluster(baseSurfaceSkinning, e=1, forceNormalizeWeights=True)

    # Create multiple bind joints onto the second surface to use as Bind Joints
    mc.skinCluster(
        baseSurfaceSkinJoints,
        nurbsSfsSecond,
        n="%s_%sSecondSurface_SC" % (side, name),
        tsb=1,
    )

    secondSurfaceBindJoints = createBindJoints(
        side=side,
        name=name + "Second",
        nurbsSfs=nurbsSfsSecond,
        numFollicles=secondNumFollicles,
        createJoints=True,
    )

    mc.parent(nurbsSfsBase, nurbsSfsSecond, "rig_GRP")

    return secondSurfaceBindJoints


def createBindJoints(
    side,
    name,
    nurbsSfs,
    numFollicles,
    createControls=False,
    createJoints=False,
    paramUList=None,
    parentNode="rig_GRP",
):
    DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

    """Creates follicles on a given nurbs surface, under which controls, joints or both can be created and parented"""
    bindJointGrp = mc.createNode("transform", n="%s_%sBindFlcJoint_GRP" % (side, name))
    attr.lockAndHide(bindJointGrp)
    if parentNode != None:
        mc.parent(bindJointGrp, parentNode)
    paramUList = paramUList
    follicle = None
    folliclesList = []
    jointParent = None
    jointList = []
    paramUIncrement = 1 / (numFollicles * 1.00)
    paramUFollicle = 1 / (numFollicles * 2.00)
    # Create a follicle at a specified parameter U if given, or uniformly.
    for follicleId in range(numFollicles):
        if paramUList is not None:
            follicle = createFollicle(
                nurbsSfs, parameterU=paramUList[follicleId], parameterV=0.5
            )
        else:
            follicle = createFollicle(
                nurbsSfs, parameterU=paramUFollicle, parameterV=0.5
            )
            paramUFollicle += paramUIncrement
        follicle = mc.rename(
            follicle, "%s_%sBind%s_FLC" % (side, name, str(follicleId).zfill(2))
        )
        folliclesList.append(follicle)
        mc.parent(follicle, bindJointGrp)
        jointParent = follicle
        # Create a sphere shaped control under each follicle:
        if createControls is True:
            ctl, ofs, grp = control.buildControl(
                side, name + str(follicleId).zfill(2), shapeCVs="sphere"
            )
            mc.parent(grp, follicle, r=1)
            jointParent = ctl

        # Create a bind joint under each follicle and add it to the skinJoints:
        if createJoints is True:
            bindJoint = mc.createNode(
                "joint", name="%s_%sBind%s_JNT" % (side, name, str(follicleId).zfill(2))
            )

            mc.parent(bindJoint, jointParent, r=1)
            jointList.append(bindJoint)

        if DEBUG_MODE == False:
            mc.setAttr(bindJoint + ".v", 0)
            mc.setAttr(follicle + "Shape.visibility", 0)
    return jointList
