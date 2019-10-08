'''
Ribbon setup for cartoon limbs.

Original idea by: Jason Dobra.
Scripted by: Vero Morera.

February 2019
v.01
'''

import maya.cmds as mc
import maya.mel as mel
from functools import partial
import maya.OpenMaya as om

'''
        @param limb: string type: arm, leg, tail, etc...
        @author: veroMo
'''
winRibbon = 'autoRibbon'

def UI():
    # Window Creation
    if (mc.window(winRibbon, exists=True)):
        mc.deleteUI(winRibbon)

    mc.window(winRibbon, title= 'VM_ribbon', h=100, w=400, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2, w=100)
    mc.text('Define scale of your ribbon. Choose between arms, legs, or none to make a default ribbon chain', h=25)
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.floatSliderGrp('ribscale', label='Ribbon Scale  ', field=True, minValue=0.01, value=True)
    mc.textFieldButtonGrp("globalCC", label="Global Scale Control  ", buttonLabel="<<", buttonCommand=normalize)
    mc.radioCollection()
    mc.radioButton('arm', label='make ribbon for both arms')
    mc.radioButton('leg', label='make ribbon for both legs')
    mc.setParent('..')
    #

    ribbonChoice = ""
    if mc.radioButton('arm', query=True, select=True):
        ribbonChoice= partial(bendy, 'arm')
    if mc.radioButton('leg', query=True, select=True):
        ribbonChoice = partial(bendy, 'leg')

    mc.rowColumnLayout(numberOfColumns=2)
    mc.button(label= 'Create Ribbon', w=100, h=40, c=partial(bendy, ribbonChoice), bgc=(.2,.2,.2))
    mc.setParent('..')


    mc.showWindow(winRibbon)

lside= 'L_'
rside= 'R_'


def normalize():
    scale_control = mc.ls(sl=True)
    mc.select(cl=True)

    if len(scale_control) > 1:
        om.MGlobal.displayError('Please select just the global scale control!')

    elif len(scale_control) == 0:
        om.MGlobal.displayError('Please select at least one control!')

    else:
        mc.textFieldButtonGrp('globalCC', edit=True, text=scale_control[0])


def bendy( limb, *args):

    if mc.radioButton('arm', query=True, select=True):
        limb='arm'
    if mc.radioButton('leg', query=True, select=True):
        limb = 'leg'


    for side in [lside, rside]:

        #make nurbs plane
        nurbPlane = mc.nurbsPlane(n= side + limb + 'RibbonPlane', p=(0,0,0), ax= (0,0,1), w=1, lr=15, d=3, u=1, v=16, ch=1)
        mc.setAttr('{}.rotateZ'.format(nurbPlane[0]), 90)

        #add folis
        mel.eval('createHair 1 12 10 0 0 0 0 5 0 2 1 1')
        mc.delete('hairSystem1OutputCurves', 'nucleus1', 'hairSystem1')
        mc.rename('hairSystem1Follicles', side + limb + 'BendyFolis_GRP')

        #make no transform group
        noTransGrp = mc.group(side + limb + 'BendyFolis_GRP',nurbPlane[0], n= side + limb + 'BendyNoTransform_GRP')
        mc.setAttr( '{}.inheritsTransform'.format(noTransGrp), 0)
        #mc.hide(noTransGrp)

        #list folis
        foliList = [side + limb+ 'RibbonPlaneFollicle5004', side + limb+ 'RibbonPlaneFollicle5012', side + limb+ 'RibbonPlaneFollicle5021', 
                    side + limb+ 'RibbonPlaneFollicle5029', side + limb+ 'RibbonPlaneFollicle5037', side + limb+ 'RibbonPlaneFollicle5045',
                    side + limb+ 'RibbonPlaneFollicle5054', side + limb+ 'RibbonPlaneFollicle5062', side + limb+ 'RibbonPlaneFollicle5070',
                    side + limb+ 'RibbonPlaneFollicle5078', side + limb+ 'RibbonPlaneFollicle5087', side + limb+ 'RibbonPlaneFollicle5095']

            
        #create foli joints
        foliJnts = []
        i=0
        for  f in foliList:
            
            jnt= mc.joint(n=side + limb + 'Ribbon'+ str(i+1) + '_JNT')
            foliJnts.append(jnt)
            mc.parent(jnt, f)
            mc.xform(t=(0,0,0))
            i= i+1

        # normalize scale
        scaleNormalize = mc.textFieldButtonGrp("globalCC", query=True, text=True)

        for foli in foliList:
            for scale in ['sx', 'sy', 'sz']:
                mc.connectAttr( '{}.{}'.format(scaleNormalize, scale), '{}.{}'.format(foli, scale))

        # -------- segment setup -------- #
        mainSegGrp = []
        aimGrps = []
        controlJnt = []
        controls = []

        #secondary segment setup
        for i in range(6):

            joint = mc.joint(n=side + limb + 'Sec0' + str(i+1) + '_JC')
            controlJnt.append(joint)
            control = mc.circle(nr=(1, 0, 0), n=side + limb + 'Sec0' + str(i+1) + '_CTRL', r=1.5, ch=False)
            controls.append(control[0])
            groupAim = mc.group(n=side + limb + 'Sec0' + str(i+1) + '_AIM_GRP') 
            aimGrps.append(groupAim)
            groupRot = mc.group(n=side + limb + 'Sec0' + str(i+1) + '_ROT_GRP') 
            group = mc.group(n=side + limb + 'Sec0' + str(i+1) + '_GRP')  
            mainSegGrp.append(group)
            mc.parent(joint, control)
            mc.xform(joint, t=(0,0,0))
            
        #crete container grp for secondary segments
        secContainer= mc.group(mainSegGrp, n=side + limb + 'Secondary_GRP')
            
        #primary segment setup    
        ccup = mc.circle(nr=(1, 0, 0), n=side + 'up' + limb + '_CTRL', r=1.5, ch=False)
        mc.makeIdentity(apply=True)
        uparmGrp= mc.group(n=side + 'up' + limb + '_GRP')
        mainSegGrp.append(uparmGrp)
        upJnt = mc.joint(n=side + 'up' + limb + 'Bendy_JC')
        mc.parent(side + 'up' + limb + 'Bendy_JC', ccup)
        #
        ccmid = mc.circle(nr=(1, 0, 0), n=side + 'mid' + limb + '_CTRL', r=1.5, ch=False)
        mc.makeIdentity(apply=True)
        midarmGrp = mc.group(n=side + 'mid' + limb + '_GRP')
        mainSegGrp.append(midarmGrp)
        midJnt= mc.joint(n=side + 'mid' + limb + 'Bendy_JC' )
        mc.parent(side + 'mid' + limb + 'Bendy_JC', ccmid)
        #
        cclo = mc.circle(nr=(1, 0, 0), n=side + 'lo' + limb + '_CTRL', r=1.5, ch=False)
        mc.makeIdentity(apply=True)
        loarmGrp= mc.group(n=side + 'lo' + limb + '_GRP')
        mainSegGrp.append(loarmGrp)
        loJnt = mc.joint(n=side + 'lo' + limb + 'Bendy_JC')
        mc.parent(side + 'lo' + limb + 'Bendy_JC', cclo)
            
        #Define segment poscition
        mc.xform(mainSegGrp[0], t=(5.5,0,0))
        mc.xform(mainSegGrp[1], t=(3.5,0,0))
        mc.xform(mainSegGrp[2], t=(1.7,0,0))
        mc.xform(mainSegGrp[3], t=(-1.7,0,0))
        mc.xform(mainSegGrp[4], t=(-3.5,0,0))
        mc.xform(mainSegGrp[5], t=(-5.5,0,0))

        #Define segment poscition
        mc.xform(mainSegGrp[6], t=(-7.5,0,0))
        mc.xform(mainSegGrp[7], t=(0,0,0))
        mc.xform(mainSegGrp[8], t=(7.5,0,0))

        #cleanUp

        for c in controls:
            for trs in ['sx', 'sy', 'sz', 'v']:
                mc.setAttr('{}.{}'.format(c, trs), lock=True, keyable=False, channelBox=False)
                mc.setAttr('{}.rotateOrder'.format(c), lock=False, keyable=True, channelBox=True)
                
        for c in [cclo[0], ccmid[0], cclo[0]]:
            for trs in ['sx', 'sy', 'sz', 'v']:
                mc.setAttr( '{}.{}'.format(c, trs), lock=True, keyable=False, channelBox=False)
                mc.setAttr('{}.rotateOrder'.format(c), lock=False, keyable=True, channelBox=True)
                mc.setAttr('{}.{}'.format(c, 'rx'), lock=True, keyable=False, channelBox=False)
                mc.setAttr('{}.{}'.format(c, 'ry'), lock=True, keyable=False, channelBox=False)
                mc.setAttr('{}.{}'.format(c, 'rz'), lock=True, keyable=False, channelBox=False)
                
        mc.hide(controlJnt, side + 'up' + limb + 'Bendy_JC', side + 'mid' + limb + 'Bendy_JC', side + 'lo' + limb + 'Bendy_JC')

        #create master ribbon container
        masterRibGrp = mc.group(mainSegGrp[6::], secContainer, noTransGrp, n=side + limb + 'Ribbon_System')

        #delete garbage from nHair
       # mc.delete(u'curve1', u'curve3', u'curve5', u'curve7', u'curve9', u'curve11', u'curve13', u'curve15', u'curve17', u'curve19', u'curve21', u'curve23')


        #------------- internal connections -------------#
            
        #point constraints master grp
        for grp in mainSegGrp[:3]:
            mc.pointConstraint(ccmid, cclo, grp, mo=1)
            
        for grp in mainSegGrp[3:6]:
            mc.pointConstraint(ccmid, ccup, grp, mo=1)

        #stablish uniform distance between segment controls    
        mc.setAttr( side + limb + 'Sec01_GRP_pointConstraint1.' + side + 'lo' + limb + '_CTRLW1', 3)
        mc.setAttr( side + limb + 'Sec01_GRP_pointConstraint1.offsetX', 0)
        mc.setAttr( side + limb + 'Sec03_GRP_pointConstraint1.' + side + 'mid' + limb + '_CTRLW0', 3)
        mc.setAttr( side + limb + 'Sec03_GRP_pointConstraint1.offsetX', 0)

        mc.setAttr( side + limb + 'Sec04_GRP_pointConstraint1.' + side + 'mid' + limb + '_CTRLW0', 3)
        mc.setAttr( side + limb + 'Sec04_GRP_pointConstraint1.offsetX', 0)
        mc.setAttr( side + limb + 'Sec06_GRP_pointConstraint1.' + side + 'up' + limb + '_CTRLW1', 3)
        mc.setAttr( side + limb + 'Sec06_GRP_pointConstraint1.offsetX', 0)

        #aim constraints master grp

        if side == lside:
            for grp in mainSegGrp[:3]:
                mc.aimConstraint(ccmid, grp, mo=False, offset=(0,0,0), aimVector=(-1,0,0), upVector=(0,1,0),
                                 worldUpType='vector', worldUpVector=(0,1,0), skip='x')

            for grp in mainSegGrp[3:6]:
                mc.aimConstraint(ccmid, grp, mo=False, offset=(0,0,0), aimVector=(1,0,0), upVector=(0,1,0),
                                 worldUpType='vector', worldUpVector=(0,1,0), skip='x')

        if side == rside:
            for grp in mainSegGrp[:3]:
                mc.aimConstraint(ccmid, grp, mo=False, offset=(0, 0, 0), aimVector=(1, 0, 0), upVector=(0, 1, 0),
                             worldUpType='vector', worldUpVector=(0, 1, 0), skip='x')

            for grp in mainSegGrp[3:6]:
                mc.aimConstraint(ccmid, grp, mo=False, offset=(0, 0, 0), aimVector=(-1, 0, 0), upVector=(0, 1, 0),
                                 worldUpType='vector', worldUpVector=(0, 1, 0), skip='x')


        #point constraints aimGrps
        lowerSeg = side + limb + 'Sec02_CTRL'
        upperSeg = side + limb + 'Sec05_CTRL'

        mc.pointConstraint(cclo,lowerSeg, aimGrps[0], mo=1)
        mc.pointConstraint(ccmid, lowerSeg, aimGrps[2], mo=1)
        mc.pointConstraint(ccmid, upperSeg, aimGrps[3], mo=1)
        mc.pointConstraint(ccup, upperSeg, aimGrps[5], mo=1)
           
        #aim constraints aimGrps


        if side == lside:
            mc.aimConstraint(lowerSeg, aimGrps[0], mo=False, aimVector=(-1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(lowerSeg, aimGrps[2], mo=False, aimVector=(1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(upperSeg, aimGrps[3], mo=False, aimVector=(-1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(upperSeg, aimGrps[5], mo=False, aimVector=(1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')

        if side == rside:
            mc.aimConstraint(lowerSeg, aimGrps[0], mo=False, aimVector=(1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(lowerSeg, aimGrps[2], mo=False, aimVector=(-1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(upperSeg, aimGrps[3], mo=False, aimVector=(1,0,0),
                              upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')
            mc.aimConstraint(upperSeg, aimGrps[5], mo=False, aimVector=(-1,0,0),
                          upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), skip='x')



        #hide secondary bendy grps
        mc.hide(side + limb + 'Sec01_GRP', side + limb + 'Sec03_GRP', side + limb + 'Sec04_GRP', side + limb + 'Sec06_GRP', side + 'lo' + limb + '_GRP', side + 'up' + limb + '_GRP') 

        #Add skincluster
        mc.skinCluster(controlJnt, upJnt, loJnt, nurbPlane[0])
        #mc.skinCluster(controlJnt, nurbPlane[0])

        # Define scale based in user choice:
        userScale = mc.floatSliderGrp('ribscale', query=True, value=True)

        for scale in ['.sx', '.sy', '.sz']:
            mc.setAttr(masterRibGrp + scale, userScale)

        mc.setAttr('{}.scaleX'.format(masterRibGrp), userScale)

        #create set for bendy bind-to-body joints
        mc.sets(foliJnts, n=side + 'bendy ' + limb + '_skinSet')

        ''' 
                #--------------- Connect ribbon setup to main arm --- ---------------#
        if mc.radioButton('arm', query=True, select=True):

            #define names for main arm (change this to your arm naming convention)

            shoulderJJ= side + 'shoulder_JJ'
            elbowJJ= side + 'elbow_JJ'
            wristJJ=side + 'wrist_JJ'
            #
            uparmA= side + 'uparmTwist_A_JJ'
            uparmB= side + 'uparmTwist_B_JJ'
            uparmC= side + 'uparmTwist_C_JJ'
            loarmA= side + 'loarmTwist_A_JJ'
            loarmB= side + 'loarmTwist_B_JJ'
            loarmC= side + 'loarmTwist_C_JJ'

            mc.parentConstraint(shoulderJJ, side + 'uparm_GRP', mo=0)
            mc.parentConstraint(elbowJJ, side + 'midarm_GRP', mo=0)
            mc.parentConstraint(wristJJ, side + 'loarm_GRP', mo=0)
        
            mc.orientConstraint(uparmA,side + limb + 'Sec06_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(uparmB,side + limb + 'Sec05_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(uparmC,side + limb + 'Sec04_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(loarmA,side + limb + 'Sec01_ROT_GRP', skip=['y','z'], mo=0) #check your naming twist joints here
            mc.orientConstraint(loarmB,side + limb + 'Sec02_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(loarmC,side + limb + 'Sec03_ROT_GRP', skip=['y','z'], mo=0)
    
         
        #--------------- Connect ribbon setup to main leg --- ---------------#
        if mc.radioButton('leg', query=True, select=True):

            hipJJ= side + 'hip_JJ'
            kneeJJ= side + 'knee_JJ'
            ankleJJ=side + 'ankle_JJ'
            #
            mc.parentConstraint(hipJJ, side + 'upleg_GRP', mo=0)
            mc.parentConstraint(kneeJJ, side + 'midleg_GRP', mo=0)
            mc.parentConstraint(ankleJJ, side + 'loleg_GRP', mo=0)
        
            mc.orientConstraint(hipJJ,side + limb + 'Sec06_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(hipJJ,side + limb + 'Sec05_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(hipJJ,side + limb + 'Sec04_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(kneeJJ,side + limb + 'Sec01_ROT_GRP', skip=['y','z'], mo=0) #check your naming twist joints here
            mc.orientConstraint(kneeJJ,side + limb + 'Sec02_ROT_GRP', skip=['y','z'], mo=0)
            mc.orientConstraint(kneeJJ,side + limb + 'Sec03_ROT_GRP', skip=['y','z'], mo=0)



#ESTO ES PARA HACER LOS FOLIS SIN USAR NHAIR, PARA FUTURAS VERSIONES

    '''

''' 
def createFollicle(inputSurface=nurbPlane, scaleGrp='', uVal=0.5, vVal=0.5, hide=0):
    
    name='L_armFoli' + str(i+1)

    #Create a follicle
    follicleShape = mc.createNode('follicle')
    #Get the transform of the follicle
    follicleTrans = mc.listRelatives(follicleShape, parent=True)[0]
    #Rename the follicle
    follicleTrans = mc.rename(follicleTrans, name)
    follicleShape = mc.rename(mc.listRelatives(follicleTrans, c=True)[0], (name + 'Shape'))
    #If the inputSurface is of type 'nurbsSurface', connect the surface to the follicle
    if mc.objectType(inputSurface[0]) == 'nurbsSurface':
        mc.connectAttr((inputSurface[0] + '.local'), (follicleShape + '.inputSurface'))
    #Connect the worldMatrix of the surface into the follicleShape
    mc.connectAttr((inputSurface[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'))
    #Connect the follicleShape to it's transform
    mc.connectAttr((follicleShape + '.outRotate'), (follicleTrans + '.rotate'))
    mc.connectAttr((follicleShape + '.outTranslate'), (follicleTrans + '.translate'))
    #Set the uValue and vValue for the current follicle
    mc.setAttr((follicleShape + '.parameterU'), uVal)
    mc.setAttr((follicleShape + '.parameterV'), vVal)
    #If a scale-group was defined and exists
    if scaleGrp and cmds.objExists(scaleGrp):
        #Connect the scale-group to the follicle
        cmds.connectAttr((scaleGrp + '.scale'), (follicleTrans + '.scale'))
        #Lock the scale of the follicle
        cmds.setAttr((follicleTrans + '.scale'), lock=True)
    #Return the follicle and it's shape
    return follicleTrans, follicleShape


createFollicle(uVal=0.5, vVal=0.042)
createFollicle(uVal=0.5, vVal=0.125)
createFollicle(uVal=0.5, vVal=0.208)
createFollicle(uVal=0.5, vVal=0.292)
createFollicle(uVal=0.5, vVal=0.375)
createFollicle(uVal=0.5, vVal=0.458)
createFollicle(uVal=0.5, vVal=0.542)
createFollicle(uVal=0.5, vVal=0.625)
createFollicle(uVal=0.5, vVal=0.708)
createFollicle(uVal=0.5, vVal=0.792)
createFollicle(uVal=0.5, vVal=0.875)
createFollicle(uVal=0.5, vVal=0.958)

'''
