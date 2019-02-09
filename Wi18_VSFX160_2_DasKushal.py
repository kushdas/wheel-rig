#Kush Das
#Project 2
#VSFX 160

import maya.cmds as cmds

def overrideColorGreen(obj):
    cmds.setAttr(obj+".overrideEnabled",1)
    cmds.setAttr(obj+".overrideColor",14)
    
#prefix for the rig
pfx = "rig1_"

#make sure that the model is already a group with a radius of about 1
#select the model
selection = cmds.ls(sl=1)
print selection[0]
wheel_model=selection[0]

exists=cmds.objExists(pfx + "*")
print(exists)
if exists==1:
    cmds.delete(pfx + "*")
    cmds.showHidden(wheel_model)

cmds.showHidden( all=True )
#duplicate the original pieces of the model
cmds.duplicate('wheel_model',n=pfx + "wheel_model")

#hide the original pieces of the model
cmds.hide("wheel_model")

#group the wheel name "wheel_rotate_grp"
cmds.group(pfx+'wheel_model', n= pfx + "wheel_rotate_grp")

#center pivot
cmds.select(pfx+"wheel_rotate_grp")
cmds.xform(cpc=True)
cmds.select(pfx+"wheel_rotate_grp")

#create a nurbs circle named "wheel_move_ctrl"
minZ=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMinZ")
maxY=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMaxY")
minY=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMinY")
centX=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxCenterX")
centY=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxCenterY")
centZ=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxCenterZ")

cmds.circle(n= pfx + "wheel_move_ctrl", nr=(0,1,0))
cmds.move(centX,minY,centX)
cmds.select(pfx + "wheel_move_ctrl.cv[1]")
cmds.move(0, 0, 0.88, relative=True)
cmds.select(pfx + "wheel_move_ctrl.cv[1]", "rig1_wheel_move_ctrl.cv[2]", "rig1_wheel_move_ctrl.cv[0]")
cmds.move(0, 0, -0.38, relative=True)
cmds.select(pfx + "wheel_move_ctrl.cv[5]")
cmds.move(0, 0, 0.65, relative=True)
cmds.select(pfx + "wheel_move_ctrl.cv[6]")
cmds.move(-0.37, 0, 0, relative=True)
cmds.select(pfx + "wheel_move_ctrl.cv[4]")
cmds.move(0.37, 0, 0, relative=True)

overrideColorGreen(pfx+"wheel_move_ctrl")

#create locator in center of wheel named "wheel_move_loc"
cmds.spaceLocator(n= pfx + "wheel_move_loc")
cmds.select(pfx + "wheel_move_loc")
cmds.move(centX,centY,centZ)

#parent locator to nurbs circle wheel_move_ctrl
cmds.parent (pfx + 'wheel_move_loc', pfx + 'wheel_move_ctrl')

#apply point constrain and scale constrain to wheel_move_loc and wheel_rotate_grp
cmds.pointConstraint (pfx + 'wheel_move_loc', pfx + 'wheel_rotate_grp')
cmds.scaleConstraint (pfx + 'wheel_move_loc', pfx + 'wheel_rotate_grp')

#wheel_rotate_grp add attribute 
#long name: offset 
#data type: float
cmds.select(pfx + 'wheel_rotate_grp')
cmds.addAttr(longName='offset', attributeType="float", defaultValue=0, keyable=True)

#wheel_move_ctrl add attribute
#long name: auto
#data type: boolean
cmds.select(pfx + 'wheel_move_ctrl')
cmds.addAttr(longName='auto', attributeType="bool", keyable=True)

#measure tool distance snapped to border of the wheel
#rename distance node wheel_size
#parent the two locators of distance node to the wheel
maxX=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMaxX")
minX=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMinX")
maxZ=cmds.getAttr(pfx+"wheel_rotate_grp.boundingBoxMaxZ")


print maxX-minX

if ((maxX-minX)==(maxY-minY)):
    cmds.distanceDimension( sp=(maxX, centY, centZ), ep=(minX, centY, centZ))
else:
    cmds.distanceDimension( sp=(centX, centY, maxZ), ep=(centX, centY, minZ))

cmds.rename("distanceDimension1", pfx+"wheel_size")
cmds.parent ("locator1", pfx + 'wheel_model')
cmds.parent ("locator2", pfx + 'wheel_model')

#apply expression to wheel_rotate_grp.rotateX

cmds.expression (s = "if (rig1_wheel_move_ctrl.auto == 1 )\n{ \n$diff = rig1_wheel_rotate_grp.translateZ - rig1_wheel_rotate_grp.offset ;\nrig1_wheel_rotate_grp.rotateX -= $diff * -360 / (rig1_wheel_sizeShape.distance*3.14) ;\n};\nrig1_wheel_rotate_grp.offset = rig1_wheel_rotate_grp.translateZ ;",  o="rig1_wheel_rotate_grp", ae=1, uc='all' )

#activate Auto for wheel_move_ctrl
cmds.setAttr(pfx+"wheel_move_ctrl.auto", 1)

#group wheel_rotate_grp again and name it wheel_orient
cmds.group(pfx + "wheel_rotate_grp", n= pfx + "wheel_orient")
#apply orient constrain to wheel_rotate_grp and wheel_move_ctrl
cmds.orientConstraint (pfx + 'wheel_move_ctrl', pfx + 'wheel_orient')


cmds.select(pfx + "wheel_move_ctrl")
