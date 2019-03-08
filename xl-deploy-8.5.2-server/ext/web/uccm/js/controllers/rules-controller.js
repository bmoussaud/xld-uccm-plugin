angular.module('uccm').controller('RulesController', function($http, $scope, notify, handleError) {
    $scope.rules = {xml: ""};

    $scope.aceOptionForRules = {
        mode: 'xml',
        theme: 'twilight'
    };

    $scope.editRules = function() {
        $http.get('/api/extension/uccm/rules').
        then(function(data) {
                $scope.rules = {xml : data.data.entity.rules};
            }, handleError
        );
    };

    $scope.saveRules = function() {
        const new_data = {rules: $scope.rules.xml};
        $http.post('/api/extension/uccm/rules', new_data).
        then(function(data) {
                notify({type: "success", title: "Rules", msg: "Saved successfully."});
            }, handleError
        );
    };

    $scope.editRules();
});