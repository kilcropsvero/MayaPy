import maya.cmds as mc
import maya.OpenMaya as om

WIN="AutoHand"

def UI():
    # Window Creation
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title= "VM Hand Rig", h=100, w=300, sizeable=True)
    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=2)
    mc.text("Select the entire hand hierarchy of ORIENTED joints.", h=25)
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=1)
    mc.radioCollection()
    mc.radioButton("fiveFingers", label="This hand have 5 fingers.")
    mc.radioButton("fourFingers", label="This hand only have 4 fingers.")
    mc.setParent('..')
    #
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button(label= "L Hand Auto", w=100, h=40, c=hand, bgc=(.2,.2,.2))
    mc.radioCollection()
    mc.radioButton("rhand", label="Mirror to Right Hand")
    mc.setParent('..')

    mc.showWindow(WIN)

def hand(*args):
    sel = mc.ls(sl=True)

    if mc.radioButton("fiveFingers", query=True, select=True):
        if len(sel) < 25:
            om.MGlobal.displayError("Please select the entire hand hierarchy")

        else:
            hand = mc.ls(sl=True)
            pinky = hand[1:5]
            ring = hand[6:10]
            middle = hand[11:15]
            index = hand[16:20]
            thumbs = hand[21:24]

            # (THIS IS FOR THE RIGHT ARM)
            if mc.radioButton("rhand", query=True, select=True):
                mc.select(hand[0])
                mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
                mc.select(hierarchy=True)
                rhand = mc.ls(sl=True)
            # (END OF THE RIGHT ARM)

            #Make controllers for the joints.
            for j in hand:
                mc.setAttr("{}.segmentScaleCompensate" .format(j), 0)

            previous_sel = None
            for j in pinky:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                #ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in ring:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in middle:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in index:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in thumbs:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls

            #Group all together
            fingrp= mc.group(n="L_fingers_GRP", empty=True)
            temp_constraint= mc.pointConstraint(hand[0], fingrp)
            mc.delete(temp_constraint)
            mc.parent("grpL_pinky01_ZERO", "grpL_ring01_ZERO", "grpL_middle01_ZERO",
                     "grpL_index01_ZERO", "grpL_thumbs01_ZERO", "L_fingers_GRP")

            #Rename joints for left hand:
            mc.rename(hand[0], "L_palm_JJ")
            mc.rename(hand[1], "L_pinky_01_JJ")
            mc.rename(hand[2], "L_pinky_02_JJ")
            mc.rename(hand[3], "L_pinky_03_JJ")
            mc.rename(hand[4], "L_pinky_04_JJ")
            mc.rename(hand[5], "L_pinky_05_JE")
            mc.rename(hand[6], "L_ring_01_JJ")
            mc.rename(hand[7], "L_ring_02_JJ")
            mc.rename(hand[8], "L_ring_03_JJ")
            mc.rename(hand[9], "L_ring_04_JJ")
            mc.rename(hand[10], "L_ring_05_JE")
            mc.rename(hand[11], "L_middle_01_JJ")
            mc.rename(hand[12], "L_middle_02_JJ")
            mc.rename(hand[13], "L_middle_03_JJ")
            mc.rename(hand[14], "L_middle_04_JJ")
            mc.rename(hand[15], "L_middle_05_JE")
            mc.rename(hand[16], "L_index_01_JJ")
            mc.rename(hand[17], "L_index_02_JJ")
            mc.rename(hand[18], "L_index_03_JJ")
            mc.rename(hand[19], "L_index_04_JJ")
            mc.rename(hand[20], "L_index_05_JE")
            mc.rename(hand[21], "L_thumbs_01_JJ")
            mc.rename(hand[22], "L_thumbs_02_JJ")
            mc.rename(hand[23], "L_thumbs_03_JJ")
            mc.rename(hand[24], "L_thumbs_04_JE")

            om.MGlobal.displayInfo("Your hand rig was created sucesfully!")

            #RIGHT ARM:
            if mc.radioButton("rhand", query=True, select=True):

                def Rhand():
                    rpinky = rhand[1:5]
                    rring = rhand[6:10]
                    rmiddle = rhand[11:15]
                    rindex = rhand[16:20]
                    rthumbs = rhand[21:24]

                    # Make controlers for the joints.
                    for j in rhand:
                        mc.setAttr("{}.segmentScaleCompensate".format(j), 0)

                    previous_sel = None
                    for j in rpinky:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rring:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rmiddle:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rindex:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rthumbs:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls

                    # Group all together
                    fingrp = mc.group(n="R_fingers_GRP", empty=True)
                    temp_constraint = mc.pointConstraint(rhand[0], fingrp)
                    mc.delete(temp_constraint)
                    mc.parent("grpR_pinky01_ZERO", "grpR_ring01_ZERO", "grpR_middle01_ZERO",
                              "grpR_index01_ZERO", "grpR_thumbs01_ZERO", "R_fingers_GRP")

                    mc.rename(rhand[0], "R_palm_JJ")
                    mc.rename(rhand[1], "R_pinky_01_JJ")
                    mc.rename(rhand[2], "R_pinky_02_JJ")
                    mc.rename(rhand[3], "R_pinky_03_JJ")
                    mc.rename(rhand[4], "R_pinky_04_JJ")
                    mc.rename(rhand[5], "R_pinky_05_JE")
                    mc.rename(rhand[6], "R_ring_01_JJ")
                    mc.rename(rhand[7], "R_ring_02_JJ")
                    mc.rename(rhand[8], "R_ring_03_JJ")
                    mc.rename(rhand[9], "R_ring_04_JJ")
                    mc.rename(rhand[10], "R_ring_05_JE")
                    mc.rename(rhand[11], "R_middle_01_JJ")
                    mc.rename(rhand[12], "R_middle_02_JJ")
                    mc.rename(rhand[13], "R_middle_03_JJ")
                    mc.rename(rhand[14], "R_middle_04_JJ")
                    mc.rename(rhand[15], "R_middle_05_JE")
                    mc.rename(rhand[16], "R_index_01_JJ")
                    mc.rename(rhand[17], "R_index_02_JJ")
                    mc.rename(rhand[18], "R_index_03_JJ")
                    mc.rename(rhand[19], "R_index_04_JJ")
                    mc.rename(rhand[20], "R_index_05_JE")
                    mc.rename(rhand[21], "R_thumbs_01_JJ")
                    mc.rename(rhand[22], "R_thumbs_02_JJ")
                    mc.rename(rhand[23], "R_thumbs_03_JJ")
                    mc.rename(rhand[24], "R_thumbs_04_JE")

                Rhand()

    elif mc.radioButton("fourFingers", query=True, select=True):
        if len(sel) < 20:
            om.MGlobal.displayError("Please select the entire hand hierarchy!")

        else:
            hand = mc.ls(sl=True)
            pinky = hand[1:5]
            middle = hand[6:10]
            index = hand[11:15]
            thumbs = hand[16:20]

            # (THIS IS FOR THE RIGHT ARM)
            if mc.radioButton("rhand", query=True, select=True):
                mc.select(hand[0])
                mc.mirrorJoint(mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
                mc.select(hierarchy=True)
                rhand = mc.ls(sl=True)
            # (END OF THE RIGHT ARM)

            # Make controllers for the joints.
            for j in hand:
                mc.setAttr("{}.segmentScaleCompensate".format(j), 0)
            previous_sel = None
            for j in pinky:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls

            previous_sel = None
            for j in middle:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in index:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls
            previous_sel = None
            for j in thumbs:
                ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                mc.makeIdentity(apply=True)
                offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                # Define the color for the controller
                mc.setAttr(offset + ".overrideEnabled", 1)
                mc.setAttr(offset + ".overrideColor", 6)
                # Copy the position and orientation of the joints to the controllers
                temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                mc.delete(temp_constraint)
                # ZeroOut
                temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                mc.delete(temp_constraint)
                mc.parent(ctrls, offset)
                mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                # Make an orient constraint from the controllers to the joints to drive them.
                mc.orientConstraint(ctrls, j)
                mc.scaleConstraint(ctrls, j)

                # If there is more than one control, parent them in FK hierarchy:
                if previous_sel:
                    mc.parent(offset, previous_sel)
                previous_sel = ctrls

            # Group all together
            fingrp = mc.group(n="L_fingers_GRP", empty=True)
            temp_constraint = mc.pointConstraint(hand[0], fingrp)
            mc.delete(temp_constraint)
            mc.parent("grpL_pinky01_ZERO", "grpL_middle01_ZERO",
                      "grpL_index01_ZERO", "grpL_thumbs01_ZERO", "L_fingers_GRP")

            # Rename joints for left hand:
            mc.rename(hand[0], "L_palm_JJ")
            mc.rename(hand[1], "L_pinky_01_JJ")
            mc.rename(hand[2], "L_pinky_02_JJ")
            mc.rename(hand[3], "L_pinky_03_JJ")
            mc.rename(hand[4], "L_pinky_04_JJ")
            mc.rename(hand[5], "L_pinky_05_JE")
            mc.rename(hand[6], "L_middle_01_JJ")
            mc.rename(hand[7], "L_middle_02_JJ")
            mc.rename(hand[8], "L_middle_03_JJ")
            mc.rename(hand[9], "L_middle_04_JJ")
            mc.rename(hand[10], "L_middle_05_JE")
            mc.rename(hand[11], "L_index_01_JJ")
            mc.rename(hand[12], "L_index_02_JJ")
            mc.rename(hand[13], "L_index_03_JJ")
            mc.rename(hand[14], "L_index_04_JJ")
            mc.rename(hand[15], "L_index_05_JE")
            mc.rename(hand[16], "L_thumbs_01_JJ")
            mc.rename(hand[17], "L_thumbs_02_JJ")
            mc.rename(hand[18], "L_thumbs_03_JJ")
            mc.rename(hand[19], "L_thumbs_04_JE")
            #

            om.MGlobal.displayInfo("Your hand rig was created sucesfully!")

            if mc.radioButton("rhand", query=True, select=True):

                def Rhand():
                    rpinky = rhand[1:5]
                    rmiddle = rhand[6:10]
                    rindex = rhand[11:15]
                    rthumbs = rhand[16:20]

                    # Make controlers for the joints.
                    for j in rhand:
                        mc.setAttr("{}.segmentScaleCompensate".format(j), 0)

                    previous_sel = None
                    for j in rpinky:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls

                    previous_sel = None
                    for j in rmiddle:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rindex:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls
                    previous_sel = None
                    for j in rthumbs:
                        ctrls = mc.circle(nr=(1, 0, 0), n=(str(j) + "_CC"), r=0.6, constructionHistory=False)
                        mc.makeIdentity(apply=True)
                        offset = mc.group(n=str("grp" + j + "_ZERO"), empty=True)
                        # Define the color for the controller
                        mc.setAttr(offset + ".overrideEnabled", 1)
                        mc.setAttr(offset + ".overrideColor", 13)
                        # Copy the position and orientation of the joints to the controllers
                        temp_constraint = mc.parentConstraint(j, ctrls, maintainOffset=0)
                        mc.delete(temp_constraint)
                        # ZeroOut
                        temp_constraint = mc.parentConstraint(j, offset, maintainOffset=0)
                        mc.delete(temp_constraint)
                        mc.parent(ctrls, offset)
                        mc.setAttr("{}.translate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.rotate".format(ctrls[0]), 0, 0, 0)
                        mc.setAttr("{}.tx".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.ty".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.tz".format(ctrls[0]), lock=True, keyable=False, channelBox=False)
                        mc.setAttr("{}.v".format(ctrls[0]), lock=True, keyable=False, channelBox=False)

                        # Make an orient constraint from the controllers to the joints to drive them.
                        mc.orientConstraint(ctrls, j)
                        mc.scaleConstraint(ctrls, j)

                        # If there is more than one control, parent them in FK hierarchy:
                        if previous_sel:
                            mc.parent(offset, previous_sel)
                        previous_sel = ctrls

                    # Group all together
                    fingrp = mc.group(n="R_fingers_GRP", empty=True)
                    temp_constraint = mc.pointConstraint(rhand[0], fingrp)
                    mc.delete(temp_constraint)
                    mc.parent("grpR_pinky01_ZERO", "grpR_middle01_ZERO",
                              "grpR_index01_ZERO", "grpR_thumbs01_ZERO", "R_fingers_GRP")

                    mc.rename(rhand[0], "R_palm_JJ")
                    mc.rename(rhand[1], "R_pinky_01_JJ")
                    mc.rename(rhand[2], "R_pinky_02_JJ")
                    mc.rename(rhand[3], "R_pinky_03_JJ")
                    mc.rename(rhand[4], "R_pinky_04_JJ")
                    mc.rename(rhand[5], "R_pinky_05_JE")
                    mc.rename(rhand[6], "R_middle_01_JJ")
                    mc.rename(rhand[7], "R_middle_02_JJ")
                    mc.rename(rhand[8], "R_middle_03_JJ")
                    mc.rename(rhand[9], "R_middle_04_JJ")
                    mc.rename(rhand[10], "R_middle_05_JE")
                    mc.rename(rhand[11], "R_index_01_JJ")
                    mc.rename(rhand[12], "R_index_02_JJ")
                    mc.rename(rhand[13], "R_index_03_JJ")
                    mc.rename(rhand[14], "R_index_04_JJ")
                    mc.rename(rhand[15], "R_index_05_JE")
                    mc.rename(rhand[16], "R_thumbs_01_JJ")
                    mc.rename(rhand[17], "R_thumbs_02_JJ")
                    mc.rename(rhand[18], "R_thumbs_03_JJ")
                    mc.rename(rhand[19], "R_thumbs_04_JE")

                Rhand()

    else:
        om.MGlobal.displayError("Choose between the 2 hand options and select the joint hierarchy!")
