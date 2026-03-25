import maya.cmds as cmds

# =========================
# UI
# =========================

def vm_wingRig_UI():
    if cmds.window("vmWingRig", exists=True):
        cmds.deleteUI("vmWingRig")

    cmds.window("vmWingRig", title="VM Wing Rig FINAL")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)

    cmds.text(label="Seleccioná Shoulder → Elbow → Wrist")
    cmds.textField("jointField")
    cmds.button(label="Load Joints (3)", command=load_joints)

    cmds.separator(h=10)

    cmds.text(label="Seleccioná Ctrl0 → Ctrl1 → Ctrl2 → Ctrl3")
    cmds.text(label="van en la primera pluma shoulder, ultima shoulder, ultima elbow, ultima wrist")
    cmds.textField("ctrlField")
    cmds.button(label="Load Controls (4)", command=load_ctrls)

    cmds.separator(h=10)

    cmds.text(label="Seleccioná grupos: Shoulder → Elbow → Wrist")
    cmds.textField("featherGroupField")
    cmds.button(label="Load Feathers Groups (3)", command=load_groups)

    cmds.separator(h=15)

    cmds.button(label="CREATE RIG", h=40, command=create_rig)

    cmds.showWindow()


# =========================
# LOADERS
# =========================

def load_joints(*args):
    sel = cmds.ls(sl=True)
    if len(sel) != 3:
        cmds.warning("Selecciona 3 joints")
        return
    cmds.textField("jointField", e=True, text=",".join(sel))


def load_ctrls(*args):
    sel = cmds.ls(sl=True)
    if len(sel) != 4:
        cmds.warning("Selecciona 4 controles")
        return
    cmds.textField("ctrlField", e=True, text=",".join(sel))


def load_groups(*args):
    sel = cmds.ls(sl=True)
    if len(sel) != 3:
        cmds.warning("Selecciona 3 grupos de plumas")
        return
    cmds.textField("featherGroupField", e=True, text=",".join(sel))


# =========================
# HELPERS
# =========================

def get_children(group):
    return cmds.listRelatives(group, c=True, type="joint") or []


def clean_old(feathers):
    for f in feathers:
        cons = cmds.listRelatives(f, type="orientConstraint") or []
        for c in cons:
            cmds.delete(c)


def create_offset(jnt):
    parent = cmds.listRelatives(jnt, p=True)

    off = cmds.duplicate(jnt, parentOnly=True)[0]
    off = cmds.rename(off, jnt + "_offset")

    children = cmds.listRelatives(off, c=True) or []
    for c in children:
        cmds.delete(c)

    if parent:
        cmds.parent(off, parent[0])

    cmds.delete(cmds.parentConstraint(jnt, off))
    cmds.parent(jnt, off)


def blend(target, A, B, t):

    const = cmds.orientConstraint(A, B, target, mo=False)[0]

    weights = cmds.orientConstraint(const, q=True, weightAliasList=True)
    w0 = const + "." + weights[0]
    w1 = const + "." + weights[1]

    cmds.setAttr(w0, 1 - t)
    cmds.setAttr(w1, t)

    pma = cmds.createNode("plusMinusAverage", name=target + "_PMA")
    cmds.setAttr(pma + ".input1D[0]", t)

    rev = cmds.createNode("reverse", name=target + "_REV")
    cmds.connectAttr(pma + ".output1D", rev + ".inputX")

    cmds.connectAttr(pma + ".output1D", w1, f=True)
    cmds.connectAttr(rev + ".outputX", w0, f=True)

    cmds.setAttr(const + ".interpType", 2)


# =========================
# MAIN
# =========================

def create_rig(*args):

    shoulder, elbow, wrist = cmds.textField("jointField", q=True, text=True).split(",")
    ctrl0, ctrl1, ctrl2, ctrl3 = cmds.textField("ctrlField", q=True, text=True).split(",")
    shoulder_grp, elbow_grp, wrist_grp = cmds.textField("featherGroupField", q=True, text=True).split(",")

    # Obtener plumas SIN confiar en orden futuro
    shoulder_feats = get_children(shoulder_grp)
    elbow_feats = get_children(elbow_grp)
    wrist_feats = get_children(wrist_grp)

    # Guardar orden ORIGINAL
    shoulder_order = shoulder_feats[:]
    elbow_order = elbow_feats[:]
    wrist_order = wrist_feats[:]

    # Limpieza
    clean_old(shoulder_feats)
    clean_old(elbow_feats)
    clean_old(wrist_feats)

    # OFFSETS
    for f in shoulder_feats + elbow_feats + wrist_feats:
        create_offset(f)

    # 🔥 USAR ORDEN ORIGINAL (NO DAG)
    shoulder_feats = shoulder_order
    elbow_feats = elbow_order
    wrist_feats = wrist_order

    shoulder_first = shoulder_feats[0]
    shoulder_last = shoulder_feats[-1]

    elbow_last = elbow_feats[-1]
    wrist_last = wrist_feats[-1]

    # =========================
    # ANCHORS
    # =========================

    cmds.orientConstraint(ctrl0, shoulder_first, mo=True)
    cmds.orientConstraint(ctrl1, shoulder_last, mo=True)
    cmds.orientConstraint(ctrl2, elbow_last, mo=True)
    cmds.orientConstraint(ctrl3, wrist_last, mo=True)

    # =========================
    # SHOULDER
    # =========================

    for i, f in enumerate(shoulder_feats[1:-1]):
        t = float(i + 1) / float(len(shoulder_feats) - 1)
        blend(f, ctrl0, ctrl1, t)

    # =========================
    # ELBOW (sin último)
    # =========================

    for i, f in enumerate(elbow_feats[:-1]):
        t = float(i + 1) / float(len(elbow_feats))
        blend(f, ctrl1, ctrl2, t)

    # =========================
    # WRIST (incluye elbow_last)
    # =========================

    extended_wrist = [elbow_last] + wrist_feats
    count = len(extended_wrist)

    for i, f in enumerate(extended_wrist):

        if f == wrist_last:
            continue

        if i == 0:
            blend(f, ctrl2, ctrl3, 0.1)
        else:
            t = float(i) / float(count - 1)
            blend(f, ctrl2, ctrl3, t)

    # =========================
    # PARENT FINAL
    # =========================

    cmds.parent(shoulder_grp, shoulder, absolute=True)
    cmds.parent(elbow_grp, elbow, absolute=True)
    cmds.parent(wrist_grp, wrist, absolute=True)

    print("Wing Rig done!")


# =========================
# RUN
# =========================

vm_wingRig_UI()
