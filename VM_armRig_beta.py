'''
Version 2 made in July 2018. Arm Rig in basic python
Scripted by Vero Morera, July 2018.
veromc1692@gmail.com
'''

import maya.cmds as mc
import maya.OpenMaya as om
import maya.mel as mel

def arms(*args):


    lside = 'L_'
    rside = 'R_'

    if mc.objExists('IK_GRP'):
        om.MGlobal.displayError('IK_GRP already exist, creation skipped')
    else:
        mc.group( n= 'IK_GRP', empty=True )


    for side in [lside, rside]:

        firstJnt = side + 'clavicle_JJ'
        mc.select(firstJnt, hi=True)

        jj = mc.ls( sl=True )
        mc.select(cl=True)
        previous_sel = None

        # IK RIG
        # Create and rename the ik chain:
        IkChain = mc.duplicate(jj[1], renameChildren=True)
        mc.select(IkChain, hi=True)
        mel.eval('searchReplaceNames JJ1 IK hierarchy')
        ik = mc.ls(sl=True)

        # Create the Iksolver:
        IKRP = mc.ikHandle(name= side + 'arm_IkRp', solver='ikRPsolver', sj=ik[0], ee=ik[2])

        # Create Controlers
        ikcc = mc.circle(n= side + 'arm_IK1_CC', c=(0, 0, 0), nr=(1, 0, 0), r=1.8, constructionHistory=False)
        mc.makeIdentity(apply=True)
        tempPoint = mc.parentConstraint(ik[2], ikcc, maintainOffset=0)
        mc.delete(tempPoint)
        temp_pos = mc.xform(ikcc, translation=True, query=True, worldSpace=True)
        temp_rot = mc.xform(ikcc, rotation=True, query=True, worldSpace=True)

        #rotate order
        mc.setAttr( '{}.rotateOrder'.format(ikcc[0]), k=False, channelBox=True )
        mc.setAttr('{}.rotateOrder'.format(ikcc[0]), 3)


        # create secondary control for IK:
        mc.duplicate(ikcc, n=side + 'arm_IK2_CC')
        ikcc2 = side + 'arm_IK2_CC'

        mc.hilite(ikcc2)
        mc.select('{}.cv[0:7]'.format(ikcc2), r=True)
        mc.scale(0.75, 0.75, 0.75, r=True)

        mc.parent(IKRP[0], ikcc2)

        #Make extra attributes for main ik control:
        mc.addAttr(ikcc[0], ln='______________', attributeType='enum', enumName='SPACES', k=True, h=False)
        mc.setAttr('{}.______________'.format(ikcc[0]), lock=True)
        mc.addAttr(ikcc, ln='ParentTo', attributeType='enum', enumName='Default:Head:Chest:COG:Pelvis:Root', k=True, h=False)
        mc.addAttr(ikcc, ln='_______________', attributeType='enum', enumName='EXTRAS', k=True, h=False)
        mc.setAttr( '{}._______________'.format(ikcc[0]), lock=True)
        mc.addAttr(ikcc, ln='StretchyOnOff', attributeType='long', min=0, max=1, dv=1, k=True, h=False)
        mc.addAttr(ikcc, ln='PoleVectorToSnap', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln='PoleVectorToElbowTwist', attributeType='long', min=0, max=1, dv=0, k=True, h=False)
        mc.addAttr(ikcc, ln='GimbalControlVis', attributeType='long', min=0, max=1, dv=1, k=True, h=False)

        # ZeroOut ikcc
        ikcc_off = mc.group(n='grp' + side + 'arm_IK1_CCZERO', empty=True)
        mc.xform(ikcc_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.xform(ikcc_off, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
        mc.parent(ikcc, ikcc_off)
        mc.setAttr('{}.translate'.format(ikcc[0]), 0, 0, 0)
        mc.setAttr('{}.rotate'.format(ikcc[0]), 0, 0, 0)
        mc.xform('grp' + side + 'arm_IK1_CCZERO', cpc=1)

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikcc[0] + trs, lock=True, keyable=False, channelBox=False)

        # ZeroOut ikcc2
        ikcc2_off = mc.group(n='grp' + side + 'arm_IK2_CCZERO', empty=True)
        mc.xform(ikcc2_off, worldSpace=True, translation=(temp_pos[0], temp_pos[1], temp_pos[2]))
        mc.xform(ikcc2_off, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
        mc.parent(ikcc2, ikcc2_off)
        mc.setAttr('{}.translate'.format(ikcc[0]), 0, 0, 0)
        mc.setAttr('{}.rotate'.format(ikcc[0]), 0, 0, 0)
        mc.xform('grp' + side + 'arm_IK2_CCZERO', cpc=1)

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikcc2 + trs, lock=True, keyable=False, channelBox=False)

        mc.parent(ikcc2_off, ikcc)
        mc.orientConstraint(ikcc2, ik[2], maintainOffset=1)

        # Pole Vector
        ikpv = mc.curve(d=1, n= side + 'arm_PV', p=[(-0.7, -1.19209e-07, 0.2),(0, 0, -1.19),
                                              (0, 0.7, 0.2),(-0.7, -1.19209e-07, 0.2),
                                              (0, -0.7, 0.2),(0, 0, -1.19),(0.7, 0, 0.2),
                                              (0, -0.7, 0.2),(0.7, 0, 0.2),(0, 0.7, 0.2)])
        mc.makeIdentity(apply=True)
        temp_constraint = mc.pointConstraint(ik[1], ikpv, maintainOffset=0)
        mc.delete(temp_constraint)
        mc.poleVectorConstraint(ikpv, IKRP[0], weight=1)
        temp_pos2 = mc.xform(ikpv, translation=True, query=True, worldSpace=True)

        # ZeroOut ikpv
        ikpv_off = mc.group(ikpv, n='grp' + side + 'arm_PVZERO')
        mc.xform(ikpv_off, worldSpace=True, translation=(temp_pos2[0], temp_pos2[1], temp_pos2[2]))
        mc.setAttr('{}.translate'.format(ikpv), 0, 0, 0)
        mc.xform(ikpv_off, cpc=1)
        mc.move(0, 0, -10, ikpv_off, r=True)

        for trs in ['.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']:
            mc.setAttr(ikpv + trs, lock=True, keyable=False, channelBox=False)

        # FK RIG
        # Create and rename the fk chain:
        FkChain = mc.duplicate(jj[1], renameChildren=True)
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

            # rotate order
            mc.setAttr('{}.rotateOrder'.format(cc[0]), k=False, channelBox=True)

            # fk hierarchy
            mc.orientConstraint(cc, j, maintainOffset=0)
            if previous_sel:
                mc.parent(offset, previous_sel)
            previous_sel = cc

        mc.addAttr(cc[0], ln='______________', attributeType='enum', enumName='SPACES', k=True, h=False)
        mc.setAttr('{}.______________'.format(ikcc[0]), lock=True)
        mc.addAttr(cc, ln='ParentTo', attributeType='enum', enumName='Default:Chest:COG:Pelvis:Root', k=True, h=False)

        #set rotateOrder to avoid gimbal
        mc.setAttr('{}.rotateOrder'.format(side + 'shoulder_FK_CC'), 3) #shoulder
        mc.setAttr('{}.rotateOrder'.format(side + 'wrist_FK_CC'), 1) #wrist

        #clavicle
        clav= mc.circle(nr=(1, 0, 0), n= side + 'clavicle_FK_CC', r=2, constructionHistory=False)
        mc.makeIdentity(apply=True)
        temp_constraint = mc.parentConstraint(jj[0], clav, maintainOffset=0)
        mc.delete(temp_constraint)
        temp_pos = mc.xform(clav, translation=True, query=True, worldSpace=True)
        temp_rot = mc.xform(clav, rotation=True, query=True, worldSpace=True)
        clav_grp=mc.group(clav, n= side + 'clavicle_FK_CCZERO')
        mc.xform(clav_grp, worldSpace=True, rotation=(temp_rot[0], temp_rot[1], temp_rot[2]))
        mc.setAttr('{}.rotate'.format(clav[0]), 0, 0, 0)
        mc.parentConstraint(clav, jj[0])

        for trs in ['.sx', '.sy', '.sz', '.v']:
            mc.setAttr(clav[0] + trs, lock=True, keyable=False, channelBox=False)

        # rotate order
        mc.setAttr('{}.rotateOrder'.format(clav[0]), k=False, channelBox=True)
        mc.setAttr('{}.rotateOrder'.format(clav[0]), 3)


        mc.parent(side + 'shoulder_FK_CCZERO', side + 'clavicle_FK_CC')
        fkhi = mc.ls( side + 'shoulder_FK_CCZERO')

        # Arm Twist (J.Dobra style)
        #Create the main chains and handles:
        upTwistHandle = mc.duplicate(jj[1], renameChildren=True)
        mc.select(upTwistHandle, hi=True)
        upTwist = mc.ls(sl=True)
        mc.delete(upTwist[2])
        mc.parent(upTwist[0], world=True)
        mc.reroot(upTwist[1]) #this is to invert the order of the chain.
        mc.rename(upTwist[0], side + 'upTwist_02_JC')
        mc.rename(upTwist[1], side + 'upTwist_01_JC')
        #
        loTwistHandle = mc.duplicate(jj[2], renameChildren=True)
        mc.select(loTwistHandle, hi=True)
        loTwist = mc.ls(sl=True)
        mc.rename(loTwist[0], side + 'loTwist_01_JC')
        mc.rename(loTwist[1], side + 'loTwist_02_JC')
        #
        mc.parent( side + 'upTwist_01_JC', jj[1])
        mc.parent( side + 'loTwist_01_JC', jj[2])
        mc.select( side + 'upTwist_01_JC', side + 'upTwist_02_JC')
        upIKSC= mc.ikHandle(name= side + 'upTwist_IkSc', solver='ikSCsolver')

        mc.select(side + 'loTwist_01_JC', side + 'loTwist_02_JC')

        loIKSC =mc.ikHandle(name= side + 'loTwist_IkSc', solver='ikSCsolver')

        mc.parent(upIKSC[0], jj[0])
        mc.parent(loIKSC[0], jj[3])

        #Create the twist joints (inspired by the method of Jay Grenier jgSplitJointChain.mel)

        #UPPERARM:
        # query master twist joints position
        mc.select(cl=True)
        pPos = mc.joint( side +  'upTwist_01_JC', query=True, position=True)
        cPos = mc.joint( side + 'upTwist_02_JC', query=True, position=True)
        # Parent Orientation
        ro = mc.joint( side + 'shoulder_IK', q=True, roo=True)

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
                     n=('temp' + str(i)))

        mc.select('temp0', hi=True)
        mc.parent(world=True)

        #Reposition to get proper orientation of the joints
        mc.parent('temp2','temp3')
        mc.parent('temp1','temp2')
        mc.parent('temp0', 'temp1')
        mc.select('temp3', hi=True)
        temp=mc.ls(sl=True)
        mc.joint(temp, side + 'shoulder_IK', e=True, oj=ro)
        mc.delete('temp0')
        # Rename
        mc.rename('temp1', side + 'uparmTwist_C_JJ')
        mc.rename('temp2', side + 'uparmTwist_B_JJ')
        mc.rename('temp3', side + 'uparmTwist_A_JJ')
        upTwi = mc.ls(sl=True)
        mc.parent(upTwi, jj[1])
        uptwiGrp = mc.group( n=side + "uptwist_grp", empty=True)
        temp = mc.pointConstraint(jj[1], uptwiGrp)
        mc.delete(temp)
        mc.parent(upTwi, uptwiGrp)
        mc.parent(uptwiGrp, jj[0])
        mc.orientConstraint(jj[1], uptwiGrp,  mo=True, skip="x")
        mc.setAttr('{}.rx'.format(uptwiGrp), 0)

        for j in upTwi:
            for axis in ['X', 'Y', 'Z']:
                mc.setAttr(j + ".jointOrient" + axis, 0)


        #LOWERARM: (repeating the process)
        # query master twist joints position
        mc.select(cl=True)
        pPos = mc.joint(side + 'loTwist_01_JC', query=True, position=True)
        cPos = mc.joint(side + 'loTwist_02_JC', query=True, position=True)
        helperJoint= mc.duplicate(side + 'loTwist_02_JC') # i need this for the last joint to be well oriented.
        #Parent Orientation
        ro = mc.joint(side + 'loTwist_01_JC', q=True, roo=True)

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
                     n=('temp' + str(i)))

        mc.parent(helperJoint, 'temp3')
        mc.select('temp0', hi=True)
        temp=mc.ls(sl=True)

        mc.joint(temp, side + 'loTwist_02_JC1', e=True, oj=ro)

        mc.parent(world=True)
        mc.delete(helperJoint)
        mc.delete('temp0')
        mc.rename('temp1', side + 'loarmTwist_A_JJ')
        mc.rename('temp2', side + 'loarmTwist_B_JJ')
        mc.rename('temp3', side + 'loarmTwist_C_JJ')
        loTwi = mc.ls(sl=True)

        mc.parent(loTwi, jj[2])

        for j in loTwi:
            for axis in ['X', 'Y', 'Z']:
                mc.setAttr(j + ".jointOrient" + axis, 0)


        # Conect the handles and make it work wth the twist joints
        mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'uparmTwist_MULT')
        mc.connectAttr(side + 'upTwist_01_JC.rx', side + 'uparmTwist_MULT.input1X')
        mc.connectAttr(side + 'upTwist_01_JC.rx', side + 'uparmTwist_MULT.input1Y')
        mc.connectAttr(side + 'upTwist_01_JC.rx', side + 'uparmTwist_MULT.input1Z')
        mc.setAttr(side + 'uparmTwist_MULT.input2X', -0.25)
        mc.setAttr(side + 'uparmTwist_MULT.input2Y', -0.50)
        mc.setAttr(side + 'uparmTwist_MULT.input2Z', -0.75)
        mc.connectAttr( side + 'uparmTwist_MULT.outputX', side + 'uparmTwist_A_JJ.rx')
        mc.connectAttr( side + 'uparmTwist_MULT.outputY', side + 'uparmTwist_B_JJ.rx')
        mc.connectAttr( side + 'uparmTwist_MULT.outputZ', side + 'uparmTwist_C_JJ.rx')
        #
        mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'loarmTwist_MULT')
        mc.connectAttr(side + 'loTwist_01_JC.rx', side + 'loarmTwist_MULT.input1X')
        mc.connectAttr(side + 'loTwist_01_JC.rx', side + 'loarmTwist_MULT.input1Y')
        mc.connectAttr(side + 'loTwist_01_JC.rx', side + 'loarmTwist_MULT.input1Z')
        mc.setAttr(side + 'loarmTwist_MULT.input2X', 0.25)
        mc.setAttr(side + 'loarmTwist_MULT.input2Y', 0.50)
        mc.setAttr(side + 'loarmTwist_MULT.input2Z', 0.75)
        mc.connectAttr(side + 'loarmTwist_MULT.outputX', side + 'loarmTwist_C_JJ.rx')
        mc.connectAttr(side + 'loarmTwist_MULT.outputY', side + 'loarmTwist_B_JJ.rx')
        mc.connectAttr(side + 'loarmTwist_MULT.outputZ', side + 'loarmTwist_A_JJ.rx')

        #Make it stretchy:
        mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'uparmStretch_MULT')
        mc.connectAttr(side + 'elbow_JJ.tx', side + 'uparmStretch_MULT.input1X')
        mc.connectAttr(side + 'elbow_JJ.tx', side + 'uparmStretch_MULT.input1Y')
        mc.connectAttr(side + 'elbow_JJ.tx', side + 'uparmStretch_MULT.input1Z')
        mc.setAttr(side + 'uparmStretch_MULT.input2X', 0.25)
        mc.setAttr(side + 'uparmStretch_MULT.input2Y', 0.50)
        mc.setAttr(side + 'uparmStretch_MULT.input2Z', 0.75)
        mc.connectAttr(side + 'uparmStretch_MULT.outputX', side + 'uparmTwist_A_JJ.tx')
        mc.connectAttr(side + 'uparmStretch_MULT.outputY', side + 'uparmTwist_B_JJ.tx')
        mc.connectAttr(side + 'uparmStretch_MULT.outputZ', side + 'uparmTwist_C_JJ.tx')
        #
        mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'loarmStretch_MULT')
        mc.connectAttr(side + 'wrist_JJ.tx', side + 'loarmStretch_MULT.input1X')
        mc.connectAttr(side + 'wrist_JJ.tx', side + 'loarmStretch_MULT.input1Y')
        mc.connectAttr(side + 'wrist_JJ.tx', side + 'loarmStretch_MULT.input1Z')
        mc.setAttr(side + 'loarmStretch_MULT.input2X', 0.25)
        mc.setAttr(side + 'loarmStretch_MULT.input2Y', 0.50)
        mc.setAttr(side + 'loarmStretch_MULT.input2Z', 0.75)
        mc.connectAttr(side + 'loarmStretch_MULT.outputX', side + 'loarmTwist_C_JJ.tx')
        mc.connectAttr(side + 'loarmStretch_MULT.outputY', side + 'loarmTwist_B_JJ.tx')
        mc.connectAttr(side + 'loarmStretch_MULT.outputZ', side + 'loarmTwist_A_JJ.tx')

        # Create IK FK control
        v1 = mc.curve(d=1, p= [(0.052, 4.96, 0),(0.061, 4.97, 0),(0.070, 4.98, 0),(0.164, 5.13, 0),(0.178, 5.14, 0),
                               (0.184, 5.14, 0),(0.196, 5.14, 0), (0.204, 5.14, 0), (0.346, 5.09, 0), (0.371, 5.08, 0),
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
                               (-0.131, 3.31, 0),(-0.137, 3.32, 0),(-0.177, 3.49, 0),(-0.181, 3.50, 0),(-0.188, 3.51, 0),
                               (-0.296, 3.55, 0),(-0.308, 3.55, 0),(-0.320, 3.54, 0),(-0.448, 3.43, 0),(-0.460, 3.42, 0),
                               (-0.470, 3.41, 0),(-0.484, 3.42, 0),(-0.603, 3.51, 0),(-0.615, 3.52, 0),(-0.615, 3.52, 0),
                               (-0.621, 3.52, 0),(-0.615, 3.54, 0),(-0.558, 3.70, 0),(-0.555, 3.72, 0),(-0.555, 3.73, 0),
                               (-0.564, 3.74, 0),(-0.619, 3.81, 0),(-0.628, 3.81, 0),(-0.637, 3.82, 0),(-0.651, 3.82, 0),
                               (-0.819, 3.80, 0),(-0.834, 3.79, 0),(-0.844, 3.80, 0),(-0.851, 3.81, 0),(-0.905, 3.95, 0),
                               (-0.910, 3.96, 0),(-0.911, 3.97, 0),(-0.895, 3.98, 0),(-0.763, 4.09, 0),(-0.752, 4.10, 0),
                               (-0.745, 4.11, 0),(-0.747, 4.12, 0),(-0.755, 4.22, 0),(-0.762, 4.23, 0),(-0.776, 4.23, 0),
                               (-0.918, 4.30, 0),(-0.947, 4.31, 0),(-0.947, 4.32, 0),(-0.916, 4.48, 0),(-0.909, 4.50, 0),
                               (-0.885, 4.51, 0),(-0.715, 4.52, 0),(-0.702, 4.52, 0),(-0.692, 4.53, 0),(-0.646, 4.62, 0),
                               (-0.648, 4.63, 0),(-0.657, 4.64, 0),(-0.744, 4.78, 0),(-0.755, 4.80, 0),(-0.754, 4.81, 0),
                               (-0.740, 4.82, 0),(-0.635, 4.93, 0),(-0.621, 4.94, 0),(-0.613, 4.95, 0),(-0.594, 4.94, 0),
                               (-0.447, 4.86, 0),(-0.432, 4.85, 0),(-0.417, 4.85, 0),(-0.345, 4.89, 0),(-0.339, 4.91, 0),
                               (-0.339, 4.93, 0),(-0.338, 5.09, 0),(-0.338, 5.10, 0),(-0.333, 5.11, 0),(-0.316, 5.11, 0),
                               (-0.162, 5.15, 0),(-0.142, 5.16, 0),(-0.135, 5.15, 0),(-0.124, 5.14, 0),(-0.040, 4.99, 0),
                               (-0.032, 4.98, 0),(-0.023, 4.97, 0),(0.052, 4.96, 0)] )
        v2 = mc.curve(d=1, p=[(0, -0.027, 0), (-0.03, 3.3, 0)])

        mc.select(v1, v2)
        mc.ls(sl=True)
        shps = mc.listRelatives(shapes=True)
        mc.parent(shps, v1, relative=True, shape=True)
        mc.delete(v2)
        sel = mc.rename(v1, side + 'arm_IK_FK_SWITCH')
        ikfk_off = mc.group(sel, name='grp' + side + 'arm_IK_FK_SwitchZERO')
        ikfkSwitch = mc.ls(sel)

        #
        mc.move(0, -2.6, 0, ikfkSwitch[0] + '.rotatePivot', r=True)
        mc.move(0, -2.6, 0, ikfk_off + '.rotatePivot', r=True)
        mc.addAttr(sel, longName= 'IK_FK', defaultValue=0, minValue=0, maxValue=1, keyable=True)

        for trs in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']:
            mc.setAttr(sel + trs, lock=True, keyable=False, channelBox=False)

        #position
        mc.pointConstraint( jj[3], ikfk_off, mo= False )
        for rot in ['.rx', '.rz']:
            mc.setAttr(ikfk_off + rot, -90)
        mc.orientConstraint(jj[3], ikfk_off, mo= True )


        # Switch_IK_FK
        PC1 = mc.parentConstraint(ik[0], fk[0], jj[1], mo=1)
        PC2 = mc.parentConstraint(ik[1], fk[1], jj[2], mo=1)
        PC3 = mc.parentConstraint(ik[2], fk[2], jj[3], mo=1)

        # Stretchy Arm
        startPos = mc.xform(ik[0], translation=True, q=True, ws=True)
        endPos = mc.xform(ik[2], translation=True, q=True, ws=True)
        dist = mc.distanceDimension(sp=(startPos[0], startPos[1], startPos[2]),
                                      ep=(endPos[0], endPos[1], endPos[2]))
        distLoc = mc.listConnections(dist)
        distShape = mc.listConnections(shapes=True)
        mc.pointConstraint(ik[0], distLoc[0])
        mc.parent(distLoc[1], ikcc[0])
        mc.rename(distLoc[0], side + 'stretchyArm_01_LOC')
        mc.rename(distLoc[1], side + 'stretchyArm_02_LOC')
        #
        div = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'arm_stretchy_DIV')
        normalizeDiv = mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'arm_normalize_DIV')
        con = mc.shadingNode('condition', asUtility=True, name= side + 'arm_CON')
        # Add Stretchy On/Off
        onOff= mc.shadingNode('multiplyDivide', asUtility=True, name= side + 'armStretchyOnOff_MULT')
        #
        mc.setAttr(div + '.operation', 2)
        mc.setAttr(normalizeDiv + '.operation', 2)
        mc.setAttr(con + '.operation', 2)
        secondTerm = mc.getAttr('{}.distance'.format(dist))
        mc.setAttr('{}.secondTerm'.format(con), secondTerm)
        mc.setAttr('{}.input2X'.format(div), secondTerm)
        mc.connectAttr('{}.outColorR'.format(con), '{}.input1X'.format(div))
        mc.connectAttr('{}.distance'.format(distShape[0]), '{}.input1X'.format(onOff))
        mc.connectAttr('{}.outputX'.format(onOff), '{}.input1X'.format(normalizeDiv))
        mc.connectAttr('{}.StretchyOnOff'.format(ikcc[0]), '{}.input2X'.format(onOff) )
        mc.connectAttr('{}.scaleY'.format('root_CC'), '{}.input2X'.format(normalizeDiv))
        mc.connectAttr('{}.outputX'.format(normalizeDiv), '{}.secondTerm'.format(con))
        mc.connectAttr('{}.outputX'.format(normalizeDiv), '{}.colorIfFalseR'.format(con))
        firstTerm = mc.getAttr('{}.distance'.format(dist))
        mc.setAttr('{}.firstTerm'.format(con), firstTerm)
        mc.setAttr('{}.colorIfTrueR'.format(con), firstTerm)
        mc.connectAttr('{}.outputX'.format(div), '{}.sx'.format(ik[0]))
        mc.connectAttr('{}.outputX'.format(div), '{}.sx'.format(ik[1]))

        mc.hide(side + 'stretchyArm_02_LOC')

        # Hide GimbalControl
        mc.connectAttr(ikcc[0] + '.GimbalControlVis', ikcc2_off + '.v')

        #Anotation for the pole vector
        elbowPos = mc.xform(ik[1], ws=True, translation=True, q=True)
        armAnnot = mc.annotate(ikpv, p=(elbowPos[0], elbowPos[1], elbowPos[2]))
        mc.parent(armAnnot, side + 'elbow_JJ')
        mc.setAttr('{}.overrideEnabled'.format(armAnnot), 1)
        mc.setAttr('{}.overrideDisplayType'.format(armAnnot), 2)
        mc.setAttr('{}.overrideDisplayType'.format(armAnnot), 1)

        # Switch IK-FK
        mc.shadingNode('reverse', asUtility=True, name=side + 'arm_REV')
        mc.connectAttr(side + 'arm_IK_FK_SWITCH.' + 'IK_FK', side + 'arm_REV.inputX')
        #
        mc.connectAttr((side + 'arm_REV.outputX'), (PC1[0] + '.' + side + 'shoulder_IKW0'))
        mc.connectAttr((ikfkSwitch[0] + '.' + 'IK_FK'), (PC1[0] + '.' + side + 'shoulder_FKW1'))
        mc.connectAttr((side + 'arm_REV.outputX'), (PC2[0] + '.' + side + 'elbow_IKW0'))
        mc.connectAttr((ikfkSwitch[0] + '.' + 'IK_FK'), (PC2[0] + '.' + side + 'elbow_FKW1'))
        mc.connectAttr((side + 'arm_REV.outputX'), (PC3[0] + '.' + side + 'wrist_IKW0'))
        mc.connectAttr((ikfkSwitch[0] + '.' + 'IK_FK'), (PC3[0] + '.' + side + 'wrist_FKW1'))

        # Switch visibilidad de los controles
        mc.connectAttr(side + 'arm_IK_FK_SWITCH.' + 'IK_FK', '{}.v'.format(fkhi[0]))
        mc.connectAttr(side + 'arm_REV.outputX', '{}.v'.format(ikcc_off))
        mc.connectAttr(side + 'arm_REV.outputX', '{}.v'.format(ikpv_off))
        #
        grp = mc.group(n= side + 'arm_GRP', empty=True)
        temp = mc.pointConstraint(jj[0], grp, maintainOffset=0)
        mc.delete(temp)
        mc.parent(jj[0], clav_grp, grp)
        mc.parent(ikpv_off, ikcc_off, ikfk_off, 'IK_GRP')
        mc.hide(ik[0], fk[0], IKRP[0])
        grpStretch = mc.group(n=side + 'stretchyArm_GRP', empty=True)
        mc.parent(side + 'stretchyArm_01_LOC', dist, grpStretch)
        mc.parent( grpStretch, 'IK_GRP')

        om.MGlobal.displayInfo('Your arm rig has been created with success!')

        #Final Clean-up
        mc.hide(upIKSC[0], loIKSC[0], side + 'loTwist_01_JC', side + 'upTwist_01_JC')
        mc.hide(grpStretch)

    #colors

    blue = [ 'L_clavicle_FK_CCZERO', 'grpL_arm_IK1_CCZERO', 'grpL_arm_PVZERO']
    red= [ 'R_clavicle_FK_CCZERO', 'grpR_arm_IK1_CCZERO', 'grpR_arm_PVZERO']
    lightBlue = ['grpL_arm_IK2_CCZERO', 'grpL_arm_IK_FK_SwitchZERO']
    lightRed = ['grpR_arm_IK2_CCZERO', 'grpR_arm_IK_FK_SwitchZERO']

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