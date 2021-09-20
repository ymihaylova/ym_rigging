from maya import cmds as mc
from ...common import control, attr
from ..base import BaseComponent

class TeethComponent(BaseComponent):
    def __init__(self):
        super(TeethComponent, self).__init__()

        DEBUG_MODE = mc.getAttr("C_top_CTL.debugMode")

        # create a simple translation/rotation control for the upper teet and joints
        for side in ["Upper", "Lower"]:
            jnt = "C_teeth%s_JNT" % side
            ctl, ofs, grp = control.buildControl("C", "teeth%s" % side, guide=jnt)
            mc.rotate(90, 0, -90, ctl + ".cv[*]")
            mc.scale(0, 1.6, 1, ctl + ".cv[*]")
            mc.parent("C_teeth%s_JNT" % side, ctl)
            mc.connectAttr("C_jaw_CTL.mcv", ctl + ".v")
            if side == "Upper":
                mc.parent(grp, "C_head_CTL")
            else:
                mc.parent(grp, "C_jaw_CTL")

            if DEBUG_MODE == False:
                mc.setAttr(jnt + ".v", 0)
                attr.lockAndHide(ctl, [".sxyz", ".v"])
