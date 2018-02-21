#import veroPythonScripts.mayalib.VM_rotationOrder as vmRotOrder
#reload(vmRotOrder)


import maya.cmds as mc

selection = mc.ls(sl=True)

for s in selection:
    mc.addAttr(longName="RotOrder", at="enum", enumName= "xyz:yzx:zxy:xzy:yxz:zyx", h=False, k=False)
    mc.setAttr("{}.RotOrder" .format(s), channelBox=True)
    mc.connectAttr("{}.RotOrder" .format(s), "{}.rotateOrder" .format(s))
