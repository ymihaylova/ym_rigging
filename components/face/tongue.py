from maya import cmds as mc
from ..common import fk

class TongueComponent(fk):
    def __init__(self, side, name, joints, parent, visibilityAttr):
        self.visibilityAttr = visibilityAttr
        super(TongueComponent, self).__init__(side, name, joints, parent)

    def build(self, side, name, joints, parent):
        super(TongueComponent, self).build(side, name, joints, parent)

        for ctl in self.controls:
            mc.rotate(0, 90, 0, ctl + ".cv[*]")
            mc.scale(1, 1.5, 3.5, ctl + ".cv[*]")
            mc.connectAttr(self.visibilityAttr, ctl + ".v")
