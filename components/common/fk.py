from maya import cmds as mc
from ...common import control, attr
from ..base import BaseComponent

class FkComponent(BaseComponent):
    def __init__(self, side, name, joints, parent):
        super(FkComponent, self).__init__()
        self.joints = joints
        self.build(side, name, joints, parent)
        self.lock()

    def build(self, side, name, joints, parent):
        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        grp = mc.createNode("transform", n="%s_%s_GRP" % (side, name))
        mc.parent(joints[0], grp)
        mc.parent(grp, parent)
        ctlParent = grp
        self.controls = []
        for i, joint in enumerate(joints[:-1]):
            ctl, ofs, grp = control.buildControl(side, "%s%02d" % (name, i), joint)
            self.controls.append(ctl)

            mc.parentConstraint(ctl, joint, mo=0)
            mc.parent(grp, ctlParent)
            ctlParent = ctl

    def lock(self):
        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        for ctl in self.controls:
            if DEBUG_MODE == False:
                attr.lockAndHide(ctl, [".txyz", ".sxyz", ".v"])

        if DEBUG_MODE == False:
            mc.setAttr(self.joints[0] + ".v", 0)
