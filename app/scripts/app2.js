'use strict';

/**
 * @ngdoc overview
 * @name demoAppApp
 * @description
 * # demoAppApp
 *
 * Main module of the application.
 */

var numerics = {'slew_time': {'Phenomenon7,Star2': 60.53, 'Phenomenon6,Star3': 51.56, 'Star4,Star0': 71.99, 'Phenomenon5,Star2': 30.24, 'Phenomenon6,Star4': 56.36, 'Star2,Star0': 8.768, 'Star0,Phenomenon7': 9.943, 'Star0,Star1': 34.35, 'Star0,Phenomenon6': 77.1, 'Phenomenon5,Star3': 7.589, 'Phenomenon7,Phenomenon6': 32.34, 'Phenomenon5,Star4': 0.5297, 'Star4,Star1': 1.526, 'Phenomenon6,Star2': 64.11, 'Star3,Star4': 49.61, 'Star3,Star2': 17.99, 'Star4,Phenomenon5': 0.5297, 'Star1,Phenomenon5': 4.095, 'Star1,Star4': 1.526, 'Star2,Phenomenon5': 30.24, 'Star2,Star4': 35.34, 'Star2,Phenomenon6': 64.11, 'Star1,Phenomenon6': 47.3, 'Phenomenon5,Phenomenon6': 67.57, 'Star3,Phenomenon6': 51.56, 'Star0,Star3': 25.66, 'Star3,Phenomenon7': 53.93, 'Star1,Star2': 18.57, 'Star1,Star3': 25.96, 'Phenomenon5,Star1': 4.095, 'Phenomenon7,Phenomenon5': 43.97, 'Phenomenon6,Phenomenon5': 67.57, 'Star1,Star0': 34.35, 'Star4,Star3': 49.61, 'Phenomenon6,Phenomenon7': 32.34, 'Phenomenon6,Star0': 77.1, 'Star2,Star1': 18.57, 'Phenomenon7,Star4': 67.87, 'Star2,Star3': 17.99, 'Star0,Star4': 71.99, 'Phenomenon7,Star1': 13.3, 'Phenomenon7,Star3': 53.93, 'Star1,Phenomenon7': 13.3, 'Star3,Star0': 25.66, 'Star2,Phenomenon7': 60.53, 'Phenomenon5,Star0': 67.92, 'Star4,Phenomenon7': 67.87, 'Star3,Phenomenon5': 7.589, 'Star0,Phenomenon5': 67.92, 'Star0,Star2': 8.768, 'Phenomenon5,Phenomenon7': 43.97, 'Star4,Phenomenon6': 56.36, 'Phenomenon7,Star0': 9.943, 'Star4,Star2': 35.34, 'Phenomenon6,Star1': 47.3, 'Star3,Star1': 25.96}, 'calibration_time': {'instrument1,Star2': 15.9, 'instrument0,Star1': 37.3, 'instrument2,Star0': 38.1, 'instrument3,Star0': 16.9}}

var initStates = [{'supports': ['instrument0', 'spectrograph2']}, {'supports': ['instrument0', 'infrared0']}, {'calibration_target': ['instrument0', 'Star1']}, {'supports': ['instrument1', 'image1']}, {'calibration_target': ['instrument1', 'Star2']}, {'supports': ['instrument2', 'infrared0']}, {'supports': ['instrument2', 'image1']}, {'calibration_target': ['instrument2', 'Star0']}, {'on_board': ['instrument0', 'satellite0']}, {'on_board': ['instrument1', 'satellite0']}, {'on_board': ['instrument2', 'satellite0']}, {'power_avail': ['satellite0']}, {'pointing': ['satellite0', 'Star4']}, {'supports': ['instrument3', 'spectrograph2']}, {'supports': ['instrument3', 'infrared0']}, {'supports': ['instrument3', 'image1']}, {'calibration_target': ['instrument3', 'Star0']}, {'on_board': ['instrument3', 'satellite1']}, {'power_avail': ['satellite1']}, {'pointing': ['satellite1', 'Star0']}]

var problemObjects = {'direction': ['Star1', 'Star2', 'Star0', 'Star3', 'Star4', 'Phenomenon5', 'Phenomenon6', 'Phenomenon7'], 'mode': ['image1', 'infrared0', 'spectrograph2'], 'satellite': ['satellite0', 'satellite1'], 'instrument': ['instrument0', 'instrument1', 'instrument2', 'instrument3']}

var problemGoals = [{'pointing': ['satellite0', 'Phenomenon5']}, {'have_image': ['Star3', 'infrared0']}, {'have_image': ['Star4', 'spectrograph2']}, {'have_image': ['Phenomenon5', 'spectrograph2']}, {'have_image': ['Phenomenon7', 'spectrograph2']}]

var shapes = ['circle', 'square', 'rectangle', 'oval', 'triangle', 'triangle_left', 'triangle_right', 'diamond', 'trapezium', 'parallelogram', 'pentagon', 'hexagon', 'octagon', 'egg', 'pacman']

var typesToShapesDict = {};

var availableShapes = shapes;

// var fromTop = 80;
// var from right = 50;


function startTable() {
  var table = document.getElementById("stateTable");
  var header = table.createHead();
  var headRow = header.insertRow(0);

  var satelliteCell = headRow.insertCell(0);
  satelliteCell.innerHTML = "<b>Satellite</b>";

  var instrumentCell = headRow.insertCell(1);
  instrumentCell.innerHTML = "<b>Instrument</b>";

  var pointingToCell = headRow.insertCell(2);
  pointingToCell.innerHTML = "<b>Pointing To</b>";

  var calibrateCell = headRow.insertCell(3);
  calibrateCell.innerHTML = "<b>Calibrate</b>"
}






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

// var sheet = window.document.styleSheets[0];
// sheet.insertRule('#driver1 {position: absolute; top: 80px; right: 100px}', sheet.cssRules.length);




// Simple GET request example:
// $http({
//   method: 'GET',

//   url: 'http://localhost:8080s',

// }).then(function successCallback(response) {
//     console.log("i have succeeded")
//   }, function errorCallback(response) {
//     console.log("i have failed :(")
//   });

// myApp.controller('LoginCtrl', function($scope, $http){
//   $scope.formData = {};

//   $scope.doLogin = function(pass){
//     $http({
//       url: ""
//       method: "GET",
//       headers: { 'Content-Type': 'application/json' },
//       data: JSON.stringify(data)
//     }).success(function(data) {
//       console.log(data)
//     });
//  }
// });

var myApp = angular.module('myApp',[]);

myApp.service('dataService', function($http) {
  console.log("i am here at all")
    delete $http.defaults.headers.common['X-Requested-With'];
    console.log("i a slightly above")
    this.getData = function() {
        // $http() returns a $promise that we can add handlers with .then()
        console.log("i am here")
        return $http({
            method: 'GET',
            url: 'server4.py',
            params: 'limit=10, sort_by=created:desc',
            headers: {'Authorization': 'Token token=xxxxYYYYZzzz'}
         });
     }
});

myApp.controller('AngularJSCtrl', function($scope, dataService) {
    $scope.data = null;
    dataService.getData().then(function(dataResponse) {
        $scope.data = dataResponse;
    });
});

// var express = require('express');
// var app = express();

// app.get('/', function(req, res){
//   res.send('hello world');
// });

// app.listen(8080);