# To be honest, I don't like this setup.It's not intuitive for animators at all.
# A lighter, less complex version than Jeff Burosky's original one
#Created by Vero Morera, march 2026

import maya.cmds as cmds


# ------------------------------------------------------------
# BUILD VARIABLE FK
# ------------------------------------------------------------

def buildVariableFK(*args):

    curve = cmds.textField("vfk_curve", q=True, text=True)
    prefix = cmds.textField("vfk_prefix", q=True, text=True)
    ctrlCount = cmds.intSliderGrp("vfk_ctrls", q=True, v=True)

    if not cmds.objExists(curve):
        cmds.warning("Curve not found")
        return

    cmds.undoInfo(openChunk=True)

    try:

        curveShape = cmds.listRelatives(curve, s=True)[0]

        cmds.setAttr(curve + ".inheritsTransform", 0)

        jointCount = len(cmds.ls(curve + ".cv[*]", fl=True))

        joints = []

        # ----------------------------------------------------
        # CREATE JOINTS EVENLY ALONG CURVE
        # ----------------------------------------------------

        for i in range(jointCount):

            param = float(i)/(jointCount-1)

            pci = cmds.createNode("pointOnCurveInfo")

            cmds.connectAttr(curveShape+".worldSpace[0]", pci+".inputCurve")
            cmds.setAttr(pci+".turnOnPercentage",1)
            cmds.setAttr(pci+".parameter",param)

            pos = cmds.getAttr(pci+".position")[0]

            j = cmds.joint(p=pos, n=f"{prefix}_jnt_{i+1}")

            cmds.addAttr(j, ln="param", at="double", k=True)
            cmds.setAttr(j+".param",param)

            joints.append(j)

            cmds.delete(pci)

        # FK hierarchy joints
        for i in range(1,len(joints)):
            cmds.parent(joints[i], joints[i-1])

        cmds.select(clear=True)

        # ----------------------------------------------------
        # CREATE CONTROLS
        # ----------------------------------------------------

        ctrls = []

        for i in range(ctrlCount):

            ctrl = cmds.circle(
                n=f"{prefix}_ctrl_{i+1}",
                r=2,
                nr=[1,0,0]
            )[0]

            slide_grp = cmds.group(ctrl, n=ctrl+"_slide")
            offset_grp = cmds.group(slide_grp, n=ctrl+"_offset")

            cmds.addAttr(ctrl, ln="position", at="double", min=0, max=1, k=True)
            cmds.addAttr(ctrl, ln="radius", at="double", min=0.001, dv=0.3, k=True)

            pci = cmds.createNode("pointOnCurveInfo", n=ctrl+"_pci")

            cmds.connectAttr(curveShape+".worldSpace[0]", pci+".inputCurve")
            cmds.setAttr(pci+".turnOnPercentage",1)

            cmds.connectAttr(ctrl+".position", pci+".parameter")
            cmds.connectAttr(pci+".position", slide_grp+".translate")

            if ctrlCount > 1:
                cmds.setAttr(ctrl+".position", float(i)/(ctrlCount-1))

            ctrls.append(ctrl)

        # ----------------------------------------------------
        # FK HIERARCHY CONTROLS
        # ----------------------------------------------------

        for i in range(len(ctrls)-1):

            parentCtrl = ctrls[i]
            childOffset = ctrls[i+1] + "_offset"

            cmds.parent(childOffset, parentCtrl)

        # ----------------------------------------------------
        # VARIABLE FK INFLUENCE
        # ----------------------------------------------------

        for j in joints:

            sumNode = cmds.createNode("plusMinusAverage")

            for i,ctrl in enumerate(ctrls):

                dist = cmds.createNode("distanceBetween")

                cmds.connectAttr(j+".param", dist+".point1X")
                cmds.connectAttr(ctrl+".position", dist+".point2X")

                remap = cmds.createNode("remapValue")

                cmds.connectAttr(dist+".distance", remap+".inputValue")

                cmds.setAttr(remap+".value[0].value_Position",0)
                cmds.setAttr(remap+".value[0].value_FloatValue",1)

                cmds.connectAttr(ctrl+".radius", remap+".value[1].value_Position")

                cmds.setAttr(remap+".value[1].value_FloatValue",0)

                mult = cmds.createNode("multiplyDivide")

                cmds.connectAttr(ctrl+".rotate", mult+".input1")

                cmds.connectAttr(remap+".outValue", mult+".input2X")
                cmds.connectAttr(remap+".outValue", mult+".input2Y")
                cmds.connectAttr(remap+".outValue", mult+".input2Z")

                cmds.connectAttr(mult+".output", sumNode+f".input3D[{i}]")

            cmds.connectAttr(sumNode+".output3D", j+".rotate")

        print("Variable FK rig created!")

    finally:

        cmds.undoInfo(closeChunk=True)


# ------------------------------------------------------------
# LOAD CURVE
# ------------------------------------------------------------

def loadCurve(*args):

    sel = cmds.ls(sl=True)

    if sel:
        cmds.textField("vfk_curve", e=True, text=sel[0])


# ------------------------------------------------------------
# UI
# ------------------------------------------------------------

def variableFK_UI():

    if cmds.window("variableFK_UI", exists=True):
        cmds.deleteUI("variableFK_UI")

    win = cmds.window(
        "variableFK_UI",
        title="Variable FK Builder",
        widthHeight=(320,220)
    )

    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    cmds.text(
        label="VARIABLE FK\n\n1 Load a curve\n2 Choose amount of controls\n3 Build the setup",
        align="left"
    )

    cmds.rowLayout(nc=2)

    cmds.textField("vfk_curve", text="curve1", width=220)
    cmds.button(label="Load Selected", command=loadCurve)

    cmds.setParent("..")

    cmds.text(label="Rig Prefix")

    cmds.textField("vfk_prefix", text="varFK")

    cmds.intSliderGrp(
        "vfk_ctrls",
        label="Controls",
        field=True,
        min=1,
        max=10,
        value=3
    )

    cmds.button(
        label="Build Variable FK",
        height=40,
        command=buildVariableFK
    )

    cmds.showWindow(win)


# ------------------------------------------------------------
# RUN UI
# ------------------------------------------------------------

variableFK_UI()
