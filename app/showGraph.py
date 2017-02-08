

import math 
import random 
#This is an (I)LP solver that is used to generate coordinates for the problem map 
#Objective Function: max((x_uf-x_ui)*(y_uf-y_ui)); s.t. x_0<=x<=x_f, y_0<=y<=y_f  
#	-maximize the area used for display such that it fits in the delagated box (using heuristic)
#Delegated box: 
# 	-given by x_o, x_f, y_o, y_f 
#	-values determined in js by x_o, y_o and x_size, y_size
#	-center of box will be the center of the circle for the heuristic
#
#Given: 
#	-box dimensions
#	-V,E
#	-V is a list of Vertex objects
#		-Vertex objects have a name, object type, list of associated predicates, and dictionary 
#			of associated numerics
#	-E is a list of Edge objects 
#		-Edge objects have a start, end, metric, and numeric
#		-Edges without giver numerics will be assigned the numeric f 
#	####these will be given in the form of problemObjects, problemInitialNumerics, problemInitialStates
#   ####we will convert to E, V unpon initialization
#	-f: the fixed amount objects with predicates given by init states are set apart from each other
#		-all related objects will be shown some factor i of f apart if there are no numerics
#
#Constraints:
#	- x_0<=x<=x_f, y_0<=y<=y_f 
#	- (x_b-x_a)^2 + (y_b-y_a)^2 <= (ni)^2
#		- where n is the numeric assigned to the objects at x_a, y_a; x_b, y_b
#
#Properties:
#	- heuristic used to maximize space: circular arrangement 
#	- we take the type of object that is most commonly linked as the child to other objects
#	- 

class ShowGraph():
	def __init__(self, x_0, y_0, x_f, y_f, initObjects, initNumerics, initStates, f):
		self.x_0 = x_0
		self.y_0 = y_0
		self.x_f = x_f
		self.y_f = y_f 
		self.f = f  #relation object distance
		self.initObjects = initObjects
		self.initNumerics = initNumerics
		self.initStates = initStates
		self.finalMap = {} #this is initializing the map that will map objects to their final destinations

		
		self.centerX = (x_0 + x_f)/2 #floor of actual value for integer pixel count
		self.centerY = (y_0 + y_f)/2 
		self.radius = min(float(x_f-x_0)/3, float(y_f-y_0)/3)

		self.vertices, self.namesToVerticesMap = self.makeVertices() 
		self.edges, self.namesToEdgesMap = self.makeEdges() 

		self.arrowOut = self.arrowOut()
		self.arrowIn = self.arrowIn()

		self.edgesByMetric = self.getEdgesByMetric

		


	def makeVertices(self):
		#returns a list of vertex objects, for each object in the problem; and a dictionary 
		#	mapping object names to vertices
		#intermediate step for fast access: object name: Vertex; add all vertices from this
		#dictionary at the end
		
		vertices = []
		nameToVertex = {}
		for t in self.initObjects:
			for obj in self.initObjects[t]:
				nameToVertex[obj] = Vertex(obj, t)
		for metric in self.initNumerics:
			for e in self.initNumerics[metric]:
				if len(e.split(","))==1:
					#if the edge is split into one piece, the numeric pertains to 1 obj only
					nameToVertex[e].addNumeric(metric, self.initNumerics[metric][e])
					#add numeric with key metric and value, value of key and e 
		for quality in self.initStates:
			#self.initStates is a list of dictionaries, quality is a dictionary
			for action in quality:
				#effected is the key that states the action
				if len(quality[action])==1:
					#if only 1 object is effected
					obj = quality[action][0]
					nameToVertex[obj].addQuality(action)
		for vertex in nameToVertex:
			vertices.append(nameToVertex[vertex])
		return vertices, nameToVertex
			


	def makeEdges(self):
		#returns a list of edge objects; regards the numeric distance rather than relation distance
		#returns a dictionary of edge names to list of edges with that name (edgeName defined by vertex names)

		#we first iterate through the set of numerics, then the set of states for relations
		#without numeric values; this minimizes backtracking and preserves edge invariants

		edgeList = []
		namesToEdges = {}
		for metric in self.initNumerics:
			for edge in self.initNumerics[metric]:
				vertexNames = edge.split(",")
				if len(vertexNames)<2:
					#if the numeric effects only 1 object
					continue 
					#move on to the next iteration of the loop

				if edge not in namesToEdges:
					namesToEdges[edge] = []
				vertexA = self.namesToVerticesMap[vertexNames[0]]
				vertexB = self.namesToVerticesMap[vertexNames[1]]
				numeric = self.initNumerics[metric][edge]
				
				backName = ",".join((vertexNames[1], vertexNames[0]))
				foundSymmetricBackEdge = False
				if backName in namesToEdges:
					#if a back edge exists in the list of edges
					backEdge = Edge(vertexB, vertexA, metric, numeric)
					for ii in range(len(namesToEdges[backName])):
						if namesToEdges[backName][ii]==backEdge:
							namesToEdges[backName][ii].setDoubleTrue()
							foundSymmetricBackEdge = True
							break
				if not foundSymmetricBackEdge:
					newEdge = Edge(vertexA, vertexB, metric, numeric)	

		for state in self.initStates:
			#state is a dictionary
			for action in state:
				if len(state[action])<2:
					continue #so we don't try to add edges from init qualities of single objects
				edgeName = ",".join(state[action])
				#add edge if it does not already exist
				#we do not add backedges because these are non-numeric connections
				if (edgeName not in namesToEdges) or self.edgesAllPredicates(namesToEdges[edgeName]):
					namesToEdges[edgeName] = []
					#only add predicates that do not already have numeric (not found in namesToEdges)
					startingVertex = self.namesToVerticesMap[state[action][0]]
					endingVertex = self.namesToVerticesMap[state[action][1]]
					initEdge = Edge(startingVertex, endingVertex, action, self.f)
					namesToEdges[edgeName].append(initEdge)


		for edge in namesToEdges:
			edgeList.extend(namesToEdges[edge])
		return edgeList, namesToEdges




	def mostConnectedComponentMetric(self):
		#returns the metric that creates the largest connected component, and the root of
		#	the most connected component (name) or the predicate with the most end:start ratio and 
		#	an object of that type
		mostConnectedComponents = 0
		MCCRoot = ""
		mostConnectedMetric = ""
		if bool(self.initNumerics):
			#if the numerics dictionary is non-empty 
			for metric in self.initNumerics:
				childrenDict = {}
				for edge in self.initNumerics[metric]:
					vertices = edge.split(",")
					if len(vertices) == 2:
						if vertices[0] not in childrenDict:
							childrenDict[vertices[0]] = []
						childrenDict[vertices[0]].append(vertices[1])
				connectedComponents, root = self.getConnectedComponents(childrenDict)
				if mostConnectedComponents<connectedComponents:
					mostConnectedComponents = connectedComponents
					MCCRoot = root
					mostConnectedMetric = metric
					#keeps track of which metric of the vertex creates the most c.c. 
			if mostConnectedComponents > 2:
				return mostConnectedMetric, MCCRoot
		else:

			mostEnds = self.mostEndsType()
			return mostEnds, self.initObjects[mostEnds][0] #keeps return type the same






	def getConnectedComponents(self, childrenDict):
		#takes in a dictionary of nodes and their children (as a graph), and returns the size of the 
		#	largest connected component in the graph, and the root that is part of that c.c.

		largestConnection = 0
		largestRoot = ""
		extended = []
		while bool(childrenDict):
			#while childrenDict is non-empty, we repeat the procedure
			r = random.randint(0, len(childrenDict.keys()))
			root = list(childrenDict.keys())[r]
			queue = [root]
			connection = 0
			while bool(queue):
				#while queue is non-empty 
				extended.append(queue[0])
				thisNode = queue.pop(0)
				if thisNode in childrenDict:
					queue.extend(childrenDict[thisNode]) #add all children of thisNode to queue
					childrenDict.pop(thisNode, None) #remove this node from the dict once it 
					#has been visited 
				connection+=1
			if connection > largestConnection:
				largestConnection = connection
				largestRoot = root
		return largestConnection, largestRoot





	def edgesAllPredicates(self, edgeList):
		#takes in a list of edges and returns true iff all edges are predicates
		for edge in edgeList:
			if not edge.isPredicate(): 
				return False
		return True



	def isIndependent(self, objA, objB):
		#objA is the dependent object
		#objB is the end object 
		#returns: true iff objA is only dependent on objB; else false
		if objB not in self.arrowIn:
			if (len(self.arrowOut[objB])==1 and self.arrowOut[objB][0]==objA):
				return True
		return False 


	def findIndependents(self, objB):
		#objB is an object that may be depended upon by other objects
		#return: list of objects that are solely dependent on objB and no others
		independents = []
		for dep in self.arrowIn[objB]:
			if isIndependent(dep, objB):
				independents.append(dep)
		return independents 


	def mostEndsType(self):
		#return: the type of object that is most often 'objB' by init states, of different types
		mostType = ''
		mostDependents = 0
		typeToEnds = {}
		for objType in self.initObjects:
			typeToEnds[objType] = 0 #initialize each type with end count 0
		for edge in self.edges:

			typeToEnds[edge.vertexB.getObjectType()] +=1 #increment count of end type

			typeToEnds[edge.vertexA.getObjectType()] -= 1 #decrement count of start type 
		for end in typeToEnds:
			#go through the counts and select the largest count
			if typeToEnds[end] > mostDependents:
				mostDependents = typeToEnds[end]
				mostType = end
			
		return mostType



	def arrowOut(self):
		#returns a dictionary: objA-[objB...]
		aToAllB = {}
		for dic in self.initStates:
			for key in dic:
				objects = dic[key]
				if len(objects)<2:
					continue #quality not relation

				objA = objects[0]
				objB = objects[1]
				if objA not in aToAllB:
					aToAllB[objA] = []
				aToAllB[objA] += objB
		for key in self.initNumerics:
			newDict = self.initNumerics[key]
			for edge in newDict:
				objects = edge.split(',')
				if len(objects)<2:
					continue #quality not relation

				objA = objects[0]
				objB = objects[1]
				if objA not in aToAllB:
					aToAllB[objA] = []
				aToAllB[objA] += objB

		return aToAllB 





	def arrowIn(self):
		#returns a dictionary: objB-[objA...]
		bToAllA = {}
		for dic in self.initStates:
			for key in dic:
				objects = dic[key]
				if len(objects)<2:
					continue #quality not relation

				objA = objects[0]
				objB = objects[1]
				if objB not in bToAllA:
					bToAllA[objB] = []
				bToAllA[objB] += objA
		for key in self.initNumerics:
			newDict = self.initNumerics[key]
			for edge in newDict:
				objects = edge.split(',')
				if len(objects)<2:
					continue #quality not relation

				objA = objects[0]
				objB = objects[1]
				if objB not in bToAllA:
					bToAllA[objB] = []
				bToAllA[objB] += objA

		return bToAllA 

	def getEdgesByMetric(self):
		#return dictionary of metric (numeric, predicate) mapped to the edges that it corresponds to
		edgesDict = {}
		for edge in self.edges:
			if edges.getMetric() not in edgesDict:
				edgesDict[edges.getMetric()] = []
			edgesDict[edges.getMetric()].append(edge)
		return edgesDict 

	# def vertexToEdges(self, metric, startVertex):
	# 	#return a dictionary of vertices to outedges of the given metric on the c.c. 
	# 	# 	of the given startVertex 
	# 	relatedEdges = [] #list of edges that are of the specified metric
	# 	extended = [] #list of vertices that have already been extended
	# 	verticesToEdges = {} #dictionary of vertices to outedges 
	# 	for edge in self.edges:
	# 		if edge.getMetric()==metric:
	# 			relatedEdges.append(edge)
	# 	queue = [startVertex]

	# 	#vertexToChildren = self.arrowOut() #map of all vertices to all connections of vertex
	# 	while bool(queue):
	# 		currentName = queue.pop(0)
	# 		extended.append(currentName)
	# 		currentVertex = self.namesToVerticesMap[currentName]
	# 		#currentVertex is type vertex 

	# 		if currentVertex not in verticesToEdges: #create edge list for vertex
	# 			verticesToEdges[currentVertex] = []
	# 		for e in relatedEdges:
	# 			if e.getStartVertex()==currentVertex:
	# 				verticesToEdges[currentVertex].append(e)
	# 				#add e to the list of edges that outgo from currentVertex
	# 				if e.getEndVertex() not in 
	# 			elif e.getEndVertex()==currentVertex and e.isDouble():
	# 				verticesToEdges[currentVertex].append(e)
	# 				#add e to the list of edges that are doublesided and ingo to currrentVertex









	def getVertices(self):
		return self.vertices

	def getNamesToVertices(self):
		return self.namesToVerticesMap

	def getEdges(self):
		return self.edges

	def getNamesToEdges(self):
		return self.namesToEdgesMap

	def setRadius(self, r):
		self.radius = r





class Edge():
	#vertexA is the start vertex of the edge (type vertex, invariant)
 	#vertexB is the end vertex of the edge (type vertex, invariant)
	#metric is the metric by which the relation from A to B are measured (invariant)
	#numeric is the quantity of the metric from A to B
	#predicate is a boolean, true if the edge is due to a predicate, not numeric 
	#	initialized at True, because not given = predicate
	#double is a boolean, true if there exists a directed edge opposite direction of same 
	#	metric and magnitude

	def __init__(self, vertexA, vertexB, metric, numeric, predicate=True, double=False):
		self.vertexA = vertexA 
		self.vertexB = vertexB
		self.metric = metric
		self.numeric = numeric
		self.predicate = predicate
		self.double = double

		
		#calculated after initialization
		self.length = 0
		self.startPoint = ObjPoint(0,0,0,0) 
		self.endPoint = ObjPoint(0,0,0,0)

	def getName(self):
		# returns the name 'objA,objB' of the edge as a string 
		return self.vertexA.getName() + ',' + self.vertexB.getName() 

	def getStartVertex(self):
		return self.vertexA

	def getEndVertex(self):
		return self.vertexB

	def getMetric(self):
		return self.metric

	def getNumeric(self):
		return self.numeric

	def isPredicate(self):
		return self.predicate

	def isDouble(self):
		return self.double

	def setNumeric(self, newNumeric):
		#sets the numeric of the metric (if the edge is a numeric)
		#returns True if the numeric is set, False otherwise
		if not self.predicate:
			self.numeric = newNumeric
			return True
		return False

	def setDoubleTrue(self):
		#sets the double boolean to true (if the edge is a numeric) after symmetric backward edge is found
		#Return false if edge is a predicate 
		if (not self.predicate):
			self.double = True		
			return True
		else:
			return False

	def setDoubleFalse(self):
		#the numeric of the an edge in the symmetric backwards pair has changed in value
		#sets the double boolean to false, and return True
		#return false if self.double is already false (not a double edge), or if edge is a predicate 
		if not self.predicate:
			self.double = False
			return True
		return False

	def setLength(self, length):
		self.length = length
		return True

	def setStartPoint(self, point):
		#param point: objPoint object that will be the start point of the edge
		self.startPoint = point

	def setEndPoint(self, point):
		#param point: objPoint object that will be the end point of the edge
		self.endPoint = point

	def getStartPoint(self):
		return self.startPoint

	def getEndPoint(self):
		return self.endPoint 





class ObjPoint():
	#xLoc = x-location of the point
	#yLoc = y-location of the point
	#centerX = center x-coordinate point of the coordinate system (cartesian)
	#centerY = center y-coordinate point of the coordinate system (cartesian)


	def __init__(self, x_location, y_location, centerX, centerY):
		self.xLoc = x_location
		self.yLoc = y_location
		self.centerX = centerX
		self.centerY = centerY


	def getXLoc(self):
		return self.xLoc

	def getYLoc(self):
		return self.yLoc

	def getCenter(self):
		#return tuple of centerX, centerY
		return self.centerX, self.centerY

	def getDistanceFromCenter(self):
		x_squared = (self.xLoc - self.centerX)**2 
		y_squared = (self.yLoc - self.centerY)**2
		return int((x_squared + y_squared)**0.5)

	def getQuadrant(self):
		#returns the quadrant [1,4] of the point with respect to the center 
		if (self.xLoc < self.centerX):
			if (self.yLoc < self.centerY):
				return 3
			else:
				return 2 
		else: 
			if (self.yLoc < self.centerY):
				return 4
			else:
				return 1

	def getAngleFromCenter(self):
		#returns the angle of the point with respect to the center [0, 2*pi]
		quadrant = self.getQuadrant()
		if quadrant%2==1:
			#if we are in quadrant 1 or 3
			angleToX = math.atan(float(self.yLoc-self.centerY)/(self.xLoc-self.centerX))
			
		else:
			#otherwise we are in quadrant 2 or 4
			angleToX = math.atan(float(self.yLoc-self.centerY)/(self.centerX-self.xLoc))
		
		if angleToX > 2:
			return angleToX + math.pi
		else: 
			return angleToX 




class Vertex():
	#name = name of the object the vertex represents (type str)
	#objectType = type of the object of the vertex
	#qualities = list of predicates that effect the object
	#numerics = dictionary relating metrics to number-value qualities of the object
	#objectPoint = point at which the vertex is located
	#locationSet = true iff the location has been changed, initiated at false 
	#	-when the vertex's point needs to be changed we change this boolean back to false

	def __init__(self, name, objectType):
		self.name = name
		self.qualities =[]
		self.objectType = objectType 
		self.numerics = {}
		self.objectPoint = ObjPoint(0,0,0,0) #we initiate the point of the vertex at (0,0)
		self.locationSet = False



	def addQuality(self, quality):
		#param quality: predicate that effects (and will be added to the qualities of) the vertex
		#returns true if the quality was added the list of qualities that effect the vertex
		#	 false if the quality already existed in the list of qualities
		if quality not in self.qualities:
			self.qualities.append(quality)
			return True
		return False 

	def deleteQuality(self, quality):
		#param quality: predicate that effects (and will be deleted from the qualities of) the vertex
		#returns true if the quality was deleted from the list of qualities
		#	false if the quality did not exist in the list of qualities 
		if (quality in self.qualities):
			self.qualities.remove(quality)
			return True
		return False 


	def addNumeric(self, metric, number):
		#param metric: metric by which the number has meaning (str)
		#param number: number value of the numeric (int)
		#return true if numeric is added/changed
		#return false if there is no change in the existing numeric
		if metric in self.numerics:
			if self.numerics[metric]==number:
				return False
		self.numerics[metric] = number 
		#should encompass rest of logic for which this holds
		return True

	def deleteNumeric(self, metric):
		#param metric: metric of the object 
		#return true: if the numeric is deleted
		#return false: if the numeric did not exist in the number
		if metric in self.numerics:
			self.numerics.pop(metric, None)
			return True
		return False


	def changePoint(self):
		self.locationSet = False


	def setPoint(self, point):
		#param point: ObjPoint object we will set self.objectPoint to 
		#changes self.locationSet to True 
		self.objectPoint = point 
		self.locationSet = True


	def getName(self):
		return self.name


	def getQualities(self):
		return self.qualities 


	def getObjectType(self):
		return self.objectType


	def getNumerics(self):
		return self.numerics

	def getNumericValue(self, metric):
		return self.numerics[metric]


	def getPoint(self):
		return self.objectPoint 


