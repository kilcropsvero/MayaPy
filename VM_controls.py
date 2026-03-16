#aun no funciona, solo tiene la UI, no crea controles. 


import maya.cmds as cmds 
import maya.mel as mel

def launch_controller_ui():
    if cmds.window("vmControllersWin", exists=True):
        cmds.deleteUI("vmControllersWin")

    window = cmds.window("vmControllersWin", title="VM Controls", widthHeight=(300, 220), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAlign='left', columnAttach=["both", 10])

    # Shapes Section with buttons
    cmds.frameLayout(label="Shapes", collapsable=True, marginHeight=5)
    cmds.rowColumnLayout(numberOfColumns=3,
                         columnWidth=[(1, 100), (2, 100), (3, 100)],
                         rowSpacing=[(1, 5), (2, 5), (3, 5), (4, 5)],
                         columnSpacing=[(1, 5), (2, 5), (3, 5)])

    for label in ["Circle X", "Circle Y", "Circle Z", "Square", "Cube", "Sphere", "Moon", "Cone", "Gear",
                  "Arrow", "Cross-Arrow", "Cross", "IK/FK", "Smily Face", "Joystick", "Null", "Locator", "Joint"]:
        cmds.button(label=label, backgroundColor=(0.2, 0.2, 0.2))

    cmds.setParent('..')  # rowColumnLayout
    cmds.separator(style='in')

    cmds.text(label="Customize Controls", align='center')
    cmds.button(label="Replace Control", height=30, backgroundColor=(0.2, 0.2, 0.2))
    
    cmds.button(label="Channel Control", height=30, 
                backgroundColor=(0.2, 0.2, 0.2), 
                command= lambda *_: mel.eval("ChannelControlEditor;"))

    cmds.floatSliderGrp(label='Control Thickness', field=True, minValue=1.0, maxValue=5.0, fieldMinValue=1.0,
                        fieldMaxValue=10.0, value=1.0,
                        columnWidth=[(1, 120), (2, 40), (3, 120)])

    cmds.showWindow(window)
launch_controller_ui()
