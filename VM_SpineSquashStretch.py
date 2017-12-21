"""
This is a basic py script for automatizing the creation of an squash-stretch IK spline.
Scripted by Vero Morera, December 2017.
veromc1692@gmail.com

Instructions:
---------------------------------------------------------------------------------
To call the main UI:

import VM_SquashStretchSpline as sss
reload (sss)
sss.UI()

"""
import maya.cmds as mc
import maya.OpenMaya as om

sssWIN = "ssswindow"

def UI():
    if (mc.window(sssWIN, exists=True)):
        mc.deleteUI(sssWIN)

    mc.window(sssWIN, title="Squash_Stretch_Spine by Vero Morera", w=300, h=100, sizeable=True)
    #
    mc.columnLayout(adj=True)
    mc.text(label="1- Select the global scale control and insert it with [ << ]", h=20)
    mc.text(label="2- Select ALL the joints of the spine and click on [ Create ]", h=20)
    mc.separator()

    mc.textFieldButtonGrp("globalCC", label= "Global Scale Control  ",
                          buttonLabel="<<", buttonCommand=normalize)
    mc.setParent('..')
    mc.rowColumnLayout(adj=True, w=10, numberOfRows=1)
    mc.button(label="Create", c=IKhandle)
    mc.setParent('..')

    mc.showWindow(sssWIN)
###-------------------------------------------------------------------------------------------------------------###
def normalize():
    scale_control = mc.ls(sl=True)
    mc.select(cl=True)

    if len(scale_control) > 1:
        om.MGlobal.displayError("Please select just the global scale control!")

    elif len(scale_control) == 0:
        om.MGlobal.displayError("Please select at least one control!")

    else:
        mc.textFieldButtonGrp("globalCC", edit=True, text=scale_control[0])

###-------------------------------------------------------------------------------------------------------------###
def IKhandle(*args):

    joints = mc.ls(sl=True)
    scaleNormalize = mc.textFieldButtonGrp("globalCC", query=True, text=True)
    mc.select(cl=True)

    if len(joints) <= 1:
        om.MGlobal.displayError("Please select at least 2 joints")

    else:
        # variables
        ik_joints = mc.ls(joints[0], joints[-1:])
        spine_connect = mc.ls(joints[:-1])
        mc.select(ik_joints)

        # create IK spline:
        IK = mc.ikHandle(n="spine_IkSp", sol="ikSplineSolver", createCurve=True, parentCurve=False)
        curve = mc.ls(IK[2])
        mc.setAttr(IK[2] + ".inheritsTransform", 0)
        spine_cv = mc.rename(curve, "spine_CV")

        # Setup spine twist
        mc.setAttr(IK[0] + ".dTwistControlEnable", 1)
        mc.setAttr(IK[0] + ".dWorldUpType", 4)
        mc.setAttr(IK[0] + ".dForwardAxis", 0)
        mc.setAttr(IK[0] + ".dWorldUpAxis", 0)
        mc.setAttr(IK[0] + ".dWorldUpVectorY", 1)
        mc.setAttr(IK[0] + ".dWorldUpVectorEndY", 1)

        # Control joints for the twist
        start = mc.duplicate(joints[0], name="spine_start_JC", po=True)
        end = mc.duplicate(joints[-1], name="spine_end_JC", po=True)
        mc.parent(end, w=True)
        mc.connectAttr("spine_start_JC.worldMatrix", (IK[0] + ".dWorldUpMatrix"))
        mc.connectAttr("spine_end_JC.worldMatrix", (IK[0] + ".dWorldUpMatrixEnd"))

        # group all together
        mc.group(spine_cv, IK[0], joints[0], start, end, name="spine_GRP")

        # skin the control joints to the spine curve
        mc.skinCluster("spine_start_JC", "spine_end_JC", spine_cv, toSelectedBones=True, bindMethod=0)

        # Create and edit the nodes for the squash_stretch
        cv_info = mc.shadingNode("curveInfo", asUtility=True, name="spine_info")
        stretch_div = mc.shadingNode("multiplyDivide", asUtility=True, name="spine_stretchy_DIV")
        squash_div = mc.shadingNode("multiplyDivide", asUtility=True, name="spine_squash_DIV")
        invert_pow = mc.shadingNode("multiplyDivide", asUtility=True, name="spine_invert_POW")
        normalize_div = mc.shadingNode("multiplyDivide", asUtility=True, name="spine_normalize_DIV")
        mc.setAttr(stretch_div + ".operation", 2)
        mc.setAttr(squash_div + ".operation", 2)
        mc.setAttr(normalize_div + ".operation", 2)
        mc.setAttr(invert_pow + ".operation", 3)

        # make the connections between the nodes
        mc.connectAttr((spine_cv + ".worldSpace[0]"), (cv_info + ".inputCurve"))
        mc.connectAttr((cv_info + ".arcLength"), (normalize_div + ".input1.input1X"))
        mc.connectAttr((normalize_div + ".outputX"), (stretch_div + ".input1.input1X"))
        mc.connectAttr(("spine_CVShape.max"), (stretch_div + ".input2.input2X"))
        mc.connectAttr((stretch_div + ".outputX"), (invert_pow + ".input1.input1X"))
        mc.setAttr(invert_pow + ".input2.input2X", 0.5)
        mc.connectAttr((invert_pow + ".outputX"), (squash_div + ".input2.input2X"))
        mc.setAttr(squash_div + ".input1.input1X", 1)
        mc.select(cl=True)

        # connect the nodes to the joints
        for s in spine_connect:
            mc.connectAttr((stretch_div + ".outputX"), (s + ".scaleX"))
            mc.connectAttr((squash_div + ".outputX"), (s + ".scaleY"))
            mc.connectAttr((squash_div + ".outputX"), (s + ".scaleZ"))

        # normalize rig
        if mc.textFieldButtonGrp("globalCC", query=True, text=True):
            mc.connectAttr((scaleNormalize + ".scaleY"), (normalize_div + ".input2.input2X"))
            om.MGlobal.displayInfo("Your squash - stretch IKspline has been created with success!")

        else:
            pass
            om.MGlobal.displayWarning("There was no Global Scale Control selected. Normalize Skiped!")
