AXIS = ['X', 'Y', 'Z']

fkjnt = ['HOMBRO_IZQ_FK', 'CODO_IZQ_FK', 'MANO_IZQ_FK']
ikjnt = ['HOMBRO_IZQ_IK', 'CODO_IZQ_IK', 'MANO_IZQ_IK']

fkctrl = ['DRIVER_HOMBRO_IZQ_FK', 'DRIVER_CODO_IZQ_FK', 'DRIVER_MANO_IZQ_FK']
ikctrl = ['DRIVER_CODO_IZQ', 'DRIVER_MANO_IZQ']

switch = cmds.getAttr('DRIVER_COLUMNA_TOP.SWITCH_IK_FK_IZQ')

def pos(obj):
	pos_ = cmds.xform(obj, q=True, t=True, ws=True)
	return round(pos, 2)
def rot(obj):
	rot_ = cmds.xform(obj, q=True, ro=True, ws=True)
	#rot_ = [round(x, 2) for x in rot_]
	return rot_

def addOffsetAttr():
	bindPose(ikctrl, '.translate')
	bindPose(ikctrl, '.rotate')
	bindPose(fkctrl, '.rotate')

def mainSwitch():
	if switch == 0:
		print 'FK',
		for x in xrange(0, 3):
			pass
			#pos_ = pos(fkjnt[x])
			#rot_ = rot(fkjnt[x])

		cmds.setAttr('DRIVER_COLUMNA_TOP.SWITCH_IK_FK_IZQ', 1)

	else:
		print 'IK',
		cmds.setAttr('DRIVER_COLUMNA_TOP.SWITCH_IK_FK_IZQ', 0)

		for x in xrange(0, 3):
			rot_ = rot(ikjnt[x])
			print rot_
			cmds.xform(fkctrl[x], ws=True, ro=(rot_[0], rot_[1], rot_[2]))


mainSwitch()