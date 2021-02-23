from maya import cmds as mc
from maya.api import OpenMaya as om2
# from maya import ctl_shapes as cs

DEBUG_MODE = True
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

HIPS_SHAPE_CVS =  [[14.590458153988756, 8.21326916344569, -8.643040618417103],
                [-2.7909669651786697e-15, -2.2095747033093933, -12.223105262706994],
                [-14.590458153988724, 8.21326916344569, -8.643040618417109],
                [-20.63402380260794, 8.21326916344569, -1.4531981665925726e-14],
                [-14.590458153988731, 8.21326916344569, 8.643040618417087],
                [-5.6629910545598045e-15, -2.209574703309397, 12.223105262706994],
                [14.590458153988717, 8.21326916344569, 8.643040618417103],
                [20.63402380260794, 8.21326916344569, 2.371570099328309e-15]]

CHEST_SHAPE_CVS = [[11.997835759804845, 15.31150051686226, -10.47413000650149],
                [-2.2531424144500868e-15, -10.467207624358378, -14.05419465079138],
                [-11.997835759804818, 15.31150051686226, -10.474130006501495],
                [-11.688723194319532, 17.449921690411195, -1.8310893880844004],
                [-11.997835759804824, 15.31150051686226, 6.811951230332701],
                [-5.125166503831222e-15, -10.467207624358382, 10.392015874622608],
                [11.997835759804811, 15.31150051686226, 6.811951230332717],
                [11.688723194319532, 17.449921690411195, -1.8310893880843835]]

SPINEMID_SHAPE_CVS = [[11.997835759804834, 0.00011820143186022515, -8.643040618417103],
                    [-1.2911283450851595e-14, -0.00013958564304051668, -12.223105262706994],
                    [-11.997835759804829, 0.00011820143186022515, -8.643040618417109],
                    [-11.688723194319543, 0.00013958564304065237, -1.4531981665925726e-14],
                    [-11.997835759804834, 0.0001182014318601292, 8.643040618417087],
                    [-1.578330754023273e-14, -0.00013958564304065237, 12.223105262706994],
                    [11.9978357598048, 0.0001182014318601292, 8.643040618417103],
                    [11.688723194319522, 0.00013958564304065237, 2.8156593091783716e-15]]
class SpineComponent:
    def __init__(self, jointChain, curve):
        self.build(jointChain, curve)
    
    def build(self, jointChain, curve):
        # Clusters and controls:
        spineCtls = []
        names = ["hips", "spineMid", "chest"]
        shapes = [HIPS_SHAPE_CVS, SPINEMID_SHAPE_CVS, CHEST_SHAPE_CVS]

        for counter, cvIDs in enumerate(["0:1", "2", "3:4"]):
            cvs = curve + ".cv[%s]" % cvIDs

            _, clusterHandle = mc.cluster(cvs, name="C_spine%s_CLS" % \
                            str(counter).zfill(2))
            ctl, _, _ = buildControl("C", names[counter], clusterHandle, \
                    shapeCVs=shapes[counter], degree=3)
            if counter != 1:
                # Create a hips/chest joint, reposition to ctl location and parent:
                joint = mc.createNode("joint",name = "C_%s_JNT" % names[counter])
                mc.delete(mc.parentConstraint(ctl, joint, mo=0))
                mc.parent(joint, ctl)
            
            spineCtls.append(ctl)
            # Parent cluster under ctl:
            mc.parent(clusterHandle, ctl)

            if not DEBUG_MODE:
                mc.hide(joint, clusterHandle)
            
        #Spline IK handle:
        splineIkh, _ = mc.ikHandle(sj="C_spine00_JNT", ee="C_spine04_JNT", \
                    solver="ikSplineSolver", createCurve=0, curve=curve)
        splineIkh = mc.rename(splineIkh, "C_spine_IKH")

        # Advanced twist:
        mc.setAttr(splineIkh + ".dTwistControlEnable", 1)
        mc.setAttr(splineIkh + ".dWorldUpType", 4)
        mc.setAttr(splineIkh + ".dForwardAxis", 0)
        mc.setAttr(splineIkh + ".dWorldUpAxis", 0)
        mc.setAttr(splineIkh + ".dWorldUpVector", -1, 0, 0)
        mc.setAttr(splineIkh+ ".dWorldUpVectorEnd", -1, 0, 0)
        mc.connectAttr(spineCtls[0]+ ".worldMatrix", splineIkh + ".dWorldUpMatrix")
        mc.connectAttr(spineCtls[-1] + ".worldMatrix", splineIkh + ".dWorldUpMatrixEnd")

def addAttr(*args, **kwargs):
    mc.addAttr(*args, **kwargs)
    
    return args[0] + "." + kwargs["ln"] 

def buildControl(side, name, guide=None, shapeCVs=[], degree=1, colour=17, offset = []):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    else:
        control = mc.curve(p=shapeCVs, degree=degree)
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

def buildLimb(side, name, parent):
    blendChain = mc.ls("%s_%s??_JNT" % (side, name))
    fkCtlsList = []
    fkCtlsOfsList =[]
    fkCtlsGrpList = []
    prevFkCtl, prevFkCtlGrp = None, None

    for jntId in range(len(blendChain)-1):
        fkCtl, fkCtlOfs, fkCtlGrp = buildControl(side, "%s%sFk" % (name, \
                            str(jntId).zfill(2)), blendChain[jntId], colour=17 
                            if side=="L" else 19)

        if prevFkCtlGrp is not None:
            mc.parent(fkCtlGrp, prevFkCtl)
        else:
            mc.parent(fkCtlGrp, parent)

        fkCtlsList.append(fkCtl)
        fkCtlsOfsList.append(fkCtlOfs)
        fkCtlsGrpList.append(fkCtlGrp)
        prevFkCtl, prevFkCtlGrp = fkCtl, fkCtlGrp

    # Create IK copy of the leg chain
    ikChain = mc.duplicate("%s_%s00_JNT" % (side, name), renameChildren=1)
    renamedIkChain = []
    for jnt in ikChain:
        renamedIkChain.append(mc.rename(jnt, jnt.replace("_JNT", "Ik_JNT")[:-1]))
        
    ikChain = renamedIkChain

    if not DEBUG_MODE:
        mc.hide(blendChain, ikChain)

    return blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain

def getPoleVectorPosition(rootPos, midPos, endPos):
    rootJntVector = om2.MVector(rootPos[0], rootPos[1], rootPos[2])
    midJntVector = om2.MVector(midPos[0], midPos[1], midPos[2])
    endJntVector = om2.MVector(endPos[0], endPos[1], endPos[2])

    rootToEnd = (endJntVector - rootJntVector)
    closestPoint = (midJntVector - rootJntVector)

    scaleValue = (rootToEnd * closestPoint) / (rootToEnd * rootToEnd)
    projectionVector = rootToEnd * scaleValue + rootJntVector

    rootToMidLen = (midJntVector - rootJntVector).length()
    midToEndLen = (endJntVector - midJntVector).length()
    totalLen = rootToMidLen + midToEndLen

    poleVectorPosition = (midJntVector - projectionVector).normal() * totalLen \
                    + midJntVector
    
    return poleVectorPosition

def getIkhPoleVecPos(ikHandle):
    jointList = mc.ikHandle(ikHandle, q=True, jointList=True)
    jointList.append(mc.listRelatives(jointList[-1], children=True, type="joint")[0])

    rootJntPos = mc.xform(jointList[0], q=1, ws=1, t=1)
    midJntPos = mc.xform(jointList[1], q=1, ws=1, t=1)
    endJntPos = mc.xform(jointList[2], q=1, ws=1, t=1)

    poleVectorPos = getPoleVectorPosition(rootJntPos, midJntPos, endJntPos)

    return poleVectorPos


def main():
    #Create a new file and import model and guides 
    mc.file(new=1, force=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_body.ma", i=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_guides.ma", i=1)

    # Build spine
    spine = SpineComponent(mc.ls("C_spine??_JNT"), "C_spine_CRV")

    # Build leg FK ctls. IK chain, Handle and Ctls
    for side in "LR":
        # Build IK chain and FK ctls
        blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain = buildLimb(side, "leg", "C_hips_CTL")

        # Adjust FK ctl shapes
        for ctl, ofs, grp in zip(fkCtlsList, fkCtlsOfsList, fkCtlsGrpList): 
                mc.scale(6,6,6,ctl + ".cv[*]")

                if ctl != fkCtlsList[-1] : # omit rotating the toe FK control CVs 
                    mc.rotate(90,0,0,ctl + ".cv[*]", ws=1)

                if ctl == fkCtlsList[0] : # move the hip FK control CVs for visual clarity
                    mc.move(0, -8, 0, ctl + ".cv[*]", ws=1, r=1)

        # Build IK foot control:
        footIkCtl, _, footIkCtlGrp = buildControl(side, "leg02Ik", "%s_leg02Ik_JNT"
                                 % side, shapeCVs=SQUARE_SHAPE_CVS, colour=18 if 
                                 side=="L" else 20)
        mc.scale(6,6,6, footIkCtl + ".cv[*]")

        # Create IK handle and parent to IK control:
        footIkHandle, _ = mc.ikHandle(sj="%s_leg00Ik_JNT" % side, 
                    ee="%s_leg02Ik_JNT" % side, sol="ikRPsolver")
        footIkHandle = mc.rename(footIkHandle, "%s_leg02_IKH" % side)
        mc.parent(footIkHandle, footIkCtl)

        # Build Pole Vector control and create pole vector constraint to leg02IK:
        kneePoleVectorCtl, _, kneePoleVectorGrp = buildControl(side, 
        "kneePoleVector", "%s_leg01Ik_JNT" % side, shapeCVs=DIAMOND_SHAPE_CVS, 
                                                colour=18 if side=="L" else 20)
        
        kneePoleVectorPos = getIkhPoleVecPos(footIkHandle)
        mc.scale(4,4,4, kneePoleVectorCtl + ".cv[*]")
        mc.move(kneePoleVectorPos.x, kneePoleVectorPos.y, kneePoleVectorPos.z, 
                        kneePoleVectorGrp)
        mc.poleVectorConstraint(kneePoleVectorCtl, footIkHandle)

        ikCtlsGrp = mc.group(kneePoleVectorGrp, footIkCtlGrp, n="%s_legIkCtls_GRP" \
                 % side, w=1)

        # Create parent constraints to bind skeleton:
        blendChainParentConstraints = []
        for blendJnt, ikJnt, fkCtl in zip(blendChain[:-1], ikChain, fkCtlsList):
            parCon = mc.parentConstraint(ikJnt, fkCtl, blendJnt, mo=0)[0]
            blendChainParentConstraints.append(parCon)
        
        # Create and position IK/FK Switch
        ikFkSwitchCtl, ikFkSwitchOfs, ikFkSwitchGrp = buildControl(side, 
                                            "ikFkSwitch", "%s_leg02_JNT" % side)
        
        if side=="L":
            mc.move(10, 5,0, ikFkSwitchGrp, r=1)
        else:
            mc.move(-10, 5, 0, ikFkSwitchGrp, r=1)
        mc.parentConstraint("%s_leg02_JNT" % side, ikFkSwitchOfs, mo=1)
        ikFkSwitchAttr = addAttr(ikFkSwitchCtl, at="float", k=1, ln="ikFkSwitch",
                     max=1, min=0, dv=0)

        # Reverse IK FK switch attribute's value:
        reversalNodeIkFk = mc.createNode("plusMinusAverage", 
                        n="%s_ikFkReversedValue_PMA" % side)
        mc.setAttr(reversalNodeIkFk + ".operation", 2)
        mc.setAttr(reversalNodeIkFk + ".input1D[0]", 1)
        mc.connectAttr(ikFkSwitchAttr, reversalNodeIkFk + ".input1D[1]")

        # Connect IK/Fk Switch to parent constraints:
        for parCon in blendChainParentConstraints:
            mc.connectAttr(ikFkSwitchAttr, parCon + ".w1")
            mc.connectAttr(reversalNodeIkFk + ".output1D", parCon +".w0")

        # Connect IK/FK Switch to control visibility:
        # for ctl in ikCtlsGrp:
        #     print(ctl)
        mc.connectAttr(reversalNodeIkFk + ".output1D", ikCtlsGrp + ".v")
        
        for ctl in fkCtlsList:
            mc.connectAttr(ikFkSwitchAttr, ctl + ".v")




    # Build arm FK ctls. IK chain, Handle and Ctls 
    # for side in "LR":

    #     armBindChain = mc.ls("%s_arm??Bind_JNT" % side)
    #     fkCtlsList = []
    #     prevFkCtl = []

    #     for jnt in range(len(armBindChain)-1):
    #         fkCtl = buildControl(side, "arm%s" % str(jnt).zfill(2) , armBindChain[jnt], 
    #              colour=17 if side == "L" else 19)

    #         mc.scale(6,6,6,fkCtl + ".cv[*]")
    #         mc.rotate(0,90,0,fkCtl + ".cv[*]", ws=1)

    #         if jnt == 0: # move the clavicle FK control CVs for visual clarity
    #             if side =="L":
    #                 mc.move(3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
    #             else:
    #                 mc.move(-3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
    #             mc.scale(1.5,1.5,1.5,fkCtl + ".cv[*]")


    #         if prevFkCtl != []:
    #             mc.parent(fkCtl[2], prevfkCtl)

    #         fkCtlsList.append(fkCtl)
    #         prevFkCtl = fkCtl 
        
    #     # Create IK copy of the leg chain
    #     ikChain = mc.duplicate("%s_arm00Bind_JNT" % side, renameChildren = 1)
    #     renamedIkChain = []

    #     for jnt in ikChain:
    #         renamedIkChain.append(mc.rename(jnt, jnt.replace("Bind_JNT1", "Ik_JNT")))
        
    #     ikChain = renamedIkChain

    #     # Build IK wrist control:
    #     ikCtlsList = []
    #     wristIkCtl = buildControl(side, "arm03Ik", "%s_arm03Ik_JNT" % side, 
    #             shapeCVs=SQUARE_SHAPE_CVS, colour=18 if side=="L" else 20)
    #     mc.scale(6,6,6, armIkCtl[0] + ".cv[*]")
    #     ikCtlsList.append(armIkCtl)

    #     # Create IK handle and parent to IK control:
        
    #     armIkHandle, _ = mc.ikHandle(sj="%s_arm01Ik_JNT" % side, ee="%s_leg03Ik_JNT" % side, sol="ikRPsolver")
    #     armIkHandle = mc.rename(armIkHandle, "%s_arm03_IKH" % side)
    #     mc.parent(armIkHandle, armIkCtl[0])

    #     # Build Pole Vector control and create pole vector constraint to leg02IK:
    #     elbowPoleVectorCtl = buildControl(side, "elbowPoleVector", "%s_arm02Ik_JNT" 
    #                     % side, shapeCVs=DIAMOND_SHAPE_CVS, colour=18 if side=="L"
    #                     else 20)
        
    #     elbowPoleVectorPos = getIkhPoleVecPos(armIkHandle)
    #     mc.scale(4,4,4, elbowPoleVectorCtl[0] + ".cv[*]")
    #     mc.move(elbowPoleVectorPos.x, elbowPoleVectorPos.y, elbowPoleVectorPos.z, 
    #                     elbowPoleVectorCtl[2])
    #     mc.poleVectorConstraint(elbowPoleVectorCtl, wristIkHandle)

    #     ikCtlsList.append(elbowPoleVectorCtl)
    #     mc.group(elbowPoleVectorCtl[2], wristIkCtl[2], n="%s_armikCtls_GRP" % side, w=1)

    #     # Create parent constraints to bind skeleton:
    #     bindChainParentConstraints = []
    #     for i in range(len(armBindChain)): # IK
    #         parCon = mc.parentConstraint(ikChain[i], armBindChain[i], mo=0)[0]
            
    #         if i != (len(legBindChain)-1): #FK
    #             mc.parentConstraint(fkCtlsList[i][0], armBindChain[i], mo=0)
    #         else:
    #             mc.parentConstraint(fkCtlsList[i-1][0], armBindChain[i], mo=1)
            
    #         bindChainParentConstraints.append(parCon)
        
    #     # Create and position IK/FK Switch 
    #     # NOTE: to be turned into a function useable by both arms and legs?
    #     ikFkSwitch = buildControl(side, "ikFkSwitch", "%s_arm03Bind_JNT" % side)
    #     mc.move(0, 5,0, ikFkSwitch[2], r=1)
    
    #     mc.parentConstraint("%s_arm03Bind_JNT" % side, ikFkSwitch[1], mo=1)
    #     mc.select(ikFkSwitch[0])
    #     mc.addAttr(at="float", k=1, ln="ikFkSwitch", max=1, min=0, dv=0)

    #     # Reverse IK FK switch attribute's value:
    #     reversalNodeIkFk = mc.createNode("plusMinusAverage", 
    #                     n="%s_ikFkReversedValue_PMA" % side)
    #     mc.setAttr(reversalNodeIkFk + ".operation", 2)
    #     mc.setAttr(reversalNodeIkFk + ".input1D[0]", 1)
    #     mc.connectAttr(ikFkSwitch[0] + ".ikFkSwitch", reversalNodeIkFk + ".input1D[1]")

    #     # Connect IK/Fk Switch to parent constraints:
    #     for parCon in bindChainParentConstraints:
    #         mc.connectAttr(ikFkSwitch[0] + ".ikFkSwitch", parCon + ".w1")
    #         mc.connectAttr(reversalNodeIkFk + ".output1D", parCon +".w0")

    #     # Connect IK/FK Switch to control visibility:
    #     for ctl in ikCtlsList:
    #         mc.connectAttr(reversalNodeIkFk + ".output1D", ctl[0] + ".v")
        
    #     for ctl in fkCtlsList:
    #          mc.connectAttr(ikFkSwitch[0] + ".ikFkSwitch", ctl[0] + ".v")
  

 

main()