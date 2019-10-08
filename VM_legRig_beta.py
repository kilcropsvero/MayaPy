'''
Version 1 made in January 2018 (week # 1): Leg Rig in basic python
Scripted by Vero Morera.
veromc1692@gmail.com
'''

import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel

WIN='AutoLeg'

def UI():
    # Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title= 'VM_Leg Rig', h=30, w=150, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2, w=100)
    mc.text('Make sure you have BOTH joint chains ORIENTED. (symetrical or assymetrical)', h=25)
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button(label= 'Leg Auto', w=100, h=40, command=legs, bgc=(.2,.2,.2))
    mc.setParent('..')
    mc.separator(h=10)
    mc.text('Choose Reverse Foot Type:', align='left', h=20)
    mc.radioCollection()
    mc.radioButton('RFLChoiceA', l='Basic Foot Roll')
    mc.radioButton('RFLChoiceB', l='Smart Foot Roll')
    mc.setParent('..')

    mc.showWindow(WIN)

def legs(*args):

    lside = 'L_'
    rside = 'R_'

    if mc.objExists('IK_GRP'):
        om.MGlobal.displayError('IK_GRP already exist, creation skipped')
    else:
        mc.group( n= 'IK_GRP', empty=True )


    for side in [lside, rside]:

        firstJnt = side + 'hip_JJ'
        mc.select(firstJnt, hi=True)

        jj = mc.ls(sl=True)
        mc.select(cl=True)
        previous_sel = None

        # RFL
        mc.select(jj)
        mc.duplicate(jj[2:5])
        mc.parent(world=True)
        dup = mc.ls(sl=True)
        mc.select(cl=True)
        mc.rename(dup[0], 'RFL_' + side + 'ankle_JC')
        mc.rename(dup[1], 'RFL_' + side + 'ball_JC')
        mc.rename(dup[2], 'RFL_' + side + 'toe_JC')
        heel = mc.duplicate('RFL_' + side + 'toe_JC', n='RFL_' + side + 'heel_JC')[0]
        temp= mc.pointConstraint(side + 'temp_heel', heel)
        mc.delete(temp, side + 'temp_heel')
        toetap = mc.duplicate('RFL_' + side + 'toe_JC', n= 'RFL_' + side + 'toeTap_JC')[0]
        tempPoint = mc.pointConstraint('RFL_' + side + 'ball_JC', toetap)
        mc.delete(tempPoint)
        mc.parent('RFL_' + side + 'ankle_JC', 'RFL_' + side + 'ball_JC')
        mc.parent('RFL_' + side + 'ball_JC', 'RFL_' + side + 'toe_JC')
        mc.parent('RFL_' + side + 'toe_JC', 'RFL_' + side + 'heel_JC')
        mc.parent('RFL_' + side + 'toeTap_JC', 'RFL_' + side + 'toe_JC')
        RFL = mc.ls(heel)

        #create main leg control
        mainLegCC = mc.curve(d=1, n= side + 'mainLeg_CC', p=[ (-0.005, 0.215, 3.88), (0.014, 1.915, 2.49), (0.024, 2.645, -0.2),
                                                         (0.014, 1.645, -2.65), (-0.005,  -0.2, -3.85), (-0.025, -1.91, -2.52),
                                                         (-0.035, -2.64, 0.03), (-0.025, -1.62, 2.7), (-0.005,  0.21, 3.88),
                                                         (2.115, 0.105, 2.57), (3.155, -0.04, 0.02), (2.045, -0.18, -2.63),
                                                         (-0.005, -0.22, -3.85), (-2.065, -0.13, -2.64), (-3.155, 0.025, -0.03),
                                                         (-2.135, 0.155, 2.55), (-0.005, 0.215, 3.88)])

        temp_constraint = mc.pointConstraint(jj[0], mainLegCC, maintainOffset=0)
        mc.delete(temp_constraint)
        temp_pos = mc.xform(mainLegCC, translation=True, query=True, worldSpace=True)

        # ZeroOut MainLeg
        mainLegCC_off = mc.group(mainLegCC, n='grp' + side +'mainLegCCZERO')
        mc.setAttr('{}.overrideEnabled'.format(mainLegCC_off), 1)
        mc.setAttr('{}.overrideColor'.format(mainLegCC_off), 14)
        mc.xform(mainLegCC_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.setAttr('{}.translate'.format(mainLegCC), 0, 0, 0)

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(mainLegCC + trs, lock=True, keyable=False, channelBox=False)


    # IK RIG
        # Create and rename the ik chain:
        IkChain = mc.duplicate(jj[0], renameChildren=True)
        mc.select(IkChain)
        mel.eval('searchReplaceNames JJ1 IK hierarchy')
        ik = mc.ls(sl=True)

        # Create the Iksolvers:
        upperleg = mc.ls(ik[0], ik[2])
        mc.select(upperleg)
        IKRP = mc.ikHandle(name= side + 'leg_IkRp', solver='ikRPsolver')
        #
        loLegBall = mc.ls(ik[2:4])
        mc.select(loLegBall)
        IKSC_1 = mc.ikHandle(name= side + 'ball_IkSc', solver='ikSCsolver')
        #
        loLegToe = mc.ls(ik[3:5])
        mc.select(loLegToe)
        IKSC_2 = mc.ikHandle(name= side + 'toe_IkSc', solver='ikSCsolver')

        # Parent solvers into RFL
        mc.parent(IKRP[0], 'RFL_' + side + 'ankle_JC')
        mc.parent(IKSC_1[0], 'RFL_' + side + 'ball_JC')
        mc.parent(IKSC_2[0], 'RFL_' + side + 'toeTap_JC')

        # Create Controlers
        ikcc = mc.circle(n= side + 'foot_IK1_CC', c=(0, 0, 0), nr=(0, 1, 0), r=2, constructionHistory=False)
        mc.hilite(ikcc)
        mc.select('{}.cv[0:2]'.format(ikcc[0]), r=True)
        mc.move(0, 0, -0.429197, r=True, wd=True)
        mc.select('{}.cv[1]'.format(ikcc[0]), r=True)
        mc.move(0, 1.118781, 0, r=True, wd=True)
        mc.select('{}.cv[4:6]'.format(ikcc[0]), r=True)
        mc.move(0, 0, 2.024508, r=True, wd=True)
        mc.select('{}.cv[5]'.format(ikcc[0]), r=True)
        mc.move(0, 0.345089, 0, r=True, wd=True)
        tempPoint = mc.pointConstraint(ik[2], ikcc, maintainOffset=0)
        mc.delete(tempPoint)
        temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)
        mc.hilite(ikcc[0])
        mc.select('{}.cv[0:7]'.format(ikcc[0]))
        mc.move(0, -2, 1.6, r=True, wd=True)

        # rotate order
        mc.setAttr('{}.rotateOrder'.format(ikcc[0]), channelBox=True, keyable=True)
        mc.setAttr('{}.rotateOrder'.format(ikcc[0]), 3)

        # create secondary control for IK:
        mc.duplicate(ikcc, n=side + 'foot_IK2_CC')
        ikcc2 = side + 'foot_IK2_CC'

        mc.hilite(ikcc2)
        mc.select('{}.cv[0:7]'.format(ikcc2), r=True)
        mc.scale(0.8, 0.8, 0.8, r=True)

        # ZeroOut ikcc
        ikcc_off = mc.group(ikcc, n='grp' + side + 'foot_IK1_CCZERO')
        mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.setAttr('{}.translate'.format(ikcc[0]), 0, 0, 0)
        mc.setAttr('{}.rotate'.format(ikcc[0]), 0, 0, 0)

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikcc2 + trs, lock=True, keyable=False, channelBox=False)

        # ZeroOut ikcc2
        ikcc2_off = mc.group(n='grp' + side + 'foot_IK2_CCZERO', empty=True)
        mc.xform(ikcc2_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.parent(ikcc2, ikcc2_off)
        mc.setAttr('{}.translate'.format(ikcc[0]), 0, 0, 0)
        mc.setAttr('{}.rotate'.format(ikcc[0]), 0, 0, 0)
        mc.xform('grp' + side + 'foot_IK2_CCZERO', cpc=1)

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikcc2 + trs, lock=True, keyable=False, channelBox=False)

        mc.parent(ikcc2_off, ikcc)

        # Pole Vector
        ikpv = mc.curve(d=1, n= side + 'leg_PV', p=[(-4.37114e-08, -1, -1),(0, 0, 1),
                                (1, 0, -1),(1.31134e-07, 1, -1),
                                (0, 0, 1),(-1, 8.74228e-08, -1),
                                (-4.37114e-08, -1, -1),(1, 0, -1),
                                (1.31134e-07, 1, -1),(-1, 8.74228e-08, -1)])
        temp_constraint = mc.pointConstraint(ik[1], ikpv, maintainOffset=0)
        mc.delete(temp_constraint)
        mc.poleVectorConstraint(ikpv, IKRP[0], weight=1, )
        temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)
        # Anotation
        kneePos = mc.xform(ik[1], ws=True, translation=True, q=True)
        legAnnot = mc.annotate(ikpv, p=(kneePos[0], kneePos[1], kneePos[2]))
        mc.parent(legAnnot, side + 'knee_JJ')
        mc.setAttr('{}.overrideEnabled' .format(legAnnot), 1)
        mc.setAttr('{}.overrideDisplayType' .format(legAnnot), 2)
        mc.setAttr('{}.overrideDisplayType' .format(legAnnot), 1)

        # ZeroOut ikpv
        ikpv_off = mc.group(ikpv, n= 'grp_' + side + 'leg_PVZERO')
        mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
        mc.setAttr('{}.translate'.format(ikpv), 0, 0, 0)
        mc.xform(ikpv_off, cpc=1)
        mc.move(0, 0, 15, ikpv_off, r=True)
        #
        for trs in [ '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikpv + trs, lock=True, keyable=False, channelBox=False)


        if mc.radioButton('RFLChoiceA', query=True, select=True):
            # Create attributes for the RFL
            mc.parent(heel, ikcc2)
            mc.addAttr(ikcc, ln='______________', attributeType='enum', enumName='RFL', k=True, h=False)
            mc.setAttr('{}.______________'.format(ikcc[0]), lock=True)
            mc.addAttr(ikcc, ln='RollHeel', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='TwistHeel', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='RollBall', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='RollToe', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='TwistToe', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='ToeTap', attributeType='double', dv=0, k=True, h=False)
            #mc.addAttr(ikcc, ln='SideToSide', attributeType='double', min=-10, max=10, dv=0, k=True, h=False)

            # Make extra attributes for main ik control:
            mc.addAttr(ikcc, ln='_______________', attributeType='enum', enumName='EXTRAS', k=True, h=False)
            mc.setAttr('{}._______________'.format(ikcc[0]), lock=True)
            mc.addAttr(ikcc, ln='StretchyOnOff', attributeType='long', min=0, max=1, dv=1, k=True, h=False)
            mc.addAttr(ikcc, ln='PoleVectorToSnap', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='PoleVectorToKneeTwist', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='GimbalControlVis', attributeType='long', min=0, max=1, dv=1, k=True, h=False)

            # Connect attributes for the RFL
            mc.connectAttr(('{}.RollHeel'.format(ikcc[0])), '{}.rz'.format(heel))
            mc.connectAttr(('{}.TwistHeel'.format(ikcc[0])), '{}.ry'.format(heel))
            mc.connectAttr(('{}.RollBall'.format(ikcc[0])), '{}.rz'.format('RFL_' + side + 'ball_JC'))
            mc.connectAttr(('{}.RollToe'.format(ikcc[0])), '{}.rz'.format('RFL_' + side + 'toe_JC'))
            mc.connectAttr(('{}.TwistToe'.format(ikcc[0])), '{}.ry'.format('RFL_' + side + 'toe_JC'))
            mc.connectAttr(('{}.ToeTap'.format(ikcc[0])), '{}.rz'.format('RFL_' + side + 'toeTap_JC'))

        elif mc.radioButton('RFLChoiceB', query=True, select=True):
            mc.parent(heel, ikcc2)

            mc.addAttr(ikcc, ln='______________', attributeType='enum', enumName='RFL', k=True, h=False)
            mc.setAttr('{}.______________'.format(ikcc[0]), lock=True)
            mc.addAttr(ikcc, ln='footRoll', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='TwistHeel', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='TwistToe', attributeType='double', dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='ToeTap', attributeType='double', dv=0, k=True, h=False)
            #mc.addAttr(ikcc, ln='SideToSide', attributeType='double', min= -10, max=10, dv=0, k=True, h=False)

            mc.addAttr(ikcc, ln='_____________', attributeType='enum', enumName='SETTINGS', k=True, h=False)
            mc.setAttr('{}._____________'.format(ikcc[0]), lock=True)
            mc.addAttr(ikcc, ln='bendLimitAngle', attributeType='double', dv=35, k=True, h=False)
            mc.addAttr(ikcc, ln='toeStraightAngle', attributeType='double', dv=55, k=True, h=False)

            # Make extra attributes for main ik control:
            mc.addAttr(ikcc, ln='_______________', attributeType='enum', enumName='EXTRAS', k=True, h=False)
            mc.setAttr('{}._______________'.format(ikcc[0]), lock=True)
            mc.addAttr(ikcc, ln='StretchyOnOff', attributeType='long', min=0, max=1, dv=1, k=True, h=False)
            mc.addAttr(ikcc, ln='PoleVectorToSnap', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='PoleVectorToKneeTwist', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
            mc.addAttr(ikcc, ln='GimbalControlVis', attributeType='long', min=0, max=1, dv=1, k=True, h=False)
            #


            for trs in [ '.sx', '.sy', '.sz', '.v']:
                mc.setAttr(ikcc[0] + trs, lock=True, keyable=False, channelBox=False)

            # heel setup
            heelRotClamp = mc.shadingNode('clamp', asUtility=True, name= side + 'heelRot_CLAMP')
            mc.setAttr('{}.minR'.format(heelRotClamp), - 90)
            mc.connectAttr('{}.footRoll'.format(ikcc[0]), '{}.inputR'.format(heelRotClamp))
            mc.connectAttr('{}.outputR'.format(heelRotClamp), '{}.rz'.format(heel))

            # toeSetup
            BendStraightClamp = mc.shadingNode('clamp', asUtility=True, name= side + 'footBendToStraigh_CLAMP')
            BendStraightPercent = mc.shadingNode('setRange', asUtility=True, name= side + 'footBendToStraight_PERCENT')
            footRollMult = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'footRoll_MULT')
            #
            mc.connectAttr('{}.footRoll'.format(ikcc[0]), '{}.inputR'.format(BendStraightClamp))
            mc.connectAttr('{}.bendLimitAngle'.format(ikcc[0]), '{}.minR'.format(BendStraightClamp))
            mc.connectAttr('{}.toeStraightAngle'.format(ikcc[0]), '{}.maxR'.format(BendStraightClamp))
            #
            mc.connectAttr('{}.inputR'.format(BendStraightClamp), '{}.valueX'.format(BendStraightPercent))
            mc.connectAttr('{}.minR'.format(BendStraightClamp), '{}.oldMinX'.format(BendStraightPercent))
            mc.connectAttr('{}.maxR'.format(BendStraightClamp), '{}.oldMaxX'.format(BendStraightPercent))
            mc.setAttr('{}.maxX'.format(BendStraightPercent), 1)
            #
            mc.connectAttr('{}.inputR'.format(BendStraightClamp), '{}.input2X'.format(footRollMult))
            mc.connectAttr('{}.outValueX'.format(BendStraightPercent), '{}.input1X'.format(footRollMult))
            mc.connectAttr('{}.outputX'.format(footRollMult), 'RFL_' + side + 'toe_JC.rz')

            # ballSetup
            BallZeroToBendClamp = mc.shadingNode('clamp', asUtility=True, name= side + 'ball_ZeroToBend_CLAMP')
            BallZeroToBendPercent = mc.shadingNode('setRange', asUtility=True, name= side + 'ball_zeroToBend_PERCENT')
            BallPercentMult = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'ball_percent_MULT')
            BallRollMult = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'ball_roll_MULT')
            FootInvertPercentage = mc.shadingNode('plusMinusAverage', asUtility=True, name= side + 'footInvertPercentage_PMA')
            mc.setAttr('{}.maxX'.format(BallZeroToBendPercent), 1)
            mc.setAttr('{}.operation'.format(FootInvertPercentage), 2)
            mc.connectAttr('{}.footRoll'.format(ikcc[0]), '{}.inputR'.format(BallZeroToBendClamp))
            mc.connectAttr('{}.toeStraightAngle'.format(ikcc[0]), '{}.minR'.format(BallZeroToBendClamp))
            mc.connectAttr('{}.bendLimitAngle'.format(ikcc[0]), '{}.maxR'.format(BallZeroToBendClamp))
            mc.connectAttr('{}.inputR'.format(BallZeroToBendClamp), '{}.valueX'.format(BallZeroToBendPercent))
            mc.connectAttr('{}.maxR'.format(BallZeroToBendClamp), '{}.oldMaxX'.format(BallZeroToBendPercent))
            mc.connectAttr('{}.minR'.format(BallZeroToBendClamp), '{}.oldMinX'.format(BallZeroToBendPercent))
            #
            mc.setAttr('{}.input1D[0]'.format(FootInvertPercentage), 1)
            mc.setAttr('{}.input1D[1]'.format(FootInvertPercentage), 1)
            mc.connectAttr('{}.outValueX'.format(BendStraightPercent), '{}.input1D[1]'.format(FootInvertPercentage))
            mc.connectAttr('{}.output1D'.format(FootInvertPercentage), '{}.input2X'.format(BallPercentMult))
            #
            mc.connectAttr('{}.outValueX'.format(BallZeroToBendPercent), '{}.input1X'.format(BallPercentMult))
            mc.connectAttr('{}.outputX'.format(BallPercentMult), '{}.input1X'.format(BallRollMult))
            mc.connectAttr('{}.footRoll'.format(ikcc[0]), '{}.input2X'.format(BallRollMult))
            mc.connectAttr('{}.outputX'.format(BallRollMult), 'RFL_' + side + 'ball_JC.rz')

            # Extra Attributes
            mc.connectAttr('{}.TwistHeel'.format(ikcc[0]), 'RFL_' + side + 'heel_JC.ry')
            mc.connectAttr('{}.TwistToe'.format(ikcc[0]), 'RFL_' + side + 'toe_JC.ry')
            mc.connectAttr('{}.ToeTap'.format(ikcc[0]), 'RFL_' + side + 'toeTap_JC.rz')

        else:
            om.MGlobal.displayWarning('No ReverseFoot Choise selected, IK foot attributes Skipped.')

    # FK RIG
        # Create and rename the fk chain:
        FkChain = mc.duplicate(jj[0], renameChildren=True)
        mc.select(FkChain)
        mel.eval('searchReplaceNames JJ1 FK hierarchy')
        fk = mc.ls(sl=True)

        for j in fk:
            cc = mc.circle(nr=(1, 0, 0), n=str(j) + '_CC', r=2, constructionHistory=False)
            mc.makeIdentity(apply=True)
            temp_constraint = mc.parentConstraint(j, cc, maintainOffset=0)
            mc.delete(temp_constraint)
            temp_rot = mc.xform(cc, rotation=True, query=True, worldSpace=True)

            # ZeroOut
            offset = mc.group(cc, n=str(j) + '_CCZERO')
            mc.xform(offset, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
            mc.setAttr('{}.rotate'.format(cc[0]), 0, 0, 0)


            for trs in ['.tx', '.ty', '.tz', '.sx', '.sy', '.sz', '.v']:
                mc.setAttr(cc[0] + trs, lock=True, keyable=False, channelBox=False)

            mc.setAttr('{}.rotateOrder'.format(cc[0]), channelBox=True, keyable=False)
            mc.setAttr('{}.rotateOrder'.format(cc[0]), 3)

            # fk hierarchy
            mc.orientConstraint(cc, j)
            if previous_sel:
                mc.parent(offset, previous_sel)
            previous_sel = cc
        fkhi = mc.ls( side + 'hip_FK_CCZERO')
        mc.delete( side +  'toe_FK_CCZERO')

        # Switch_IK_FK
        PC1 = mc.parentConstraint(ik[0], fk[0], jj[0], mo=1)
        PC2 = mc.parentConstraint(ik[1], fk[1], jj[1], mo=1)
        PC3 = mc.parentConstraint(ik[2], fk[2], jj[2], mo=1)
        PC4 = mc.parentConstraint(ik[3], fk[3], jj[3], mo=1)
        PC5 = mc.parentConstraint(ik[4], fk[4], jj[4], mo=1)

        #Stretchy Leg
        startPos= mc.xform(ik[0], translation=True, q=True, ws=True)
        endPos= mc.xform(ik[2], translation=True, q=True, ws=True)
        dist = mc.distanceDimension(sp=(startPos[0], startPos[1], startPos[2]),
                                      ep=(endPos[0], endPos[1], endPos[2]))
        distLoc= mc.listConnections(dist)
        distShape= mc.listConnections(shapes=True)
        mc.pointConstraint(ik[0], distLoc[0])
        mc.parent(distLoc[1], ikcc[0])
        mc.rename(distLoc[0], side + 'stretchyLeg_01_LOC')
        mc.rename(distLoc[1], side + 'stretchyLeg_02_LOC')
        #
        div= mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'leg_stretchy_DIV')
        normalizeDiv = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'leg_normalize_DIV')
        con= mc.shadingNode('condition', asUtility=True, name= side + 'leg_CON')
        # Add Stretchy On/Off
        onOff = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'legStretchyOnOff_MULT')

        mc.setAttr(div + '.operation', 2)
        mc.setAttr(normalizeDiv + '.operation', 2)
        mc.setAttr(con + '.operation', 2)
        secondTerm = mc.getAttr('{}.distance'.format(dist))
        mc.setAttr('{}.secondTerm' .format(con), secondTerm)
        mc.setAttr('{}.input2X' .format(div), secondTerm)
        mc.connectAttr('{}.outColorR' .format(con), '{}.input1X' .format(div))
        mc.connectAttr('{}.distance'.format(distShape[0]), '{}.input1X'.format(onOff))
        mc.connectAttr('{}.outputX'.format(onOff), '{}.input1X'.format(normalizeDiv))
        mc.connectAttr('{}.StretchyOnOff'.format(ikcc[0]), '{}.input2X'.format(onOff))
        mc.connectAttr('{}.scaleY'.format('root_CC'), '{}.input2X' .format(normalizeDiv))
        mc.connectAttr('{}.outputX'.format(normalizeDiv), '{}.secondTerm'.format(con))
        mc.connectAttr('{}.outputX'.format(normalizeDiv), '{}.colorIfFalseR'.format(con))
        firstTerm = mc.getAttr('{}.distance' .format(dist))
        mc.setAttr('{}.firstTerm'.format(con), firstTerm)
        mc.setAttr('{}.colorIfTrueR'.format(con), firstTerm)
        mc.connectAttr('{}.outputX' .format(div), '{}.sx' .format(ik[0]))
        mc.connectAttr('{}.outputX' .format(div), '{}.sx'.format(ik[1]))

        stretchGRP= mc.group(side + 'stretchyLeg_01_LOC', dist, n= side + 'stretchyLeg_GRP')
        mc.hide(side + 'stretchyLeg_02_LOC')

        #Hide GimbalControl
        mc.connectAttr(ikcc[0] + '.GimbalControlVis', ikcc2_off + '.v')

        # Create IK FK control
        v1 = mc.curve(d=1, p=[(0.052, 4.96, 0), (0.061, 4.97, 0), (0.070, 4.98, 0), (0.164, 5.13, 0), (0.178, 5.14, 0),
                              (0.184, 5.14, 0), (0.196, 5.14, 0), (0.204, 5.14, 0), (0.346, 5.09, 0), (0.371, 5.08, 0),
                              (0.375, 5.07, 0), (0.373, 5.05, 0), (0.364, 4.88, 0), (0.365, 4.87, 0), (0.368, 4.86, 0),
                              (0.425, 4.82, 0), (0.438, 4.82, 0), (0.453, 4.82, 0), (0.606, 4.89, 0), (0.621, 4.90, 0),
                              (0.632, 4.90, 0), (0.644, 4.88, 0), (0.746, 4.76, 0), (0.759, 4.74, 0), (0.760, 4.73, 0),
                              (0.747, 4.72, 0), (0.650, 4.58, 0), (0.642, 4.57, 0), (0.639, 4.56, 0), (0.668, 4.49, 0),
                              (0.679, 4.48, 0), (0.694, 4.48, 0), (0.863, 4.46, 0), (0.877, 4.45, 0), (0.886, 4.45, 0),
                              (0.888, 4.43, 0), (0.910, 4.26, 0), (0.909, 4.26, 0), (0.909, 4.25, 0), (0.901, 4.25, 0),
                              (0.886, 4.24, 0), (0.733, 4.17, 0), (0.721, 4.17, 0), (0.712, 4.16, 0), (0.699, 4.08, 0),
                              (0.703, 4.07, 0), (0.717, 4.06, 0), (0.844, 3.94, 0), (0.853, 3.94, 0), (0.860, 3.93, 0),
                              (0.854, 3.91, 0), (0.783, 3.76, 0), (0.778, 3.75, 0), (0.770, 3.75, 0), (0.759, 3.75, 0),
                              (0.752, 3.75, 0), (0.588, 3.78, 0), (0.574, 3.78, 0), (0.561, 3.78, 0), (0.500, 3.71, 0),
                              (0.498, 3.70, 0), (0.503, 3.68, 0), (0.548, 3.52, 0), (0.554, 3.50, 0), (0.551, 3.50, 0),
                              (0.533, 3.48, 0), (0.410, 3.41, 0), (0.392, 3.39, 0), (0.385, 3.40, 0), (0.369, 3.41, 0),
                              (0.253, 3.52, 0), (0.241, 3.54, 0), (0.228, 3.54, 0), (0.127, 3.51, 0), (0.118, 3.50, 0),
                              (0.114, 3.48, 0), (0.065, 3.32, 0), (0.060, 3.31, 0), (0.053, 3.30, 0), (-0.123, 3.30, 0),
                              (-0.131, 3.31, 0), (-0.137, 3.32, 0), (-0.177, 3.49, 0), (-0.181, 3.50, 0),
                              (-0.188, 3.51, 0),
                              (-0.296, 3.55, 0), (-0.308, 3.55, 0), (-0.320, 3.54, 0), (-0.448, 3.43, 0),
                              (-0.460, 3.42, 0),
                              (-0.470, 3.41, 0), (-0.484, 3.42, 0), (-0.603, 3.51, 0), (-0.615, 3.52, 0),
                              (-0.615, 3.52, 0),
                              (-0.621, 3.52, 0), (-0.615, 3.54, 0), (-0.558, 3.70, 0), (-0.555, 3.72, 0),
                              (-0.555, 3.73, 0),
                              (-0.564, 3.74, 0), (-0.619, 3.81, 0), (-0.628, 3.81, 0), (-0.637, 3.82, 0),
                              (-0.651, 3.82, 0),
                              (-0.819, 3.80, 0), (-0.834, 3.79, 0), (-0.844, 3.80, 0), (-0.851, 3.81, 0),
                              (-0.905, 3.95, 0),
                              (-0.910, 3.96, 0), (-0.911, 3.97, 0), (-0.895, 3.98, 0), (-0.763, 4.09, 0),
                              (-0.752, 4.10, 0),
                              (-0.745, 4.11, 0), (-0.747, 4.12, 0), (-0.755, 4.22, 0), (-0.762, 4.23, 0),
                              (-0.776, 4.23, 0),
                              (-0.918, 4.30, 0), (-0.947, 4.31, 0), (-0.947, 4.32, 0), (-0.916, 4.48, 0),
                              (-0.909, 4.50, 0),
                              (-0.885, 4.51, 0), (-0.715, 4.52, 0), (-0.702, 4.52, 0), (-0.692, 4.53, 0),
                              (-0.646, 4.62, 0),
                              (-0.648, 4.63, 0), (-0.657, 4.64, 0), (-0.744, 4.78, 0), (-0.755, 4.80, 0),
                              (-0.754, 4.81, 0),
                              (-0.740, 4.82, 0), (-0.635, 4.93, 0), (-0.621, 4.94, 0), (-0.613, 4.95, 0),
                              (-0.594, 4.94, 0),
                              (-0.447, 4.86, 0), (-0.432, 4.85, 0), (-0.417, 4.85, 0), (-0.345, 4.89, 0),
                              (-0.339, 4.91, 0),
                              (-0.339, 4.93, 0), (-0.338, 5.09, 0), (-0.338, 5.10, 0), (-0.333, 5.11, 0),
                              (-0.316, 5.11, 0),
                              (-0.162, 5.15, 0), (-0.142, 5.16, 0), (-0.135, 5.15, 0), (-0.124, 5.14, 0),
                              (-0.040, 4.99, 0),
                              (-0.032, 4.98, 0), (-0.023, 4.97, 0), (0.052, 4.96, 0)])
        v2 = mc.curve(d=1, p=[(0, -0.027, 0), (-0.03, 3.3, 0)])

        mc.select(v1, v2)
        mc.ls(sl=True)
        shps = mc.listRelatives(shapes=True)
        mc.parent(shps, v1, relative=True, shape=True)
        mc.delete(v2)
        sel = mc.rename(v1, side + 'leg_IK_FK_SWITCH')
        ikfk_off = mc.group(sel, name='grp' + side + 'leg_IK_FK_SwitchZERO')
        ikfkSwitch = mc.ls(sel)

        #
        mc.move(0, -2.6, 0, ikfkSwitch[0] + '.rotatePivot', r=True)
        mc.move(0, -2.6, 0, ikfk_off + '.rotatePivot', r=True)
        mc.addAttr(sel, longName='IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)

        for trs in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']:
            mc.setAttr(sel + trs, lock=True, keyable=False, channelBox=False)

        # position
        mc.pointConstraint(jj[2], ikfk_off, mo=False)
        for rot in ['.rx', '.rz']:
            mc.setAttr(ikfk_off + rot, -90)
        mc.orientConstraint(jj[2], ikfk_off, mo=True)

        #Switch IK-FK
        mc.shadingNode ('reverse', asUtility=True, name=  side + 'leg_REV')
        mc.connectAttr( side + 'leg_IK_FK_SWITCH.' + 'IK_FK', side + 'leg_REV.inputX' )
        #
        mc.connectAttr( (side + 'leg_REV.outputX'), ( PC1[0] + '.' + side + 'hip_IKW0' ) )
        mc.connectAttr( (ikfkSwitch[0] + '.' + 'IK_FK'), (PC1[0] + '.' + side + 'hip_FKW1') )
        mc.connectAttr( (side + 'leg_REV.outputX'), (PC2[0] + '.' + side + 'knee_IKW0'))
        mc.connectAttr( (ikfkSwitch[0] + '.' + 'IK_FK'), (PC2[0] + '.' + side + 'knee_FKW1') )
        mc.connectAttr( (side + 'leg_REV.outputX'), ( PC3[0] + '.' + side + 'ankle_IKW0') )
        mc.connectAttr( (ikfkSwitch[0] + '.' + 'IK_FK'), (PC3[0] + '.' + side + 'ankle_FKW1') )
        mc.connectAttr( (side + 'leg_REV.outputX'), (PC4[0] + '.' + side + 'ball_IKW0') )
        mc.connectAttr( (ikfkSwitch[0] + '.' + 'IK_FK'), (PC4[0] + '.' + side + 'ball_FKW1') )
        mc.connectAttr( (side + 'leg_REV.outputX'), (PC5[0] + '.' + side + 'toe_IKW0') )
        mc.connectAttr( (ikfkSwitch[0] + '.' + 'IK_FK'), (PC5[0] + '.' + side + 'toe_FKW1') )

        # Switch visibilidad de los controles
        mc.connectAttr( side + 'leg_IK_FK_SWITCH.' + 'IK_FK', '{}.v'.format(fkhi[0]) )
        mc.connectAttr( side + 'leg_REV.outputX', '{}.v'.format(ikcc_off) )
        mc.connectAttr( side + 'leg_REV.outputX', '{}.v'.format(ikpv_off))
        mc.connectAttr( side + 'leg_REV.outputX', '{}.v'.format(legAnnot))
        #
        grp = mc.group(n= side + 'leg_GRP', empty=True)
        temp = mc.pointConstraint(jj[0], grp)
        mc.delete(temp)
        mc.parent(jj[0], ik[0], fk[0], fkhi, mainLegCC)
        mc.parent(mainLegCC_off, grp)

        mc.parent(ikpv_off, ikcc_off, ikfk_off, 'IK_GRP')
        mc.parent(stretchGRP, 'IK_GRP')
        mc.hide(ik[0], fk[0], RFL, stretchGRP)
        #
        om.MGlobal.displayInfo('Your leg rig has been created with success!')


    blue = ['grpL_foot_IK1_CCZERO', 'L_hip_FK_CCZERO', 'grp_L_leg_PVZERO']
    red = ['grpR_foot_IK1_CCZERO', 'R_hip_FK_CCZERO', 'grp_R_leg_PVZERO']
    lightBlue = ['grpL_foot_IK2_CCZERO', 'grpL_leg_IK_FK_SwitchZERO']
    lightRed = ['grpR_foot_IK2_CCZERO', 'grpR_leg_IK_FK_SwitchZERO']

    for b in blue:
        mc.setAttr('{}.overrideEnabled'.format(b), 1)
        mc.setAttr('{}.overrideColor'.format(b), 6)

    for r in red:
        mc.setAttr('{}.overrideEnabled'.format(r), 1)
        mc.setAttr('{}.overrideColor'.format(r), 13)

    for lb in lightBlue:
        mc.setAttr('{}.overrideEnabled'.format(lb), 1)
        mc.setAttr('{}.overrideColor'.format(lb), 18)

    for lr in lightRed:
        mc.setAttr('{}.overrideEnabled'.format(lr), 1)
        mc.setAttr('{}.overrideColor'.format(lr), 20)
