"""This is a basic py script for automatizing the FK control creation in a joint chain.
    Scripted by Vero Morera, December 2017.
    veromc1692@gmail.com

Instructions:
---------------------------------------------------------------------------------
    1-Select one or more joints to create an FK for them...
    2- Choose the size of your controllers.
    3- Choose the suffix of the controller.
    4- Choose the color of your controllers.
    5- Click on the "Generate FKs"button.
---------------------------------------------------------------------------------
"""
import maya.cmds as mc
import maya.OpenMaya as om

WIN = "FkWin"
RGB = (1, 0.2, 0.5)  #This is my default pink color for the UI. Used in code line: 33

def UI():
# Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title="Fk Generator by Vero Morera", h=100, w=300, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=1)
    mc.text("Select one or more joints to create an FK for them...", h=25)
    mc.separator(h=10)
    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.floatSliderGrp("consize", label="Control Size  ", field=True, minValue=0.1, maxValue=500, value=True, h=25)
    mc.textFieldGrp("suf", label="Control Suffix  ", text="_CC", editable=True)
    mc.colorSliderGrp("color", label="Control Color  ", rgb=RGB, h=30)
    mc.setParent('..')
    #
    mc.button(label="Generate FKs", h=30, w=10, command=MainFK)

    mc.showWindow(WIN)

###.....................................................................................................###

def MainFK(*args):

#variables:

    con_radius = mc.floatSliderGrp("consize", query=True, value=True)
    con_suff = mc.textFieldGrp("suf", query=True, text=True)
    con_color = mc.colorSliderGrp("color", query=True, rgb=True)
    a, b, c = con_color  #This is my way of decomposing RGB colors for the overrideColorRGB, code line: 65
    sel = mc.ls(sl=True)
    previous_sel = None

    if len(sel) <= 0:
        om.MGlobal.displayError("Please select at least one joint!")

    else:
        for s in sel:
        # Create controllers and offsets for each joint
            ctrls = mc.circle(nr= (1, 0, 0), n= str(s + con_suff), radius= con_radius)
            mc.makeIdentity(apply=True)
            offset = mc.group(n=str("grp" + s.capitalize() + "_ZERO"))
        #Define the color for the controller
            mc.setAttr (offset + ".overrideEnabled", 1)
            mc.setAttr(offset + ".overrideRGBColors", 1)
            mc.setAttr(offset + ".overrideColorRGB", a, b, c)
        # Copy the position and orientation of the joints to the controllers
            temp_constraint= mc.parentConstraint(s, ctrls, maintainOffset=0)
            mc.delete(temp_constraint)
        #Make an orient constraint from the controllers to the joints to drive them.
            mc.orientConstraint(ctrls, s)

        #If there is more than one control, parent them in FK hierarchy:
            if previous_sel:
                mc.parent(offset, previous_sel)
            previous_sel = ctrls

        om.MGlobal.displayInfo("Your FK Control Chain has been created with success!")
