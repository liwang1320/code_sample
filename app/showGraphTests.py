
import unittest
import math

from showGraph import ObjPoint
from showGraph import Vertex
from showGraph import ShowGraph
from showGraph import Edge
# from showGraph.py import ShowGraph
# from showGraph.py import Vertex 
# from showGraph.py import Edge 


#ObjPoint Tests
#Test getters
#Test distance from center
#Test angle from center
#Test get quadrant 


class TestObjPoint(unittest.TestCase):

	# point1 = ObjPoint(3, 4, 0, 0) #quadrant 1, 0-center
	# point2 = ObjPoint(-2, -2, 1, 1) #quadrant 3, non-0-center
	# point3 = ObjPoint(16, -3, 4, 2) #quandrant 4, non-0-center
	# point4 = ObjPoint(-3, 0, -2, -2) #quadrant 2, negative-center

	def testGetters(self):
		point1 = ObjPoint(3, 4, 0, 0) #quadrant 1, 0-center
		self.assertEqual(point1.getXLoc(), 3, "testing...")
		self.assertEqual(point1.getYLoc(), 4, "testing...")
		self.assertEqual(point1.getCenter(), (0,0), "0-center")

	def testCalculations(self):
		point1 = ObjPoint(3, 4, 0, 0) #quadrant 1, 0-center
		point2 = ObjPoint(-2, -2, 1, 1) #quadrant 3, non-0-center
		point3 = ObjPoint(16, -3, 4, 2) #quandrant 4, non-0-center
		point4 = ObjPoint(-3, 0, -2, -2) #quadrant 2, negative-center

		#quadrant 1 point1 test
		self.assertEqual(point1.getDistanceFromCenter(), 5, "3-4-5 triangle")
		self.assertEqual(point1.getAngleFromCenter(), math.atan(float(4)/3), "theta=atan(4/3)")
		self.assertEqual(point1.getQuadrant(), 1, "in quadrant 1")

		#quadrant 2 point4 test
		self.assertEqual(point4.getDistanceFromCenter(), 2, "sqrt(5) floor is 2")
		self.assertEqual(point4.getAngleFromCenter(), math.atan(float(2)), "theta=atan(2)")
		self.assertEqual(point4.getQuadrant(), 2, "in quadrant 2")

		#quadrant 3 point2 test
		self.assertEqual(point2.getDistanceFromCenter(), 4, "3*sqrt(2) floor is 4")
		self.assertEqual(point2.getAngleFromCenter(), math.atan(float(1)), "theta=atan(1)")
		self.assertEqual(point2.getQuadrant(), 3, "in quadrant 3")

		#quadrant 4 point3 test
		self.assertEqual(point3.getDistanceFromCenter(), 13, "5-12-13 triangle")
		self.assertEqual(point3.getAngleFromCenter(), math.atan(float(5)/12), "theta=atan(5/12)")
		self.assertEqual(point3.getQuadrant(), 4, "in quadrant 4")


class TestVertex(unittest.TestCase):

	def testQualityChanges(self):
		vertex1 = Vertex("driver1", "driver")

		#test quality getter
		self.assertEqual(vertex1.getQualities(), [], "should be init at empty list")

		#test quality add
		self.assertTrue(vertex1.addQuality("here"), "addQuality success = True")
		self.assertEqual(vertex1.getQualities(), ["here"], "should contain 'here'")
		self.assertFalse(vertex1.addQuality("here"), "addQuality fail-existing quality =")

		#test quality delete
		self.assertTrue(vertex1.deleteQuality("here")) 
		self.assertEqual(vertex1.getQualities(), [], "should be init at empty list")
		self.assertFalse(vertex1.deleteQuality("her"), "should be false, quality doesn't exist")

	def testNumericChanges(self):
		vertex1 = Vertex("driver1", "driver")

		#test numeric getter
		self.assertEqual(vertex1.getNumerics(), {}, "should be empty dict")

		#test numeric add
		self.assertTrue(vertex1.addNumeric("time-to-walk", 90), "true = success")
		self.assertEqual(vertex1.getNumericValue("time-to-walk"), 90, "get val of key")
		self.assertEqual(vertex1.getNumerics(), {"time-to-walk":90}, "key:val inserted in dict")
		self.assertFalse(vertex1.addNumeric("time-to-walk", 90), "false because numeric already exists")

		#test numeric change
		self.assertTrue(vertex1.addNumeric("time-to-walk", 100), "changes value to 100")
		self.assertEqual(vertex1.getNumerics(), {"time-to-walk":100}, "changes to 100")

		#test numeric delete
		self.assertTrue(vertex1.deleteNumeric("time-to-walk"), "delete occured = true")
		self.assertEqual(vertex1.getNumerics(), {}, "empty dict")
		self.assertFalse(vertex1.deleteNumeric("heroooo"), "numeric doesn't exist = false")

	def testPointChanges(self):
		vertex1 = Vertex("driver1", "driver")

		#initialized vertex has a location set of false
		self.assertFalse(vertex1.locationSet, "init false")

		#set vertex to a point
		point1 = ObjPoint(3, 4, 0, 0)
		vertex1.setPoint(point1)
		self.assertTrue(vertex1.locationSet, "location set should be true")
		self.assertEqual(vertex1.getPoint(), point1, "vertex at point1")
		vertex1.changePoint()
		self.assertFalse(vertex1.locationSet, "location should be unset again")


class TestEdges(unittest.TestCase):
	def testPredicateEdge(self):
		vertex1 = Vertex("driver1", "driver")
		vertex2 = Vertex("s-1", "location")
		f = 5
		predicateEdge = Edge(vertex1, vertex2, "at", f)

		#test getName()
		self.assertEqual(predicateEdge.getName(), "driver1,s-1", "name is combined vertices name")

		#test getStartObject()
		self.assertEqual(predicateEdge.getStartObject(), vertex1, "vertex1 is the start vertex")

		#test getEndObject()
		self.assertEqual(predicateEdge.getEndObject(), vertex2, "vertex2 is the end vertex")

		#test initialization of edge at predicate = True
		self.assertTrue(predicateEdge.isPredicate(), "predicate = true")

		#test initialization of edge at double = False
		self.assertFalse(predicateEdge.double, "double is false")

		#test getMetric 
		self.assertEqual(predicateEdge.getMetric(), "at", "metric is at")

		#test that numeric and double functions do not apply to predicates
		self.assertFalse(predicateEdge.setNumeric(5), "predicates do not have set numerics")
		self.assertFalse(predicateEdge.setDoubleTrue(), "predicates cannot have double = true")
		self.assertFalse(predicateEdge.setDoubleFalse(), "predicates do not change in double value")

	def testNumericEdge(self):
		vertex1 = Vertex("p-1", "location")
		vertex2 = Vertex("s-1", "location")
		numericEdge = Edge(vertex1, vertex2, "time-to-walk", 45, False)

		#test getNumeric
		self.assertEqual(numericEdge.getNumeric(), 45, "numeric is 45")
		#test change numeric
		self.assertTrue(numericEdge.setNumeric(30), "numeric changed")
		self.assertEqual(numericEdge.getNumeric(), 30, "numeric is now 30")

		#test double change
		self.assertTrue(numericEdge.setDoubleTrue(), "double set to true")
		self.assertTrue(numericEdge.double, "double = true")
		self.assertTrue(numericEdge.setDoubleFalse(), "double set to false")

		self.assertFalse(numericEdge.isPredicate(), "numeric edge is not a predicate")
		self.assertFalse(numericEdge.double, "double = false")














class TestShowGraph(unittest.TestCase):

	#tests the current construction of the graph
	def testDriverLogGraph(self):
		problemInitialNumerics = {'time-to-walk': {'p0-2,s2': 7.0, 's2,p0-2': 7.0, 's0,p0-2': 68.0, 'p0-2,s0': 68.0, 'p2-1,s2': 30.0, 's1,p0-1': 39.0, 'p0-1,s0': 37.0, 's0,p0-1': 37.0, 'p2-1,s1': 19.0, 's2,p2-1': 30.0, 'p0-1,s1': 39.0, 's1,p2-1': 19.0}, 'time-to-drive': {'s0,s2': 52.0, 's1,s2': 86.0, 's1,s0': 63.0, 's2,s0': 52.0, 's2,s1': 86.0, 's0,s1': 63.0}}

		problemInitialStates = [{'at': ['driver1', 's0']}, {'at': ['driver2', 's0']}, {'at': ['truck1', 's0']}, {'empty': ['truck1']}, {'at': ['truck2', 's1']}, {'empty': ['truck2']}, {'at': ['package1', 's2']}, {'at': ['package2', 's1']}, {'at': ['package3', 's1']}, {'path': ['s0', 'p0-1']}, {'path': ['p0-1', 's0']}, {'path': ['s1', 'p0-1']}, {'path': ['p0-1', 's1']}, {'path': ['s0', 'p0-2']}, {'path': ['p0-2', 's0']}, {'path': ['s2', 'p0-2']}, {'path': ['p0-2', 's2']}, {'path': ['s2', 'p2-1']}, {'path': ['p2-1', 's2']}, {'path': ['s1', 'p2-1']}, {'path': ['p2-1', 's1']}, {'link': ['s0', 's2']}, {'link': ['s2', 's0']}, {'link': ['s1', 's0']}, {'link': ['s0', 's1']}, {'link': ['s1', 's2']}, {'link': ['s2', 's1']}]

		problemObjects = {'driver': ['driver1', 'driver2'], 'obj': ['package1', 'package2', 'package3'], 'location': ['s0', 's1', 's2', 'p0-1', 'p0-2', 'p1-0', 'p2-1'], 'truck': ['truck1', 'truck2']}

		vertexNames = []
		for t in problemObjects:
			vertexNames.extend(problemObjects[t])
		#vertexNames is a list of all objects by name 

		driverGraph = ShowGraph(0, 0, 300, 300, problemObjects, problemInitialNumerics, problemInitialStates, 5)

		#tests that all vertices are present in the graph
		namesToVertices = driverGraph.getNamesToVertices() 
		for name in vertexNames:
			self.assertTrue(namesToVertices[name] is not None, "vertex exists")

		#test that all edges are valid vertices of the graph
		namesToEdges = driverGraph.getNamesToEdges()
		for edge in namesToEdges:
			vertices = edge.split(",")
			vertex1 = vertices[0]
			vertex2 = vertices[1]
			self.assertTrue(namesToVertices[vertex1] is not None, "vertex exists")
			self.assertTrue(namesToVertices[vertex2] is not None, "vertex exists")


	def testGraphFunctionsEnds(self):

		problemInitialNumerics = {'time-to-walk': {'p0-2,s2': 7.0, 's2,p0-2': 7.0, 's0,p0-2': 68.0, 'p0-2,s0': 68.0, 'p2-1,s2': 30.0, 's1,p0-1': 39.0, 'p0-1,s0': 37.0, 's0,p0-1': 37.0, 'p2-1,s1': 19.0, 's2,p2-1': 30.0, 'p0-1,s1': 39.0, 's1,p2-1': 19.0}, 'time-to-drive': {'s0,s2': 52.0, 's1,s2': 86.0, 's1,s0': 63.0, 's2,s0': 52.0, 's2,s1': 86.0, 's0,s1': 63.0}}

		problemInitialStates = [{'at': ['driver1', 's0']}, {'at': ['driver2', 's0']}, {'at': ['truck1', 's0']}, {'empty': ['truck1']}, {'at': ['truck2', 's1']}, {'empty': ['truck2']}, {'at': ['package1', 's2']}, {'at': ['package2', 's1']}, {'at': ['package3', 's1']}, {'path': ['s0', 'p0-1']}, {'path': ['p0-1', 's0']}, {'path': ['s1', 'p0-1']}, {'path': ['p0-1', 's1']}, {'path': ['s0', 'p0-2']}, {'path': ['p0-2', 's0']}, {'path': ['s2', 'p0-2']}, {'path': ['p0-2', 's2']}, {'path': ['s2', 'p2-1']}, {'path': ['p2-1', 's2']}, {'path': ['s1', 'p2-1']}, {'path': ['p2-1', 's1']}, {'link': ['s0', 's2']}, {'link': ['s2', 's0']}, {'link': ['s1', 's0']}, {'link': ['s0', 's1']}, {'link': ['s1', 's2']}, {'link': ['s2', 's1']}]

		problemObjects = {'driver': ['driver1', 'driver2'], 'obj': ['package1', 'package2', 'package3'], 'location': ['s0', 's1', 's2', 'p0-1', 'p0-2', 'p1-0', 'p2-1'], 'truck': ['truck1', 'truck2']}

		vertexNames = []
		for t in problemObjects:
			vertexNames.extend(problemObjects[t])
		#vertexNames is a list of all objects by name 

		driverGraph = ShowGraph(0, 0, 300, 300, problemObjects, problemInitialNumerics, problemInitialStates, 5)

		self.assertEqual(driverGraph.mostEndsType(), 'location', "most ends type is location")

	def testGraphFunctionsConnectedComponents(self):
		problemInitialNumerics = {'time-to-walk': {'p0-2,s2': 7.0, 's2,p0-2': 7.0, 's0,p0-2': 68.0, 'p0-2,s0': 68.0, 'p2-1,s2': 30.0, 's1,p0-1': 39.0, 'p0-1,s0': 37.0, 's0,p0-1': 37.0, 'p2-1,s1': 19.0, 's2,p2-1': 30.0, 'p0-1,s1': 39.0, 's1,p2-1': 19.0}, 'time-to-drive': {'s0,s2': 52.0, 's1,s2': 86.0, 's1,s0': 63.0, 's2,s0': 52.0, 's2,s1': 86.0, 's0,s1': 63.0}}

		problemInitialStates = [{'at': ['driver1', 's0']}, {'at': ['driver2', 's0']}, {'at': ['truck1', 's0']}, {'empty': ['truck1']}, {'at': ['truck2', 's1']}, {'empty': ['truck2']}, {'at': ['package1', 's2']}, {'at': ['package2', 's1']}, {'at': ['package3', 's1']}, {'path': ['s0', 'p0-1']}, {'path': ['p0-1', 's0']}, {'path': ['s1', 'p0-1']}, {'path': ['p0-1', 's1']}, {'path': ['s0', 'p0-2']}, {'path': ['p0-2', 's0']}, {'path': ['s2', 'p0-2']}, {'path': ['p0-2', 's2']}, {'path': ['s2', 'p2-1']}, {'path': ['p2-1', 's2']}, {'path': ['s1', 'p2-1']}, {'path': ['p2-1', 's1']}, {'link': ['s0', 's2']}, {'link': ['s2', 's0']}, {'link': ['s1', 's0']}, {'link': ['s0', 's1']}, {'link': ['s1', 's2']}, {'link': ['s2', 's1']}]

		problemObjects = {'driver': ['driver1', 'driver2'], 'obj': ['package1', 'package2', 'package3'], 'location': ['s0', 's1', 's2', 'p0-1', 'p0-2', 'p1-0', 'p2-1'], 'truck': ['truck1', 'truck2']}

		vertexNames = []
		for t in problemObjects:
			vertexNames.extend(problemObjects[t])
		#vertexNames is a list of all objects by name 

		driverGraph = ShowGraph(0, 0, 300, 300, problemObjects, problemInitialNumerics, problemInitialStates, 5)

		self.assertEqual(driverGraph.mostConnectedComponentMetric()[0], "time-to-walk", "most c.c. metric")

if __name__ == '__main__':
    unittest.main()