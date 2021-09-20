from maya import cmds as mc
from . import shapes

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
