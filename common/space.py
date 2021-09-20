from maya import cmds as mc
from . import attr


def createSpaces(ctl, spaces=[]):
    # This function takes a control and adds an enum Space attribute to it.
    # Then goes through the list of objects to be used as spaces and creates a
    # parent constraint with offset maintained for them,
    # and uses a set driven key to space switch:
    ofs = mc.listRelatives(ctl, p=1)[0]
    names = ""
    parConAttrs = []
    for space in spaces:
        # For the attribute
        names += space[2:-4] + ":"
        # Create parentConstraints to the offset of the control
        parCon = mc.parentConstraint(space, ofs, mo=1)[0]
        parConAttrs.append(parCon + "." + mc.listAttr(parCon, st=space + "*")[0])
    spacesAttr = attr.addAttr(ctl, ln="spaceSwitch", at="enum", en=names, k=1)

    for spaceId in range(len(spaces)):
        for parConId in range(len(parConAttrs)):
            if parConId == spaceId:
                mc.setDrivenKeyframe(
                    parConAttrs[parConId], cd=spacesAttr, dv=spaceId, v=1
                )
            else:
                mc.setDrivenKeyframe(
                    parConAttrs[parConId], cd=spacesAttr, dv=spaceId, v=0
                )


def orientToParent(parentCtl, drivenCtl, drivenGrp, worldControl="C_top_CTL"):
    # Create an attribute for the control
    orientAttr = attr.addAttr(
        drivenCtl, at="float", ln="orientToParent", k=1, min=0, max=1
    )
    # create a zeroed out transform at the parent location
    worldOrientedNode = mc.createNode(
        "transform", n=drivenCtl[:-4] + "WorldOrientation_TRN"
    )
    mc.parent(worldOrientedNode, parentCtl, r=1)
    mc.rotate(0, 0, 0, worldOrientedNode, ws=1)
    # Orient constrain the drivenGroup:
    orientConstraintNode = mc.orientConstraint(
        worldControl, worldOrientedNode, drivenGrp, mo=1
    )[0]
    # Connect the attr to the parentCtlConstraint
    mc.connectAttr(orientAttr, orientConstraintNode + ".w1")
    reverse = mc.createNode("reverse", n=drivenGrp[:-4] + "ReverseInfluence_RV")
    mc.connectAttr(orientConstraintNode + ".w1", reverse + ".inputX")
    mc.connectAttr(reverse + ".outputX", orientConstraintNode + ".w0")
