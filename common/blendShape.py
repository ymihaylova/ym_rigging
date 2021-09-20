from maya import cmds as mc
import os

def loadBlendShapes(geo, fileName, path):
    return mc.blendShape(
        geo, n=geo.rsplit("_", 1)[0] + "_BLS",
        ip=os.path.join(path, fileName))[0]

