from maya import cmds as mc
# import ctl_shapes as cs

DIAMOND_SHAPE_CVS = [[-1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [1.0, 0.0, 0.0],
                     [0.0, -1.0, 0.0],
                     [-1.0, 0.0, 0.0],
                     [0.0, 0.0, -1.0],
                     [1.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0],
                     [-1.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0],
                     [0.0, 1.0, 0.0],
                     [0.0, 0.0, -1.0],
                     [0.0, -1.0, 0.0],
                     [0.0, 0.0, 1.0]]
                     
SQUARE_SHAPE_CVS = [[-1.0, 0.0, -1.0],
                    [-1.0, 0.0, 1.0],
                    [1.0, 0.0, 1.0],
                    [1.0, 0.0, -1.0],
                    [-1.0, 0.0, -1.0]]



def buildControl(side, name, guide=None, shapeCVs=[], colour=17, offset = []):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    else:
        control = mc.curve(p=shapeCVs, degree=1)
    offset = mc.group(control)
    group = mc.group(offset)

        # NOTE: Check whether name exists and handle it if it does
    control = mc.rename(control, "%s_%s_CTL" % (side, name))
    offset = mc.rename(offset, "%s_%s_OFS" % (side, name))
    group = mc.rename(group, "%s_%s_GRP" % (side, name))

    # #snap to guide
    mc.delete(mc.parentConstraint(guide, group, maintainOffset=0))
    # if offset != []:
    #     mc.move(offset[0], offset[1], offset[2], group, relative=True)

    # Set colour
    mc.setAttr(control + ".overrideEnabled", 1)
    mc.setAttr(control + ".overrideColor", colour)

    return control, offset, group


def main():

    #Create a new file and import model and guides 
    mc.file(new=1, force=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_body.ma", i=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_guides.ma", i=1)


    #create and rename IK copies of joints

    #build FK ctls. IK chain, Handle and Ctls
    fkCtlsList = []
    ikCtlsList = []

    for side in "LR":
        ikChain = mc.duplicate("%s_leg00Bind_JNT" % side, renameChildren = 1)
        renamedIkChain = []
        for jnt in ikChain:
            renamedIkChain.append(mc.rename(jnt, jnt.replace("Bind_JNT1", "Ik_JNT")))
        
        ikChain = renamedIkChain

        for jnt in range(len(ikChain) -1, -1, -1):
            if jnt == (len(ikChain) - 1):
                lastFkCtl = buildControl(side, "leg0%s" % jnt , ikChain[jnt],
                    colour=17 if side == "L" else 19)
                mc.scale(6,6,6,lastFkCtl[0] + ".cv[*]")
                mc.rotate(90,0,0,lastFkCtl[0] + ".cv[*]")
                fkCtlsList.append(lastFkCtl[0])
            else:
                fkCtl = buildControl(side, "leg0%s" % jnt , ikChain[jnt], 
                    colour=17 if side == "L" else 19)
                if jnt == 0:
                    if side == "L":
                     mc.move(0, 0, 1.5, fkCtl[0] + ".cv[*]", os=1, wd=1, r=1)
                    else: 
                        mc.move(0, 0, -1.5
                        , fkCtl[0] + ".cv[*]", os=1, wd=1, r=1)

                mc.scale(6,6,6,fkCtl[0] + ".cv[*]")
                mc.rotate(0,90,0,fkCtl[0] + ".cv[*]")
                mc.parent(lastFkCtl[2], fkCtl[0])
                lastFkCtl = fkCtl


# if limb == "arm":
#                 mc.parent(ikChain[1], w = True)
#                 mc.delete(ikChain.pop(-1), ikChain.pop(0))    

 

main()