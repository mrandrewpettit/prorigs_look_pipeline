import maya.cmds as mc
import maya.mel as mel

def bake_uv_tranfer():
    sel = mc.ls(sl=True)
    src = sel[0]
    trg = sel[-1]
    mc.polyTransfer(trg, uv=1, ao=src)
    mc.select(sel[-1])
    mel.eval('doBakeNonDefHistory(1, {"prePost"});')
    
bake_uv_tranfer()