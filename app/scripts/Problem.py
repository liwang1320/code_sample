#!/usr/bin/env python
#
# Reading/Parsing of PDDL problem files
# -Written by Joseph Kim

import re

class Problem():
    def __init__(self, pfile):
        self.pfile = pfile

       # Preprocessing
        self.pfile = [x.strip(' ') for x in self.pfile] # remove start/trailing spaces
        self.pfile = [x.strip('\t') for x in self.pfile] # remove start/trailing tabs
        self.pfile = filter(bool, self.pfile)           # remove empty lines
        self.pfile = [x for x in self.pfile if x not in [')','(']]  # remove any line containing only one paranthesis
        self.pfile = [re.sub(r'\)\)$',')',x) for x in self.pfile]  # remove double closing paranthesis
        self.pfile = [x for x in self.pfile if x not in [')','(']]  # remove any line containing only one paranthesis
        
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
            match = re.search(r'- .+$', line)
            match = re.search(r'\w+$',match.group())
            otype = match.group()
            
            if otype not in objects:
                objects[otype] = []
            
            current_objs = re.sub(r' - .+$','',line)
            current_objs = [x for x in current_objs.split()]
            
            for obj in current_objs:
                objects[otype].append(obj)
        
        self.objects = objects
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
        
        self.initStates = initStates
        return initStates
        
        
    def getGoalStates(self):
        temp = ["(:goal" in s for s in self.pfile]
        i_goal = [i for i, x in enumerate(temp) if x][0]
        temp = ["(:metric" in s for s in self.pfile]
        if True in temp:
            i_metric = [i for i, x in enumerate(temp) if x][0]
            goal_list = self.pfile[i_goal+1:i_metric] # str format
        else:
            goal_list = self.pfile[i_goal+1:]
   
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
        
        self.goalStates = goalStates
        self.goalStr = goal_list
        return goalStates, goal_list
        

    def getMetric(self):
        temp = ["(:metric" in s for s in self.pfile]
        if True in temp:
            i_metric = [i for i, x in enumerate(temp) if x][0]
            line = self.pfile[i_metric]
            metric = re.sub(r'\(:metric','',line).strip(' ')
            metric = re.sub(r'\)\)$',')',metric)
        else:
            metric = 'none'
        self.metric = metric
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
        self.initNumerics = initNumerics
        return initNumerics