import maya.cmds as mc
import maya.OpenMaya as om

WIN="AutoHead"

def UI():
    # Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title= "VM Head Rig", h=100, w=300, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2)
    mc.text("1- Please make sure the neck and/or spine rigs are already done.", h=20)
    mc.setParent('..')
    mc.text("2- Select the entire head hierarchy of ORIENTED joints.", h=20, al="left" )
    mc.separator(h=10)
    mc.setParent('..')

    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.radioCollection()
    mc.radioButton("eyes", label= "Create eyes rig:")
    mc.separator(h=10)
    mc.text("Attach HeadSpace to:", align="left", h=20)
    mc.radioCollection()
    mc.radioButton("spaceChoiceA", l="Neck (default)")
    mc.radioButton("spaceChoiceB", l="Spine (if there isn't a neck)")
    mc.setParent('..')
    #
    mc.columnLayout(adj=True)
    mc.button(label= "Head Auto", w=100, h=40, c=head, bgc=(.2,.2,.2) )
    mc.setParent('..')

    mc.showWindow(WIN)

def head(*args):
    headJJ = mc.ls(sl=True)

    if len(headJJ) < 6:
        om.MGlobal.displayError("Please select the entire head hierarchy")

    elif len(headJJ) > 6:
        om.MGlobal.displayError("Please select just the head hierarchy")

    else:

        #head control
        headcc = mc.circle(n="head_CC", r=3, nr=(0, 1, 0))
        temp = mc.pointConstraint(headJJ[0], headcc, maintainOffset=0)
        mc.delete(temp)
        mc.addAttr(headcc, ln="HeadSpace", attributeType="enum", enumName="NECK:COG:ROOT", k=True, h=False)
        temp_pos = mc.xform(headcc, translation=True, query=True, worldSpace=True)
        # zero out
        headcc_off = mc.group(n="grpHead_CCZERO", empty=True)
        mc.setAttr("{}.overrideEnabled".format(headcc_off), 1)
        mc.setAttr("{}.overrideColor".format(headcc_off), 18)
        mc.xform(headcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.parent(headcc, headcc_off)
        mc.setAttr("{}.translate".format(headcc[0]), 0, 0, 0)
        mc.xform(headcc_off, cpc=1)
        mc.setAttr(headcc[0] + ".tx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".ty", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".tz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(headcc[0] + ".v", lock=True, keyable=False, channelBox=False)
        mc.orientConstraint(headcc, headJJ[0], maintainOffset=1)

        #lo head control
        loheadcc = mc.circle(n="LoHead_CC", r=2, nr=(0, 1, 0))
        temp = mc.pointConstraint(headJJ[1], loheadcc, maintainOffset=0)
        mc.delete(temp)
        temp_pos = mc.xform(loheadcc, translation=True, query=True, worldSpace=True)
        # zero out
        loheadcc_off = mc.group(n="grpLoHead_CCZERO", empty=True)
        mc.setAttr("{}.overrideEnabled".format(loheadcc_off), 1)
        mc.setAttr("{}.overrideColor".format(loheadcc_off), 18)
        mc.xform(loheadcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.parent(loheadcc, loheadcc_off)
        mc.setAttr("{}.translate".format(loheadcc[0]), 0, 0, 0)
        mc.xform(loheadcc_off, cpc=1)
        mc.setAttr(loheadcc[0] + ".sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(loheadcc[0] + ".sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr(loheadcc[0] + ".sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(loheadcc[0] + ".v", lock=True, keyable=False, channelBox=False)
        mc.parentConstraint(loheadcc, headJJ[1], maintainOffset=1)

        #jaw control
        jawcc = mc.circle(n="jaw_CC", r=1, nr=(0, 0, 1))
        mc.hilite(jawcc[0])
        mc.select("{}.cv[1]".format(jawcc[0]), r=True)
        mc.softSelect(ssd=1.740202, sud=19)
        mc.move(0, -1.331663, 0, r=True, wd=True)
        temp = mc.parentConstraint(headJJ[3], jawcc, maintainOffset=0)
        mc.delete(temp)
        temp_pos = mc.xform(jawcc, translation=True, query=True, worldSpace=True)
        # zero out
        jawcc_off = mc.group(n="grpJaw_CCZERO", empty=True)
        mc.setAttr("{}.overrideEnabled".format(jawcc_off), 1)
        mc.setAttr("{}.overrideColor".format(jawcc_off), 9)
        mc.xform(jawcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.parent(jawcc, jawcc_off)
        mc.setAttr("{}.translate".format(jawcc[0]), 0, 0, 0)
        mc.xform(jawcc_off, cpc=1)
        mc.setAttr(jawcc[0] + ".rx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".ry", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".rz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr(jawcc[0] + ".v", lock=True, keyable=False, channelBox=False)
        #
        jaw = mc.ls(headJJ[2:4])
        mc.select(jaw)
        jawik= mc.ikHandle(n="jaw_IKSC", solver="ikSCsolver")
        mc.parent(jawik[0], jawcc)
        mc.hide(jawik[0])

        # Parent
        mc.parent(jawcc_off, loheadcc_off, headcc)
        grp= mc.group(n="head_GRP", empty=True)
        temp = mc.pointConstraint(headJJ[0], grp, maintainOffset=0)
        mc.delete(temp)
        mc.parent(headJJ[0], headcc_off, grp)

        # eyes control
        if mc.radioButton("eyes", query=True, select=True):

            #mirror eye joint
            mc.select(headJJ[5])
            mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
            mc.select("L_eye", "R_eye")
            eyeJts= mc.ls(sl=True)
            mc.select(cl=True)
            #create controllers
            Leye= mc.circle(n="L_eye_CC", nr=(0, 0, 1), c=(2, 0, 0))
            temp_pos = mc.xform(Leye, translation=True, query=True, worldSpace=True)
            #zeroOut
            Leye_off = mc.group(n="grpL_eye_CCZERO", empty=True)
            mc.setAttr("{}.overrideEnabled".format(Leye_off), 1)
            mc.setAttr("{}.overrideColor".format(Leye_off), 6)
            mc.xform(Leye_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
            mc.parent(Leye, Leye_off)
            mc.setAttr("{}.translate".format(Leye[0]), 0, 0, 0)
            mc.xform(Leye[0], Leye_off, cpc=1)
            mc.setAttr(Leye[0] + ".rx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".ry", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".rz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".sx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".sy", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".sz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Leye[0] + ".v", lock=True, keyable=False, channelBox=False)
            #
            Reye = mc.circle(n="R_eye_CC", nr=(0, 0, 1), c=(-2, 0, 0) )
            temp_pos = mc.xform(Leye, translation=True, query=True, worldSpace=True)
            # zeroOut
            Reye_off = mc.group(n="grpR_eye_CCZERO", empty=True)
            mc.setAttr("{}.overrideEnabled".format(Reye_off), 1)
            mc.setAttr("{}.overrideColor".format(Reye_off), 13)
            mc.xform(Reye_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
            mc.parent(Reye, Reye_off)
            mc.setAttr("{}.translate".format(Leye[0]), 0, 0, 0)
            mc.xform(Reye[0], Reye_off, cpc=1)
            mc.setAttr(Reye[0] + ".rx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".ry", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".rz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".sx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".sy", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".sz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(Reye[0] + ".v", lock=True, keyable=False, channelBox=False)
            #
            visor = mc.circle(n="visor_CC", nr=(0, 0, 1))
            mc.hilite(visor[0])
            mc.select("{}.cv[0:7]".format(visor[0]), r=True)
            mc.scale(2.17, 2.17, 2.17, r=True, p=(0, 0, 0) )
            mc.scale(1.82, 1, 1, r=True, p=(0, 0, 0) )
            mc.select("{}.cv[1]".format(visor[0]), "{}.cv[5]".format(visor[0]) )
            mc.scale(1, 0.2, 1, r=True, p=(0, 0, 0) )
            mc.select("{}.cv[2]".format(visor[0]), "{}.cv[4]".format(visor[0]) )
            mc.scale(1, 1.2, 1, r=True, p=(0, 0, 0) )
            mc.select("{}.cv[0]".format(visor[0]), "{}.cv[6]".format(visor[0]) )
            mc.scale(1, 1.2, 1, r=True, p=(0, 0, 0) )
            temp_pos = mc.xform(Leye, translation=True, query=True, worldSpace=True)
            # zeroOut
            visor_off = mc.group(n="grpVisor_CCZERO", empty=True)
            mc.setAttr("{}.overrideEnabled".format(visor_off), 1)
            mc.setAttr("{}.overrideColor".format(visor_off), 17)
            mc.xform(visor_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
            mc.parent(visor,visor_off)
            mc.setAttr("{}.translate".format(Leye[0]), 0, 0, 0)
            mc.xform(visor_off, cpc=1)
            mc.setAttr(visor[0] + ".rx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".ry", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".rz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".sx", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".sy", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".sz", lock=True, keyable=False, channelBox=False)
            mc.setAttr(visor[0] + ".v", lock=True, keyable=False, channelBox=False)

            #Connect controllers to joints
            mc.aimConstraint(Leye[0], eyeJts[0], mo=1, weight=1, aimVector=(1,0, 0), upVector= (0, 0, 1),
                                                worldUpType="object", worldUpObject= "head_CC")
            mc.aimConstraint(Reye[0], eyeJts[1], mo=1, weight=1, aimVector=(1, 0, 0), upVector=(0, 0, 1),
                             worldUpType="object", worldUpObject="head_CC")

            #eyes hierarchy
            mc.parent(Leye_off, Reye_off, visor)
            temp=mc.pointConstraint(eyeJts, visor_off, mo=0)
            mc.delete(temp)
            mc.parent(visor_off, grp)

        else:
            mc.delete("L_eye")

        # head space
        neckLoc = mc.spaceLocator(n="headspace_NECK_LOC")
        temp = mc.pointConstraint(headJJ[0], neckLoc, mo=0)
        mc.delete(temp)
        cogLoc = mc.spaceLocator(n="headspace_COG_LOC")
        temp = mc.pointConstraint(headJJ[0], cogLoc, mo=0)
        mc.delete(temp)
        rootLoc = mc.spaceLocator(n="headspace_ROOT_LOC")
        temp = mc.pointConstraint(headJJ[0], rootLoc, mo=0)
        mc.delete(temp)
        #
        orient = mc.orientConstraint(neckLoc, cogLoc, rootLoc, grp, mo=1)

        # SDK de los locators al head space attr:
        mc.setAttr("{}.HeadSpace".format(headcc[0]), 0)  # neck space
        mc.setAttr("{}.headspace_NECK_LOCW0".format(orient[0]), 1)
        mc.setAttr("{}.headspace_COG_LOCW1".format(orient[0]), 0)
        mc.setAttr("{}.headspace_ROOT_LOCW2".format(orient[0]), 0)
        mc.setDrivenKeyframe("{}.headspace_NECK_LOCW0".format(orient[0]), "{}.headspace_COG_LOCW1".format(orient[0]),
                             "{}.headspace_ROOT_LOCW2".format(orient[0]), cd="{}.HeadSpace".format(headcc[0]))
        #
        mc.setAttr("{}.HeadSpace".format(headcc[0]), 1)  # cog space
        mc.setAttr("{}.headspace_NECK_LOCW0".format(orient[0]), 0)
        mc.setAttr("{}.headspace_COG_LOCW1".format(orient[0]), 1)
        mc.setAttr("{}.headspace_ROOT_LOCW2".format(orient[0]), 0)

        mc.setDrivenKeyframe("{}.headspace_NECK_LOCW0".format(orient[0]), "{}.headspace_COG_LOCW1".format(orient[0]),
                             "{}.headspace_ROOT_LOCW2".format(orient[0]), cd="{}.HeadSpace".format(headcc[0]))
        #
        mc.setAttr("{}.HeadSpace".format(headcc[0]), 2)  # root space
        mc.setAttr("{}.headspace_NECK_LOCW0".format(orient[0]), 0)
        mc.setAttr("{}.headspace_COG_LOCW1".format(orient[0]), 0)
        mc.setAttr("{}.headspace_ROOT_LOCW2".format(orient[0]), 1)

        mc.setDrivenKeyframe("{}.headspace_NECK_LOCW0".format(orient[0]), "{}.headspace_COG_LOCW1".format(orient[0]),
                             "{}.headspace_ROOT_LOCW2".format(orient[0]), cd="{}.HeadSpace".format(headcc[0]))

        mc.setAttr("{}.HeadSpace".format(headcc[0]), 0)  # get back to default

        # headspace hierarchy
        mc.parent(cogLoc, "COG_CC")
        mc.parent(rootLoc, "move_CC")

        if mc.radioButton("spaceChoiceA", query=True, select=True):
            mc.pointConstraint("neck_02_JE", grp, mo=1)
            mc.parent(neckLoc, "neck_CC")

        elif mc.radioButton("spaceChoiceB", query=True, select=True):
            mc.pointConstraint("spine_IK_02_CC", grp, mo=1)
            mc.parent(neckLoc, "spine_IK_02_CC")

        else:
            om.MGlobal.displayWarning("HeadSpace locators relocation was skipped")

        #rename head joints
        mc.rename(headJJ[0], "head_01_JJ")
        mc.rename(headJJ[1], "head_02_JJ")
        mc.rename(headJJ[2], "jaw_01_JJ")
        mc.rename(headJJ[3], "jaw_02_JJ")
        mc.rename(headJJ[4], "head_03_JE")
        mc.rename(eyeJts[0], "L_eye_JJ")
        mc.rename(eyeJts[1], "R_eye_JJ")


