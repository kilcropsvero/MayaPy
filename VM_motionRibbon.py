#Select a curve to create 5 motion ribbons.

import maya.cmds as mc
import maya.OpenMaya as om

cv = mc.ls(sl=True)
mc.select(cl=True)

if len(cv) == 0:
    om.MGlobal.displayError("Please select a curve!")

else:
    cvShape = mc.listRelatives(cv, shapes=True)[0]  # that [0] query the elements, without the Unicode.  
    numberOfLocs = 5

    for i in range(numberOfLocs):
        mPath = mc.createNode("motionPath", n="moPathRibbon_0" + str(i + 1))
        mc.setAttr("{}.fractionMode".format(mPath), 1)
        #
        loc = mc.spaceLocator(n="offsetLoc_0" + str(i + 1))[0]
        pass
        jnt = mc.joint()
        mc.group(jnt)
        cc = mc.circle()
        ccShape = mc.listRelatives(cc, shapes=True)
        mc.parent(ccShape, jnt, relative=True, shape=True)
        mc.delete(cc)
        #
        mc.connectAttr(("{}.worldSpace[0]".format(cvShape)), ("{}.geometryPath".format(mPath)))
        mc.connectAttr(("{}.allCoordinates".format(mPath)), ("{}.translate".format(loc)))
        # mc.

    paths = mc.listConnections(cvShape, type='motionPath')
    mc.setAttr(paths[1] + ".uValue", 0)  # I don't get why py is reading this values inversed paths[0,1]
    mc.setAttr(paths[0] + ".uValue", 0.25)
    mc.setAttr(paths[2] + ".uValue", 0.50)
    mc.setAttr(paths[3] + ".uValue", 0.75)
    mc.setAttr(paths[4] + ".uValue", 1)
