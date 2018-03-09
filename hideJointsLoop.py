import maya.cmds as mc


joints= mc.ls(sel=True)

for j in joints:
  mc.setAttr(j + '.drawStyle', 2)
  

#body control shape colors should be: see existing body controls:
#center_primary=17, center_secondary=21, left_primary=6, left_secondary=18, right_primary=13, right_secondary=12

for 
mc.setAttr("{}.overrideEnabled".format(), 1)
mc.setAttr("{}.overrideColor".format(), 6)
