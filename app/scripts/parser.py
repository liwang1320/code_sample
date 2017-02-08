#!/usr/bin/env python
#
#
# Main parser for PDDL - JOe's version (don't overwrite!)
# Written by Joseph Kim


from Problem import Problem
import ast

#==============================================================================
# MAIN
#==============================================================================
# Reading the main problem file
with open('C:/Users/liwan/Desktop/myStuff/spring2016/summer/UROP/prelim_work/pfile2', 'r') as f:
    filein = f.read().splitlines()
    
p = Problem(filein)
p.getObjects()
p.getInitStates()
p.getInitNumerics()
p.getGoalStates()
p.getMetric()


#print (p.getInitNumerics())

def parseToWorkableInitStates(initState):
        #initState is a list of dictionaries with 1 key (as a string) and values that are lists
        allPredicates = {}
        for predicate in initState:
                #every predicate is a dictionary
                for key in predicate:
                        #there is only 1
                        if key not in allPredicates:
                                allPredicates[key] = []
                        allPredicates[key].append(tuple(predicate[key]))
        return allPredicates

def parseToWorkableNumerics(initNumbers):
        #initNumbers is a list of strings
        allActions = {}

        for s in initNumbers:
                splitLeft = s.split(")") #split to separate number from the rest 
                num = float(splitLeft[1]) #resulting 2nd number will be the number with extra spaces
                splitRight = splitLeft[0].split("(") #split so that action and objects are left
                splitBySpaces = splitRight[-1].split(" ") #separates action and objects
                action = splitBySpaces[0] #first value is the action
                if action not in allActions:
                        allActions[action] = {}
                allActions[action][tuple(splitBySpaces[1:])] = num #keys of dictionary are the tuples of objects
        return allActions


print (p.getObjects())
