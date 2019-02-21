angular
    .module('uccm', ['ui.ace'])
    .controller(
        'UccmController',
        function($http, $scope, $window) {
            $scope.view_mode = "list";
            $scope.currentTemplate = null;
            $scope.templateNames = [];

            $scope.refreshPage = function() {
                $window.location.reload();
            };

            $scope.addBlueprint = function() {
                $scope.currentTemplate = {
                    name: null,
                    template: ""
                }
                $scope.view_mode = "edit";
            };

            $scope.aceLoaded = function(_editor) {
                // Options
                //_editor.setReadOnly(true);
            };

            $scope.aceChanged = function(e) {
                //
            };


            $scope.loadTemplateNames = function() {
                $http.get('/api/extension/uccm/templates').
                then(function(data) {
                    $scope.templateNames = data.data.entity;
                },
                function(data) {
                    console.log(data)
                });
            };

            $scope.cancelEdit = function() {
                $scope.currentTemplate = null;
                $scope.view_mode = "list";
                $scope.loadTemplateNames();
            };


            $scope.editTemplate = function(name) {
                $http.get('/api/extension/uccm/templates?name=' + name).
                then(function(data) {
                        $scope.currentTemplate = data.data.entity;
                        $scope.view_mode = "edit";
                    },
                    function(data) {
                        console.log(data)
                    });
            };

            $scope.saveTemplate = function() {
                const new_data = $scope.currentTemplate;
                console.log($scope.currentTemplate);
                $http.post('/api/extension/uccm/templates', new_data).
                then(function(data) {
                        $scope.currentTemplate = null;
                        $scope.view_mode = "list";
                        $scope.loadTemplateNames();
                    },
                    function(data) {
                        console.log(data)
                    });
            };



            $scope.getView = function() {
                switch($scope.view_mode)
                {
                    case "list":
                        return 'partials/list.html';
                    default:
                        return 'partials/edit.html';
                }
            };


            $scope.loadTemplateNames();
        });