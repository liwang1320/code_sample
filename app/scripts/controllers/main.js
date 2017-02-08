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
      $scope.list.push(myText);
      $scope.text = '';
      console.log(myText);
      $scope.types = showTypes(); 
      // setShapes($scope.types);
      // console.log(showObjects())
      $scope.showObjects = showObjects();
      $scope.typesToObjects = showTypesAndObjects();
      viewObjects(); 
      $scope.typesToShapes = typesToShapes();
      arrangeObjects();

    }
  };

  $scope.getTypeShape = function(type) {
    console.log(getShape(type));
    return getShape(type);
  }
}]);

