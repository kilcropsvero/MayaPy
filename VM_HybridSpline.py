#Este script crea sobre cualquier cadena de joints un FK hibrido y un spline, puede ser sencillo, dinamico o con un sine deformer.
#El sine no tiene atributos ajustados ni automatizacion, la hibrida tiene el follicle en both ends y tiene settings default.



import maya.cmds as cmds
import maya.mel as mel


# ---------------------------------------------------
# GET JOINT CHAIN
# ---------------------------------------------------

def get_joint_chain(start,end):

    chain=[]
    j=start

    while True:

        chain.append(j)

        if j==end:
            break

        children=cmds.listRelatives(j,c=True,type="joint")

        if not children:
            break

        j=children[0]

    return chain


# ---------------------------------------------------
# CLEAN OFFSET
# ---------------------------------------------------

def create_offset(obj,name):

    offset=cmds.group(empty=True,n=name)

    cmds.delete(cmds.parentConstraint(obj,offset))

    parent=cmds.listRelatives(obj,p=True)

    if parent:
        cmds.parent(offset,parent[0])

    cmds.parent(obj,offset)

    return offset


# ---------------------------------------------------
# IK CONTROLS
# ---------------------------------------------------

def create_ik_controls(chain,curve):

    base=chain[0]

    mid=len(chain)//2

    joints=[chain[0],chain[mid],chain[-1]]

    ctrl_grp=cmds.group(empty=True,n=base+"_IK_ctrl_grp")

    ctrls=[]

    for i,j in enumerate(joints):

        ctrl=cmds.circle(nr=(0,1,0),s=4)[0]

        ctrl=cmds.rename(ctrl,"%s_IK0%s_ctrl"%(base,i+1))

        cmds.scale(2,2,2,ctrl)

        cmds.makeIdentity(ctrl,apply=True,s=1)

        cmds.delete(ctrl,ch=True)

        cmds.delete(cmds.parentConstraint(j,ctrl))

        offset=create_offset(ctrl,ctrl.replace("_ctrl","_offset"))

        cmds.parent(offset,ctrl_grp)

        ctrls.append(ctrl)

    cvs=cmds.ls(curve+".cv[*]",fl=True)

    start_cluster=cmds.cluster(cvs[0],n=base+"_start_cls")
    mid_cluster=cmds.cluster(cvs[len(cvs)//2],n=base+"_mid_cls")
    end_cluster=cmds.cluster(cvs[-1],n=base+"_end_cls")

    clusters=[start_cluster[1],mid_cluster[1],end_cluster[1]]

    for i,handle in enumerate(clusters):

        grp_offset=cmds.group(handle,n=handle+"_offset")

        cmds.delete(cmds.parentConstraint(ctrls[i],grp_offset))

        cmds.parent(grp_offset,ctrls[i])


# ---------------------------------------------------
# STRETCH
# ---------------------------------------------------

def create_stretch(chain,curve):

    base=chain[0]

    shape=cmds.listRelatives(curve,s=True)[0]

    curve_info=cmds.createNode("curveInfo",n=base+"_curveInfo")

    cmds.connectAttr(shape+".worldSpace[0]",curve_info+".inputCurve")

    original_length=cmds.getAttr(curve_info+".arcLength")

    stretch_md=cmds.createNode("multiplyDivide",n=base+"_stretch_divide")

    cmds.setAttr(stretch_md+".operation",2)

    cmds.connectAttr(curve_info+".arcLength",stretch_md+".input1X")

    cmds.setAttr(stretch_md+".input2X",original_length)

    for j in chain:

        cmds.connectAttr(stretch_md+".outputX",j+".scaleX")


# ---------------------------------------------------
# BASIC SPLINE
# ---------------------------------------------------

def build_basic(chain):

    base=chain[0]

    handle,eff,curve=cmds.ikHandle(
        sj=chain[0],
        ee=chain[-1],
        sol="ikSplineSolver",
        ccv=True
    )

    handle=cmds.rename(handle,base+"_IKSP")
    curve=cmds.rename(curve,base+"_CV")
    cmds.setAttr(curve+".inheritsTransform",0)

    create_ik_controls(chain,curve)

    create_stretch(chain,curve)

    return handle,curve


# ---------------------------------------------------
# SINE SPLINE
# ---------------------------------------------------

def build_sine(chain):

    base=chain[0]

    handle,eff,curve=cmds.ikHandle(
        sj=chain[0],
        ee=chain[-1],
        sol="ikSplineSolver",
        ccv=True
    )

    handle=cmds.rename(handle,base+"_IKSP")
    curve=cmds.rename(curve,base+"_CV")
    cmds.setAttr(curve+".inheritsTransform",0)

    sine_curve=cmds.duplicate(curve,n=base+"_sineDriver")[0]

    cmds.move(5,0,0,sine_curve,r=True)

    sine,defHandle=cmds.nonLinear(sine_curve,type="sine")

    sine=cmds.rename(sine,base+"_sineDef")
    defHandle=cmds.rename(defHandle,base+"_sineHandle")

    blend=cmds.blendShape(sine_curve,curve,n=base+"_sineBlend")[0]

    cmds.setAttr(blend+"."+sine_curve,1)

    create_ik_controls(chain,curve)

    create_stretch(chain,curve)

    return handle,curve


# ---------------------------------------------------
# HYBRID IK
# ---------------------------------------------------

def build_hybrid(chain,input_curve):

    base=chain[0]

    # guardar nodos existentes
    follicles_before=set(cmds.ls(type="follicle"))
    hair_before=set(cmds.ls(type="hairSystem"))
    nucleus_before=set(cmds.ls(type="nucleus"))
    curves_before=set(cmds.ls(type="nurbsCurve"))

    cmds.select(input_curve)

    mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"}')

    # detectar nodos nuevos
    follicles_after=set(cmds.ls(type="follicle"))
    hair_after=set(cmds.ls(type="hairSystem"))
    nucleus_after=set(cmds.ls(type="nucleus"))
    curves_after=set(cmds.ls(type="nurbsCurve"))

    new_follicle=list(follicles_after-follicles_before)[0]
    new_hair=list(hair_after-hair_before)[0]
    new_nucleus=list(nucleus_after-nucleus_before)[0]

    new_curves=list(curves_after-curves_before)

    output_curve=None

    for c in new_curves:

        t=cmds.listRelatives(c,p=True)[0]

        if t!=input_curve:
            output_curve=t
            break

    follicle_transform=cmds.listRelatives(new_follicle,p=True)[0]

    follicle_transform=cmds.rename(follicle_transform,base+"_dynFollicle")
    new_hair=cmds.rename(new_hair,base+"_dynHairSystem")
    new_nucleus=cmds.rename(new_nucleus,base+"_dynNucleus")
    output_curve=cmds.rename(output_curve,base+"_dynOutputCurve")

    handle,eff=cmds.ikHandle(
        sj=chain[0],
        ee=chain[-1],
        sol="ikSplineSolver",
        curve=output_curve,
        ccv=False
    )

    handle=cmds.rename(handle,base+"_IKSP")

    move_grp=cmds.group(handle,follicle_transform,n=base+"_move_grp")

    cmds.group(output_curve,new_hair,new_nucleus,n=base+"_noTouch_grp")

    create_ik_controls(chain,output_curve)

    create_stretch(chain,output_curve)

    return move_grp,output_curve


# ---------------------------------------------------
# FK SYSTEM
# ---------------------------------------------------

def build_fk(chain):

    base=chain[0]

    fk_root=cmds.duplicate(chain[0],rc=True)[0]

    fk_chain=[fk_root]

    children=cmds.listRelatives(fk_root,ad=True,type="joint") or []

    children.reverse()

    fk_chain.extend(children)

    cmds.delete(fk_chain[-1])

    fk_chain=fk_chain[:-1]

    offsets=[]

    for i,j in enumerate(fk_chain):

        name="%s_FK0%s_ctrl"%(base,i+1)

        j=cmds.rename(j,name)

        ctrl=cmds.circle(nr=(1,0,0))[0]

        cmds.delete(ctrl,ch=True)

        cmds.delete(cmds.parentConstraint(j,ctrl))

        shape=cmds.listRelatives(ctrl,s=True)[0]

        cmds.parent(shape,j,r=True,s=True)

        cmds.delete(ctrl)

        offset=create_offset(j,name.replace("_ctrl","_offset"))

        offsets.append(offset)

    return offsets


# ---------------------------------------------------
# CONNECT ORIGINAL → FK
# ---------------------------------------------------

def connect_original(chain,offsets):

    cmds.parentConstraint(chain[0],offsets[0],mo=True)

    for i in range(1,len(offsets)):

        cmds.connectAttr(chain[i]+".translate",offsets[i]+".translate",f=True)

        cmds.connectAttr(chain[i]+".rotate",offsets[i]+".rotate",f=True)


# ---------------------------------------------------
# CLEANUP BASIC / SINE
# ---------------------------------------------------

def cleanup_basic(base,chain,offsets,handle,curve):

    grp=cmds.group(empty=True,n=base+"_grp")

    cmds.parent(chain[0],grp)

    cmds.parent(offsets[0],grp)

    if cmds.objExists(base+"_IK_ctrl_grp"):
        cmds.parent(base+"_IK_ctrl_grp",grp)

    cmds.parent(handle,grp)
    cmds.parent(curve,grp)


# ---------------------------------------------------
# BUILD
# ---------------------------------------------------

def build():

    start=cmds.textField("startField",q=True,text=True)
    end=cmds.textField("endField",q=True,text=True)

    mode=cmds.optionMenu("ikMode",q=True,v=True)

    chain=get_joint_chain(start,end)

    offsets=build_fk(chain)

    connect_original(chain,offsets)

    base=chain[0]

    if mode=="Basic IK":

        handle,curve=build_basic(chain)

        cleanup_basic(base,chain,offsets,handle,curve)

    elif mode=="Sine Spline":

        handle,curve=build_sine(chain)

        cleanup_basic(base,chain,offsets,handle,curve)

    elif mode=="Hybrid IK":

        input_curve=cmds.textField("curveField",q=True,text=True)

        move_grp,output_curve=build_hybrid(chain,input_curve)

        cleanup_basic(base,chain,offsets,move_grp,output_curve)


# ---------------------------------------------------
# UI
# ---------------------------------------------------

def load_start():

    sel=cmds.ls(sl=True)

    if sel:
        cmds.textField("startField",e=True,text=sel[0])


def load_end():

    sel=cmds.ls(sl=True)

    if sel:
        cmds.textField("endField",e=True,text=sel[0])


def load_curve():

    sel=cmds.ls(sl=True)

    if sel:
        cmds.textField("curveField",e=True,text=sel[0])


def update_ui(*args):

    mode=cmds.optionMenu("ikMode",q=True,v=True)

    cmds.rowLayout("curveRow",e=True,vis=(mode=="Hybrid IK"))


def ui():

    if cmds.window("HybridRigUI",exists=True):
        cmds.deleteUI("HybridRigUI")

    cmds.window("HybridRigUI",title="Hybrid IK Builder")

    cmds.columnLayout(adj=True)

    cmds.text(l="Creates hybrid spline FK systems: basic, dynamic and sine.",align="left")

    cmds.separator(h=10)

    cmds.text("Start Joint")

    cmds.rowLayout(nc=2)
    cmds.textField("startField")
    cmds.button(l="Load",c=lambda x:load_start())
    cmds.setParent("..")

    cmds.text("End Joint")

    cmds.rowLayout(nc=2)
    cmds.textField("endField")
    cmds.button(l="Load",c=lambda x:load_end())
    cmds.setParent("..")

    cmds.separator(h=10)

    cmds.text("Mode")

    cmds.optionMenu("ikMode",changeCommand=update_ui)
    cmds.menuItem(l="Basic IK")
    cmds.menuItem(l="Hybrid IK")
    cmds.menuItem(l="Sine Spline")

    cmds.rowLayout("curveRow",nc=2,vis=False)
    cmds.textField("curveField")
    cmds.button(l="Load Curve",c=lambda x:load_curve())
    cmds.setParent("..")

    cmds.separator(h=10)

    cmds.button(l="BUILD",h=40,c=lambda x:build())

    cmds.showWindow()


ui()
