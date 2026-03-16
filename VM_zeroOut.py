import maya.cmds as cmds
import re

def zero_out():
    selection = cmds.ls(selection=True, type='transform')

    if not selection:
        cmds.warning("No objects selected.")
        return

    for ctrl in selection:
        # Get short name (no hierarchy)
        short_name = cmds.ls(ctrl, shortNames=True)[0]

        # Remove any existing ZERO suffix
        base_name = re.sub(r'ZERO\d*$', '', short_name)
        base_name = base_name[0].upper() + base_name[1:]

        # Try base name first
        base_grp_name = f"grp{base_name}ZERO"
        grp_name = base_grp_name

        # If name exists, add numeric suffix
        i = 2
        while cmds.objExists(grp_name):
            grp_name = f"{base_grp_name}{i}"
            i += 1

        # Get current scale values
        scale = cmds.getAttr(ctrl + ".scale")[0]

        # Unlock transform attributes if locked
        for attr in ['translateX', 'translateY', 'translateZ',
                     'rotateX', 'rotateY', 'rotateZ',
                     'scaleX', 'scaleY', 'scaleZ']:
            if cmds.getAttr(ctrl + "." + attr, lock=True):
                cmds.setAttr(ctrl + "." + attr, lock=False)

        # Freeze only scale if needed
        if scale != (1.0, 1.0, 1.0):
            cmds.makeIdentity(ctrl, apply=True, t=False, r=False, s=True, n=0)

        # Get transform values
        pos = cmds.xform(ctrl, q=True, ws=True, t=True)
        rot = cmds.xform(ctrl, q=True, ws=True, ro=True)

        # Create the group
        grp = cmds.group(empty=True, name=grp_name)
        cmds.xform(grp, ws=True, t=pos)
        cmds.xform(grp, ws=True, ro=rot)

        # Parent to original parent if any
        parent = cmds.listRelatives(ctrl, parent=True)
        if parent:
            cmds.parent(grp, parent[0])

        # Parent the control under the new group
        cmds.parent(ctrl, grp)

        # Zero out translate and rotate (no freeze)
        cmds.setAttr(ctrl + ".translate", 0, 0, 0)
        cmds.setAttr(ctrl + ".rotate", 0, 0, 0)

        print(f"Zero out group created: {grp_name}")

    print("Zero out complete.")
    
  
