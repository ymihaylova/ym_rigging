from maya import cmds as mc
from maya.api import OpenMaya as om2
import ctl_shapes as cs

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

SWITCH_SHAPE_CVS = [[-1.0, 0.0, -1.0], 
                    [1.0, 0.0, -1.0],
                    [1.0, 0.0, -2.0],
                    [3.0, 0.0, 0.0],
                    [1.0, 0.0, 2.0],
                    [1.0, 0.0, 1.0],
                    [-1.0, 0.0, 1.0],
                    [-1.0, 0.0, 2.0],
                    [-3.0, 0.0, 0.0],
                    [-1.0, 0.0, -2.0],
                    [-1.0, 0.0, -1.0]]

HIPS_SHAPE_CVS =  [[13.521550917395674, 3.1581145713258447, -8.76270854476018], 
                    [-6.414032771168875e-16, -2.7630149794215506, -8.911075851857634], 
                    [-13.52155091739566, 3.1581145713258447, -8.76270854476019], 
                    [-15.924522426699285, 3.158114571325844, -4.468505684192871e-15], 
                    [-13.52155091739566, 3.158114571325843, 8.76270854476018], 
                    [-3.2159284098157265e-15, -2.7630149794215524, 8.911075851857635], 
                    [13.521550917395636, 3.158114571325843, 8.762708544760192], 
                    [15.924522426699285, 3.158114571325844, 8.559556971168099e-15], 
                    [13.521550917395674, 3.1581145713258447, -8.76270854476018], 
                    [-6.414032771168875e-16, -2.7630149794215506, -8.911075851857634], 
                    [-13.52155091739566, 3.1581145713258447, -8.76270854476019]]
HIPS_SHAPE_KNOTS = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

CHEST_SHAPE_CVS = [[12.157922912047004, 23.28205818338543, -15.489740553421376], 
                    [-5.519651062259706e-15, -9.458901538787543, -15.583216846085413], 
                    [-12.157922912046995, 23.28205818338543, -15.489740553421377], 
                    [-12.226821724328058, 25.949710441420194, -6.616584791811977], 
                    [-12.157922912046995, 23.28205818338543, 2.2565709697974317], 
                    [-1.0890122449525352e-14, -9.458901538787543, 9.513857592148566], 
                    [12.157922912046988, 23.28205818338543, 2.2565709697974334], 
                    [12.226821724328058, 25.949710441420194, -6.616584791811967], 
                    [12.157922912047004, 23.28205818338543, -15.489740553421376], 
                    [-5.519651062259706e-15, -9.458901538787543, -15.583216846085413], 
                    [-12.157922912046995, 23.28205818338543, -15.489740553421377]]
CHEST_SHAPE_KNOTS = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

SPINEMID_SHAPE_CVS = [[11.97727846744739, 7.333967868827961e-16, -9.744127355522792],
                    [-1.7713046701598608e-15, 7.183548693826223e-16, -9.54427597573159], 
                    [-11.977278467447366, 7.333967868827967e-16, -9.744127355522796], 
                    [-11.73162531242101, 2.081612693272302e-31, -7.14763447638548e-15], 
                    [-11.977278467447382, -7.333967868827963e-16, 9.744127355522792], 
                    [-3.967834159940196e-15, -7.183548693826232e-16, 9.54427597573159], 
                    [11.97727846744736, -7.333967868827967e-16, 9.744127355522796], 
                    [11.73162531242101, -3.858298016650096e-31, 1.943393706603877e-15], 
                    [11.97727846744739, 7.333967868827961e-16, -9.744127355522792], 
                    [-1.7713046701598608e-15, 7.183548693826223e-16, -9.54427597573159], 
                    [-11.977278467447366, 7.333967868827967e-16, -9.744127355522796]]
SPINEMID_SHAPE_KNOTS = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

SPINEFK_SHAPE_CVS = [[13.432212793806672, 5.639242577694782e-16, -6.602030440243778], 
                    [-1.8407667716785875e-15, 7.97509333488778e-16, -9.33668098779277], 
                    [-13.432212793806666, 5.639242577694787e-16, -6.602030440243781], 
                    [-18.996017505682797, 2.310982527368571e-31, -1.9511143632069017e-15], 
                    [-13.432212793806666, -5.639242577694785e-16, 6.6020304402437775], 
                    [-5.397419113399601e-15, -7.97509333488778e-16, 9.336680987792771], 
                    [13.432212793806665, -5.639242577694787e-16, 6.602030440243781], 
                    [18.996017505682797, -4.283438187457663e-31, 5.769171773668925e-15], 
                    [13.432212793806672, 5.639242577694782e-16, -6.602030440243778], 
                    [-1.8407667716785875e-15, 7.97509333488778e-16, -9.33668098779277], 
                    [-13.432212793806666, 5.639242577694787e-16, -6.602030440243781]]
SPINEFK_SHAPE_KNOTS = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
 


class SpineComponent:
    def __init__(self, jointChain, curve):
        self.build(jointChain, curve)
    
    def build(self, jointChain, curve):
        # Clusters and controls:
        spineCtls = []
        spineCtlsGrps = []
        names = ["hips", "spineMid", "chest"]
        shapes = [HIPS_SHAPE_CVS, SPINEMID_SHAPE_CVS, CHEST_SHAPE_CVS]
        shapeKnotsList = [HIPS_SHAPE_KNOTS, SPINEMID_SHAPE_KNOTS, CHEST_SHAPE_KNOTS]
        hipFkCtl, hipFkGrp = [], []
        spineMidFkCtl, spineMidFkGrp = [], []
        #Root Ctl:        
        rootCtl, _, rootGrp=buildControl("C", "root", "C_spine00_JNT", \
                shapeCVs=SPINEMID_SHAPE_CVS, shapeKnots=SPINEMID_SHAPE_KNOTS)
        mc.scale(1.5, 1.5, 1.5, rootCtl +".cv[*]")
        mc.rotate(0, 0, 0, rootGrp, ws=1)

        for counter, cvIDs in enumerate(["0:1", "2", "3:4"]):
            cvs = curve + ".cv[%s]" % cvIDs

            _, clusterHandle = mc.cluster(cvs, name="C_spine%s_CLS" % \
                            str(counter).zfill(2))
            ctl, _, group = buildControl("C", names[counter], clusterHandle, \
                    shapeCVs=shapes[counter],shapeKnots=shapeKnotsList[counter], degree=3)
            if counter != 1:
                #Create a "FK like" hip control
                if counter == 0:
                    hipFkCtl, _, hipFkGrp = buildControl("C", "hipFk", clusterHandle, \
                            shapeCVs=SPINEFK_SHAPE_CVS, shapeKnots=SPINEFK_SHAPE_KNOTS, colour=9)
                # Create a hips/chest joint, reposition to ctl location and parent:
                joint = mc.createNode("joint",name = "C_%s_JNT" % names[counter])
                mc.delete(mc.parentConstraint(ctl, joint, mo=0))
                mc.parent(joint, ctl)
            if counter == 1:
                spineMidFkCtl, _, spineMidFkGrp = buildControl("C", "spineMidFk", clusterHandle, \
                        shapeCVs=SPINEFK_SHAPE_CVS, shapeKnots=SPINEFK_SHAPE_KNOTS, colour=9)    
            
            spineCtls.append(ctl)
            spineCtlsGrps.append(group)
            # Parent cluster under ctl:
            mc.parent(clusterHandle, ctl)

            if not DEBUG_MODE:
                mc.hide(joint, clusterHandle)
        #Parenting Controls
        mc.parent(hipFkGrp, spineCtlsGrps[0], rootCtl)
        mc.parent(spineMidFkGrp, hipFkCtl)
        mc.parent(spineCtlsGrps[1:], spineMidFkCtl)
        mc.parent(jointChain[0], rootCtl)
        #Spine stretch setup
        #Claculating spine length  
        spineLen = mc.createNode("curveInfo", n="C_spineLen_INF")
        mc.connectAttr(curve +"Shape.worldSpace", spineLen + ".inputCurve")
        staticSpineLen = mc.getAttr(spineLen + ".arcLength")
        #Calcualting stretch factor:
        stretchFactor = mc.createNode("multiplyDivide", n="C_spineStretchFactor_MDV")
        mc.connectAttr(spineLen + ".arcLength", stretchFactor + ".input1.input1X")
        mc.setAttr(stretchFactor + ".input2.input2X", staticSpineLen)
        mc.setAttr(stretchFactor +".operation", 2)
        #Stretching Joints
        jointStretch = mc.createNode("multiplyDivide", n="C_spineJointStretch_MDV")
        mc.connectAttr(stretchFactor + ".output.outputX", jointStretch + ".input1.input1X")
        mc.setAttr(jointStretch + ".input2.input2X", mc.getAttr("C_spine01_JNT.tx"))
        for jnt in jointChain:
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
        #Spline IK handle:
        splineIkh, _ = mc.ikHandle(sj="C_spine00_JNT", ee="C_spine04_JNT", \
                    solver="ikSplineSolver", createCurve=0, curve=curve)
        splineIkh = mc.rename(splineIkh, "C_spine_IKH")
        mc.hide(splineIkh)
        mc.parent(splineIkh, rootCtl)

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

def buildControl(side, name, guide=None, shapeCVs=[], shapeKnots=None, degree=1, colour=17):
    if not shapeCVs:
        control = mc.circle(constructionHistory=0)[0]
    else:
        if not shapeKnots:
            control = mc.curve(p=shapeCVs, degree=degree)
        else:
            control = mc.curve(p=shapeCVs, knot=shapeKnots, periodic=1)
    offset = mc.group(control)
    group = mc.group(offset)
    #Temporary ugly fix:
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

    # Create IK copy of the blend chain
    ikChain = mc.duplicate("%s_%s00_JNT" % (side, name), renameChildren=1)
    renamedIkChain = []
    for jnt in ikChain:
        renamedIkChain.append(mc.rename(jnt, jnt.replace("_JNT", "Ik_JNT")[:-1]))
        
    ikChain = renamedIkChain

    limbGrp = mc.group(blendChain[0], ikChain[0])
    limbGrp = mc.rename(limbGrp, "%s_%s_GRP" % (side, name))
    mc.parent(limbGrp, parent)

    if not DEBUG_MODE:
        mc.hide(blendChain, ikChain)

    return blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain

def limbStretch(side, name, startEnd, endControl, conditional=1):
    #NOTE: cycles as 1st transform is currently parented under 1st joint - 
    #to be moved to a IK base ctl when this is created.
    #Create a transform to locate start of stretchable chain
    print(startEnd)
    startPoint = mc.createNode("transform", n=startEnd[0][:-4] + "_TRN")
    mc.parent(startPoint, startEnd[0], r=1) #Parent to start joint and snap location 
    #Create a transform to locate end of stretchable chain
    endPoint = mc.createNode("transform", n=startEnd[-1][:-4]+"_TRN")
    mc.parent(endPoint, endControl, r=1)
    
    #Calculate actual length:
    length = 0
    for jnt in startEnd[1:]:
        length += mc.getAttr(jnt + ".tx")

    # Calculate stretch factor
    stretchDistance = mc.createNode("distanceBetween", n="%s_%sStretched_DB" %(side, name))
    mc.connectAttr(startPoint + ".worldMatrix", stretchDistance + ".inMatrix1")
    mc.connectAttr(endPoint + ".worldMatrix", stretchDistance + ".inMatrix2")
    stretchFactor = mc.createNode("multiplyDivide", n="%s_%sStretchFactor_MDV" %(side, name))
    mc.connectAttr(stretchDistance + ".distance", stretchFactor + ".input1.input1X")
    mc.setAttr(stretchFactor + ".input2.input2X", length)
    mc.setAttr(stretchFactor + ".operation", 2)
    
    if conditional == 0:
        jointStretchMDVsList = []
        for jnt in startEnd[1:]:
            jointStretch = mc.createNode("multiplyDivide", n="%s_%s%sIndividualStretch_MDV" % (side, name, str(startEnd.index(jnt)).zfill(2)))
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(stretchFactor + ".output.outputX", jointStretch + ".input2.input2X")
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
            jointStretchMDVsList.append(jointStretch)
    
    else:
        isLimbStretched = mc.createNode("condition", n="%s_%sIsStretched_CD" %(side, name))
        mc.connectAttr(stretchFactor + ".output.outputX", isLimbStretched + ".firstTerm")
        mc.connectAttr(stretchFactor + ".output.outputX", isLimbStretched + ".colorIfTrue.colorIfTrueR")
        mc.setAttr(isLimbStretched + ".secondTerm", 1)
        mc.setAttr(isLimbStretched + ".operation", 2)

        jointStretchMDVsList = []
        for jnt in startEnd[1:]:
            jointStretch = mc.createNode("multiplyDivide", n="%s_%s%sIndividualStretch_MDV" % (side, name, str(startEnd.index(jnt)).zfill(2)))
            jntTx = mc.getAttr(jnt + ".tx")
            mc.setAttr(jointStretch + ".input1.input1X", jntTx)
            mc.connectAttr(isLimbStretched + ".outColorR", jointStretch + ".input2.input2X")
            mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")
            jointStretchMDVsList.append(jointStretch) 
    # mc.setAttr(jointStretch + ".input2.input2X", mc.getAttr("C_spine01_JNT.tx"))
    
    # for jnt in jointChain:
    #     mc.connectAttr(jointStretch + ".output.outputX", jnt + ".tx")


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
    #Get joints influencing the IK handle and call poleVectorPos() on them
    jointList = mc.ikHandle(ikHandle, q=True, jointList=True)
    jointList.append(mc.listRelatives(jointList[-1], children=True, type="joint")[0])

    rootJntPos = mc.xform(jointList[0], q=1, ws=1, t=1)
    midJntPos = mc.xform(jointList[1], q=1, ws=1, t=1)
    endJntPos = mc.xform(jointList[2], q=1, ws=1, t=1)

    poleVectorPos = getPoleVectorPosition(rootJntPos, midJntPos, endJntPos)

    return poleVectorPos

def parentConstrain(driven, *args, **kwargs):
    constraintsList = []
    for arg in args:
        for comp, driver in zip(driven, arg):
            parCon = mc.parentConstraint(driver, comp, **kwargs)[0]
            if parCon not in constraintsList:
                constraintsList.append(parCon)
    return constraintsList

def main():
    #Create a new file and import model and guides 
    mc.file(new=1, force=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_body.ma", i=1)
    mc.file("/Desktop/projectFolder/HPScripted/scenes/hp_guides.ma", i=1)

    #Housekeeping setup:
    harryCtl, _, _ = buildControl("C", "harry", shapeCVs=SQUARE_SHAPE_CVS)
    mc.scale(15, 15, 15, harryCtl + ".cv[*]")
    ctlsGrp = mc.group(em=1)
    ctlsGrp = mc.rename(ctlsGrp, "ctls_GRP")
    rigGrp = mc.group(em=1)
    rigGrp = mc.rename(rigGrp, "rig_GRP")

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
        mc.parent(ikCtlsGrp, ctlsGrp)

        #Make limb stretchable:
        limbStretch(side, "leg", ikChain[:-2], footIkCtl)
        # Create parent constraints to bind skeleton:
        blendChainParentConstraints = parentConstrain(blendChain[:-1], \
                                ikChain[:-1], fkCtlsList, mo=0)
        
        # Create and position IK/FK Switch
        ikFkSwitchCtl, ikFkSwitchOfs, ikFkSwitchGrp = buildControl(side, 
                "legIkFkSwitch", "%s_leg02_JNT" % side, shapeCVs=SWITCH_SHAPE_CVS)

        mc.rotate(90, 0, 90, ikFkSwitchGrp, r=1, ws=1)    
        if side=="L":
            mc.move(15, 10,0, ikFkSwitchGrp, r=1)
        else:
            mc.move(-15, -10, 0, ikFkSwitchGrp, r=1)
        mc.parentConstraint("%s_leg02_JNT" % side, ikFkSwitchOfs, mo=1)
        ikFkSwitchAttr = addAttr(ikFkSwitchCtl, at="float", k=1, ln="ikFkSwitch",
                     max=1, min=0, dv=0)

        # Reverse IK FK switch attribute's value:
        reversalNodeIkFk = mc.createNode("plusMinusAverage", 
                        n="%s_legIkFkReversedValue_PMA" % side)
        mc.setAttr(reversalNodeIkFk + ".operation", 2)
        mc.setAttr(reversalNodeIkFk + ".input1D[0]", 1)
        mc.connectAttr(ikFkSwitchAttr, reversalNodeIkFk + ".input1D[1]")

        # Connect IK/Fk Switch to parent constraints:
        for parCon in blendChainParentConstraints:
            mc.connectAttr(ikFkSwitchAttr, parCon + ".w1")
            mc.connectAttr(reversalNodeIkFk + ".output1D", parCon +".w0")

        # Connect IK/FK Switch to control visibility:
        mc.connectAttr(reversalNodeIkFk + ".output1D", ikCtlsGrp + ".v")
        mc.connectAttr(ikFkSwitchAttr, fkCtlsGrpList[0] + ".v")
        #Place switch in the hierarchy
        mc.parent(ikFkSwitchGrp, "%s_leg_GRP" % side)

     # Build arm FK ctls. IK chain, Handle and Ctls 
    for side in "LR":
                # Build IK chain and FK ctls
        blendChain, fkCtlsList, fkCtlsOfsList, fkCtlsGrpList, ikChain = buildLimb(side, "arm", "C_chest_CTL")
        #Re-size and position FK Ctls
        for fkCtl in fkCtlsList:
            mc.scale(6,6,6,fkCtl + ".cv[*]")
            mc.rotate(0,90,0,fkCtl + ".cv[*]", r=1)

            if fkCtl == fkCtlsList[0]: # move the clavicle FK control CVs for visual clarity
                if side =="L":
                    mc.move(3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                else:
                    mc.move(-3, 0, 0, fkCtl + ".cv[*]", ws=1, r=1)
                mc.scale(1.5,1.5,1.5,fkCtl + ".cv[*]")

        # Build IK wrist control:
        wristIkCtl, _, wristIkGrp = buildControl(side, "arm03Ik", "%s_arm03Ik_JNT" % side, 
                shapeCVs=SQUARE_SHAPE_CVS, colour=18 if side=="L" else 20)
        mc.scale(6,6,6, wristIkCtl + ".cv[*]")
        mc.rotate(0,0,90, wristIkCtl + ".cv[*]", r=1)

        
        # Create IK handle and parent to IK control:
        wristIkHandle, _ = mc.ikHandle(sj="%s_arm01Ik_JNT" % side, \
                        ee="%s_arm03Ik_JNT" % side, sol="ikRPsolver")
        wristIkHandle = mc.rename(wristIkHandle, "%s_arm03_IKH" % side)
        mc.parent(wristIkHandle, wristIkCtl)

        # Build Pole Vector control and create pole vector constraint to leg02IK:
        elbowPoleVectorCtl, _, elbowPoleVectorGrp = buildControl(side, \
                            "elbowPoleVector", "%s_arm02Ik_JNT" % side,\
                            shapeCVs=DIAMOND_SHAPE_CVS, colour=18 if side=="L" else 20)
        
        elbowPoleVectorPos = getIkhPoleVecPos(wristIkHandle)
        mc.scale(4,4,4, elbowPoleVectorCtl + ".cv[*]")
        mc.move(elbowPoleVectorPos.x, elbowPoleVectorPos.y, elbowPoleVectorPos.z, 
                        elbowPoleVectorGrp)
        mc.poleVectorConstraint(elbowPoleVectorCtl, wristIkHandle)

        # #Make limb stretchable:
        limbStretch(side, "arm", ikChain[1:-1], wristIkCtl)
        
        ikCtlsGrp = mc.group(elbowPoleVectorGrp, wristIkGrp, n="%s_armIkCtls_GRP"\
                 % side, w=1)
        mc.parent(ikCtlsGrp, ctlsGrp)

        # Create parent constraints to bind skeleton:
        blendChainParentConstraints = parentConstrain(blendChain[:-1], fkCtlsList,\
                                ikChain[:-1], mo=0)
        
        # Create and position IK/FK Switch 
        # NOTE: to be turned into a function useable by both arms and legs?
        # Create and position IK/FK Switch
        ikFkSwitchCtl, ikFkSwitchOfs, ikFkSwitchGrp = buildControl(side, 
                "armIkFkSwitch", "%s_arm03_JNT" % side, shapeCVs=SWITCH_SHAPE_CVS)
        mc.move(0, 10, -10, ikFkSwitchGrp, r=1, ws=1)
        mc.rotate(90, 0, 0, ikFkSwitchGrp, ws=1, r=1)
        mc.parentConstraint("%s_arm03_JNT" % side, ikFkSwitchOfs, mo=1)
    
        ikFkSwitchAttr = addAttr(ikFkSwitchCtl, at="float", k=1, ln="ikFkSwitch",
                     max=1, min=0, dv=0)

        # Reverse IK FK switch attribute's value:
        reversalNodeIkFk = mc.createNode("plusMinusAverage", 
                        n="%s_armIkFkReversedValue_PMA" % side)
        mc.setAttr(reversalNodeIkFk + ".operation", 2)
        mc.setAttr(reversalNodeIkFk + ".input1D[0]", 1)
        mc.connectAttr(ikFkSwitchAttr, reversalNodeIkFk + ".input1D[1]")

        # Connect IK/Fk Switch to parent constraints:
        for parCon in blendChainParentConstraints:
            mc.connectAttr(ikFkSwitchAttr, parCon + ".w0")
            mc.connectAttr(reversalNodeIkFk + ".output1D", parCon +".w1")

        # Connect IK/FK Switch to control visibility:
        mc.connectAttr(reversalNodeIkFk + ".output1D", ikCtlsGrp + ".v")
        mc.connectAttr(ikFkSwitchAttr, fkCtlsGrpList[0] + ".v")

        mc.parent(ikFkSwitchGrp, "%s_arm_GRP" % side)
    #Housekeeping:
    #Geometry in hierarchy
    mc.setAttr("C_geometry_GRP.inheritsTransform", 0)
    mc.parent("C_geometry_GRP", harryCtl)
    #Spine curve and root in hierarchy
    mc.parent("C_root_GRP", harryCtl)
    mc.parent("C_spine_CRV", harryCtl)
    mc.setAttr("C_spine_CRV.inheritsTransform", 0)

main()