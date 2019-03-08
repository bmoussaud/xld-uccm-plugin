angular.module('uccm').factory('notify', ['toaster', function(toaster) {
    return function(info) {
        info = angular.extend({type: "success", title: "", msg: ""}, info);
        toaster.pop({
            type: info.type,
            title: info.title,
            body: info.msg,
            timeout: 2000
        });
    };
}]);

angular.module('uccm').factory('handleError', ['toaster', function(toaster) {
    return function(data) {
        console.error(data);
        toaster.pop({
            type: 'error',
            title: "Server call failure!",
            body: data,
            timeout: 3000
        });
    };
}]);
