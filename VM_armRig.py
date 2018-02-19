'''
import VM_armRig as vmarm
reload(vmarm)
vmarm.UI()
'''
'''
Version 1 made in January 2018 (week # 1): Arm Rig in basic python
Scripted by Vero Morera, January 2018.
veromc1692@gmail.com
'''

import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel

WIN="AutoArm"

def UI():
    # Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title= "VM_Arm Rig", h=100, w=400, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2, w=100)
    mc.text("Select the clavicle, shoulder, elbow, wrist joints ORIENTED.", h=25)
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.radioCollection()
    mc.radioButton("ikfkex", label="Use existing IK/FK Switcher (Recommended)")
    mc.radioButton("ikfkcc", label="Create IK/FK Switcher")
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button(label= "L Arm Auto", w=100, h=40, c=L_arm, bgc=(.2,.2,.2))
    mc.radioCollection()
    mc.radioButton("rarm", label="Mirror to Right Arm")
    mc.setParent('..')

    mc.showWindow(WIN)


def L_arm(*args):
    origArm = mc.ls(sl=True)
    mc.select(cl=True)
    previous_sel = None

    if len(origArm) < 4:
        om.MGlobal.displayError("Please select the entire leg. (exactly 4 joints)")

    elif len(origArm) > 4:
        om.MGlobal.displayError("Please select just 4 joints!")

    else:
        # JJ RIG
        mc.select(origArm)
        mc.rename(origArm[0], "L_clavicle_JJ")
        mc.rename(origArm[1], "L_shoulder_JJ")
        mc.rename(origArm[2], "L_elbow_JJ")
        mc.rename(origArm[3], "L_wrist_JJ")
        jj = mc.ls(sl=True)

    # (THIS IS FOR THE RIGHT ARM)
        if mc.radioButton("rarm", query=True, select=True):
            mc.select(jj[0])
            mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
            mc.select(hierarchy=True)
            rjj = mc.ls(sl=True)
    # (END OF THE RIGHT ARM)

        # IK RIG
        # Create and rename the ik chain:
        IkChain = mc.duplicate(jj[1], renameChildren=True)
        mc.select(IkChain, hi=True)
        mel.eval('searchReplaceNames JJ1 IK hierarchy')
        ik = mc.ls(sl=True)

        # Create the Iksolver:
        IKRP = mc.ikHandle(name="L_arm_IkRp", solver="ikRPsolver", sj=ik[0], ee=ik[2])

        # Create Controlers
        ikcc = mc.circle(n="L_arm_CC", c=(0, 0, 0), nr=(1, 0, 0), r=1.3, constructionHistory=False)
        mc.makeIdentity(apply=True)
        tempPoint = mc.parentConstraint(ik[2], ikcc, maintainOffset=0)
        mc.delete(tempPoint)
        temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)
        temp_rot = mc.xform(ikcc, rotation=True, query=True, worldSpace=True)
        mc.parent(IKRP[0], ikcc)

        # ZeroOut ikcc
        ikcc_off = mc.group(n="grpL_arm_CCZERO", empty=True)
        mc.setAttr("{}.overrideEnabled".format(ikcc_off), 1)
        mc.setAttr("{}.overrideColor".format(ikcc_off), 6)
        mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.xform(ikcc_off, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
        mc.parent(ikcc, ikcc_off)
        mc.setAttr("{}.translate".format(ikcc[0]), 0, 0, 0)
        mc.setAttr("{}.rotate".format(ikcc[0]), 0, 0, 0)
        mc.xform("grpL_arm_CCZERO", cpc=1)
        mc.setAttr("L_arm_CC.sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_CC.sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_CC.sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_CC.v", lock=True, keyable=False, channelBox=False)
        mc.orientConstraint(ikcc, ik[2], maintainOffset=1)

        # Pole Vector
        ikpv = mc.curve(d=1, n="L_arm_PV", p=[(-0.7, -1.19209e-07, 0.2),(0, 0, -1.19),
                                              (0, 0.7, 0.2),(-0.7, -1.19209e-07, 0.2),
                                              (0, -0.7, 0.2),(0, 0, -1.19),(0.7, 0, 0.2),
                                              (0, -0.7, 0.2),(0.7, 0, 0.2),(0, 0.7, 0.2)])
        mc.makeIdentity(apply=True)
        temp_constraint = mc.pointConstraint(ik[1], ikpv, maintainOffset=0)
        mc.delete(temp_constraint)
        mc.poleVectorConstraint(ikpv, IKRP[0], weight=1)
        temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)

        # ZeroOut ikpv
        ikpv_off = mc.group(ikpv, n="grpL_arm_PVZERO")
        mc.setAttr("{}.overrideEnabled".format(ikpv_off), 1)
        mc.setAttr("{}.overrideColor".format(ikpv_off), 6)
        mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
        mc.setAttr("{}.translate".format(ikpv), 0, 0, 0)
        mc.xform(ikpv_off, cpc=1)
        mc.move(0, 0, -10, ikpv_off, r=True)
        mc.setAttr("L_arm_PV.rx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.ry", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.rz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_arm_PV.v", lock=True, keyable=False, channelBox=False)


        # FK RIG
        # Create and rename the fk chain:
        FkChain = mc.duplicate(jj[1], renameChildren=True)
        mc.select(FkChain)
        mel.eval('searchReplaceNames JJ1 FK hierarchy')
        fk = mc.ls(sl=True)

        for j in fk:
            cc = mc.circle(nr=(1, 0, 0), n=str(j) + "_CC", r=2, constructionHistory=False)
            mc.makeIdentity(apply=True)
            temp_constraint = mc.parentConstraint(j, cc, maintainOffset=0)
            mc.delete(temp_constraint)
            temp_rot = mc.xform(cc, rotation=True, query=True, worldSpace=True)

            # ZeroOut
            offset = mc.group(cc, n=str(j) + "_CCZERO")
            mc.setAttr("{}.overrideEnabled".format(offset), 1)
            mc.setAttr("{}.overrideColor".format(offset), 6)
            mc.xform(offset, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
            mc.setAttr("{}.rotate".format(cc[0]), 0, 0, 0)
            mc.setAttr("{}.tx".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.ty".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.tz".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sx".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sy".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sz".format(cc[0]), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.v".format(cc[0]), lock=True, keyable=False, channelBox=False)

            # fk hierarchy
            mc.orientConstraint(cc, j, maintainOffset=0)
            if previous_sel:
                mc.parent(offset, previous_sel)
            previous_sel = cc

        #clavicle
        clav= mc.circle(nr=(1, 0, 0), n= "L_clavicle_FK_CC", r=2, constructionHistory=False)
        mc.makeIdentity(apply=True)
        temp_constraint = mc.parentConstraint(jj[0], clav, maintainOffset=0)
        mc.delete(temp_constraint)
        temp_rot = mc.xform(clav, rotation=True, query=True, worldSpace=True)
        clav_grp=mc.group(clav, n="L_clavicle_FK_CCZERO")
        mc.setAttr("{}.overrideEnabled".format(clav_grp), 1)
        mc.setAttr("{}.overrideColor".format(clav_grp), 6)
        mc.xform(clav_grp, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
        mc.setAttr("{}.rotate".format(clav[0]), 0, 0, 0)
        mc.orientConstraint(clav, jj[0])
        mc.setAttr("{}.tx".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.ty".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.tz".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.sx".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.sy".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.sz".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.setAttr("{}.v".format(clav[0]), lock=True, keyable=False, channelBox=False)
        mc.parent("L_shoulder_FK_CCZERO","L_clavicle_FK_CC")
        fkhi = mc.ls("L_shoulder_FK_CCZERO")


        # Arm Twist (J.Dobra style)
        #Create the main chains and handles:
        upTwistHandle = mc.duplicate(jj[1], renameChildren=True)
        mc.select(upTwistHandle, hi=True)
        upTwist = mc.ls(sl=True)
        mc.delete(upTwist[2])
        mc.parent(upTwist[0], world=True)
        mc.reroot(upTwist[1]) #this is to invert the order of the chain.
        mc.rename(upTwist[0], "L_upTwist_02_JC")
        mc.rename(upTwist[1], "L_upTwist_01_JC")
        #
        loTwistHandle = mc.duplicate(jj[2], renameChildren=True)
        mc.select(loTwistHandle, hi=True)
        loTwist = mc.ls(sl=True)
        mc.rename(loTwist[0], "L_loTwist_01_JC")
        mc.rename(loTwist[1], "L_loTwist_02_JC")
        #
        mc.parent("L_upTwist_01_JC", jj[1])
        mc.parent("L_loTwist_01_JC", jj[2])
        mc.select("L_upTwist_01_JC", "L_upTwist_02_JC")
        upIKSC= mc.ikHandle(name="L_upTwist_IkSc", solver="ikSCsolver")
        mc.select("L_loTwist_01_JC", "L_loTwist_02_JC")
        loIKSC =mc.ikHandle(name="L_loTwist_IkSc", solver="ikSCsolver")
        mc.parent(upIKSC[0], jj[0])
        mc.parent(loIKSC[0], jj[3])

        #Create the twist joints (inspired by the method of Jay Grenier jgSplitJointChain.mel)

        #UPPERARM:
        # query master twist joints position
        mc.select(cl=True)
        pPos = mc.joint("L_upTwist_01_JC", query=True, position=True)
        cPos = mc.joint("L_upTwist_02_JC", query=True, position=True)
        # Parent Orientation
        ro = mc.joint("L_shoulder_IK", q=True, roo=True)

        # Vector
        numberOfJoints = 4
        jVector = [0, 1, 2] #this is to get a estimate position for each twisting joint.
        jVector[0] = (cPos[0] - pPos[0]) / numberOfJoints
        jVector[1] = (cPos[1] - pPos[1]) / numberOfJoints
        jVector[2] = (cPos[2] - pPos[2]) / numberOfJoints

        # Loop and setup joints
        for i in range(numberOfJoints):
            # Create Joints
            mc.joint(p=(pPos[0] + (i * jVector[0]), pPos[1] + (i * jVector[1]), pPos[2] + (i * jVector[2])),
                     n=("temp" + str(i)))

        mc.select("temp0", hi=True)
        mc.parent(world=True)
        #Reposition to get proper orientation of the joints
        mc.parent("temp2","temp3")
        mc.parent("temp1","temp2")
        mc.parent("temp0", "temp1")
        mc.select("temp3", hi=True)
        temp=mc.ls(sl=True)
        mc.joint(temp, "L_shoulder_IK", e=True, oj=ro, sao="ydown", zso=True)
        mc.delete("temp0")
        # Rename
        mc.rename("temp1", "L_uparmTwist_C_JJ")
        mc.rename("temp2", "L_uparmTwist_B_JJ")
        mc.rename("temp3", "L_uparmTwist_A_JJ")
        upTwi = mc.ls(sl=True)
        mc.parent(world=True)

        if mc.radioButton("rarm", query=True, select=True):
            for j in upTwi:
                mc.mirrorJoint(j, mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
            mc.select("R_uparmTwist_A_JJ", "R_uparmTwist_B_JJ", "R_uparmTwist_C_JJ")
            RupTwi= mc.ls(sl=True)

        mc.parent(upTwi, jj[1])

        #LOWERARM: (repeating the process)
        # query master twist joints position
        mc.select(cl=True)
        pPos = mc.joint("L_loTwist_01_JC", query=True, position=True)
        cPos = mc.joint("L_loTwist_02_JC", query=True, position=True)
        helperJoint= mc.duplicate("L_loTwist_02_JC") # i need this for the last joint to be well oriented.
        #Parent Orientation
        ro = mc.joint("L_loTwist_01_JC", q=True, roo=True)

        # Vector
        numberOfJoints = 4
        jVector = [0, 1, 2]
        jVector[0] = (cPos[0] - pPos[0]) / numberOfJoints
        jVector[1] = (cPos[1] - pPos[1]) / numberOfJoints
        jVector[2] = (cPos[2] - pPos[2]) / numberOfJoints

        # Loop and setup joints
        for i in range(numberOfJoints):
            # Create Joints
            mc.joint(p=(pPos[0] + (i * jVector[0]), pPos[1] + (i * jVector[1]), pPos[2] + (i * jVector[2])),
                     n=("temp" + str(i)))

        mc.parent(helperJoint, "temp3")
        mc.select("temp0", hi=True)
        temp=mc.ls(sl=True)
        mc.joint(temp, "L_loTwist_01_JC", e=True, oj=ro, sao="ydown", zso=True)
        mc.parent(world=True)
        mc.delete(helperJoint)
        mc.delete("temp0")
        mc.rename("temp1", "L_loarmTwist_A_JJ")
        mc.rename("temp2", "L_loarmTwist_B_JJ")
        mc.rename("temp3", "L_loarmTwist_C_JJ")
        loTwi = mc.ls(sl=True)

        if mc.radioButton("rarm", query=True, select=True):
            for j in loTwi:
                mc.mirrorJoint(j, mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
            mc.select("R_loarmTwist_A_JJ", "R_loarmTwist_B_JJ", "R_loarmTwist_C_JJ")
            RloTwi = mc.ls(sl=True)

        mc.parent(loTwi, jj[2])

        # Conect the handles and make it work wth the twist joints
        mc.shadingNode("multiplyDivide", asUtility=True, name="L_uparmTwist_MULT")
        mc.connectAttr("L_upTwist_01_JC.rx", "L_uparmTwist_MULT.input1X")
        mc.connectAttr("L_upTwist_01_JC.ry", "L_uparmTwist_MULT.input1Y")
        mc.connectAttr("L_upTwist_01_JC.rz", "L_uparmTwist_MULT.input1Z")
        mc.setAttr("L_uparmTwist_MULT.input2X", 0.25)
        mc.setAttr("L_uparmTwist_MULT.input2Y", 0.50)
        mc.setAttr("L_uparmTwist_MULT.input2Z", 0.75)
        mc.connectAttr("L_uparmTwist_MULT.outputX", "L_uparmTwist_A_JJ.rx")
        mc.connectAttr("L_uparmTwist_MULT.outputY", "L_uparmTwist_B_JJ.rx")
        mc.connectAttr("L_uparmTwist_MULT.outputZ", "L_uparmTwist_C_JJ.rx")
        #
        mc.shadingNode("multiplyDivide", asUtility=True, name="L_loarmTwist_MULT")
        mc.connectAttr("L_loTwist_01_JC.rx", "L_loarmTwist_MULT.input1X")
        mc.connectAttr("L_loTwist_01_JC.ry", "L_loarmTwist_MULT.input1Y")
        mc.connectAttr("L_loTwist_01_JC.rz", "L_loarmTwist_MULT.input1Z")
        mc.setAttr("L_loarmTwist_MULT.input2X", 0.25)
        mc.setAttr("L_loarmTwist_MULT.input2Y", 0.50)
        mc.setAttr("L_loarmTwist_MULT.input2Z", 0.75)
        mc.connectAttr("L_loarmTwist_MULT.outputX", "L_loarmTwist_C_JJ.rx")
        mc.connectAttr("L_loarmTwist_MULT.outputY", "L_loarmTwist_B_JJ.rx")
        mc.connectAttr("L_loarmTwist_MULT.outputZ", "L_loarmTwist_A_JJ.rx")

        #Make it stretchy:
        mc.shadingNode("multiplyDivide", asUtility=True, name="L_uparmStretch_MULT")
        mc.connectAttr("L_elbow_JJ.tx", "L_uparmStretch_MULT.input1X")
        mc.connectAttr("L_elbow_JJ.tx", "L_uparmStretch_MULT.input1Y")
        mc.connectAttr("L_elbow_JJ.tx", "L_uparmStretch_MULT.input1Z")
        mc.setAttr("L_uparmStretch_MULT.input2X", 0.25)
        mc.setAttr("L_uparmStretch_MULT.input2Y", 0.50)
        mc.setAttr("L_uparmStretch_MULT.input2Z", 0.75)
        mc.connectAttr("L_uparmStretch_MULT.outputX", "L_uparmTwist_A_JJ.tx")
        mc.connectAttr("L_uparmStretch_MULT.outputY", "L_uparmTwist_B_JJ.tx")
        mc.connectAttr("L_uparmStretch_MULT.outputZ", "L_uparmTwist_C_JJ.tx")
        #
        mc.shadingNode("multiplyDivide", asUtility=True, name="L_loarmStretch_MULT")
        mc.connectAttr("L_wrist_JJ.tx", "L_loarmStretch_MULT.input1X")
        mc.connectAttr("L_wrist_JJ.tx", "L_loarmStretch_MULT.input1Y")
        mc.connectAttr("L_wrist_JJ.tx", "L_loarmStretch_MULT.input1Z")
        mc.setAttr("L_loarmStretch_MULT.input2X", 0.25)
        mc.setAttr("L_loarmStretch_MULT.input2Y", 0.50)
        mc.setAttr("L_loarmStretch_MULT.input2Z", 0.75)
        mc.connectAttr("L_loarmStretch_MULT.outputX", "L_loarmTwist_C_JJ.tx")
        mc.connectAttr("L_loarmStretch_MULT.outputY", "L_loarmTwist_B_JJ.tx")
        mc.connectAttr("L_loarmStretch_MULT.outputZ", "L_loarmTwist_A_JJ.tx")

        # Switch_IK_FK
        PC1 = mc.parentConstraint(ik[0], fk[0], jj[1], mo=1)
        PC2 = mc.parentConstraint(ik[1], fk[1], jj[2], mo=1)
        PC3 = mc.parentConstraint(ik[2], fk[2], jj[3], mo=1)

        # Stretchy Arm
        startPos = mc.xform(ik[0], translation=True, q=True, ws=True)
        endPos = mc.xform(ik[2], translation=True, q=True, ws=True)
        L_dist = mc.distanceDimension(sp=(startPos[0], startPos[1], startPos[2]),
                                      ep=(endPos[0], endPos[1], endPos[2]))
        distLoc = mc.listConnections(L_dist)
        distShape = mc.listConnections(shapes=True)
        mc.pointConstraint(ik[0], distLoc[0])
        mc.parent(distLoc[1], ikcc[0])
        mc.rename(distLoc[0], "L_stretchyArm_01_LOC")
        mc.rename(distLoc[1], "L_stretchyArm_02_LOC")
        #
        div = mc.shadingNode("multiplyDivide", asUtility=True, name="L_arm_stretchy_DIV")
        normalizeDiv = mc.shadingNode("multiplyDivide", asUtility=True, name="L_arm_normalize_DIV")
        con = mc.shadingNode("condition", asUtility=True, name="L_arm_CON")
        mc.setAttr(div + ".operation", 2)
        mc.setAttr(normalizeDiv + ".operation", 2)
        mc.setAttr(con + ".operation", 2)
        secondTerm = mc.getAttr("{}.distance".format(L_dist))
        mc.setAttr("{}.secondTerm".format(con), secondTerm)
        mc.setAttr("{}.input2X".format(div), secondTerm)
        mc.connectAttr("{}.outColorR".format(con), "{}.input1X".format(div))
        mc.connectAttr("{}.distance".format(distShape[0]), "{}.input1X".format(normalizeDiv))
        mc.connectAttr("{}.scaleY".format("root_CC"), "{}.input2X".format(normalizeDiv))
        mc.connectAttr("{}.outputX".format(normalizeDiv), "{}.secondTerm".format(con))
        mc.connectAttr("{}.outputX".format(normalizeDiv), "{}.colorIfFalseR".format(con))
        firstTerm = mc.getAttr("{}.distance".format(L_dist))
        mc.setAttr("{}.firstTerm".format(con), firstTerm)
        mc.setAttr("{}.colorIfTrueR".format(con), firstTerm)
        mc.connectAttr("{}.outputX".format(div), "{}.sx".format(ik[0]))
        mc.connectAttr("{}.outputX".format(div), "{}.sx".format(ik[1]))

        mc.hide("L_stretchyArm_02_LOC")

        #Anotation for the pole vector
        elbowPos = mc.xform(ik[1], ws=True, translation=True, q=True)
        LarmAnnot = mc.annotate(ikpv, p=(elbowPos[0], elbowPos[1], elbowPos[2]))
        mc.parent(LarmAnnot, "L_elbow_JJ")
        mc.setAttr("{}.overrideEnabled".format(LarmAnnot), 1)
        mc.setAttr("{}.overrideDisplayType".format(LarmAnnot), 2)
        mc.setAttr("{}.overrideDisplayType".format(LarmAnnot), 1)

        if mc.radioButton("ikfkex", query=True, select=True):
            mc.select("IK_FK_SWITCH")
            ikfkSwitch = mc.ls(sl=True)
            mc.addAttr(ikfkSwitch, longName='L_arm_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)
            mc.addAttr(ikfkSwitch, longName='R_arm_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)

            # Switch IK-FK
            mc.shadingNode("reverse", asUtility=True, name="L_arm_REV")
            mc.connectAttr("IK_FK_SWITCH.L_arm_IK_FK", "L_arm_REV.inputX")
            #
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_shoulder_IKW0".format(PC1[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_shoulder_FKW1".format(PC1[0])))
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_elbow_IKW0".format(PC2[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_elbow_FKW1".format(PC2[0])))
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_wrist_IKW0".format(PC3[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_wrist_FKW1".format(PC3[0])))

            # Switch visibilidad de los controles
            mc.connectAttr("IK_FK_SWITCH.L_arm_IK_FK", "{}.v".format(fkhi[0]))
            mc.connectAttr("L_arm_REV.outputX", "{}.v".format(ikcc_off))
            mc.connectAttr("L_arm_REV.outputX", "{}.v".format(ikpv_off))
            #
            grp = mc.group(n="L_arm_GRP", empty=True)
            temp = mc.pointConstraint(jj[0], grp, maintainOffset=0)
            mc.delete(temp)
            mc.parent(jj[0], clav_grp, grp)
            mc.parent(ikpv_off, ikcc_off, "IK_GRP")
            mc.hide(ik[0], fk[0], IKRP[0])
            mc.parent("L_stretchyArm_01_LOC", L_dist, "stretchy_GRP")
            #
            om.MGlobal.displayInfo("Your arm rig has been created with success!")

        elif mc.radioButton("ikfkcc", query=True, select=True):

            # Create IK FK control
            v1 = mc.curve(d=1,
                          p=[(-3.36, 0, 1.64), (-3.36, 0, 3.76), (-2.81, 0, 3.76), (-2.81, 0, 1.65), (-3.36, 0, 1.64)])
            v2 = mc.curve(d=1,
                          p=[(-2.59, 0, 1.69), (-2.57, 0, 3.76), (-2.03, 0, 3.76), (-2.03, 0, 2.87), (-1.80, 0, 3.76),
                             (-1.24, 0, 3.76), (-1.58, 0, 2.60), (-1.28, 0, 1.66), (-1.79, 0, 1.66), (-2.03, 0, 2.47),
                             (-2.03, 0, 1.66), (-2.59, 0, 1.69)])
            v3 = mc.curve(d=1,
                          p=[(-0.14, 0, 1.63), (-0.77, 0, 3.80), (-0.37, 0, 3.80), (0.25, 0, 1.60), (-0.14, 0, 1.63)])
            v4 = mc.curve(d=1, p=[(0.84, 0, 1.67), (0.85, 0, 3.76), (1.40, 0, 3.76), (1.41, 0, 2.87), (1.74, 0, 2.87),
                                  (1.74, 0, 2.48), (1.40, 0, 2.47), (1.41, 0, 2.07), (1.78, 0, 2.07), (1.78, 0, 1.67),
                                  (0.84, 0, 1.67)])
            v5 = mc.curve(d=1, p=[(1.92, 0, 1.72), (1.92, 0, 3.76), (2.47, 0, 3.76), (2.47, 0, 2.87), (2.69, 0, 3.76),
                                  (3.26, 0, 3.76), (2.92, 0, 2.61), (3.23, 0, 1.65), (2.71, 0, 1.67), (2.47, 0, 2.47),
                                  (2.47, 0, 1.68), (1.92, 0, 1.72)])
            mc.select(v1, v2, v3, v4, v5)
            mc.ls(sl=True)
            shps = mc.listRelatives(shapes=True)
            mc.parent(shps, v1, relative=True, shape=True)
            mc.delete(v2, v3, v4, v5)
            sel = mc.rename(v1, "IK_FK_SWITCH")
            ikfk_off = mc.group(sel, name="grpIK_FK_SWITCHZERO")
            mc.setAttr("{}.overrideEnabled".format(ikfk_off), 1)
            mc.setAttr("{}.overrideColor".format(ikfk_off), 9)
            ikfkSwitch = mc.ls(sel)
            #
            mc.addAttr(sel, longName='L_arm_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)
            mc.addAttr(sel, longName='R_arm_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)
            mc.setAttr("{}.tx".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.ty".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.tz".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.rx".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.ry".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.rz".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sx".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sy".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.sz".format(sel), lock=True, keyable=False, channelBox=False)
            mc.setAttr("{}.v".format(sel), lock=True, keyable=False, channelBox=False)

            # Switch IK-FK
            mc.shadingNode("reverse", asUtility=True, name="L_arm_REV")
            mc.connectAttr("IK_FK_SWITCH.L_arm_IK_FK", "L_arm_REV.inputX")
            #
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_shoulder_IKW0".format(PC1[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_shoulder_FKW1".format(PC1[0])))
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_elbow_IKW0".format(PC2[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_elbow_FKW1".format(PC2[0])))
            mc.connectAttr(("L_arm_REV.outputX"), ("{}.L_wrist_IKW0".format(PC3[0])))
            mc.connectAttr(("{}.L_arm_IK_FK".format(ikfkSwitch[0])), ("{}.L_wrist_FKW1".format(PC3[0])))

            # Switch visibilidad de los controles
            mc.connectAttr("IK_FK_SWITCH.L_arm_IK_FK", "{}.v".format(fkhi[0]))
            mc.connectAttr("L_arm_REV.outputX", "{}.v".format(ikcc_off))
            mc.connectAttr("L_arm_REV.outputX", "{}.v".format(ikpv_off))
            #
            grp = mc.group(n="L_arm_GRP", empty=True)
            temp = mc.pointConstraint(jj[0], grp, maintainOffset=0)
            mc.delete(temp)
            mc.parent(jj[0], clav_grp, grp)
            mc.group(ikpv_off, ikcc_off, ikfk_off, n="IK_GRP")
            mc.hide(ik[0], fk[0], IKRP[0])
            mc.parent("L_stretchyArm_01_LOC", L_dist, "stretchy_GRP")

            #
            om.MGlobal.displayInfo("Your arm rig has been created with success!")

        else:
            grp = mc.group(n="L_arm_GRP", empty=True)
            temp = mc.pointConstraint(jj[0], grp, maintainOffset=0)
            mc.delete(temp)
            mc.parent(jj[0], clav_grp, grp)
            mc.group(ikpv_off, ikcc_off, n="IK_GRP")
            mc.hide(ik[0], fk[0], IKRP[0])

            #
            om.MGlobal.displayWarning("There was no IK_FK control, Switching skipped!")

        #Final Clean-up
        mc.hide(upIKSC[0], loIKSC[0], "L_loTwist_01_JC", "L_upTwist_01_JC")

        # RIGHT LEG MIRROR
        if mc.radioButton("rarm", query=True, select=True):

            def R_arm():
                previous_sel = None

                # IK RIG
                # Create and rename the ik chain:
                IkChain = mc.duplicate(rjj[1], renameChildren=True)
                mc.select(IkChain, hi=True)
                mel.eval('searchReplaceNames JJ1 IK hierarchy')
                rik = mc.ls(sl=True)

                # Create the Iksolver:
                ikarm = mc.ls(rik[0], rik[2])
                mc.select(ikarm)
                IKRP = mc.ikHandle(name="R_arm_IkRp", solver="ikRPsolver")

                # Create Controlers
                ikcc = mc.circle(n="R_arm_CC", c=(0, 0, 0), nr=(1, 0, 0), r=1.3, constructionHistory=False)
                mc.makeIdentity(apply=True)
                tempPoint = mc.parentConstraint(rik[2], ikcc, maintainOffset=0)
                mc.delete(tempPoint)
                temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)
                temp_rot = mc.xform(ikcc, rotation=True, query=True, worldSpace=True)
                mc.parent(IKRP[0], ikcc)

                # ZeroOut ikcc
                ikcc_off = mc.group(ikcc, n="grpR_arm_CCZERO", empty=True)
                mc.setAttr("{}.overrideEnabled".format(ikcc_off), 1)
                mc.setAttr("{}.overrideColor".format(ikcc_off), 13)
                mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
                mc.xform(ikcc_off, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
                mc.parent(ikcc, ikcc_off)
                mc.setAttr("{}.translate".format(ikcc[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ikcc[0]), 0, 0, 0)
                mc.xform("grpR_arm_CCZERO", cpc=1)
                mc.setAttr("R_arm_CC.sx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_CC.sy", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_CC.sz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_CC.v", lock=True, keyable=False, channelBox=False)
                mc.orientConstraint(ikcc, rik[2], maintainOffset=1)

                # Pole Vector
                ikpv = mc.curve(d=1, n="R_arm_PV", p=[(-0.7, -1.19209e-07, 0.2), (0, 0, -1.19),
                                                      (0, 0.7, 0.2), (-0.7, -1.19209e-07, 0.2),
                                                      (0, -0.7, 0.2), (0, 0, -1.19), (0.7, 0, 0.2),
                                                      (0, -0.7, 0.2), (0.7, 0, 0.2), (0, 0.7, 0.2)])
                mc.makeIdentity(apply=True)
                temp_constraint = mc.pointConstraint(rik[1], ikpv, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.poleVectorConstraint(ikpv, IKRP[0], weight=1)
                temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)

                # ZeroOut ikpv
                ikpv_off = mc.group(ikpv, n="grpR_arm_PVZERO")
                mc.setAttr("{}.overrideEnabled".format(ikpv_off), 1)
                mc.setAttr("{}.overrideColor".format(ikpv_off), 13)
                mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
                mc.setAttr("{}.translate".format(ikpv), 0, 0, 0)
                mc.xform(ikpv_off, cpc=1)
                mc.move(0, 0, -10, ikpv_off, r=True)
                mc.setAttr("R_arm_PV.rx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.ry", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.rz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.sx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.sy", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.sz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_arm_PV.v", lock=True, keyable=False, channelBox=False)

                # FK RIG
                # Create and rename the fk chain:
                FkChain = mc.duplicate(rjj[1], renameChildren=True)
                mc.select(FkChain)
                mel.eval('searchReplaceNames JJ1 FK hierarchy')
                rfk = mc.ls(sl=True)

                for j in rfk:
                    cc = mc.circle(nr=(1, 0, 0), n=str(j) + "_CC", r=2, constructionHistory=False)
                    mc.makeIdentity(apply=True)
                    temp_constraint = mc.parentConstraint(j, cc, maintainOffset=0)
                    mc.delete(temp_constraint)
                    temp_rot = mc.xform(cc, rotation=True, query=True, worldSpace=True)

                    # ZeroOut
                    offset = mc.group(cc, n=str(j) + "_CCZERO")
                    mc.setAttr("{}.overrideEnabled".format(offset), 1)
                    mc.setAttr("{}.overrideColor".format(offset), 13)
                    mc.xform(offset, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
                    mc.setAttr("{}.rotate".format(cc[0]), 0, 0, 0)
                    mc.setAttr("{}.tx".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.ty".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.tz".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.sx".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.sy".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.sz".format(cc[0]), lock=True, keyable=False, channelBox=False)
                    mc.setAttr("{}.v".format(cc[0]), lock=True, keyable=False, channelBox=False)

                    # fk hierarchy
                    mc.orientConstraint(cc, j, maintainOffset=0)
                    if previous_sel:
                        mc.parent(offset, previous_sel)
                    previous_sel = cc

                # clavicle
                clav = mc.circle(nr=(1, 0, 0), n="R_clavicle_FK_CC", r=2, constructionHistory=False)
                mc.makeIdentity(apply=True)
                temp_constraint = mc.parentConstraint(rjj[0], clav, maintainOffset=0)
                mc.delete(temp_constraint)
                temp_rot = mc.xform(clav, rotation=True, query=True, worldSpace=True)
                clav_grp = mc.group(clav, n="R_clavicle_FK_CCZERO")
                mc.setAttr("{}.overrideEnabled".format(clav_grp), 1)
                mc.setAttr("{}.overrideColor".format(clav_grp), 13)
                mc.xform(clav_grp, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
                mc.setAttr("{}.rotate".format(clav[0]), 0, 0, 0)
                mc.orientConstraint(clav, rjj[0])
                mc.setAttr("{}.tx".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.sx".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.sy".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.sz".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(clav[0]), lock=True, keyable=False, channelBox=False)
                mc.parent("R_shoulder_FK_CCZERO", "R_clavicle_FK_CC")
                fkhi = mc.ls("R_shoulder_FK_CCZERO")

                # Arm Twist (J.Dobra style)
                # Create the main chains and handles:
                upTwistHandle = mc.duplicate(rjj[1], renameChildren=True)
                mc.select(upTwistHandle, hi=True)
                upTwist = mc.ls(sl=True)
                mc.delete(upTwist[2])
                mc.parent(upTwist[0], world=True)
                mc.reroot(upTwist[1])  # this is to invert the order of the chain.
                mc.rename(upTwist[0], "R_upTwist_02_JC")
                mc.rename(upTwist[1], "R_upTwist_01_JC")
                #
                loTwistHandle = mc.duplicate(rjj[2], renameChildren=True)
                mc.select(loTwistHandle, hi=True)
                loTwist = mc.ls(sl=True)
                mc.rename(loTwist[0], "R_loTwist_01_JC")
                mc.rename(loTwist[1], "R_loTwist_02_JC")
                #
                mc.parent("R_upTwist_01_JC", rjj[1])
                mc.parent("R_loTwist_01_JC", rjj[2])
                mc.select("R_upTwist_01_JC", "R_upTwist_02_JC")
                upIKSC = mc.ikHandle(name="R_upTwist_IkSc", solver="ikSCsolver")
                mc.select("R_loTwist_01_JC", "R_loTwist_02_JC")
                loIKSC = mc.ikHandle(name="R_loTwist_IkSc", solver="ikSCsolver")
                mc.parent(upIKSC[0], rjj[0])
                mc.parent(loIKSC[0], rjj[3])

                #Parent twist hierarchy under right arm
                mc.parent(RupTwi, rjj[1])
                mc.parent(RloTwi, rjj[2])

                # Conect the handles and make it work wth the twist joints
                mc.shadingNode("multiplyDivide", asUtility=True, name="R_uparmTwist_MULT")
                mc.connectAttr("R_upTwist_01_JC.rx", "R_uparmTwist_MULT.input1X")
                mc.connectAttr("R_upTwist_01_JC.ry", "R_uparmTwist_MULT.input1Y")
                mc.connectAttr("R_upTwist_01_JC.rz", "R_uparmTwist_MULT.input1Z")
                mc.setAttr("R_uparmTwist_MULT.input2X", 0.25)
                mc.setAttr("R_uparmTwist_MULT.input2Y", 0.50)
                mc.setAttr("R_uparmTwist_MULT.input2Z", 0.75)
                mc.connectAttr("R_uparmTwist_MULT.outputX", "R_uparmTwist_A_JJ.rx")
                mc.connectAttr("R_uparmTwist_MULT.outputY", "R_uparmTwist_B_JJ.rx")
                mc.connectAttr("R_uparmTwist_MULT.outputZ", "R_uparmTwist_C_JJ.rx")
                #
                mc.shadingNode("multiplyDivide", asUtility=True, name="R_loarmTwist_MULT")
                mc.connectAttr("R_loTwist_01_JC.rx", "R_loarmTwist_MULT.input1X")
                mc.connectAttr("R_loTwist_01_JC.ry", "R_loarmTwist_MULT.input1Y")
                mc.connectAttr("R_loTwist_01_JC.rz", "R_loarmTwist_MULT.input1Z")
                mc.setAttr("R_loarmTwist_MULT.input2X", 0.25)
                mc.setAttr("R_loarmTwist_MULT.input2Y", 0.50)
                mc.setAttr("R_loarmTwist_MULT.input2Z", 0.75)
                mc.connectAttr("R_loarmTwist_MULT.outputX", "R_loarmTwist_C_JJ.rx")
                mc.connectAttr("R_loarmTwist_MULT.outputY", "R_loarmTwist_B_JJ.rx")
                mc.connectAttr("R_loarmTwist_MULT.outputZ", "R_loarmTwist_A_JJ.rx")
                #
                # Make it stretchy:
                mc.shadingNode("multiplyDivide", asUtility=True, name="R_uparmStretch_MULT")
                mc.connectAttr("R_elbow_JJ.tx", "R_uparmStretch_MULT.input1X")
                mc.connectAttr("R_elbow_JJ.tx", "R_uparmStretch_MULT.input1Y")
                mc.connectAttr("R_elbow_JJ.tx", "R_uparmStretch_MULT.input1Z")
                mc.setAttr("R_uparmStretch_MULT.input2X", 0.25)
                mc.setAttr("R_uparmStretch_MULT.input2Y", 0.50)
                mc.setAttr("R_uparmStretch_MULT.input2Z", 0.75)
                mc.connectAttr("R_uparmStretch_MULT.outputX", "R_uparmTwist_A_JJ.tx")
                mc.connectAttr("R_uparmStretch_MULT.outputY", "R_uparmTwist_B_JJ.tx")
                mc.connectAttr("R_uparmStretch_MULT.outputZ", "R_uparmTwist_C_JJ.tx")
                #
                mc.shadingNode("multiplyDivide", asUtility=True, name="R_loarmStretch_MULT")
                mc.connectAttr("R_wrist_JJ.tx", "R_loarmStretch_MULT.input1X")
                mc.connectAttr("R_wrist_JJ.tx", "R_loarmStretch_MULT.input1Y")
                mc.connectAttr("R_wrist_JJ.tx", "R_loarmStretch_MULT.input1Z")
                mc.setAttr("R_loarmStretch_MULT.input2X", 0.25)
                mc.setAttr("R_loarmStretch_MULT.input2Y", 0.50)
                mc.setAttr("R_loarmStretch_MULT.input2Z", 0.75)
                mc.connectAttr("R_loarmStretch_MULT.outputX", "R_loarmTwist_C_JJ.tx")
                mc.connectAttr("R_loarmStretch_MULT.outputY", "R_loarmTwist_B_JJ.tx")
                mc.connectAttr("R_loarmStretch_MULT.outputZ", "R_loarmTwist_A_JJ.tx")

                # Switch_IK_FK
                PC1 = mc.parentConstraint(rik[0], rfk[0], rjj[1], mo=1)
                PC2 = mc.parentConstraint(rik[1], rfk[1], rjj[2], mo=1)
                PC3 = mc.parentConstraint(rik[2], rfk[2], rjj[3], mo=1)

                # Stretchy Arm
                startPos = mc.xform(rik[0], translation=True, q=True, ws=True)
                endPos = mc.xform(rik[2], translation=True, q=True, ws=True)
                R_dist = mc.distanceDimension(sp=(startPos[0], startPos[1], startPos[2]),
                                              ep=(endPos[0], endPos[1], endPos[2]))
                distLoc = mc.listConnections(R_dist)
                distShape = mc.listConnections(shapes=True)
                mc.pointConstraint(rik[0], distLoc[0])
                mc.parent(distLoc[1], ikcc[0])
                mc.rename(distLoc[0], "R_stretchyArm_01_LOC")
                mc.rename(distLoc[1], "R_stretchyArm_02_LOC")
                #
                div = mc.shadingNode("multiplyDivide", asUtility=True, name="R_arm_stretchy_DIV")
                normalizeDiv= mc.shadingNode("multiplyDivide", asUtility=True, name="R_arm_normalize_DIV")
                con = mc.shadingNode("condition", asUtility=True, name="R_arm_CON")
                mc.setAttr(div + ".operation", 2)
                mc.setAttr(normalizeDiv + ".operation", 2)
                mc.setAttr(con + ".operation", 2)
                secondTerm = mc.getAttr("{}.distance".format(R_dist))
                mc.setAttr("{}.secondTerm".format(con), secondTerm)
                mc.setAttr("{}.input2X".format(div), secondTerm)
                mc.connectAttr("{}.outColorR".format(con), "{}.input1X".format(div))
                mc.connectAttr("{}.distance".format(distShape[0]), "{}.input1X".format(normalizeDiv))
                mc.connectAttr("{}.scaleY".format("root_CC"), "{}.input2X".format(normalizeDiv))
                mc.connectAttr("{}.outputX".format(normalizeDiv), "{}.secondTerm".format(con))
                mc.connectAttr("{}.outputX".format(normalizeDiv), "{}.colorIfFalseR".format(con))
                firstTerm = mc.getAttr("{}.distance".format(R_dist))
                mc.setAttr("{}.firstTerm".format(con), firstTerm)
                mc.setAttr("{}.colorIfTrueR".format(con), firstTerm)
                mc.connectAttr("{}.outputX".format(div), "{}.sx".format(rik[0]))
                mc.connectAttr("{}.outputX".format(div), "{}.sx".format(rik[1]))

                mc.hide("R_stretchyArm_02_LOC")

                # Anotation for the pole vector
                elbowPos = mc.xform(rik[1], ws=True, translation=True, q=True)
                RarmAnnot = mc.annotate(ikpv, p=(elbowPos[0], elbowPos[1], elbowPos[2]))
                mc.parent(RarmAnnot, "R_elbow_JJ")
                mc.setAttr("{}.overrideEnabled".format(RarmAnnot), 1)
                mc.setAttr("{}.overrideDisplayType".format(RarmAnnot), 2)
                mc.setAttr("{}.overrideDisplayType".format(RarmAnnot), 1)

                if mc.radioButton("ikfkex", query=True, select=True):

                    # Switch IK-FK
                    mc.shadingNode("reverse", asUtility=True, name="R_arm_REV")
                    mc.connectAttr("IK_FK_SWITCH.R_arm_IK_FK", "R_arm_REV.inputX")
                    #
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_shoulder_IKW0".format(PC1[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_shoulder_FKW1".format(PC1[0])))
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_elbow_IKW0".format(PC2[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_elbow_FKW1".format(PC2[0])))
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_wrist_IKW0".format(PC3[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_wrist_FKW1".format(PC3[0])))

                    # Switch visibilidad de los controles
                    mc.connectAttr("IK_FK_SWITCH.R_arm_IK_FK", "{}.v".format(fkhi[0]))
                    mc.connectAttr("R_arm_REV.outputX", "{}.v".format(ikcc_off))
                    mc.connectAttr("R_arm_REV.outputX", "{}.v".format(ikpv_off))
                    #
                    grp = mc.group(n="R_arm_GRP", empty=True)
                    temp = mc.pointConstraint(rjj[0], grp, maintainOffset=0)
                    mc.delete(temp)
                    mc.parent(rjj[0], clav_grp, grp)
                    mc.parent(ikpv_off, ikcc_off, "IK_GRP")
                    mc.hide(rik[0], rfk[0], IKRP[0])
                    mc.parent("R_stretchyArm_01_LOC", R_dist, "stretchy_GRP")

                    #
                    om.MGlobal.displayInfo("Your arm rig has been created with success!")

                elif mc.radioButton("ikfkcc", query=True, select=True):

                    # Switch IK-FK
                    mc.shadingNode("reverse", asUtility=True, name="R_arm_REV")
                    mc.connectAttr("IK_FK_SWITCH.R_arm_IK_FK", "R_arm_REV.inputX")
                    #
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_shoulder_IKW0".format(PC1[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_shoulder_FKW1".format(PC1[0])))
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_elbow_IKW0".format(PC2[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_elbow_FKW1".format(PC2[0])))
                    mc.connectAttr(("R_arm_REV.outputX"), ("{}.R_wrist_IKW0".format(PC3[0])))
                    mc.connectAttr(("{}.R_arm_IK_FK".format(ikfkSwitch[0])), ("{}.R_wrist_FKW1".format(PC3[0])))

                    # Switch visibilidad de los controles
                    mc.connectAttr("IK_FK_SWITCH.R_arm_IK_FK", "{}.v".format(fkhi[0]))
                    mc.connectAttr("R_arm_REV.outputX", "{}.v".format(ikcc_off))
                    mc.connectAttr("R_arm_REV.outputX", "{}.v".format(ikpv_off))
                    #
                    mc.parent(ikpv_off, ikcc_off, ikfk_off, "IK_GRP")
                    grp = mc.group(n="R_arm_GRP", empty=True)
                    temp = mc.pointConstraint(rjj[0], grp, maintainOffset=0)
                    mc.delete(temp)
                    mc.parent(rjj[0], clav_grp, grp)
                    mc.hide(rik[0], rfk[0], IKRP[0])
                    mc.parent("R_stretchyArm_01_LOC", R_dist, "stretchy_GRP")
                    #
                    om.MGlobal.displayInfo("Your arm rig has been created with success!")

                else:
                    grp = mc.group(n="R_arm_GRP", empty=True)
                    temp = mc.pointConstraint(rjj[0], grp, maintainOffset=0)
                    mc.delete(temp)
                    mc.parent(rjj[0], clav_grp, grp)
                    mc.parent(ikpv_off, ikcc_off, "IK_GRP")
                    mc.hide(rik[0], rfk[0], IKRP[0])
                    #
                    om.MGlobal.displayWarning("There was no IK_FK control, Switching skipped!")

                # Final Clean-up
                mc.hide(upIKSC[0], loIKSC[0], "R_loTwist_01_JC", "R_upTwist_01_JC")
            R_arm()
