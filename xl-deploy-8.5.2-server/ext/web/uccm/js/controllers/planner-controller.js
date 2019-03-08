angular.module('uccm').controller( 'PlannerController', function($http, $scope, $window) {
        $scope.view_mode = "list";
        $scope.currentPlanner = null;
        $scope.plannerNames = [];


        $scope.pyAceOption = {
            mode: 'python',
            theme: 'twilight'
        };

        $scope.addPlanner = function() {
            let template = {
                name: "",
                planner: ""
            };
            $scope.currentPlanner = template;
            $scope.view_mode = "edit";
        };

        $scope.loadPlannerNames = function() {
            $http.get('/api/extension/uccm/planners').
            then(function(data) {
                    $scope.plannerNames = data.data.entity;
                },
                function(data) {
                    console.log(data)
                });
        };

        $scope.cancelPlannerEdit = function() {
            $scope.currentPlanner = null;
            $scope.view_mode = "list";
            $scope.loadPlannerNames();
        };

        $scope.editPlanner = function(planner) {
            $http.get('/api/extension/uccm/planners?name=' + planner.name).
            then(function(data) {
                    $scope.currentPlanner = data.data.entity;
                    $scope.view_mode = "edit";
                },
                function(data) {
                    console.log(data)
                });
        };

        $scope.savePlanner = function() {
            const new_data = $scope.currentPlanner;
            $http.post('/api/extension/uccm/planners', new_data).
            then(function(data) {
                    $scope.currentPlanner = null;
                    $scope.view_mode = "list";
                    $scope.loadPlannerNames();
                },
                function(data) {
                    console.log(data)
                });
        };

        $scope.getView = function() {
            switch($scope.view_mode)
            {
                case "list":
                    return 'partials/planners/list.html';
                default:
                    return 'partials/planners/edit.html';
            }
        };

        $scope.loadPlannerNames();

});