import maya.cmds as cmds
import maya.mel as mel
from VM_riggingTools import VM_rename, VM_orient, VM_controllers, VM_zeroOut


def launch_vm_rigging_tools_ui():
    if cmds.window("VMToolsWin", exists=True):
        cmds.deleteUI("VMToolsWin")

    win = cmds.window("VMToolsWin", title="VM_riggingTools", widthHeight=(320, 500), sizeable=1)
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # Rename Section
    cmds.frameLayout(label="Rename", collapsable=True, marginHeight=5)
    cmds.button(label="Rename Menu", 
                height=30, 
                bgc=(0.2, 0.2, 0.2),
                command=lambda *_: VM_rename.launch_rename_ui())
    cmds.setParent(main_layout)

    # Orient Section
    cmds.frameLayout(label="Orient Joints", collapsable=True, marginHeight=5)
    cmds.button(label="Orient Joint Menu", 
                height=30, 
                bgc=(0.2, 0.2, 0.2), 
                command=lambda *_: VM_orient.launch_joint_orient_ui())
    cmds.setParent(main_layout)

    # Shapes
    cmds.frameLayout(label="Shapes", collapsable=True, marginHeight=5)
    cmds.button(label="Shapes and Controls Menu", 
                height=30, 
                bgc=(0.2, 0.2, 0.2), 
                command=lambda *_: VM_controllers.launch_controller_ui())
    cmds.setParent(main_layout)
        

    # Zero Out / Null Section
    cmds.frameLayout(label="Zero Out", collapsable=True, marginHeight=5)
    cmds.button(label="Make ZeroOut", 
                height=30, 
                bgc=(0.2, 0.2, 0.2),
                command=lambda *_: VM_zeroOut.zero_out())
    cmds.setParent(main_layout)
    
    cmds.separator(style='in')
    
    # Conection Window
    cmds.frameLayout(label="Connection Tools", collapsable=True, marginHeight=5)
    cmds.rowColumnLayout(numberOfColumns=3,
                         columnWidth=[(1, 120), (2, 120), (3, 120)],
                         rowSpacing=[(1, 5), (2, 5), (3, 5), (4, 5)],
                         columnSpacing=[(1, 5), (2, 5), (3, 5)])
    
    handlers = {
        "Connection Editor":  lambda *_: mel.eval("ConnectionEditor;"),
        "Node Editor":        lambda *_: mel.eval("NodeEditorWindow;"),
        "Set Driven Key":     lambda *_: mel.eval("SetDrivenKey;"),
        "Expression Editor":  lambda *_: mel.eval("ExpressionEditor;"),
        "Script Editor":      lambda *_: mel.eval("ScriptEditor;"),
        "Component Editor":    lambda *_: mel.eval("ComponentEditor;")
    }
    
    for label in ["Connection Editor", "Node Editor", "Set Driven Key",
                  "Expression Editor", "Script Editor", "Component Editor"]:
        cmds.button(label=label,
                    bgc=(0.2, 0.2, 0.2),
                    command=handlers[label])
    
    
    cmds.setParent('..') 
    cmds.setParent('..') 
    cmds.separator(style='in')


    cmds.showWindow(win)
    
    
launch_vm_rigging_tools_ui()
