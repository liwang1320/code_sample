'use strict';

/**
 * @ngdoc function
 * @name demoAppApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the demoAppApp
 */


angular.module('inputApp', [])
.controller('ExampleController', ['$scope', function($scope) {
  $scope.list = [];
  $scope.text = 'hello';
  $scope.submit = function() {
    if ($scope.text) {
      var myText = this.text
      startTable();
      addToTable();
      $('#stateTable').show();
     
    }
  };

  // $scope.getTypeShape = function(type) {
  //   console.log(getShape(type));
  //   return getShape(type);
  // }
}]);

function startTable() {
  var table = document.getElementById("stateTable");
  var header = table.createTHead();
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


