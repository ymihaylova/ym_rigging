from maya import cmds as mc

def addAttr(*args, **kwargs):
    mc.addAttr(*args, **kwargs)

    return args[0] + "." + kwargs["ln"]
    
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
