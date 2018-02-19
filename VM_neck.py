WIN = "neckwin"

def neck(*args):
    neckJJ = mc.ls(sl=True)

    if len(neckJJ) < 2:
        om.MGlobal.displayError("Please select the neck hierarchy joints!")

    elif len(neckJJ) > 2:
        om.MGlobal.displayError("Please select just the neck hierarchy joints!")

    else:
        neckcc = mc.circle(n="neck_CC", r=3, nr=(0, 1, 0))
        temp = mc.pointConstraint(neckJJ[0], neckcc, maintainOffset=0)
        mc.delete(temp)
        temp_pos = mc.xform(neckcc, translation=True, query=True, worldSpace=True)
        # zero out
        neckcc_off = mc.group(n="grpNeck_CCZERO", empty=True)
        mc.setAttr("{}.overrideEnabled".format(neckcc_off), 1)
        mc.setAttr("{}.overrideColor".format(neckcc_off), 18)
        mc.xform(neckcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.parent(neckcc, neckcc_off)
        mc.setAttr("{}.translate".format(neckcc[0]), 0, 0, 0)
        mc.xform("grpNeck_CCZERO", cpc=1)
        mc.setAttr(neckcc[0] + ".tx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".ty", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".tz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(neckcc[0] + ".v", lock=True, keyable=False, channelBox=False)
        mc.orientConstraint(neckcc, neckJJ[0], maintainOffset=1)
        #
        grp= mc.group(n="neck_GRP", empty=True)
        temp = mc.pointConstraint(neckJJ[0], grp, maintainOffset=0)
        mc.delete(temp)
        mc.parent(neckJJ[0], neckcc_off, grp)

        #Rename joints:
        mc.rename(neckJJ[0], "neck_01_JJ")
        mc.rename(neckJJ[1], "neck_02_JE")

