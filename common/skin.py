from maya import cmds as mc
from . import attr

def addToSkinJoints(joint, skinJointsMessageAttr="C_top_CTL.skinJoints"):
    jointMessageAttr = attr.addAttr(joint, ln="skinJoint", at="message")
    mc.connectAttr(skinJointsMessageAttr, jointMessageAttr)
