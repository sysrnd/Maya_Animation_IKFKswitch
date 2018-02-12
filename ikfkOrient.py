class FKIKorient(object):
	def __init__(self):
		self.sides = ['IZQ', 'DER']

		self.fkjnt = ['HOMBRO_IZQ_FK', 'CODO_IZQ_FK', 'MANO_IZQ_FK']
		self.ikjnt = ['HOMBRO_IZQ_IK', 'CODO_IZQ_IK', 'MANO_IZQ_IK']

		self.fkctrl = ['DRIVER_HOMBRO_IZQ_FK', 'DRIVER_CODO_IZQ_FK', 'DRIVER_MANO_IZQ_FK']
		self.ikctrl = ['DRIVER_CODO_IZQ', 'DRIVER_MANO_IZQ']

		self.chunk = cmds.undoInfo(ock=True)

	def mainFK(self):
		for side in range(0, len(self.sides)):

			tempGrps = []
			grps = []
			transforms = []

			for index in range(0, len(self.fkctrl)):
				fkctrl = self.changeSide(self.fkctrl[index], self.sides[side], self.sides[side-1])
				self.deleteIncomingCons(fkctrl, 'orientConstraint')
				tempGrp = self.shapeToDummy(fkctrl)
				grp = self.group(fkctrl)
				
				tempGrps.append(tempGrp)
				grps.append(grp)

			for index in range(0, len(self.fkctrl)):
				fkjnt = self.changeSide(self.fkjnt[index], self.sides[side], self.sides[side-1])
				fkctrl = self.changeSide(self.fkctrl[index], self.sides[side], self.sides[side-1])
				orCons = self.orientCons(fkjnt, grps[index])
				cmds.delete(orCons)
				self.shapeToCtrl(fkctrl, tempGrps[index])

			
			for index in range(0, len(self.fkctrl)):
				fkjnt = self.changeSide(self.fkjnt[index], self.sides[side], self.sides[side-1])
				fkctrl = self.changeSide(self.fkctrl[index], self.sides[side], self.sides[side-1])

				self.centerPivot(grps[index], self.fkjnt[index])
				self.centerPivot(fkctrl, fkjnt)
				self.orientCons(fkctrl, fkjnt)

		cmds.undoInfo(cck=True)

	
	def mainIK(self):
		pass

	def changeSide(self, obj, src, dest):
		newStr = obj.replace(src, dest)
		return newStr

	def shapeToDummy(self, ctrl):
		#cmds.select(cl=True)
		tempGrp = cmds.group(em=True, n=ctrl + '_tempGRP')

		shapes = cmds.listRelatives(ctrl, s=True)
		for shape in shapes:
			cmds.parent(shape, tempGrp, r=True, s=True)
		return tempGrp

	def shapeToCtrl(self, ctrl, grp):
		shapes = cmds.listRelatives(grp, s=True)

		for shape in shapes:
			newShape = cmds.parent(shape, ctrl, s=True, r=False)[0]
			parentShape = cmds.listRelatives(newShape, p=True)[0]
			cmds.makeIdentity(parentShape, apply=True, t=1, r=1, s=0, n=0)
			newShape = cmds.parent(newShape, ctrl, s=True, r=True)
			cmds.delete(parentShape)
		cmds.delete(grp)

	def deleteIncomingCons(self, ctrl, typeConn):
		cons = cmds.listConnections(ctrl, t=typeConn)[0]
		cmds.delete(cons)

	def orientCons(self, source, dest):
		orientCons_ = cmds.orientConstraint(source, dest, mo=False)
		return orientCons_

	def centerPivot(self, obj, pivot):
		pos = cmds.xform(pivot, q=True, ws=True, piv=True)
		cmds.xform(obj, ws=True, piv=(pos[0], pos[1], pos[2]))

	def group(self, obj):
		grp_ = cmds.group(obj, n=obj + '_orientGRP')
		return grp_

	def orientCons(self, par, child):
		cons = cmds.orientConstraint(par, child, mo=False)
		return cons



fkik = FKIKorient()
fkik.mainFK()
