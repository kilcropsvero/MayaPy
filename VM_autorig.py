import maya.cmds as mc
import maya.OpenMaya as om

WIN = "autowin"

def UI():
    if (mc.window(WIN, exists=True)):
        mc.deleteUI(WIN)

    mc.window(WIN, title="VM_AutoRig v0.1", w=300, h=200, sizeable=True)
    #
    mc.columnLayout(adj=True)
    mc.text(label="This is a modular rig, just click on the button you need!", h=20)
    mc.separator()
    mc.symbolButton(image="VM_autorig/VM_autorig-09.png", h=32, c=proxy)
    mc.separator()

    mc.rowColumnLayout(adj=True, numberOfColumns=4, columnWidth=(1,100),
                       cs=[(2,3),(3,3),(4,3)], rs=[(2,3),(3,3),(4,3)] )
    mc.symbolButton(image="VM_autorig/VM_autorig-01.png", w=100, h=100, c=button_01)
    mc.symbolButton(image="VM_autorig/VM_autorig-02.png", w=100, h=100, c=button_02)
    mc.symbolButton(image="VM_autorig/VM_autorig-03.png", w=100, h=100, c=button_03)
    mc.symbolButton(image="VM_autorig/VM_autorig-04.png", w=100, h=100, c=button_04)
    mc.symbolButton(image="VM_autorig/VM_autorig-05.png", w=100, h=100, c=button_05)
    mc.symbolButton(image="VM_autorig/VM_autorig-06.png", w=100, h=100, c=button_06)
    mc.symbolButton(image="VM_autorig/VM_autorig-07.png", w=100, h=100, c=button_07)
    mc.symbolButton(image="VM_autorig/VM_autorig-08.png", w=100, h=100, c=button_08)
    mc.setParent('..')
    mc.separator()
    mc.symbolButton(image="VM_autorig/VM_autorig-10.png", h=32, c=cleanRig)
    mc.showWindow(WIN)

def proxy(*args):
    import veroPythonScripts.mayalib.VM_proxyAutoRig as vmproxy
    reload(vmproxy)
    vmproxy.body()
    om.MGlobal.displayInfo("Proxy skeleton created sucesfully")

def button_01(*args):
    import veroPythonScripts.mayalib.VM_legRig as vmleg
    reload(vmleg)
    vmleg.UI()

def button_02(*args):
    import veroPythonScripts.mayalib.VM_armRig as vmarm
    reload(vmarm)
    vmarm.UI()

def button_03(*args):
    import veroPythonScripts.mayalib.VM_hand as vmhand
    reload(vmhand)
    vmhand.UI()

def button_04(*args):
    import veroPythonScripts.mayalib.VM_SquashStretchSpline2 as sss
    reload(sss)
    sss.UI()

def button_05(*args):
    import veroPythonScripts.mayalib.VM_neck as vmneck
    reload(vmneck)
    vmneck.neck()

def button_06(*args):
    import veroPythonScripts.mayalib.VM_head as vmhead
    reload(vmhead)
    vmhead.UI()

def button_07(*args):
    import veroPythonScripts.mayalib.VM_FkGenerator as vmfk
    reload(vmfk)
    vmfk.UI()

def button_08(*args):
    import veroPythonScripts.mayalib.VM_motionRibbon as mr
    reload(mr)

def cleanRig(*args):
    import veroPythonScripts.mayalib.VM_finishAutoRig as vmfinish
    reload(vmfinish)
    vmfinish.finish()
