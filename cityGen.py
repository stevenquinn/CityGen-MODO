#python

import lx


# Simplify creating a cube
class Cube:
	
	def __init__(self, posX, posY, posZ, sizeX, sizeY, sizeZ, name, subdX = 1, subdY = 1, subdZ = 1):
		self.posX = posX
		self.posY = posY
		self.posZ = posZ
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.sizeZ = sizeZ
		self.name = name
		self.subdX = subdX;
		self.subdY = subdY;
		self.subdZ = subdZ;
		self.create()
		
	def create(self):
		#create a standard cube
		lx.eval('layer.new')
		lx.eval('tool.set prim.cube on')
		lx.eval('tool.setAttr prim.cube cenX %f' % self.posX)
		lx.eval('tool.setAttr prim.cube cenY %f' % self.posY)
		lx.eval('tool.setAttr prim.cube cenZ %f' % self.posZ)
		lx.eval('tool.setAttr prim.cube sizeX %f' % self.sizeX)
		lx.eval('tool.setAttr prim.cube sizeY %f' % self.sizeY)
		lx.eval('tool.setAttr prim.cube sizeZ %f' % self.sizeZ)
		lx.eval('tool.setAttr prim.cube segmentsX %f' % self.subdX)
		lx.eval('tool.setAttr prim.cube segmentsY %f' % self.subdY)
		lx.eval('tool.setAttr prim.cube segmentsZ %f' % self.subdZ)
		lx.eval('tool.setAttr prim.cube axis 1')
		lx.eval('tool.apply')
		lx.eval('select.type vertex')
		lx.eval('item.name {%s} mesh' % (self.name))
		
		
		

class CityGen:
		def __init__(self, sizeX, sizeZ, blockSize, streetSize):
				self.sizeX = sizeX
				self.sizeZ = sizeZ
				self.buildingSize = 12
				self.points = 0
				self.blockSize = blockSize
				self.streetSize = streetSize
				self.create()
		
		def create(self):
				# Get the currently selected items
				selected_items = lx.eval('item.name ?')

				# Group them in the item list and clear the selection
				lx.eval('layer.groupSelected')
				
				# Select the individual meshes again
				i = 0
				for item in selected_items:
					if (i == 0):
						lx.eval('select.Item {%s} set' % item)
					else:
						lx.eval('select.Item {%s} add' % item)
					i += 1

				# Create a group 
				lx.eval('group.create Buildings std selItems')
				group_name = lx.eval('item.name ?')
				group_id = lx.eval('query sceneservice item.id ? {%s}' % group_name)
				
				# Create the ground points
				ground_id = self.createGroundPoints()
				
				# Create replicator
				lx.eval('item.create replicator')
				
				# Set the source for the replicator to the buildings group
				lx.eval('replicator.source {%s}' % group_id)
				lx.eval('replicator.particle {%s}' % ground_id)
				lx.eval('item.channel replicator$source particle')
				lx.eval('item.channel replicator$snapRot true')
				lx.eval('item.channel replicator$sclUniform false')
				lx.eval('item.channel sclRand.Y 0.4')
				
		def createGroundPoints(self):
			currentX = 0.0
			currentZ = 0.0
			blockX = 0.0
			blockZ = 0.0
			
			# Create the mesh
			lx.eval('item.create mesh')
			lx.eval('item.name Ground')
			lx.eval('select.Item Ground set')
			ground_id = lx.eval('query sceneservice item.id ? Ground')
			lx.out(ground_id)
			lx.eval('tool.set prim.pen on 0')
			lx.eval('tool.attr prim.pen type vertices')
			
			# Fill by columns then rows
			while (currentX < self.sizeX):
				currentZ = 0.0
				blockZ = 0.0
				
				while (currentZ < self.sizeZ):
					self.createPoint(currentX, currentZ)
					
					if (blockZ > self.blockSize):
						blockZ = 0.0
						currentZ += self.buildingSize + self.streetSize
					else:
						currentZ += self.buildingSize
						blockZ += self.buildingSize
				
				
				if (blockX > self.blockSize):
					blockX = 0.0
					currentX += self.buildingSize + self.streetSize
				else:
					blockX += self.buildingSize
					currentX += self.buildingSize
				
			return ground_id
			
		def createPoint(self, x, z):
			lx.eval('tool.setAttr prim.pen current 0')
			lx.eval('tool.setAttr prim.pen posX %f' % x)
			lx.eval('tool.setAttr prim.pen posY 0.0')
			lx.eval('tool.setAttr prim.pen posZ %f' % z)
			lx.eval('tool.attr prim.pen merge false')
			lx.eval('tool.doApply')
			self.points += 1
			
				

				
					
city = CityGen(500, 500, 60, 10)
