angular.module('uccm').controller('UccmController', function($http, $scope, $window, toaster) {
    $scope.show_success = function(title, msg) {
        toaster.pop({
            type: 'success',
            title: title,
            body: msg,
            timeout: 3000
        });
    };

    $scope.handle_error = function(data) {
        toaster.pop({
            type: 'error',
            title: 'Server call failed.',
            body: data,
            timeout: 3000
        });
    };

});