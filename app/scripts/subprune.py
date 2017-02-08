#!/usr/bin/env python
#
# PDDL pruner based on subgoals

import re
import copy
import time
import os
import argparse

__author__ = 'Joseph Kim'
__version__ = '0.1'
__email__ = 'jokim@mit.edu'

class Problem():
    def __init__(self, pfile):
        self.pfile = pfile

       # Preprocessing
        self.pfile = [x.strip(' ') for x in self.pfile] # remove start/trailing spaces
        self.pfile = [x.strip('\t') for x in self.pfile] # remove start/trailing tabs
        self.pfile = filter(bool, self.pfile)           # remove empty lines
        self.pfile = [x for x in self.pfile if x not in [')','(']]  # remove any line containing only one paranthesis
        self.pfile = [re.sub(r'\)\)$',')',x) for x in self.pfile]  # remove double closing paranthesis
        
    def getFile(self):
        return self.pfile
        
    def getObjects(self):
        i_objects = self.pfile.index("(:objects")
        i_init = self.pfile.index("(:init")
        obj_list = self.pfile[i_objects+1:i_init]
        
        # If last element contains a closing parenthesis, remove it
        if obj_list[-1][-1] == ')':
            obj_list[-1] = obj_list[-1][:-1]
                    
        # Get object types and put in dictionary
        objects = {}
        for i, line in enumerate(obj_list):
            match = re.search(r'-.+$', line)
            match = re.search(r'\w+$',match.group())
            otype = match.group()
            
            cur_list = re.sub(r'-.+$','',line)
            cur_list = [x for x in cur_list.split()]
            objects[otype] = cur_list
            
        return objects
        
    def getInitStates(self):
        i_init = self.pfile.index("(:init")
        temp = ["(:goal" in s for s in self.pfile]
        i_goal = [i for i, x in enumerate(temp) if x][0]
        init_list = self.pfile[i_init+1:i_goal]
        
        # Get rid of numeric fluents
        init_list = [s for s in init_list if "(= " not in s]  # string format
        
        # Put in lists of dicts form
        initStates = []
        local_dict = {}
        for i, line in enumerate(init_list):
            # Get rid of paranthesis
            line = re.sub(r'^\(','',line)
            line = re.sub(r'\)$','',line)
            parts = line.split()
            key = parts[0]
            params = parts[1:]
            local_dict = {}
            local_dict[key]=params
            initStates.append(local_dict)
        
        return initStates
        
        
    def getGoalStates(self):
        temp = ["(:goal" in s for s in self.pfile]
        i_goal = [i for i, x in enumerate(temp) if x][0]
        temp = ["(:metric" in s for s in self.pfile]
        i_metric = [i for i, x in enumerate(temp) if x][0]
        
        goal_list = self.pfile[i_goal+1:i_metric] # str format
        
        # Put in lists of dicts form
        goalStates = []
        local_dict = {}
        for i, line in enumerate(goal_list):
            # Get rid of paranthesis
            line = re.sub(r'^\(','',line)
            line = re.sub(r'\)$','',line)
            parts = line.split()
            key = parts[0]
            params = parts[1:]
            local_dict = {}
            local_dict[key]=params
            goalStates.append(local_dict)
        
        return goalStates, goal_list
        

    def getMetric(self):
        temp = ["(:metric" in s for s in self.pfile]
        i_metric = [i for i, x in enumerate(temp) if x][0]
        line = self.pfile[i_metric]
        metric = re.sub(r'\(:metric','',line).strip(' ')
        metric = re.sub(r'\)\)$',')',metric)
        return metric
        
    def getInitNumerics(self):
        i_init = self.pfile.index("(:init")
        temp = ["(:goal" in s for s in self.pfile]
        i_goal = [i for i, x in enumerate(temp) if x][0]
        init_list = self.pfile[i_init+1:i_goal]
        if init_list[-1] == ")":
            init_list.pop()
        
        # Only consider ones with (=
        initNumerics = [s for s in init_list if "(= " in s]
        return initNumerics
        
    
        
class Pruner():
    def __init__(self, initStates, subgoals, objects):
        self.initStates = initStates
        self.subgoals = subgoals
        self.objects = copy.deepcopy(objects)
        self.goalParams = []
        self.substates = []
        self.subobjects = dict()
        
    def getGoalParams(self):
        for line in self.subgoals:
            values = list(line.values())[0]
            for value in values:
                self.goalParams.append(value)
                
    def prune_states(self):
        prune_indices = []
        
        # Collapse into dictionary with list of lists
        subgoal = dict()
        for line in self.subgoals:
            key = list(line.keys())[0]
            values = list(line.values())[0]
            if key not in subgoal:
                subgoal[key] = []
            subgoal[key].append(values)
            
        # For each subgoal type, get relevant params
        for key in list(subgoal.keys()):
            i_params = [i for i,x in enumerate(self.initStates) if list(x.keys())[0] == key]
            params = [list(x.values())[0] for x in self.initStates if list(x.keys())[0] == key]
            
            # Check overlap for each param
            # flatten_values = [item for sublist in subgoal[key] for item in sublist]
            for j,param in enumerate(params):
                if not set(self.goalParams) & set(param):  # there is no overlap - to be removed
                    prune_indices.append(i_params[j])
       
        # Prune based on indices
        substates = [x for i, x in enumerate(self.initStates) if i not in prune_indices]
        self.substates = substates   
        return substates
            
    def prune_objects(self):
        # Do this after you call prune_states
        paramlist = set()
        for line in self.substates:
            values = list(line.values())[0]
            for value in values:
                if value not in paramlist:
                    paramlist.add(value)
                    
        for k,v in self.objects.items():
            self.subobjects[k] = [x for i, x in enumerate(v) if x in paramlist]
            
        return self.subobjects
                
#=========================
#PRINTING problem method
def printSubProblem(filename, pr, initNumerics, subgoals, metric):
    with open(filename, 'w') as f:
        f.write('(define (problem subplan)\n')
        f.write('\t(:domain movingpr2)\n')
        
        # Writing of subobjects
        f.write('\t(:objects\n')
        for k,v in pr.subobjects.items():
            f.write('\t\t')
            f.write(' '.join(v))
            f.write(' - '+k+ '\n')
        f.write('\t)\n')
        
        # Writing of subStates
        f.write('\t(:init\n')
        for line in pr.substates:
            f.write('\t\t(')
            f.write(list(line.keys())[0]+' ')
            f.write(' '.join(list(line.values())[0]))
            f.write(')\n')
        f.write('\n')
        
        # Writing of numerics
        for line in initNumerics:
            f.write('\t\t' + line + '\n')
        f.write('\t)\n')
        
        # Writing of the subgoal
        f.write('\t(:goal (and\n')
        for line in subgoals:
            f.write('\t\t(')
            f.write(list(line.keys())[0]+' ')
            f.write(' '.join(list(line.values())[0]))
            f.write(')\n')
        f.write('\t))\n')
        
        # Write original metric
        f.write('\t(:metric ' + metric + ')\n')
        f.write(')')
#                
                
                

#==============================================================================
# MAIN
#==============================================================================
"""
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, required=True, help='input problem file')
parser.add_argument('-o', type=str, required=False, help='input output filename')
args = parser.parse_args()

# Read the main problem file
with open(args.f, 'r') as f:
    filein = f.read().splitlines()

# Output file
if args.o:
    fileout = args.o
else:
    fileout = 'subprob.pddl'

p = Problem(filein)
pfile = p.pfile
objects = p.getObjects()
initStates = p.getInitStates()
initNumerics = p.getInitNumerics()
goalStates, goalStr = p.getGoalStates()
metric = p.getMetric()

# Show goal list to the user
print("Original Goal States")
for i, line in enumerate(goalStr):
    print i,": ", line
    
# Ask user to choose the subgoal
id_sub = raw_input("Please choose a set of subgoals (e.g., 0,3,4): ")  #comma-separated list
id_sub = id_sub.split(',')
id_sub = [int(n) for n in id_sub]

subgoals = [goalStates[i] for i in id_sub]
subgoals_str = [goalStr[i] for i in id_sub]

# Pruner based on subgoals
pr = Pruner(initStates, subgoals, objects)
pr.getGoalParams()
substates = pr.prune_states()
print '\nWith current SubGoal..'
print '# of predicates pruned: '+str(len(initStates)-len(substates))+ ' / '+str(len(initStates))

subobjects = pr.prune_objects()
flatten1 = [item for sublist in objects.values() for item in sublist]
flatten2 = [item for sublist in subobjects.values() for item in sublist]
print '# of objects pruned: '+str(len(flatten1)-len(flatten2))+' / '+str(len(flatten1))

# Now create a new problem file based on what have been pruned
printSubProblem(fileout)
print '\nSubproblem generated: ' + fileout

"""

####################################################
# # Now run the planner with the new subproblem
# command = 'popf3-clp domain.pddl '+filename+ ' > out.txt'
# os.system(command)

# ######## Now read the planner's output
# with open('out.txt', 'r') as f:
#     filein = f.read()
         
# match = re.search(r';\sStates evaluated:\s\d+', filein)
# match = re.search(r'\d+',match.group())
# numNodes = match.group()
# match = re.search(r';\sCost:\s[\.\d]+', filein)
# match = re.search(r'[\.\d]+',match.group())
# cost = match.group()
# match = re.search(r';\sTime\s[\.\d]+', filein)
# match = re.search(r'[\.\d]+',match.group())
# planTime = match.group()
# print 'Subplan Result'
# print 'Cost: ' + cost
# print '# of nodes evaluated: ' + numNodes
# print 'Time to solve: ' + planTime


# ########## Run validator to get goal states as result of actions
# with open('out.txt','r') as f:
#     sysout = f.read().splitlines()
# temp = ["; Time" in s for s in sysout]
# ii = [i for i, x in enumerate(temp) if x][0]
# subplan = sysout[ii+1:]

# # Write this out for validator to run
# with open('subplan.txt', 'w') as f:
#     for line in subplan:
#         f.write(line+'\n')
        
# # Call validator and get final states







