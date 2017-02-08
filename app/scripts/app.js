'use strict';

/**
 * @ngdoc overview
 * @name demoAppApp
 * @description
 * # demoAppApp
 *
 * Main module of the application.
 */

var problemMetic = "minimize (total-time)"

var problemGoals = [{'at': ['driver1', 's1']}, {'at': ['driver2', 's1']}, {'at': ['truck1', 's2']}, {'at': ['truck2', 's0']}, {'at': ['package1', 's0']}, {'at': ['package2', 's2']}, {'at': ['package3', 's0']}]

var problemGoalsStr = ['(at driver1 s1)', '(at driver2 s1)', '(at truck1 s2)', '(at truck2 s0)', '(at package1 s0)', '(at package2 s2)', '(at package3 s0)']

var problemInitialNumerics = {'time-to-walk': {'p0-2,s2': 7.0, 's2,p0-2': 7.0, 's0,p0-2': 68.0, 'p0-2,s0': 68.0, 'p2-1,s2': 30.0, 's1,p0-1': 39.0, 'p0-1,s0': 37.0, 's0,p0-1': 37.0, 'p2-1,s1': 19.0, 's2,p2-1': 30.0, 'p0-1,s1': 39.0, 's1,p2-1': 19.0}, 'time-to-drive': {'s0,s2': 52.0, 's1,s2': 86.0, 's1,s0': 63.0, 's2,s0': 52.0, 's2,s1': 86.0, 's0,s1': 63.0}}

var problemInitialStates = [{'at': ['driver1', 's0']}, {'at': ['driver2', 's0']}, {'at': ['truck1', 's0']}, {'empty': ['truck1']}, {'at': ['truck2', 's1']}, {'empty': ['truck2']}, {'at': ['package1', 's2']}, {'at': ['package2', 's1']}, {'at': ['package3', 's1']}, {'path': ['s0', 'p0-1']}, {'path': ['p0-1', 's0']}, {'path': ['s1', 'p0-1']}, {'path': ['p0-1', 's1']}, {'path': ['s0', 'p0-2']}, {'path': ['p0-2', 's0']}, {'path': ['s2', 'p0-2']}, {'path': ['p0-2', 's2']}, {'path': ['s2', 'p2-1']}, {'path': ['p2-1', 's2']}, {'path': ['s1', 'p2-1']}, {'path': ['p2-1', 's1']}, {'link': ['s0', 's2']}, {'link': ['s2', 's0']}, {'link': ['s1', 's0']}, {'link': ['s0', 's1']}, {'link': ['s1', 's2']}, {'link': ['s2', 's1']}]

var problemObjects = {'driver': ['driver1', 'driver2'], 'obj': ['package1', 'package2', 'package3'], 'location': ['s0', 's1', 's2', 'p0-1', 'p0-2', 'p1-0', 'p2-1'], 'truck': ['truck1', 'truck2']}

var shapes = ['circle', 'square', 'rectangle', 'oval', 'triangle', 'triangle_left', 'triangle_right', 'diamond', 'trapezium', 'parallelogram', 'pentagon', 'hexagon', 'octagon', 'egg', 'pacman']

var typesToShapesDict = {};

var availableShapes = shapes;

var fromTop = 80;
var from right = 50;

function showObjects() {
  var structuredList = [];
  for (var key in problemObjects) {
    //console.log(problemObjects[key])
    var thisType = problemObjects[key]
    for (var obj = 0;  obj < thisType.length; obj++) {
      // console.log("key: " + key);
      // console.log("object: " + obj)


      var dict = {}
      dict.type = key;
      dict.name = thisType[obj]
      structuredList.push(dict)
    }
  }
  return structuredList;
}


//returns a dictionary
//dict.types = list of types
//dict.objectsByType = dictionary 
function showTypesAndObjects(){
  return problemObjects;
}

function showTypes(){
  var keys = [];
  for (var key in problemObjects) {keys.push(key)}
  return keys;

}

//type to shape dictionary
function getShape(type){
  if (type in typesToShapesDict){
    return typesToShapesDict[type];
  
  }else{
    typesToShapesDict.type = availableShapes[0]
    availableShapes.shift()
    if (availableShapes.length < 1){
      availableShapes = shapes;
    }
    return typesToShapesDict[type]

  }

}

function isInArray(value, array) {
  return array.indexOf(value) > -1;
}

//returns a dictionary where keys are object types, values are shapes
function setShapes(typeList){

  for (var type in typeList) {
    if (!(type in typesToShapesDict)){
      typesToShapesDict.type = availableShapes[0];
      availableShapes.shift();

    }
  }
  return typesToShapesDict;
}

function viewObjects(){
  var addDivs = "";
  for (var type in problemObjects) {
    if (type in typesToShapesDict) {
      var shape = typesToShapesDict[type];
    }else {
      if (availableShapes.length < 1){
        availableShapes = shapes;
      }
      var shape = availableShapes.shift();
      typesToShapesDict[type] = shape; 
    }
    // var newDiv =  document.createElement('div');
    // newDiv.className = "allObjects"; 


    var divString= '<div ng-repeat="obj in typesToObjects.' + type + '"' + ' class= "' + shape + '"/>\
      {{obj}}\
      <p> (' + type + ') </p>\
    </div>';
    // //console.log(newDiv);
    // document.getElementById('insertObjects').appendChild(newDiv);
    var newDiv = angular.element('<div ng-repeat="obj in typesToObjects.' + type + '"' + ' class= "' + shape + '"/>\
      {{obj}}\
      <p> (' + type + ') </p>\
    </div>')

  }


}



function typesToShapes(){
  console.log(typesToShapesDict)
  return typesToShapesDict;
}

var sheet = window.document.styleSheets[0];
sheet.insertRule('#driver1 {position: absolute; top: 80px; right: 100px}', sheet.cssRules.length);


function arrangeObjects(){
  

}


