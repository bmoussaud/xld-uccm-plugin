angular
    .module('uccm', ['ui.ace', 'ui.bootstrap'])
    .controller(
        'UccmController',
        function($http, $scope, $window) {
            $scope.view_mode = "list";
            $scope.currentTemplate = {type: 'py'};
            $scope.templateNames = [];

            $scope.ftlTemplateNames = [];
            $scope.awsPyProcessorNames = [];
            $scope.k8sPyProcessorNames = [];
            $scope.genericPyProcessorNames = [];

            $scope.aceOption = {
                mode: 'ftl',
                theme: 'twilight'
            };

            $scope.refreshPage = function() {
                $window.location.reload();
            };

            $scope.addBlueprint = function(type_name) {
                let template = {
                    name: null,
                    template: "",
                    type: type_name
                };

                if (type_name == 'py') {
                    template.template = "def process(template, profile_dictionary, deployed, deployed_application):\n" +
                                        "    return template";
                } else {
                    template.template = '<#import "/uccm/utils/ftl/dictionary.ftl" as dict>\n' +
                        '{\n' +
                        '    "kind": "Deployment",\n' +
                        '    "apiVersion": "extensions/v1beta1",\n' +
                        '    "metadata": {\n' +
                        '    "name": "${deployed.name}-depl",\n' +
                        '    "labels": {\n' +
                        '        "application": "${application}",\n' +
                        '        "version": "${version}"\n' +
                        '        "environment": "${dict.resolve(\'env\', \'test2\')}"\n' +
                        '    }\n' +
                        '}'
                }

                $scope.currentTemplate = template;
                $scope.setAceMode();
                $scope.view_mode = "edit";
            };

            $scope.loadTemplateNames = function() {
                $http.get('/api/extension/uccm/templates').
                then(function(data) {
                        $scope.templateNames = data.data.entity;
                        let ftlTemplateNames = [];
                        let awsPyProcessorNames = [];
                        let k8sPyProcessorNames = [];
                        let genericPyProcessorNames = [];
                        angular.forEach(data.data.entity, function(value) {
                            if (value.type == 'ftl') {
                                ftlTemplateNames.push(value);
                            } else if (value.name.endsWith("_aws")) {
                                awsPyProcessorNames.push(value);
                            } else if (value.name.endsWith("_k8s")) {
                                k8sPyProcessorNames.push(value);
                            } else {
                                genericPyProcessorNames.push(value);
                            }
                        });
                        $scope.ftlTemplateNames = ftlTemplateNames;
                        $scope.awsPyProcessorNames = awsPyProcessorNames;
                        $scope.k8sPyProcessorNames = k8sPyProcessorNames;
                        $scope.genericPyProcessorNames = genericPyProcessorNames;
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

            $scope.setAceMode = function() {
                let mode = $scope.currentTemplate.type ==  'py' ? 'python' : 'ftl';
                $scope.aceOption = angular.extend({}, $scope.aceOption, {'mode': mode});
            };

            $scope.editTemplate = function(template) {
                $http.get('/api/extension/uccm/templates?name=' + template.name + '&type=' + template.type).
                then(function(data) {
                        $scope.currentTemplate = data.data.entity;
                        $scope.setAceMode();
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