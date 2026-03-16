#esta herramienta es un desastre, esta a anios luz de servir... pero pongo el avance marzo 2025

import maya.cmds as cmds

def launch_joint_orient_ui():
    if cmds.window("vmJointOrientWin", exists=True):
        cmds.deleteUI("vmJointOrientWin")

    window = cmds.window("vmJointOrientWin", title="VM Joint Orient", widthHeight=(300, 220), sizeable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAlign='left', columnAttach=["both", 10])

    # Aim Axis
    cmds.text(label="Aim Axis:")
    cmds.rowLayout(numberOfColumns=4, columnWidth4=(50, 50, 50, 70), adjustableColumn=4)
    aim_axis_radio = cmds.radioButtonGrp(labelArray3=["X", "Y", "Z"], numberOfRadioButtons=3, select=1)
    aim_reverse_cb = cmds.checkBox(label="Reverse")
    cmds.setParent("..")

    # Up Axis
    cmds.text(label="Up Axis:")
    cmds.rowLayout(numberOfColumns=4, columnWidth4=(50, 50, 50, 70), adjustableColumn=4)
    up_axis_radio = cmds.radioButtonGrp(labelArray3=["X", "Y", "Z"], numberOfRadioButtons=3, select=3)
    up_reverse_cb = cmds.checkBox(label="Reverse")
    cmds.setParent("..")

    # World Up Direction
    cmds.text(label="World Up Direction:")
    world_up_fields = cmds.floatFieldGrp(numberOfFields=3, value1=0.0, value2=1.0, value3=0.0, label="", columnWidth=[(1, 30), (2, 60), (3, 60), (4, 60)])

    # Auto Guess checkbox
    auto_guess_cb = cmds.checkBox(label="Auto-Guess Up Direction", value=False)

    # Orient Button
    cmds.separator(height=10, style='in')
    cmds.button(label="Orient Joints", height=30, bgc=(.3, .6, .3), command=lambda *_:
        orient_selected_joints(
            aim_axis_radio, aim_reverse_cb,
            up_axis_radio, up_reverse_cb,
            world_up_fields, auto_guess_cb
        )
    )

    cmds.setParent("..")
    cmds.showWindow(window)


def orient_selected_joints(aim_radio, aim_rev, up_radio, up_rev, world_up_fields, auto_guess_cb):
    selection = cmds.ls(selection=True, type="joint")
    if not selection:
        cmds.warning("Please select one or more joints.")
        return

    # Get axis selections
    aim_index = cmds.radioButtonGrp(aim_radio, query=True, select=True) - 1
    up_index = cmds.radioButtonGrp(up_radio, query=True, select=True) - 1
    axes = ["x", "y", "z"]
    aim_axis = axes[aim_index]
    up_axis = axes[up_index]

    # Reverse settings
    if cmds.checkBox(aim_rev, query=True, value=True):
        aim_axis = "-" + aim_axis
    if cmds.checkBox(up_rev, query=True, value=True):
        up_axis = "-" + up_axis

    # World Up vector
    if cmds.checkBox(auto_guess_cb, query=True, value=True):
        world_up = guess_world_up_direction(selection)
    else:
        world_up = cmds.floatFieldGrp(world_up_fields, query=True, value=True)

    for jnt in selection:
        children = cmds.listRelatives(jnt, children=True, type="joint")
        if not children:
            continue
        cmds.joint(jnt, edit=True,
                   orientJoint=aim_axis + "up" + up_axis,
                   secondaryAxisOrient=up_axis,
                   worldUpType="vector",
                   worldUpVector=world_up)


def guess_world_up_direction(joints):
    """
    Estimate a world up direction based on first two joints in the chain.
    Simple heuristic: cross product of joint vector and world forward.
    """
    if len(joints) < 2:
        return [0, 1, 0]  # default
    try:
        jnt1 = joints[0]
        jnt2 = cmds.listRelatives(jnt1, children=True, type="joint")[0]
        pos1 = cmds.xform(jnt1, q=True, ws=True, t=True)
        pos2 = cmds.xform(jnt2, q=True, ws=True, t=True)
        vec = [pos2[i] - pos1[i] for i in range(3)]

        # Cross product with world forward (e.g., X)
        forward = [1, 0, 0]
        up = [vec[1]*forward[2] - vec[2]*forward[1],
              vec[2]*forward[0] - vec[0]*forward[2],
              vec[0]*forward[1] - vec[1]*forward[0]]
        return up
    except:
        return [0, 1, 0]


# Lanzar la interfaz (esto se ejecuta cuando corres el script)
if __name__ == "__main__":
    launch_joint_orient_ui()
