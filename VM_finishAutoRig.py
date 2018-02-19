import maya.cmds as mc
import maya.OpenMaya as om

def finish(*args):

    mc.select("root_CC")
    rootshape= mc.listRelatives("root_CC", shapes=True)
    rootGrp= mc.group(n="grpRoot_CCZERO")
    mc.setAttr("{}.overrideEnabled".format(rootshape[0]), 1)
    mc.setAttr("{}.overrideColor".format(rootshape[0]), 14)
    mc.select("move_CC")
    moveshape= mc.listRelatives("move_CC", shapes=True)
    moveGrp = mc.group(n="grpMove_CCZERO")
    mc.setAttr("{}.overrideEnabled".format(moveshape[0]), 1)
    mc.setAttr("{}.overrideColor".format(moveshape[0]), 17)
    masterGRP= mc.group(n="RIG_GRP", empty=True)
    mc.parent(moveGrp, "root_CC")
    mc.parent(rootGrp, masterGRP)
    mc.parent("L_leg_GRP", "R_leg_GRP", "L_arm_GRP", "R_arm_GRP",
              "spine_GRP", "neck_GRP", "head_GRP", "IK_GRP", "move_CC")


    #Hand fingers hierarchy:
    mc.parent("L_palm_JJ", "L_wrist_JJ")
    mc.parent("R_palm_JJ", "R_wrist_JJ")
    mc.parent("L_fingers_GRP", "L_arm_GRP")
    mc.parentConstraint("L_wrist_JJ", "L_fingers_GRP", mo=True)
    mc.parent("R_fingers_GRP", "R_arm_GRP")
    mc.parentConstraint("R_wrist_JJ", "R_fingers_GRP", mo=True)

    #Finish hierarchy
    mc.parentConstraint("spine_IK_02_CC", "neck_GRP", mo=True)
    mc.parentConstraint("spine_IK_02_CC", "L_arm_GRP", mo=True)
    mc.parentConstraint("spine_IK_02_CC", "R_arm_GRP", mo=True)

    if mc.objExists("pelvis_CC"):
        mc.parentConstraint("pelvis_CC", "L_leg_GRP", mo=True)
        mc.parentConstraint("pelvis_CC", "R_leg_GRP", mo=True)
    else:
        mc.parentConstraint("COG_CC", "L_leg_GRP", mo=True)
        mc.parentConstraint("COG_CC", "R_leg_GRP", mo=True)

    #Clean up
    mc.delete("Proxy_RIG")

    #Create joint set for skinning
    mc.select("L_hip_JJ", "L_knee_JJ", "L_ankle_JJ", "L_ball_JJ",
                    "R_hip_JJ", "R_knee_JJ", "R_ankle_JJ", "R_ball_JJ",
                    "L_clavicle_JJ",
                    "L_pinky_01_JJ", "L_pinky_02_JJ", "L_pinky_03_JJ", "L_pinky_04_JJ",
                    "L_ring_01_JJ", "L_ring_02_JJ", "L_ring_03_JJ", "L_ring_04_JJ",
                    "L_middle_01_JJ", "L_middle_02_JJ", "L_middle_03_JJ", "L_middle_04_JJ",
                    "L_index_01_JJ", "L_index_02_JJ", "L_index_03_JJ", "L_index_04_JJ",
                    "L_thumbs_01_JJ", "L_thumbs_02_JJ", "L_thumbs_03_JJ",
                    "L_loarmTwist_A_JJ", "L_loarmTwist_B_JJ", "L_loarmTwist_C_JJ",
                    "L_uparmTwist_A_JJ", "L_uparmTwist_B_JJ", "L_uparmTwist_C_JJ",
                    "R_clavicle_JJ",
                    "R_pinky_01_JJ", "R_pinky_02_JJ", "R_pinky_03_JJ", "R_pinky_04_JJ",
                    "R_ring_01_JJ", "R_ring_02_JJ", "R_ring_03_JJ", "R_ring_04_JJ",
                    "R_middle_01_JJ", "R_middle_02_JJ", "R_middle_03_JJ", "R_middle_04_JJ",
                    "R_index_01_JJ", "R_index_02_JJ", "R_index_03_JJ", "R_index_04_JJ",
                    "R_thumbs_01_JJ", "R_thumbs_02_JJ", "R_thumbs_03_JJ",
                    "R_loarmTwist_A_JJ", "R_loarmTwist_B_JJ", "R_loarmTwist_C_JJ",
                    "R_uparmTwist_A_JJ", "R_uparmTwist_B_JJ", "R_uparmTwist_C_JJ",
                    "spine_01_JJ", "spine_02_JJ", "spine_03_JJ", "spine_04_JJ",
                    "neck_01_JJ", "head_01_JJ", "head_02_JJ", "jaw_01_JJ")

    setList= mc.ls(sl=True)
    mc.sets(setList, name="BIND_JOINTS_SET")

    om.MGlobal.displayInfo("Your rig was cleaned and grouped sucesfully!")
