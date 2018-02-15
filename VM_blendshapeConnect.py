"""
Automatize blendshape connections via nodes
Vero Morera February 2018
For facial rigging
"""

import maya.cmds as mc
import maya.OpenMaya as om

WIN = "autowin"

def UI():
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title="VM_blendShape Connect", w=450, h=200, sizeable=True)
    mc.columnLayout(rowSpacing=5)
    mc.textFieldGrp('blend1', w=800, label='Positive blendshape. Ex: BS.smile', text='')
    mc.textFieldGrp('blend2', label='Negative blendshape. Ex: BS.frown', text='')
    mc.textFieldButtonGrp('control', label='Control', text='', buttonLabel='<<')
    mc.text('Choose the axis:')
    mc.radioCollection()
    mc.radioButton('axisX',label='X')
    mc.radioButton('axisY', label='Y')
    mc.setParent('..')
    mc.columnLayout()
    mc.button(label='Connect the blendshapes to the GUI', w=420, h=40, bgc=(0.2, 0.2, 0.2), command=connectBS)

    mc.showWindow(WIN)


def connectBS(*args):

    bs1= mc.textFieldGrp("blend1", query=True, text=True)
    bs2= mc.textFieldGrp("blend2", query=True, text=True)
    cc = mc.textFieldButtonGrp('control', query=True, text=True)


    if mc.textFieldGrp("blend1", query=True, text=True) and mc.textFieldGrp("blend2", query=True, text=True):
        if mc.textFieldButtonGrp('control', query=True, text=True):

            #This is to connect en X axis
            if mc.radioButton('axisX', q=True, select=True):

                clamp= mc.shadingNode('clamp', asUtility=True)
                mult= mc.shadingNode('multiplyDivide', asUtility=True)
                mc.connectAttr('{}.tx' .format(cc), '{}.inputR' .format(clamp))
                mc.connectAttr('{}.tx'.format(cc), '{}.inputG'.format(clamp))
                mc.setAttr('{}.maxR' .format(clamp), 1)
                mc.setAttr('{}.minG'.format(clamp), -1)
                mc.connectAttr('{}.outputG' .format(clamp), '{}.input1X' .format(mult))
                mc.setAttr('{}.input2X'.format(mult), -1)
                mc.connectAttr('{}.outputR' .format(clamp), bs1)
                mc.connectAttr('{}.outputX'.format(mult), bs2)

            # This is to connect en Y axis
            elif mc.radioButton('axisY', q=True, select=True):
                clamp = mc.shadingNode('clamp', asUtility=True)
                mult = mc.shadingNode('multiplyDivide', asUtility=True)
                mc.connectAttr('{}.ty'.format(cc), '{}.inputR'.format(clamp))
                mc.connectAttr('{}.ty'.format(cc), '{}.inputG'.format(clamp))
                mc.setAttr('{}.maxR'.format(clamp), 1)
                mc.setAttr('{}.minG'.format(clamp), -1)
                mc.connectAttr('{}.outputG'.format(clamp), '{}.input1X'.format(mult))
                mc.setAttr('{}.input2X'.format(mult), -1)
                mc.connectAttr('{}.outputR'.format(clamp), bs1)
                mc.connectAttr('{}.outputX'.format(mult), bs2)

    else:
        om.MGlobal.displayError('Please fill all the information')
