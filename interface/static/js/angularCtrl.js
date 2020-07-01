var app = angular.module('dwitterAngularModule',[]);

app.config(function($interpolateProvider, $httpProvider){
    // $interpolateProvider.startSymbol("[[[");
    // $interpolateProvider.endSymbol("]]]");
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $httpProvider.defaults.xsrfCookieName=  "csrftoken";
    $httpProvider.defaults.xsrfHeaderName=  "X-CSRFToken";
});



app.controller('dwitterCtrl', ['$scope','menuItems','restApi', function(scope,menuItems,restApi){
    window.scope = scope;
    scope.sampleDweet = {
                "full_name" : "Mayank Shrivastava",
                "username" : "makriss",
                "posted_when" : "10 min",
                "dweet": "Kya baat hai"
            }

    scope.optionsMenu = menuItems()
//    restApi.likeDweet(13)
    // Move to sending promises from present structure
    // https://stackoverflow.com/questions/20555472/can-you-resolve-an-angularjs-promise-before-you-return-it
    restApi.getFeed().then(function(response){
                scope.dweetsFeed = response.data;
            }, function(response){
                console.error(response)
            })

}])

app.constant('menuItems', function(){
    return [
        {"name": "Home", "icon":"home"},
        {"name":"Bookmarks", "icon":"bookmark"},
        {"name":"Profile", "icon":"person"}
    ]
})