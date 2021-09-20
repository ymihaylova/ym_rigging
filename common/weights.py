from maya import cmds as mc

def loadDeformerWeights(fileName, path, deformer):
    mc.deformerWeights(
        fileName, path=path, deformer=deformer, im=1, method="index")
