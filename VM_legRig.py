"""
Version 1 made in January 2018 (week # 1): Leg Rig in basic python
Scripted by Vero Morera. 
veromc1692@gmail.com
"""

import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel

WIN="AutoLeg"

def UI():
    # Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title= "VM_Leg Rig", h=30, w=150, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2, w=100)
    mc.text("Select the 5 ORIENTED joints of the leg.", h=25)
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.radioCollection()
    mc.radioButton("ikfkcc", label= "Create IK/FK Switcher")
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button(label= "L Leg Auto", w=100, h=40, command=L_leg, bgc=(.2,.2,.2))
    mc.radioCollection()
    mc.radioButton("rleg", label="Mirror to Right Leg")
    mc.setParent('..')

    mc.showWindow(WIN)

def L_leg(*args):

    origLeg = mc.ls(sl=True)
    mc.select(cl=True)
    previous_sel = None

    if len(origLeg) < 5:
        om.MGlobal.displayError("Please select the entire leg. (exactly 5 joints)")

    elif len(origLeg) > 5:
        om.MGlobal.displayError("Please select just 5 joints!")

    else:
    # JJ RIG
        mc.select(origLeg)
        mc.rename(origLeg[0], "L_hip_JJ")
        mc.rename(origLeg[1], "L_knee_JJ")
        mc.rename(origLeg[2], "L_ankle_JJ")
        mc.rename(origLeg[3], "L_ball_JJ")
        mc.rename(origLeg[4], "L_toe_JJ")
        jj = mc.ls(sl=True)

        # RFL
        mc.select(jj)
        mc.duplicate(jj[2:5])
        mc.parent(world=True)
        dup = mc.ls(sl=True)
        mc.select(cl=True)
        mc.rename(dup[0], "RFL_L_ankle_JC")
        mc.rename(dup[1], "RFL_L_ball_JC")
        mc.rename(dup[2], "RFL_L_toe_JC")
        heel = mc.joint(n="RFL_L_heel_JC", p=(0, 0, 0))
        toetap = mc.joint(n="RFL_L_toeTap_JC")
        tempPoint = mc.pointConstraint("RFL_L_ball_JC", toetap)
        mc.delete(tempPoint)
        mc.parent("RFL_L_ankle_JC", "RFL_L_ball_JC")
        mc.parent("RFL_L_ball_JC", "RFL_L_toe_JC")
        mc.parent("RFL_L_toe_JC", "RFL_L_heel_JC")
        mc.parent("RFL_L_toeTap_JC", "RFL_L_toe_JC")
        RFL = mc.ls(heel)

    #(THIS IS FOR THE RIGHT LEG)
        if mc.radioButton("rleg", query=True, select=True):
            mc.select(jj[0])
            mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
            mc.select(hierarchy=True)
            rjj = mc.ls(sl=True)
            mc.select(heel)
            mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("_L_", "_R_"))
            R_RFL = mc.ls(sl=True)
    # (END OF THE RIGHT LEG)
            
    # IK RIG
        # Create and rename the ik chain:
        IkChain = mc.duplicate(jj[0], renameChildren=True)
        mc.select(IkChain)
        mel.eval('searchReplaceNames JJ1 IK hierarchy')
        ik = mc.ls(sl=True)

        # Create the Iksolvers:
        upperleg = mc.ls(ik[0], ik[2])
        mc.select(upperleg)
        IKRP = mc.ikHandle(name="L_leg_IkRp", solver="ikRPsolver")
        #
        loLegBall = mc.ls(ik[2:4])
        mc.select(loLegBall)
        IKSC_1 = mc.ikHandle(name="L_ball_IkSc", solver="ikSCsolver")
        #
        loLegToe = mc.ls(ik[3:5])
        mc.select(loLegToe)
        IKSC_2 = mc.ikHandle(name="L_toe_IkSc", solver="ikSCsolver")

        # Parent solvers into RFL
        mc.parent(IKRP[0], "RFL_L_ankle_JC")
        mc.parent(IKSC_1[0], "RFL_L_ball_JC")
        mc.parent(IKSC_2[0], "RFL_L_toeTap_JC")

        # Create Controlers
        ikcc = mc.circle(n="L_foot_CC", c=(0, 0, 0), nr=(0, 1, 0), constructionHistory=False)
        mc.hilite(ikcc)
        mc.select("{}.cv[0:2]".format(ikcc[0]), r=True)
        mc.move(0, 0, -0.429197, r=True, wd=True)
        mc.select("{}.cv[1]".format(ikcc[0]), r=True)
        mc.move(0, 1.118781, 0, r=True, wd=True)
        mc.select("{}.cv[4:6]".format(ikcc[0]), r=True)
        mc.move(0, 0, 2.024508, r=True, wd=True)
        mc.select("{}.cv[5]".format(ikcc[0]), r=True)
        mc.move(0, 0.345089, 0, r=True, wd=True)
        tempPoint = mc.pointConstraint(ik[2], ikcc, maintainOffset=0)
        mc.delete(tempPoint)
        temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)

        # ZeroOut ikcc
        ikcc_off = mc.group(ikcc, n="grpL_foot_CCZERO")
        mc.setAttr("{}.overrideEnabled" .format(ikcc_off), 1)
        mc.setAttr("{}.overrideColor" .format(ikcc_off), 6)
        mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.setAttr("{}.translate".format(ikcc[0]), 0, 0, 0)
        mc.setAttr("{}.rotate".format(ikcc[0]), 0, 0, 0)

        # Pole Vector
        ikpv = mc.curve(d=1, n="L_leg_PV", p=[(-4.37114e-08, -1, -1),(0, 0, 1),
                                (1, 0, -1),(1.31134e-07, 1, -1),
                                (0, 0, 1),(-1, 8.74228e-08, -1),
                                (-4.37114e-08, -1, -1),(1, 0, -1),
                                (1.31134e-07, 1, -1),(-1, 8.74228e-08, -1)])
        temp_constraint = mc.pointConstraint(ik[1], ikpv, maintainOffset=0)
        mc.delete(temp_constraint)
        mc.poleVectorConstraint(ikpv, IKRP[0], weight=1, )
        temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)

        # ZeroOut ikpv
        ikpv_off = mc.group(ikpv, n= "grpL_leg_PVZERO")
        mc.setAttr("{}.overrideEnabled".format(ikpv_off), 1)
        mc.setAttr("{}.overrideColor".format(ikpv_off), 6)
        mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
        mc.setAttr("{}.translate".format(ikpv), 0, 0, 5)
        #
        mc.setAttr("L_leg_PV.rx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.ry", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.rz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_leg_PV.v", lock=True, keyable=False, channelBox=False)

        # Create attributes for the RFL
        mc.parent(heel, ikcc)
        mc.addAttr(ikcc, ln="RFL", nn="__________________RFL", h=False)
        mc.addAttr(ikcc, ln="RollHeel", attributeType="double", dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln="TwistHeel", attributeType="double", dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln="RollBall", attributeType="double", dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln="RollToe", attributeType="double", dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln="TwistToe", attributeType="double", dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln="ToeTap", attributeType="double", dv=0, k=True, h=False)
        mc.setAttr("L_foot_CC.sx", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_foot_CC.sy", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_foot_CC.sz", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_foot_CC.v", lock=True, keyable=False, channelBox=False)
        mc.setAttr("L_foot_CC.RFL", lock=True, channelBox=True, keyable=False)

        # Connect attributes for the RFL
        mc.connectAttr(("{}.RollHeel".format(ikcc[0])), "{}.rz".format(heel))
        mc.connectAttr(("{}.TwistHeel".format(ikcc[0])), "{}.ry".format(heel))
        mc.connectAttr(("{}.RollBall".format(ikcc[0])), "{}.rz".format("RFL_L_ball_JC"))
        mc.connectAttr(("{}.RollToe".format(ikcc[0])), "{}.rz".format("RFL_L_toe_JC"))
        mc.connectAttr(("{}.TwistToe".format(ikcc[0])), "{}.ry".format("RFL_L_toe_JC"))
        mc.connectAttr(("{}.ToeTap".format(ikcc[0])), "{}.rx".format("RFL_L_toeTap_JC"))


    # FK RIG
        # Create and rename the fk chain:
        FkChain = mc.duplicate(jj[0], renameChildren=True)
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
            mc.orientConstraint(cc, j)
            if previous_sel:
                mc.parent(offset, previous_sel)
            previous_sel = cc
        fkhi = mc.ls("L_hip_FK_CCZERO")
        mc.delete("L_toe_FK_CCZERO")

        # Switch_IK_FK
        PC1 = mc.parentConstraint(ik[0], fk[0], jj[0], mo=1)
        PC2 = mc.parentConstraint(ik[1], fk[1], jj[1], mo=1)
        PC3 = mc.parentConstraint(ik[2], fk[2], jj[2], mo=1)
        PC4 = mc.parentConstraint(ik[3], fk[3], jj[3], mo=1)
        PC5 = mc.parentConstraint(ik[4], fk[4], jj[4], mo=1)

        if mc.radioButton("ikfkcc", query=True, select=True):

            #Create IK FK control
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
            ikfk_off= mc.group(sel, name= "grpIK_FK_SWITCHZERO")
            mc.setAttr("{}.overrideEnabled".format(ikfk_off), 1)
            mc.setAttr("{}.overrideColor".format(ikfk_off), 9)
            ikfkSwitch = mc.ls(sel)
            #
            mc.addAttr(sel, longName='L_leg_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)
            mc.addAttr(sel, longName='R_leg_IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)
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

            #Switch IK-FK
            mc.shadingNode ("reverse", asUtility=True, name= "L_leg_REV")
            mc.connectAttr( "IK_FK_SWITCH.L_leg_IK_FK", "L_leg_REV.inputX" )
            #
            mc.connectAttr( ("L_leg_REV.outputX"), ("{}.L_hip_IKW0" .format(PC1[0])) )
            mc.connectAttr( ("{}.L_leg_IK_FK".format(ikfkSwitch[0])), ("{}.L_hip_FKW1".format(PC1[0])) )
            mc.connectAttr( ("L_leg_REV.outputX"), ("{}.L_knee_IKW0".format(PC2[0])))
            mc.connectAttr(("{}.L_leg_IK_FK".format(ikfkSwitch[0])), ("{}.L_knee_FKW1".format(PC2[0])) )
            mc.connectAttr(("L_leg_REV.outputX"), ("{}.L_ankle_IKW0".format(PC3[0])))
            mc.connectAttr(("{}.L_leg_IK_FK".format(ikfkSwitch[0])), ("{}.L_ankle_FKW1".format(PC3[0])) )
            mc.connectAttr(("L_leg_REV.outputX"), ("{}.L_ball_IKW0".format(PC4[0])))
            mc.connectAttr(("{}.L_leg_IK_FK".format(ikfkSwitch[0])), ("{}.L_ball_FKW1".format(PC4[0])))
            mc.connectAttr(("L_leg_REV.outputX"), ("{}.L_toe_IKW0".format(PC5[0])))
            mc.connectAttr(("{}.L_leg_IK_FK".format(ikfkSwitch[0])), ("{}.L_toe_FKW1".format(PC5[0])))

            # Switch visibilidad de los controles
            mc.connectAttr( "IK_FK_SWITCH.L_leg_IK_FK", "{}.v".format(fkhi[0]) )
            mc.connectAttr( "L_leg_REV.outputX", "{}.v".format(ikcc_off) )
            mc.connectAttr("L_leg_REV.outputX", "{}.v".format(ikpv_off))
            #
            mc.group(jj[0], ik[0], fk[0], fkhi, n="L_leg_GRP")
            mc.group(ikpv_off, ikcc_off, ikfk_off, n="IK_GRP")
            mc.hide(ik[0], fk[0], RFL)
            #
            om.MGlobal.displayInfo("Your leg rig has been created with success!")

        else:
            mc.group(jj[0], ik[0], fk[0], fkhi, n="L_leg_GRP")
            mc.group(ikpv_off, ikcc_off, n="IK_GRP")
            mc.hide(ik[0], fk[0], RFL)
            #
            om.MGlobal.displayWarning("There was no IK_FK control, Switching skipped!")

        #RIGHT LEG MIRROR
        if mc.radioButton("rleg", query=True, select=True):

            def R_LEG():

                previous_sel = None

                # IK RIG
                # Create and rename the ik chain:
                IkChain = mc.duplicate(rjj[0], renameChildren=True)
                mc.select(IkChain)
                mel.eval('searchReplaceNames JJ1 IK hierarchy')
                rik = mc.ls(sl=True)

                # Create the Iksolvers:
                upperleg = mc.ls(rik[0], rik[2])
                mc.select(upperleg)
                IKRP = mc.ikHandle(name="R_leg_IkRp", solver="ikRPsolver")
                #
                loLegBall = mc.ls(rik[2:4])
                mc.select(loLegBall)
                IKSC_1 = mc.ikHandle(name="R_ball_IkSc", solver="ikSCsolver")
                #
                loLegToe = mc.ls(rik[3:5])
                mc.select(loLegToe)
                IKSC_2 = mc.ikHandle(name="R_toe_IkSc", solver="ikSCsolver")

                # Parent solvers into RFL
                mc.parent(IKRP[0], "RFL_R_ankle_JC")
                mc.parent(IKSC_1[0], "RFL_R_ball_JC")
                mc.parent(IKSC_2[0], "RFL_R_toeTap_JC")

                # Create Controlers
                ikcc = mc.circle(n="R_foot_CC", c=(0, 0, 0), nr=(0, 1, 0), r=2, constructionHistory=False)
                mc.hilite(ikcc)
                mc.select("{}.cv[0:2]".format(ikcc[0]), r=True)
                mc.move(0, 0, -0.429197, r=True, wd=True)
                mc.select("{}.cv[1]".format(ikcc[0]), r=True)
                mc.move(0, 1.118781, 0, r=True, wd=True)
                mc.select("{}.cv[4:6]".format(ikcc[0]), r=True)
                mc.move(0, 0, 2.024508, r=True, wd=True)
                mc.select("{}.cv[5]".format(ikcc[0]), r=True)
                mc.move(0, 0.345089, 0, r=True, wd=True)
                tempPoint = mc.pointConstraint(rik[2], ikcc, maintainOffset=0)
                mc.delete(tempPoint)
                temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)

                # ZeroOut ikcc
                ikcc_off = mc.group(ikcc, n="grpR_foot_CCZERO")
                mc.setAttr("{}.overrideEnabled".format(ikcc_off), 1)
                mc.setAttr("{}.overrideColor".format(ikcc_off), 13)
                mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
                mc.setAttr("{}.translate".format(ikcc[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ikcc[0]), 0, 0, 0)

                # Pole Vector
                ikpv = mc.curve(d=1, n="R_leg_PV", p=[(-4.37114e-08, -1, -1), (0, 0, 1),
                                                      (1, 0, -1), (1.31134e-07, 1, -1),
                                                      (0, 0, 1), (-1, 8.74228e-08, -1),
                                                      (-4.37114e-08, -1, -1), (1, 0, -1),
                                                      (1.31134e-07, 1, -1), (-1, 8.74228e-08, -1)])
                temp_constraint = mc.pointConstraint(rik[1], ikpv, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.poleVectorConstraint(ikpv, IKRP[0], weight=1, )
                temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)

                # ZeroOut ikpv
                ikpv_off = mc.group(ikpv, n="grpR_leg_PVZERO")
                mc.setAttr("{}.overrideEnabled".format(ikpv_off), 1)
                mc.setAttr("{}.overrideColor".format(ikpv_off), 13)
                mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
                mc.setAttr("{}.translate".format(ikpv), 0, 0, 5)
                #
                mc.setAttr("R_leg_PV.rx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.ry", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.rz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.sx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.sy", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.sz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_leg_PV.v", lock=True, keyable=False, channelBox=False)

                # Create attributes for the RFL
                mc.parent(R_RFL, ikcc)
                mc.addAttr(ikcc, ln="RFL", nn="__________________RFL", h=False)
                mc.addAttr(ikcc, ln="RollHeel", attributeType="double", dv=0, k=True, h=False)
                mc.addAttr(ikcc, ln="TwistHeel", attributeType="double", dv=0, k=True, h=False)
                mc.addAttr(ikcc, ln="RollBall", attributeType="double", dv=0, k=True, h=False)
                mc.addAttr(ikcc, ln="RollToe", attributeType="double", dv=0, k=True, h=False)
                mc.addAttr(ikcc, ln="TwistToe", attributeType="double", dv=0, k=True, h=False)
                mc.addAttr(ikcc, ln="ToeTap", attributeType="double", dv=0, k=True, h=False)
                mc.setAttr("R_foot_CC.sx", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_foot_CC.sy", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_foot_CC.sz", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_foot_CC.v", lock=True, keyable=False, channelBox=False)
                mc.setAttr("R_foot_CC.RFL", lock=True, channelBox=True, keyable=False)

                # Connect attributes for the RFL
                mc.connectAttr(("{}.RollHeel".format(ikcc[0])), "{}.rz".format(R_RFL[0]))
                mc.connectAttr(("{}.TwistHeel".format(ikcc[0])), "{}.ry".format(R_RFL[0]))
                mc.connectAttr(("{}.RollBall".format(ikcc[0])), "{}.rz".format("RFL_R_ball_JC"))
                mc.connectAttr(("{}.RollToe".format(ikcc[0])), "{}.rz".format("RFL_R_toe_JC"))
                mc.connectAttr(("{}.TwistToe".format(ikcc[0])), "{}.ry".format("RFL_R_toe_JC"))
                mc.connectAttr(("{}.ToeTap".format(ikcc[0])), "{}.rx".format("RFL_R_toeTap_JC"))

                # FK RIG
                # Create and rename the fk chain:
                FkChain = mc.duplicate(rjj[0], renameChildren=True)
                mc.select(FkChain)
                mel.eval('searchReplaceNames JJ1 FK hierarchy')
                rfk = mc.ls(sl=True)

                for j in rfk:
                    cc = mc.circle(nr=(1, 0, 0), n=str(j) + "_CC", constructionHistory=False)
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
                    mc.orientConstraint(cc, j)
                    if previous_sel:
                        mc.parent(offset, previous_sel)
                    previous_sel = cc
                fkhi = mc.ls("R_hip_FK_CCZERO")
                mc.delete("R_toe_FK_CCZERO")

                # Switch_IK_FK
                PC1 = mc.parentConstraint(rik[0], rfk[0], rjj[0], mo=1)
                PC2 = mc.parentConstraint(rik[1], rfk[1], rjj[1], mo=1)
                PC3 = mc.parentConstraint(rik[2], rfk[2], rjj[2], mo=1)
                PC4 = mc.parentConstraint(rik[3], rfk[3], rjj[3], mo=1)
                PC5 = mc.parentConstraint(rik[4], rfk[4], rjj[4], mo=1)

                if mc.radioButton("ikfkcc", query=True, select=True):

                    # Switch IK-FK
                    mc.shadingNode("reverse", asUtility=True, name="R_leg_REV")
                    mc.connectAttr("IK_FK_SWITCH.R_leg_IK_FK", "R_leg_REV.inputX")
                    #
                    mc.connectAttr(("R_leg_REV.outputX"), ("{}.R_hip_IKW0".format(PC1[0])))
                    mc.connectAttr(("{}.R_leg_IK_FK".format(ikfkSwitch[0])), ("{}.R_hip_FKW1".format(PC1[0])))
                    mc.connectAttr(("R_leg_REV.outputX"), ("{}.R_knee_IKW0".format(PC2[0])))
                    mc.connectAttr(("{}.R_leg_IK_FK".format(ikfkSwitch[0])), ("{}.R_knee_FKW1".format(PC2[0])))
                    mc.connectAttr(("R_leg_REV.outputX"), ("{}.R_ankle_IKW0".format(PC3[0])))
                    mc.connectAttr(("{}.R_leg_IK_FK".format(ikfkSwitch[0])), ("{}.R_ankle_FKW1".format(PC3[0])))
                    mc.connectAttr(("R_leg_REV.outputX"), ("{}.R_ball_IKW0".format(PC4[0])))
                    mc.connectAttr(("{}.R_leg_IK_FK".format(ikfkSwitch[0])), ("{}.R_ball_FKW1".format(PC4[0])))
                    mc.connectAttr(("R_leg_REV.outputX"), ("{}.R_toe_IKW0".format(PC5[0])))
                    mc.connectAttr(("{}.R_leg_IK_FK".format(ikfkSwitch[0])), ("{}.R_toe_FKW1".format(PC5[0])))

                    # Switch visibilidad de los controles
                    mc.connectAttr("IK_FK_SWITCH.R_leg_IK_FK", "{}.v".format(fkhi[0]))
                    mc.connectAttr("R_leg_REV.outputX", "{}.v".format(ikcc_off))
                    mc.connectAttr("R_leg_REV.outputX", "{}.v".format(ikpv_off))
                    #
                    mc.group(rjj[0], rik[0], rfk[0], fkhi, n="R_leg_GRP")
                    mc.parent(ikpv_off, ikcc_off, ikfk_off, "IK_GRP")
                    mc.hide(rik[0], rfk[0], R_RFL)
                    #
                    om.MGlobal.displayInfo("Your right leg rig has been mirrored with success!")

                else:
                    mc.group(rjj[0], rik[0], rfk[0], fkhi, n="R_leg_GRP")
                    mc.parent(ikpv_off, ikcc_off, "IK_GRP")
                    mc.hide(rik[0], rfk[0], R_RFL)
                    #
                    om.MGlobal.displayWarning("There was no IK_FK control, Switching skipped!")
            R_LEG()

        else:
