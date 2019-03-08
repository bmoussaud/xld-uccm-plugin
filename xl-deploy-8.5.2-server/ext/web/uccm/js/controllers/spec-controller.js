angular.module('uccm').controller( 'SpecController', function($http, $scope, notify, handleError) {
        $scope.view_mode = "list";
        $scope.currentSpec = null;
        $scope.specNames = [];


        $scope.jsonAceOption = {
            mode: 'json',
            theme: 'twilight'
        };

        $scope.addSpec = function() {
            let template = {
                apiVersion: "",
                spec: "",
                schema: ""
            };
            $scope.currentSpec = template;
            $scope.view_mode = "edit";
        };

        $scope.loadSpecNames = function() {
            $http.get('/api/extension/uccm/specs').
            then(function(data) {
                    $scope.specNames = data.data.entity;
                }, handleError);
        };

        $scope.cancelSpecEdit = function() {
            $scope.currentSpec = null;
            $scope.view_mode = "list";
            $scope.loadSpecNames();
        };

        $scope.editSpec = function(spec) {
            $http.get('/api/extension/uccm/specs?name=' + spec.name).
            then(function(data) {
                    $scope.currentSpec = data.data.entity;
                    $scope.view_mode = "edit";
                }, handleError);
        };

        $scope.saveSpec = function() {
            const new_data = {
                name: $scope.currentSpec.name,
                spec: {
                    apiVersion: $scope.currentSpec.spec.apiVersion,
                    spec: angular.fromJson($scope.currentSpec.spec.spec),
                    schema: angular.fromJson($scope.currentSpec.spec.schema)
                }
            };
            $http.post('/api/extension/uccm/specs', new_data).
            then(function(data) {
                    notify({title: "Saved Spec"});
                    $scope.currentSpec = null;
                    $scope.view_mode = "list";
                    $scope.loadSpecNames();
                }, handleError);
        };

        $scope.generateSchema = function() {
            const new_data = {
                spec: angular.fromJson($scope.currentSpec.spec.spec)
            };
            $http.post('/api/extension/uccm/schema', new_data).
            then(function(data) {
                    $scope.currentSpec.spec.schema = JSON.stringify(data.data.entity, null, 4);
                    $scope.currentSpec = angular.extend({}, $scope.currentSpec);
                    notify({title: "Generated Schema", msg: "Generated and updated schema field. You still need to save."});
                }, handleError);
        };

        $scope.getView = function() {
            switch($scope.view_mode)
            {
                case "list":
                    return 'partials/specs/list.html';
                default:
                    return 'partials/specs/edit.html';
            }
        };

        $scope.loadSpecNames();

});