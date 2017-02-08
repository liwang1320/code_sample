
from Problem import Problem
import ast 
import os
import subprune


class GenericPlannerInterface():
	#where p is a Problem object

	def __init__(self, pfile):
		with open(pfile, 'r') as f:
			filein = f.read().splitlines()

		p = Problem(filein)

		self.readProblem = filein

		self.objects = p.getObjects() 
		#self.objects is a dictionary where keys are object types, 
		#  values are lists of names of objects of the key type

		self.initialStates = p.getInitStates()
		#self.initialStates is a list of dictionaries where each dictionary has actions as keys and 
    	#list of objects that the key effects as values

		self.intialNumerics = p.getInitNumerics()
		#self.objects is a dictonary with keys that are action/function names
		# 	values that are dictionaries with keys as objects effected and values as floats relating them

		self.goalState = p.getGoalStates()[0]
		#goalState is currently a tuple, the first value is a list of the states

		self.goalStateStr = p.getGoalStates()[1]
		#goalStateStr is the string version of goalState

		self.Metric = p.getMetric()
		#String decribing what we are trying to min/max


		#self.domainPath = dfile
	


	def simplifyGoals(self, goalsToKeep):
		
		subgoals = [self.goalStates for i in goalsToKeep]
		subgoals_str = [self.goalStateStr for i in goalsToKeep]

		pr = subprune.Pruner(self.initialStates, subgoals, self.getObjects)
		pr.getGoalParams()
		substates = pr.prune_states()

		subobjects = pr.prune_objects()
		flatten1 = [item for sublist in self.objects.values() for item in sublist]
		flatten2 = [item for sublist in subobjects.values() for item in sublist]

		subprune.printSubProblem(self.domainPath, pr, self.intialNumerics, subgoals, self.getMetric)


	def getProblem(self):
		#returns problem in plain text
		return self.readProblem

	def getObjects(self):
		#returns a dictionary where keys are object types, 
		#  values are lists of names of objects of the key type
		return self.objects

	def getInitialStates(self):
		#returns a list of dictionaries where each dictionary has actions as keys and 
    	#list of objects that the key effects as values
		return self.initialStates

	def getInitalNumerics(self):
		#returns a dictionary with actions as keys and dictionaries as values 
		#inner dictionaries have tuples of effected objects as keys and numeric as value
		return self.parseToWorkableNumerics()

	def getGoalStateComparision(self):
		#returns a list comparable to the initialStates list
		return self.goalState

	def getGoalString(self):
		#returns goal state as a string
		return self.goalStateStr

	def getMetric(self):
		#returns string describing metric
		return self.metric



	# def parseToWorkableInitStates(initState):
	# 	#initState is a list of dictionaries with 1 key (as a string) and values that are lists
	# 	allPredicates = {}
	# 	for predicate in initState:
	# 		#every predicate is a dictionary
	# 		for key in predicate:
	# 			#there is only 1
	# 			if key not in allPredicates:
	# 				allPredicates[key] = []
	# 			allPredicates[key].append(tuple(predicate[key]))
	# 	return allPredicates 

	def parseToWorkableNumerics(self):
		#initNumbers is a list of strings
		allActions = {}

		for s in self.intialNumerics:
			splitLeft = s.split(")") 
			#split to separate number from the rest 

			num = float(splitLeft[1]) 
			#resulting 2nd number will be the number with extra spaces

			splitRight = splitLeft[0].split("(") 
			#split so that action and objects are left

			splitBySpaces = splitRight[-1].split(" ") 
			#separates action and objects

			action = splitBySpaces[0] 
			#first value is the action

			if action not in allActions:
				allActions[action] = {}
			allActions[action][",".join(splitBySpaces[1:])] = num 
			#keys of dictionary are the tuples of objects
		return allActions


	def objectsToString(self):
		#returns a string of objects and types with special separators 
		objectString = ""
		for objType in self.objects:
			objectString += (objType + "=") 
			#object types indicate their objects by =
			objString = ""
			for obj in self.objects[objType]:
				objString += (obj + ",")
				#add all objects to string separated by commas
			#get rid of the trailing "," at the end
			objectString += objString[:(len(objString)-1)] #add the string for objects of each type to the running string
			objectString += " " #object types are separated by " "
		#get rid of trailing " "
		return objectString[:(len(objectString)-1)]

	def statesToString(self, states):
		#states is a list of dictionaries 
		statesString = ""
		for predicate in states:
			#for each dictionary in states
			for key in predicate:
				#for the key in the dictionary
				statesString += (key + "=") #add key to string with = indicating it effects the following objects
				predString = ""
				for obj in predicate[key]:
					#for all objects effected by the predicate
					predString += (obj + ",") #add obj to stateString separated by commas
				#remove trialing comma
			statesString += (predString[:(len(predString)-1)] + " ") #add whiteSpace to separate predicates 
		#remove trailing whitespace 
		return statesString[:(len(statesString)-1)] 

	def initStatesToString(self):
		return self.statesToString(self.initialStates)

	def goalStatesToString(self):
		return self.statesToString(self.goalState)

	def numericsToString(self):
		numerics = self.parseToWorkableNumerics()
		numericString = ""
		for metric in numerics:
			numericString += (metric + ":") #add all metrics separated by : to string
			thisMetric = numerics[metric]
			metricString = ""
			for effected in thisMetric:
				#for all keys of the dictionary given by the metric
				metricString += (effected + "=" + str(thisMetric[effected]) + "%")
				#add key=value separated by %
			#get rid of trailing %
			numericString += metricString[:(len(metricString) -1)] #add whitespace to separate metrics 
			
		
		#print (numericString[:(len(numericString)-1)])
		return numericString[:(len(numericString)-1)]

 



problem1 = GenericPlannerInterface("pfile3_satellite.txt")
# print ("numerics = ")
# print (problem1.numericsToString())
# print ("initStates = ")
# print (problem1.initStatesToString())
# print ("problemObjects = ")
# print (problem1.objectsToString())
# print ("problemGoals = ")
# print (problem1.goalStatesToString())

